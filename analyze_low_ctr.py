"""
Analyze pages with high GSC impressions but low CTR, then enrich with GA4 traffic data.

Setup:
  1. Copy .env.example to .env and fill in your values.
  2. Place your Google service-account JSON key at the path set in SERVICE_ACCOUNT_FILE.
  3. pip install google-api-python-client google-auth google-analytics-data tabulate
  4. python analyze_low_ctr.py
"""

import os
import sys
from datetime import date, timedelta

from dotenv import dotenv_values

# ---------------------------------------------------------------------------
# Config — read from .env (or environment)
# ---------------------------------------------------------------------------

_env = {**dotenv_values(".env"), **os.environ}


def _require(key: str) -> str:
    val = _env.get(key, "").strip()
    if not val:
        sys.exit(f"ERROR: missing required config '{key}'. Set it in .env or as an env var.")
    return val


SERVICE_ACCOUNT_FILE = _require("SERVICE_ACCOUNT_FILE")
GSC_SITE_URL = _require("GSC_SITE_URL")          # e.g. "https://example.com/" or "sc-domain:example.com"
GA4_PROPERTY_ID = _require("GA4_PROPERTY_ID")    # numeric, e.g. "123456789"

DAYS_BACK = int(_env.get("DAYS_BACK", "90"))
MIN_IMPRESSIONS = int(_env.get("MIN_IMPRESSIONS", "500"))
MAX_CTR = float(_env.get("MAX_CTR", "0.03"))      # 3 %
TOP_N = int(_env.get("TOP_N", "25"))

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

from google.oauth2 import service_account  # noqa: E402
from googleapiclient.discovery import build  # noqa: E402
from google.analytics.data_v1beta import BetaAnalyticsDataClient  # noqa: E402
from google.analytics.data_v1beta.types import (  # noqa: E402
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    Filter,
)


def _credentials():
    return service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )


# ---------------------------------------------------------------------------
# GSC — fetch high-impression / low-CTR pages
# ---------------------------------------------------------------------------

def fetch_gsc_pages() -> list[dict]:
    """Return pages sorted by impressions descending, filtered by CTR threshold."""
    creds = _credentials()
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    end_date = date.today() - timedelta(days=3)  # GSC lags ~3 days
    start_date = end_date - timedelta(days=DAYS_BACK)

    body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["page"],
        "rowLimit": 25000,
        "dataState": "final",
    }

    response = (
        service.searchanalytics()
        .query(siteUrl=GSC_SITE_URL, body=body)
        .execute()
    )

    rows = response.get("rows", [])
    results = []
    for row in rows:
        impressions = row["impressions"]
        ctr = row["ctr"]
        if impressions >= MIN_IMPRESSIONS and ctr <= MAX_CTR:
            results.append(
                {
                    "page": row["keys"][0],
                    "impressions": int(impressions),
                    "clicks": int(row["clicks"]),
                    "ctr_pct": round(ctr * 100, 2),
                    "avg_position": round(row["position"], 1),
                }
            )

    results.sort(key=lambda r: r["impressions"], reverse=True)
    return results[:TOP_N]


# ---------------------------------------------------------------------------
# GA4 — fetch sessions/users for a list of page paths
# ---------------------------------------------------------------------------

def fetch_ga4_traffic(pages: list[dict]) -> dict[str, dict]:
    """Return a dict keyed by page path with GA4 session + user counts."""
    if not pages:
        return {}

    creds = _credentials()
    client = BetaAnalyticsDataClient(credentials=creds)

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=DAYS_BACK)

    # GA4 pagePath strips the domain — extract just the path portion.
    path_map: dict[str, str] = {}  # ga4_path -> original page URL
    for p in pages:
        url = p["page"]
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path or "/"
            if parsed.query:
                path += "?" + parsed.query
        except Exception:
            path = url
        path_map[path] = url

    # Build an OR filter across all paths using individual Filter objects
    # combined through FilterExpression. GA4 supports up to 50 values in
    # an inListFilter, which is far simpler.
    in_list_filter = FilterExpression(
        filter=Filter(
            field_name="pagePath",
            in_list_filter=Filter.InListFilter(values=list(path_map.keys())),
        )
    )

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="totalUsers"),
            Metric(name="screenPageViews"),
        ],
        date_ranges=[
            DateRange(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )
        ],
        dimension_filter=in_list_filter,
    )

    response = client.run_report(request)

    ga4_data: dict[str, dict] = {}
    for row in response.rows:
        path = row.dimension_values[0].value
        ga4_data[path] = {
            "ga4_sessions": int(row.metric_values[0].value),
            "ga4_users": int(row.metric_values[1].value),
            "ga4_pageviews": int(row.metric_values[2].value),
        }

    # Re-key by original URL for easy join
    result: dict[str, dict] = {}
    for path, url in path_map.items():
        result[url] = ga4_data.get(path, {"ga4_sessions": 0, "ga4_users": 0, "ga4_pageviews": 0})
    return result


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def build_report(gsc_rows: list[dict], ga4_map: dict[str, dict]) -> list[dict]:
    merged = []
    for row in gsc_rows:
        ga4 = ga4_map.get(row["page"], {"ga4_sessions": 0, "ga4_users": 0, "ga4_pageviews": 0})
        merged.append({**row, **ga4})
    return merged


def print_report(report: list[dict]) -> None:
    try:
        from tabulate import tabulate
    except ImportError:
        # Fallback: plain CSV
        headers = list(report[0].keys()) if report else []
        print(",".join(headers))
        for row in report:
            print(",".join(str(v) for v in row.values()))
        return

    headers = {
        "page": "Page",
        "impressions": "Impressions",
        "clicks": "Clicks (GSC)",
        "ctr_pct": "CTR %",
        "avg_position": "Avg Position",
        "ga4_sessions": "GA4 Sessions",
        "ga4_users": "GA4 Users",
        "ga4_pageviews": "GA4 Pageviews",
    }

    table_data = [
        [row[k] for k in headers] for row in report
    ]

    print(
        f"\nLow-CTR pages — GSC impressions >= {MIN_IMPRESSIONS:,}, "
        f"CTR <= {MAX_CTR * 100:.0f}%, last {DAYS_BACK} days\n"
    )
    print(tabulate(table_data, headers=list(headers.values()), tablefmt="github"))
    print(f"\n{len(report)} pages shown (TOP_N={TOP_N})\n")


def export_csv(report: list[dict], path: str = "low_ctr_report.csv") -> None:
    import csv
    if not report:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(report[0].keys()))
        writer.writeheader()
        writer.writerows(report)
    print(f"Report saved to {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Fetching GSC data…")
    gsc_rows = fetch_gsc_pages()
    print(f"  {len(gsc_rows)} pages match filters.")

    print("Fetching GA4 data…")
    ga4_map = fetch_ga4_traffic(gsc_rows)

    report = build_report(gsc_rows, ga4_map)
    print_report(report)
    export_csv(report)
