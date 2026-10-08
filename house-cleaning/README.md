# House cleaning site (Centrepointe, Ottawa)

Static site, no build step. Open `index.html` or serve with `python3 -m http.server`.

- `index.html` single-page site with LocalBusiness and FAQ schema
- `styles.css` styles
- `gbp-setup.md` Google Business Profile content and setup checklist

## Before launch

Replace in `index.html`: business name, phone `(613) 555-0100`, email, domain `example.ca` (canonical + schema), Formspree ID, hours. Remove the `address` block in schema if you are a service-area business without a public address.
