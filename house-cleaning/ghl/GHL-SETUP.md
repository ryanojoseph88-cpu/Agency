# Put the Centrepointe site on GoHighLevel

Two files:

- `page-body.html`: the whole page (styles + content). Goes in a **Custom HTML** element.
- `page-head.html`: schema (LocalBusiness + FAQ). Goes in the page's **Header tracking code**.

Styles are scoped to `#cphc`, so GHL's theme fonts and colours don't bleed in and this CSS doesn't touch the rest of your funnel/site.

## 1. Fix placeholders first

Find and replace in both files:

| Placeholder | Replace with |
|---|---|
| `Centrepointe Home Cleaning` | real business name |
| `(613) 555-0100` and `+16135550100` / `+1-613-555-0100` | real phone (all three formats) |
| `hello@example.ca` | real email |
| `https://www.example.ca/` | your live domain (schema `url`) |
| `Mon–Sat, 8am–6pm` / `08:00`–`18:00` | real hours |

If you have no public storefront, delete the `"address":{...},` line in `page-head.html`.

## 2. Build the page

1. Sites > Websites (or Funnels) > your site > add a page, open the builder.
2. Delete the default sections/header/footer.
3. Add a **Section** set to full width, then a **1-column row**. Set section, row and column padding/margin to 0.
4. Add Elements > **Custom JS/HTML** into the column > Open Code Editor > paste all of `page-body.html` > Save.
5. Preview at desktop and mobile.

## 3. Route leads into GHL (recommended)

The built-in form posts to a Formspree placeholder, so leads won't reach your CRM. To fix:

1. Sites > Forms > Builder: create a form with Name, Phone, Email, Service (dropdown), Home size (dropdown), Neighbourhood/postal code, Notes.
2. Form > Integrate > copy the embed code.
3. In `page-body.html`, delete everything from `<form action=` to `</form>` (just below the `GHL:` comment) and paste the embed code there. Re-save the Custom HTML element.

Then set a workflow trigger on "Form Submitted" to text/email you instantly. Speed-to-lead is most of the conversion rate.

## 4. Page settings (gear icon > Settings)

**SEO Meta Data**

- Title: `House Cleaning in Centrepointe, Ottawa | Centrepointe Home Cleaning`
- Description: `Trusted house cleaning in Centrepointe, Nepean (Ottawa). Regular, deep, move-out and Airbnb cleaning. Same-week availability. Get a free quote today.`
- Social image: a real photo of your team/work, 1200x630.
- Page URL/path: `/` if this is the homepage, otherwise `/house-cleaning-centrepointe`.

**Tracking Code > Header**: paste all of `page-head.html`.

Keep the business name, phone and address identical to your Google Business Profile (NAP consistency).

## 5. Verify after publishing

- Google Rich Results Test on the live URL: should detect LocalBusiness (HouseCleaningService) and FAQ.
- Tap the phone links on a real phone.
- Submit a test lead and confirm it lands in Contacts.
