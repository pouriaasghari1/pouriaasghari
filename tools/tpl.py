#!/usr/bin/env python3
"""Shared layout + content data for the Pouria Business site."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = "Pouria Business"
BRAND_SHORT = "POURIA"
BRAND_TAG = "BUSINESS"
# --------------------------------------------------------------------------
# pricing
# --------------------------------------------------------------------------
# Catalogue prices were set in EUR. They are presented in USD (the primary
# currency) with the original EUR figure kept as a reference, converted at a
# fixed published rate so the two never drift apart between pages.
EUR_USD = 1.12          # reference rate used for the displayed conversions
PRICES_AS_OF = "November 2026"

# EUR reference for every headline figure, keyed by the USD amount.
EUR_REF = {
    "290": "€260",
    "325": "€290",
    "340": "€305",
    "390": "€350",
    "435": "€390",
    "490": "€435",
    "590": "€525",
    "655": "€585",
    "660": "€590",
    "900": "€800",
    "1000": "€895",
    "1500": "€1340",
}


def usd(amount, prefix=""):
    """Format a USD figure, e.g. usd(325) -> '$325'."""
    return f"{prefix}${amount:,}"


def ref(amount):
    """EUR reference for a USD figure, e.g. ref(325) -> '(≈ €290)'."""
    eur = EUR_REF.get(str(amount))
    return f" (≈ {eur})" if eur else ""


# Conversion note rendered under every price block.
PRICE_NOTE = (f"Prices in USD. EUR shown for reference at ≈ €1 = ${EUR_USD:.2f} "
              f"({PRICES_AS_OF}). Final quote is confirmed in writing before any work starts — "
              f"the exact figure depends on your scope, data and requirements.")

SITE_TITLE = "Pouria Business | Excel Automation & Business Solutions"
SITE_DESCRIPTION = ("Pouria Business by Pouria Asghari provides smart Excel automation solutions for sales "
                    "management, inventory tracking, business reporting, and order management.")
SITE_URL = "https://pouriaasghari1.github.io/pouriaasghari"
EMAIL = "pouriabusines1@gmail.com"
INSTAGRAM = "https://www.instagram.com/pouria_busines/"
INSTAGRAM_HANDLE = "@pouria_busines"
# Telegram is intentionally empty until the owner supplies the real handle.
TELEGRAM = "https://t.me/pouria_busines"
TELEGRAM_HANDLE = "@pouria_busines"
GITHUB = "https://github.com/pouriaasghari1"

# --------------------------------------------------------------------------
# icons (inline svg, 24x24 stroke style)
# --------------------------------------------------------------------------
def ico(name, cls="", sw=1.7):
    p = {
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "arrow-up-right": '<path d="M7 17 17 7M8 7h9v9"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        "box": '<path d="M21 8.5 12 3 3 8.5v7L12 21l9-5.5z"/><path d="M3 8.5 12 14l9-5.5M12 14v7"/>',
        "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h2.5l2.6 11h11L21 7H6"/>',
        "truck": '<path d="M2 7h11v9H2zM13 10h4l4 3.5V16h-8z"/><circle cx="6.5" cy="18.5" r="1.6"/><circle cx="17" cy="18.5" r="1.6"/>',
        "card": '<rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M2 10h20"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "bolt": '<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
        "shield": '<path d="M12 2.6 4.5 6v6.2c0 4.2 3 7.4 7.5 9.2 4.5-1.8 7.5-5 7.5-9.2V6z"/><path d="m8.6 12 2.5 2.5 4.4-4.6"/>',
        "sparkle": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3.2 2"/>',
        "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
        "mouse": '<rect x="6" y="2.5" width="12" height="19" rx="6"/><path d="M12 7v3"/>',
        "download": '<path d="M12 3v12M7 11l5 5 5-5M4 20h16"/>',
        "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m3 7 9 6.5L21 7"/>',
        "send": '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4z"/>',
        "phone": '<path d="M6.5 3h3l1.5 4-2 1.5a11 11 0 0 0 6.5 6.5L17 13l4 1.5v3A2.5 2.5 0 0 1 18.5 20C10.5 19.4 4.6 13.5 4 5.5A2.5 2.5 0 0 1 6.5 3z"/>',
        "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
        "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
        "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>',
        "lock": '<rect x="4.5" y="10" width="15" height="11" rx="2.5"/><path d="M8.5 10V7.5a3.5 3.5 0 0 1 7 0V10"/>',
        "users": '<circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16.5 5.2a3.2 3.2 0 0 1 0 5.9M17.5 14.4a6 6 0 0 1 4 5.6"/>',
        "wrench": '<path d="M15 3a5 5 0 0 0-4.4 7.4L3 18v3h3l7.6-7.6A5 5 0 0 0 21 9l-3 3-3-3 3-3a5 5 0 0 0-3-3z"/>',
        "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
        "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 5 5"/>',
        "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
        "menu": '',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
        "chevron-down": '<path d="m6 9 6 6 6-6"/>',
        "play": '<path d="M8 5.5v13l11-6.5z"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 3 2.6 15 0 18M12 3c-2.6 3-2.6 15 0 18"/>',
        "database": '<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
        "instagram": '<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.2"/><circle cx="12" cy="12" r="4.1"/><circle cx="17.2" cy="6.9" r="1.05" fill="currentColor" stroke="none"/>',
        "broom": '<path d="M4 21l5-5M14 3l7 7-4 2-5-5z"/><path d="M9 12l-4 9 9-4"/>',
    }
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>'
            % (sw, (' class="' + cls + '"') if cls else '', p.get(name, "")))

# --------------------------------------------------------------------------
# product catalogue
# --------------------------------------------------------------------------
PRODUCTS = [
    {
        "slug": "inventory",
        "name": "Inventory Command Center",
        "short": "Inventory System",
        "tagline": "Know exactly what you have, what is running out and what to reorder — before it costs you a sale.",
        "desc": "Excel inventory system with live reorder alerts, stock valuation and supplier lead times — so you know exactly what to reorder.",
        "icon": "box",
        "image": "dash-inventory",
        "price": "$435",
        "price_eur": "€390",
        "price_note": "one-time build · starting from",
        "badge": "Most requested",
        "categories": "retail wholesale",
        "best": "Retailers &amp; wholesalers with 200–5,000 SKUs",
        "best_title": "retailers and wholesalers",
        "deliverables": [
            "Stock master sheet with validated SKU entry",
            "Automatic reorder flags against your reorder points",
            "Valuation dashboard (cost, retail, dead stock)",
            "Supplier list with lead times and open orders",
            "Stock movement log + monthly PDF report",
        ],
        "inside": [
            ("tbl_Stock", "One row per SKU: code, name, category, supplier, cost, price, on-hand, reorder point, lead time."),
            ("tbl_Movements", "Every receipt, sale and adjustment. On-hand is calculated from this log, so nothing drifts."),
            ("Dashboard", "KPI cards, stock-health ring, category mix and a 12-month movement chart."),
            ("Reorder sheet", "Only the SKUs that need attention, with a suggested order quantity based on lead time."),
            ("Valuation", "Cost and retail valuation with dead-stock highlighting and slow-mover ranking."),
        ],
        "metrics": [("Inventory value", "$1,428,900", "Sample"), ("Active SKUs", "2,486", "Sample"), ("Low-stock alerts", "37", "Sample")],
        "features": [
            ("Live reorder logic", "Reorder status is a formula, not a judgement call. Change a reorder point and every flag, alert and dashboard card follows."),
            ("Movement-based stock", "On-hand is derived from receipts and sales, so the sheet reconciles with reality instead of guesses."),
            ("Two-warehouse ready", "Track main stock and secondary locations side by side with an automatic transfer log."),
            ("Dead-stock detection", "Items with no movement in 60/90/180 days are ranked so you can free up cash."),
        ],
        "demo": "inventory",
        "faqs": [
            ("How many SKUs can it handle?", "Comfortably a few thousand on a normal laptop. Above roughly 10,000 rows we move the heavy lists to Power Query so the workbook stays fast."),
            ("Does it work with barcodes?", "The stock sheet has a barcode/SKU column. If you use a scanner or a POS export, we can import that file automatically each day."),
            ("Can I keep my current product codes?", "Yes. Your codes stay exactly as they are — the system is built around your existing file, not a new numbering scheme."),
        ],
    },
    {
        "slug": "sales",
        "name": "Sales Performance Studio",
        "short": "Sales System",
        "tagline": "Every sale in one place, with revenue, margin and channel performance that update themselves.",
        "desc": "Excel sales system that turns order entry into revenue, margin and channel dashboards — no manual reporting.",
        "icon": "cart",
        "image": "dash-sales",
        "price": "$435",
        "price_eur": "€390",
        "price_note": "one-time build · starting from",
        "badge": "",
        "categories": "retail wholesale",
        "best": "Shops and distributors invoicing from Excel",
        "best_title": "shops and distributors",
        "deliverables": [
            "Fast order entry with product and price lookup",
            "Automatic revenue, margin and AOV calculation",
            "Product, channel and customer breakdowns",
            "Monthly target vs actual tracking",
            "Returns and discount handling",
        ],
        "inside": [
            ("tbl_Sales", "Order lines with date, product, quantity, unit price, discount and channel."),
            ("tbl_Products", "Product and price list the order form looks up, so prices cannot be mistyped."),
            ("Dashboard", "Revenue vs target, channel mix, top products and daily averages."),
            ("Targets", "Monthly targets per channel; the dashboard shows the gap and the run rate."),
            ("Reports", "A printable monthly summary with the numbers your accountant asks for."),
        ],
        "metrics": [("Net revenue", "$286,430", "Sample"), ("Orders", "3,742", "Sample"), ("Avg order value", "$76.54", "Sample")],
        "features": [
            ("Entry designed for speed", "Typing a product code fills the name and price. Duplicate order numbers and impossible quantities are blocked on entry."),
            ("Margins you can trust", "Cost sits on the product table, so gross margin is calculated per line and per product, not estimated."),
            ("Targets and run-rate", "See whether the month is on track, not just what happened last month."),
            ("Clean hand-off", "One click produces a monthly summary sheet and PDF for your accountant."),
        ],
        "demo": "sales",
        "faqs": [
            ("Can it import my till or POS exports?", "Yes — CSV exports from most POS systems can be dropped into an import sheet that cleans and appends them automatically."),
            ("Does it handle VAT?", "Yes. Prices can be entered gross or net and the workbook shows both, with the VAT rate on each line."),
            ("Can I invoice from it?", "The system generates a clean invoice layout you can print or export to PDF. It is not a certified e-invoicing platform, but it produces the document."),
        ],
    },
    {
        "slug": "wholesale",
        "name": "Wholesale Order Hub",
        "short": "Wholesale System",
        "tagline": "Purchase orders, trade accounts, backorders and receivables without a single lost email.",
        "desc": "Excel wholesale system for purchase orders, trade accounts, fill rates, receivables and delivery schedules in one workbook.",
        "icon": "truck",
        "image": "dash-wholesale",
        "price": "$660",
        "price_eur": "€590",
        "price_note": "one-time build · starting from",
        "badge": "B2B",
        "categories": "wholesale",
        "best": "Wholesalers and B2B distributors",
        "best_title": "wholesalers and B2B distributors",
        "deliverables": [
            "Trade account register with agreed price lists",
            "Purchase order pipeline with status flow",
            "Fill-rate and backorder tracking",
            "Receivables ageing by customer",
            "Delivery schedule and reminder sheet",
        ],
        "inside": [
            ("tbl_PurchaseOrders", "PO header plus lines, with a validated status flow so no order silently skips a stage."),
            ("tbl_Accounts", "Trade customers, agreed discount levels, credit limits and payment terms."),
            ("Pipeline", "Kanban-style status counts: confirmed, picking, in transit, delivered."),
            ("Receivables", "Ageing buckets (current, 1–30, 31–60, 60+) calculated from invoice dates."),
            ("Delivery planner", "One sheet showing what must leave the warehouse this week."),
        ],
        "metrics": [("Open POs", "148", "Sample"), ("Fulfilled value", "$412,900", "Sample"), ("Fill rate", "96.4%", "Sample")],
        "features": [
            ("Multi-line POs without chaos", "One PO can hold dozens of lines with per-line quantities and prices, while the header stays a single order."),
            ("Fill rate that is calculated", "Delivered lines ÷ ordered lines, per PO and per account — no manual percentage typing."),
            ("Credit visibility", "Outstanding balances per account against agreed limits, so you see risk before you ship."),
            ("Status that cannot skip", "Dropdown validation and conditional formatting keep the workflow honest."),
        ],
        "demo": "wholesale",
        "faqs": [
            ("Can several people work in it?", "The workbook can sit on a shared drive or in OneDrive/SharePoint for multi-user editing. For heavier use we split entry and reporting into two files linked by Power Query."),
            ("Does it produce customer-facing documents?", "Yes — a branded order confirmation and delivery note layout are included."),
            ("Can it link to my accounting app?", "Through CSV import/export, usually. It is not a live two-way accounting integration."),
        ],
    },
    {
        "slug": "expenses",
        "name": "Expense Control Center",
        "short": "Expense System",
        "tagline": "See where the money actually goes — by category, vendor and month — without chasing receipts.",
        "desc": "Excel expense system with approvals, budget-versus-actual by team and a month-end close that takes minutes.",
        "icon": "card",
        "image": "dash-expenses",
        "price": "$325",
        "price_eur": "€290",
        "price_note": "one-time build · starting from",
        "badge": "",
        "categories": "retail wholesale",
        "best": "Small businesses that need cost control",
        "best_title": "small businesses",
        "deliverables": [
            "Expense log with categories and vendors",
            "Budget vs actual per month and per team",
            "Approval status with pending queue",
            "Recurring cost register",
            "Monthly expense summary report",
        ],
        "inside": [
            ("tbl_Expenses", "Date, vendor, category, amount, tax, payment method, status, receipt reference."),
            ("Budgets", "Per category and per month. Actual spend pulls straight from the expense log."),
            ("Approvals", "Pending, approved and rejected in one status column with a review queue."),
            ("Recurring costs", "Rent, subscriptions and utilities flagged so they are never forgotten."),
            ("Close checklist", "A short month-end routine so nothing is missed before the report is sent."),
        ],
        "metrics": [("Monthly spend", "$84,260", "Sample"), ("Budget used", "72%", "Sample"), ("Pending approval", "9", "Sample")],
        "features": [
            ("Budget versus actual, live", "Every approved expense immediately moves the bar and the remaining-budget figure."),
            ("Vendor view", "Spend by vendor highlights where consolidation or renegotiation would pay off."),
            ("Receipt discipline", "Each row carries a receipt reference and a link field, so audits are painless."),
            ("Month-end in minutes", "A prepared close sheet and a one-page summary keep the routine under ten minutes."),
        ],
        "demo": "expenses",
        "faqs": [
            ("Can I photograph receipts?", "The workbook holds links or file names; kept in the same cloud folder, image links open with one click. It is not OCR software."),
            ("Does it support multiple currencies?", "Yes, with a rate table you update monthly. Totals convert into your base currency."),
            ("Can I track personal and company spending together?", "You can, but we recommend separate files and a combined reporting sheet — that keeps the books clean."),
        ],
    },
    {
        "slug": "reporting",
        "name": "Executive Reporting Suite",
        "short": "Reporting System",
        "tagline": "One page that answers the question your bank, your partner or your accountant always asks.",
        "desc": "Excel reporting system that consolidates your data into a one-page scorecard and a print-ready board pack.",
        "icon": "chart",
        "image": "dash-reporting",
        "price": "$545",
        "price_eur": "€490",
        "price_note": "one-time build · starting from",
        "badge": "Board-ready",
        "categories": "retail wholesale reporting",
        "best": "Owners who need one honest number",
        "best_title": "business owners",
        "deliverables": [
            "Consolidation of up to 6 source files or sheets",
            "Executive scorecard with month and quarter views",
            "Cash, margin and working-capital indicators",
            "Automatic refresh routine (Power Query)",
            "Print-ready board pack layout",
        ],
        "inside": [
            ("Sources", "Stock, sales, wholesale and expense figures pulled into one clean model, either by formula or Power Query."),
            ("Scorecard", "Metric, this month, last month, change and status — the page a board actually reads."),
            ("Indicators", "Gross margin, cash runway estimate, receivables days and inventory turns."),
            ("Board pack", "A four-page printable layout generated from the same data."),
            ("Notes", "A commentary sheet so the numbers carry their explanation with them."),
        ],
        "metrics": [("Reports delivered", "128", "Sample"), ("Sources", "6", "Sample"), ("Refresh time", "38s", "Sample")],
        "features": [
            ("One source of truth", "Report figures are linked, never retyped, so the board pack cannot disagree with the workbook."),
            ("Power Query refresh", "Point it at your folders or exports and press refresh; the model rebuilds itself."),
            ("Built for printing", "Page breaks, headers and footers are set so the PDF looks deliberate, not accidental."),
            ("Commentary included", "A notes sheet next to the numbers makes the pack explain itself."),
        ],
        "demo": "reporting",
        "faqs": [
            ("Can it combine several companies?", "Yes, up to six entities in the standard build, with per-entity and consolidated views."),
            ("Do I need Power BI?", "No. This is native Excel. Power BI is a separate option if you later want web dashboards."),
            ("How current are the numbers?", "As current as a refresh: one button, then the pack is up to date."),
        ],
    },
]

PRODUCT_BY_SLUG = {p["slug"]: p for p in PRODUCTS}

# --------------------------------------------------------------------------
# layout
# --------------------------------------------------------------------------
def jsonld(*blocks):
    """Serialise one or more JSON-LD graphs into a script tag."""
    import json
    payload = blocks[0] if len(blocks) == 1 else {"@context": "https://schema.org", "@graph": [b for b in blocks]}
    text = json.dumps(payload, ensure_ascii=False, indent=1)
    return '<script type="application/ld+json">\n' + text + "\n</script>\n"


def site_identity():
    """Organization + WebSite + Person graph. No invented addresses, phones or ratings."""
    import json
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": BRAND,
        "alternateName": "Pouria Business — Excel Automation",
        "url": SITE_URL + "/",
        "description": SITE_DESCRIPTION,
        "email": EMAIL,
        "logo": {
            "@type": "ImageObject",
            "url": SITE_URL + "/assets/img/favicon-512.png",
            "width": 512,
            "height": 512,
        },
        "image": SITE_URL + "/assets/img/og-image.png",
        "founder": {"@id": SITE_URL + "/#person"},
        "employee": {"@id": SITE_URL + "/#person"},
        "sameAs": [INSTAGRAM, TELEGRAM, GITHUB],
        "knowsAbout": [
            "Excel automation",
            "Inventory management",
            "Sales reporting",
            "Wholesale order management",
            "Expense tracking",
            "Business reporting",
            "Power Query",
            "VBA",
        ],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Excel automation systems"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom Excel development"}},
        ],
    }
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE_URL + "/#website",
        "name": BRAND,
        "url": SITE_URL + "/",
        "description": SITE_DESCRIPTION,
        "inLanguage": "en",
        "publisher": {"@id": SITE_URL + "/#organization"},
    }
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": SITE_URL + "/#person",
        "name": "Pouria Asghari",
        "jobTitle": "Founder",
        "description": "Founder of Pouria Business, building Excel automation systems for small businesses, retailers and wholesalers.",
        "worksFor": {"@id": SITE_URL + "/#organization"},
        "email": "mailto:" + EMAIL,
        "url": SITE_URL + "/about.html",
        "image": SITE_URL + "/pouria.jpg",
        "sameAs": [INSTAGRAM, TELEGRAM, GITHUB],
    }
    return jsonld(org, website, person)


def head(title, description, base="", extra="", canonical="", page_type="website", structured=None, image="assets/img/og-image.png"):
    url = canonical or (SITE_URL + "/")
    og_image = image if image.startswith("http") else SITE_URL + "/" + image
    ld = site_identity() if structured is None else structured
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#050706">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Pouria Business">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="googlebot" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<!-- Open Graph -->
<meta property="og:type" content="{page_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND} — Excel automation systems for small business">
<meta property="og:url" content="{url}">
<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@pouria_busines">
<meta name="twitter:creator" content="@pouria_busines">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{BRAND} — Excel automation systems for small business">
<!-- Icons: profile photo, square, multi-size -->
<link rel="icon" href="{base}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="16x16" href="{base}assets/img/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="{base}assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="{base}assets/img/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="{base}assets/img/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="{base}assets/img/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{base}assets/img/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="192x192" href="{base}assets/img/favicon-192.png">
<link rel="mask-icon" href="{base}assets/favicon.svg" color="#34e0a1">
<link rel="manifest" href="{base}site.webmanifest">
<meta name="application-name" content="{BRAND}">
<meta name="apple-mobile-web-app-title" content="{BRAND}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="preload" href="{base}assets/fonts/SpaceGrotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/Inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}css/site.css">
{extra}
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav(base="", active=""):
    def a(href, label, key):
        cls = ' class="nav__link is-active"' if key == active else ' class="nav__link"'
        return f'<a href="{base}{href}"{cls}>{label}</a>'

    product_items = "".join(
        f'<a class="menu__item" href="{base}products/{p["slug"]}.html">'
        f'<span class="menu__icon">{ico(p["icon"], sw=1.8)}</span>'
        f'<span><span class="menu__t">{p["short"]}</span>'
        f'<span class="menu__d">{p["tagline"][:62]}…</span></span></a>'
        for p in PRODUCTS
    )
    drawer_items = "".join(
        f'<a href="{base}products/{p["slug"]}.html" data-nav>{p["short"]}<span>System</span></a>'
        for p in PRODUCTS
    )
    return f"""<header class="nav" id="site-nav">
 <div class="container nav__inner">
  <a class="brand" href="{base}index.html" aria-label="{BRAND} — home" title="{BRAND}">
   <img class="brand__mark" src="{base}assets/logo.svg" alt="{BRAND} logo" width="36" height="36">
   <span class="brand__text"><span class="brand__name">{BRAND}</span><span class="brand__tag">EXCEL AUTOMATION</span></span>
  </a>
  <nav class="nav__links" aria-label="Main">
   <a href="{base}index.html"{' class="nav__link is-active"' if active == 'home' else ' class="nav__link"'}>Home</a>
   <div class="has-menu">
    <a href="{base}products.html"{' class="nav__link is-active"' if active == 'products' else ' class="nav__link"'}>Systems {ico('chevron-down', sw=2.2)}</a>
    <div class="menu" role="group" aria-label="Excel systems">
     {product_items}
     <a class="menu__item" href="{base}products.html" style="border-top:1px solid var(--line-soft);margin-top:4px;padding-top:12px">
      <span class="menu__icon">{ico('grid', sw=1.8)}</span>
      <span><span class="menu__t">All systems</span><span class="menu__d">Compare the full catalog and pricing</span></span>
     </a>
     <a class="menu__item" href="{base}demo.html" style="border-top:1px solid var(--line-soft);margin-top:4px;padding-top:12px">
      <span class="menu__icon">{ico('play', sw=1.8)}</span>
      <span><span class="menu__t">Live demos</span><span class="menu__d">Try the calculation logic in your browser</span></span>
     </a>
    </div>
   </div>
   <a href="{base}services.html"{' class="nav__link is-active"' if active == 'services' else ' class="nav__link"'}>Custom work</a>
   <a href="{base}pricing.html"{' class="nav__link is-active"' if active == 'pricing' else ' class="nav__link"'}>Pricing</a>
   <a href="{base}about.html"{' class="nav__link is-active"' if active == 'about' else ' class="nav__link"'}>About</a>
   <a href="{base}contact.html"{' class="nav__link is-active"' if active == 'contact' else ' class="nav__link"'}>Contact</a>
  </nav>
  <div class="nav__actions">
   <a class="btn btn--ghost btn--sm" href="{base}contact.html">Book a call</a>
   <a class="btn btn--primary btn--sm" href="{base}pricing.html">See pricing {ico('arrow', sw=2)}</a>
   <button class="burger" type="button" aria-label="Toggle menu" aria-expanded="false" aria-controls="drawer">
    <i></i><i></i><i></i>
   </button>
  </div>
 </div>
