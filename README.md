# Pouria Business — Excel Automation Studio

The business website for **Pouria Business**, an Excel automation studio offering
professional Excel systems for small businesses, retailers and wholesalers.

Live site: **https://pouriaasghari1.github.io/pouriaasghari/**

> The earlier personal portfolio that used to live at this URL is preserved, unchanged,
> at [`portfolio.html`](portfolio.html). Nothing was deleted from the repository.

---

## What is on the site

| Page | Purpose |
| --- | --- |
| `index.html` | Homepage: hero, catalog overview, why-Excel-automation, demo teaser, process, pricing preview, about, FAQ, contact |
| `products.html` | Full catalog with category filters |
| `products/inventory.html` | Inventory Command Center — product page |
| `products/sales.html` | Sales Performance Studio — product page |
| `products/wholesale.html` | Wholesale Order Hub — product page |
| `products/expenses.html` | Expense Control Center — product page |
| `products/reporting.html` | Executive Reporting Suite — product page |
| `demo.html` | Interactive product demonstrations (working simulations on sample data) |
| `services.html` | Custom Excel development services |
| `pricing.html` | Packages (€290 / €590 / custom from €900), comparison table, add-ons, payment terms |
| `about.html` | About the studio, principles, ways of working |
| `faq.html` | Grouped FAQ |
| `contact.html` | Project briefing form + direct contact channels |
| `404.html` | Custom not-found page |

Supporting files:

- `css/site.css` — the whole design system (dark charcoal + emerald, Space Grotesk + Inter).
- `js/site.js` — nav, mobile drawer, scroll reveals, tabs, catalog filters, form composer, toast.
- `js/demo.js` — the interactive demo engine for the five systems.
- `assets/logo.svg`, `assets/favicon.svg` — original logo mark (works, rising automation bars, spark).
- `assets/fonts/*.woff2` — self-hosted Space Grotesk and Inter (no external requests).
- `assets/img/*.webp|png|jpg` — original dashboard mockups (see below).
- `robots.txt`, `sitemap.xml`, `.nojekyll` — crawling and GitHub Pages plumbing.

## Visuals — all original

Every dashboard image on this site was **drawn from scratch** as vector geometry in
`tools/dash.py` + `tools/compose.py` (SVG sources in `tools/svg/`, rasterised with `sharp`):

| File | Shows |
| --- | --- |
| `dash-hero` | Consolidated executive overview (hero) |
| `dash-inventory` | Inventory Command Center |
| `dash-sales` | Sales Performance Studio |
| `dash-wholesale` | Wholesale Order Hub |
| `dash-expenses` | Expense Control Center |
| `dash-reporting` | Executive Reporting Suite |
| `og-image` | Social share card |

No stock images, no third-party screenshots, no AI-generated text artefacts.

## Honesty rules followed

- The figures inside the mockups are **labelled sample data**; the site says so next to them.
- **No testimonials, no customer counts, no invented statistics** anywhere.
- The demos are described as *simulations of the calculation logic* — not as the product itself.
- The contact form does not fake a server submission: it composes a pre-filled email in the
  visitor's own mail client (this is a static GitHub Pages site).
- Real contact details only: `pouriabusines1@gmail.com`,
  `instagram.com/pouria_busines`, `github.com/pouriaasghari1`.

## Telegram

Telegram is intentionally **not** linked on the site yet: the owner has not supplied an
official Telegram handle, and no username is invented. To enable it, set `TELEGRAM` in
`tools/tpl.py` to the real link and rebuild — the footer icon, footer link and Contact page
row all render automatically.

```python
TELEGRAM = "https://t.me/<handle>"   # tools/tpl.py — set only when the owner supplies one
```

## Search appearance (SEO)

Everything Google needs to show the site correctly is generated from `tools/tpl.py`
(`head()`, `site_identity()`) — do not hand-edit the `<head>` of generated pages.

| Item | Source | Value |
| --- | --- | --- |
| Search title (home) | `SITE_TITLE` | `Pouria Business | Excel Automation & Business Solutions` |
| Meta description (home) | `SITE_DESCRIPTION` | the 159-character description in `tools/tpl.py` |
| Site name | `WebSite` JSON-LD `name`, `og:site_name` | `Pouria Business` |
| Founder | `Person` JSON-LD | `Pouria Asghari` |
| Canonical / OG URL | `SITE_URL` | `https://pouriaasghari1.github.io/pouriaasghari/` |

**Favicon.** `favicon.ico` (16/32/48 multi-size) plus `assets/img/favicon-{16,32,48,96,180,192,512}.png`
and `assets/img/apple-touch-icon.png` are all square crops of the owner's profile photo
(`pouria.jpg`). Google requires a square, crawlable icon at a stable URL; to regenerate after
replacing the photo, re-crop and re-export the same sizes.

**Structured data.** Every page carries `Organization`, `WebSite` and `Person`; the catalog adds
`ItemList` + `BreadcrumbList`, product pages add `Product` + `BreadcrumbList`, the FAQ page adds
`FAQPage`, and the contact page adds `ContactPage`. No addresses, phone numbers, ratings or
customer counts are declared anywhere — only verifiable facts.

**Crawling.** `robots.txt` allows everything and points at `sitemap.xml`, which lists the 13
business pages. `site.webmanifest` supplies the PWA name and icons. The 404 page is
`noindex,follow` by design.

**After publishing,** changed titles, descriptions, favicons and site names only show up once
Google recrawls. Use Search Console → URL Inspection → *Request Indexing* for the homepage to
speed it up; favicon and site-name changes typically take days to a few weeks and Google may
still choose its own thumbnail.

## Publishing

The site is plain static HTML/CSS/JS with **relative links**, so it works at a project URL
(`/pouriaasghari/`) as well as on a custom domain.

**Already published:** GitHub Pages is enabled on this repository, serving the `main`
branch root. Pushing the new files to `main` is all that is needed:

```
git add .
git commit -m "Rebrand site as Pouria Business"
git push origin main
```

Then check **Settings → Pages** (Source: *Deploy from a branch*, Branch: `main` / `/ (root)`).
The build takes a minute or two; hard-refresh afterwards to bypass caches.

## Rebuilding the site (optional)

The pages are generated by small Python scripts so navigation, footer and product data stay
in sync.

```bash
cd tools
python3 build_all.py        # rewrites every HTML page from tpl.py + product data
```

To regenerate the dashboard artwork:

```bash
cd tools
npm install sharp
python3 compose.py          # writes SVG sources into tools/svg/
node render.js              # renders PNG / JPG / WebP into assets/img/
```

## Local preview

```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

A local server is required to see the WebP images and fonts exactly as deployed; opening
`index.html` directly from disk also works with the PNG fallbacks.

---

© Pouria Business. Code, copy, logo and artwork in this repository are original work for
this project.