</header>
<div class="drawer" id="drawer" inert>
 <a href="{base}index.html">Home<span>01</span></a>
 <p class="drawer__group">Excel systems</p>
 {drawer_items}
 <a href="{base}products.html">All systems<span>Catalog</span></a>
 <a href="{base}demo.html">Live demos<span>Try it</span></a>
 <p class="drawer__group">Studio</p>
 <a href="{base}services.html">Custom Excel work<span>Services</span></a>
 <a href="{base}pricing.html">Pricing<span>Plans</span></a>
 <a href="{base}about.html">About<span>Studio</span></a>
 <a href="{base}contact.html">Contact<span>Start</span></a>
 <a class="btn btn--primary btn--block" href="{base}contact.html">Start a project {ico('arrow', sw=2)}</a>
</div>
"""


def footer(base=""):
    # Telegram stays hidden until the owner supplies the real handle/link.
    telegram_social = (f'<a href="{TELEGRAM}" target="_blank" rel="noopener noreferrer" '
                       f'aria-label="Telegram {TELEGRAM_HANDLE}" title="Telegram {TELEGRAM_HANDLE}">'
                       f'{ico("send", sw=1.8)}</a>') if TELEGRAM else ""
    telegram_link = (f'<li><a href="{TELEGRAM}" target="_blank" rel="noopener noreferrer">'
                     f'Telegram {TELEGRAM_HANDLE}</a></li>') if TELEGRAM else ""
    links = "".join(
        f'<li><a href="{base}products/{p["slug"]}.html">{p["short"]}</a></li>' for p in PRODUCTS
    )
    return f"""<footer class="footer">
 <div class="container">
  <div class="footer__top">
   <div class="footer__brand">
    <a class="brand" href="{base}index.html" aria-label="{BRAND} — home" title="{BRAND}">
     <img class="brand__mark" src="{base}assets/logo.svg" alt="{BRAND} logo" width="36" height="36">
     <span class="brand__text"><span class="brand__name">{BRAND}</span><span class="brand__tag">EXCEL AUTOMATION</span></span>
    </a>
    <p>Professional Excel automation systems for small businesses, retailers and wholesalers.</p>
    <div class="owner">
     <img class="owner__photo" src="{base}pouria.jpg" alt="Pouria Asghari, founder of Pouria Business" width="120" height="120" loading="lazy" decoding="async">
     <div class="owner__text">
      <strong>Pouria Asghari</strong>
      <span>Founder &amp; owner · {BRAND}</span>
      <em>These Instagram, Telegram and email accounts are the official channels of this site.</em>
     </div>
    </div>
    <div class="social" style="margin-top:18px">
     <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Instagram {INSTAGRAM_HANDLE}" title="Instagram {INSTAGRAM_HANDLE}">{ico('instagram', sw=1.8)}</a>
     <a href="mailto:{EMAIL}" aria-label="Email {BRAND}" title="{EMAIL}">{ico('mail', sw=1.8)}</a>
     {telegram_social}
     <a href="{GITHUB}" target="_blank" rel="noopener noreferrer" aria-label="GitHub profile" title="GitHub">{ico('code', sw=1.8)}</a>
    </div>
   </div>
   <div>
    <h4>Systems</h4>
    <ul>{links}<li><a href="{base}products.html">All systems</a></li></ul>
   </div>
   <div>
    <h4>Studio</h4>
    <ul>
     <li><a href="{base}services.html">Custom Excel development</a></li>
     <li><a href="{base}pricing.html">Pricing</a></li>
     <li><a href="{base}demo.html">Product demonstrations</a></li>
     <li><a href="{base}about.html">About</a></li>
     <li><a href="{base}faq.html">FAQ</a></li>
    </ul>
   </div>
   <div>
    <h4>Contact</h4>
    <ul>
     <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram {INSTAGRAM_HANDLE}</a></li>
     {telegram_link}
     <li><a href="{base}contact.html">Project briefing form</a></li>
     <li><a href="{base}portfolio.html">Personal portfolio (older)</a></li>
    </ul>
   </div>
  </div>
  <div class="footer__bottom">
   <span>© <span data-year>2026</span> {BRAND}. All rights reserved.</span>
   <span>Built with plain HTML, CSS and JavaScript · Excel automation by Pouria Business</span>
  </div>
 </div>
</footer>
<script src="{base}js/site.js" defer></script>
"""


def page(filename, title, description, body, base="", active="", extra_head="", canonical="", body_class="", structured=None, page_type="website", image="assets/img/og-image.png"):
    html = (head(title, description, base, extra_head, canonical,
                 page_type=page_type, structured=structured, image=image)
            + nav(base, active)
            + body
            + footer(base)
            + f"\n</body>\n</html>\n")
    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename, len(html))


def picture(name, alt, base="", sizes="100vw", cls="", loading="lazy", w=1440, h=900, priority=False):
    fp = 'fetchpriority="high" ' if priority else ''
    ld = 'eager' if priority else loading
    return ('<picture class="' + cls + '">'
            '<source type="image/webp" srcset="' + base + 'assets/img/' + name + '.webp">'
            '<img src="' + base + 'assets/img/' + name + '.png" alt="' + alt + '" width="' + str(w) + '" height="' + str(h) + '" '
            'loading="' + ld + '" ' + fp + 'decoding="async"></picture>')
