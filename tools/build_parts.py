#!/usr/bin/env python3
"""Catalog, product detail pages, demo page."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import *

# ---------------------------------------------------------------- shared parts
def cta_band(base, title, text, primary=(("contact.html", "Start a project"),), secondary=None):
    btns = "".join(
        f'<a class="btn {"btn--primary" if i == 0 else "btn--ghost"}" href="{base}{href}">{label} {ico("arrow", sw=2) if i == 0 else ""}</a>'
        for i, (href, label) in enumerate(primary))
    bs = f'<a class="btn btn--ghost" href="{base}{secondary[0]}">{secondary[1]}</a>' if secondary else ""
    return f"""<section class="section section--tight">
 <div class="container">
  <div class="card reveal" style="padding:clamp(26px,4vw,50px);text-align:center;
     background:radial-gradient(120% 140% at 50% 0%,rgba(52,224,161,.14),transparent 62%),var(--surface);border-color:rgba(52,224,161,.2)">
   <h2 style="font-size:clamp(24px,3.4vw,38px);max-width:22ch;margin-inline:auto">{title}</h2>
   <p style="color:var(--muted);max-width:58ch;margin:14px auto 0">{text}</p>
   <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:26px">{btns}{bs}</div>
  </div>
 </div>
</section>"""


def price_cards(base=""):
    return f"""<div class="price-grid">
 <div class="card price reveal">
  <span class="price__name">Starter system</span>
  <div><span class="price__amount">€290<span>one-time</span></span></div>
  <p class="price__desc">One core workbook for a single job — expense control or a clean sales tracker.</p>
  <ul class="price__list">
   <li>{ico('check', sw=2.2)}One catalog system (Expense Control Center)</li>
   <li>{ico('check', sw=2.2)}Up to 3 source sheets</li>
   <li>{ico('check', sw=2.2)}Dashboard + one printable report</li>
   <li>{ico('check', sw=2.2)}Input validation and protected formulas</li>
   <li>{ico('check', sw=2.2)}Handover call + written manual</li>
   <li>{ico('check', sw=2.2)}14 days of post-handover support</li>
  </ul>
  <div class="price__foot"><a class="btn btn--ghost btn--block" href="{base}contact.html" data-select-plan="Starter">Choose Starter {ico('arrow', sw=2)}</a></div>
 </div>
 <div class="card price price--feature reveal" data-d="1">
  <span class="tag price__badge">Most chosen</span>
  <span class="price__name">Business system</span>
  <div><span class="price__amount">€590<span>one-time</span></span></div>
  <p class="price__desc">A full operating system: inventory, sales, wholesale orders or consolidated reporting.</p>
  <ul class="price__list">
   <li>{ico('check', sw=2.2)}Any one catalog system</li>
   <li>{ico('check', sw=2.2)}Up to 8 sheets + full dashboard</li>
   <li>{ico('check', sw=2.2)}Automated refresh routine (Power Query)</li>
   <li>{ico('check', sw=2.2)}Validated inputs + sheet protection</li>
   <li>{ico('check', sw=2.2)}Recorded walkthrough + written manual</li>
   <li>{ico('check', sw=2.2)}30 days of post-handover support</li>
  </ul>
  <div class="price__foot"><a class="btn btn--primary btn--block" href="{base}contact.html" data-select-plan="Business">Choose Business {ico('arrow', sw=2)}</a></div>
 </div>
 <div class="card price reveal" data-d="2">
  <span class="price__name">Custom build</span>
  <div><span class="price__amount">Quoted<span>from €900</span></span></div>
  <p class="price__desc">A system designed from scratch for how your business actually runs.</p>
  <ul class="price__list">
   <li>{ico('check', sw=2.2)}Discovery call + written blueprint</li>
   <li>{ico('check', sw=2.2)}Unlimited sheets within agreed scope</li>
   <li>{ico('check', sw=2.2)}Formulas, Power Query or VBA as needed</li>
   <li>{ico('check', sw=2.2)}Data cleanup and migration included</li>
   <li>{ico('check', sw=2.2)}Multi-user layout for OneDrive/SharePoint</li>
   <li>{ico('check', sw=2.2)}60 days of post-handover support</li>
  </ul>
  <div class="price__foot"><a class="btn btn--ghost btn--block" href="{base}contact.html" data-select-plan="Custom">Request a quote {ico('arrow', sw=2)}</a></div>
 </div>
</div>"""


def faq_block(items, open_first=False):
    out = ['<div class="faq reveal">']
    for i, (q, a) in enumerate(items):
        out.append(f'<details class="faq__item"{" open" if (open_first and i == 0) else ""}>'
                   f'<summary class="faq__q">{q}<i></i></summary>'
                   f'<div class="faq__a">{a}</div></details>')
    out.append("</div>")
    return "".join(out)


# =========================================================== products.html
def build_catalog():
    cards = []
    for i, p in enumerate(PRODUCTS):
        cards.append(f"""<article class="card product-card reveal" data-category="{p['categories']}" data-d="{min(i,4)}">
 <a class="product-card__media" href="products/{p['slug']}.html" aria-label="Open {p['name']}">
  {f'<span class="tag product-card__badge">{p["badge"]}</span>' if p['badge'] else ''}
  {picture(p['image'], 'Original dashboard mockup of the ' + p['name'], '', w=1440, h=900)}
 </a>
 <div class="product-card__body">
  <div style="display:flex;align-items:center;gap:10px">
   <span class="icon icon--sm">{ico(p['icon'])}</span>
   <span class="eyebrow eyebrow--plain">{p['short']}</span>
  </div>
  <h3 class="product-card__title"><a href="products/{p['slug']}.html">{p['name']}</a></h3>
  <p class="product-card__desc">{p['tagline']}</p>
  <ul class="feature-list" style="margin-top:4px;gap:8px">
   {''.join(f'<li>{ico("check", sw=2.2)}<span style="font-size:12.8px">{d}</span></li>' for d in p['deliverables'][:3])}
  </ul>
  <div class="product-card__foot">
   <span class="product-card__price">{p['price']}<small>{p['price_note']}</small></span>
   <a class="product-card__link" href="products/{p['slug']}.html">View system {ico('arrow-up-right', sw=2)}</a>
  </div>
 </div>
</article>""")

    body = f"""<main id="main">
<section class="page-head">
 <div class="page-head__glow" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Systems</span></nav>
  <span class="eyebrow">The catalog</span>
  <h1 style="margin-top:18px">Five Excel systems, built to be used — not admired.</h1>
  <p class="page-head__lede">Each system is a complete, protected workbook with a dashboard, a clean data model and a short manual.
  Buy one, or combine them. Prices shown are starting points for the standard scope.</p>
  <div class="page-head__meta">
   <span class="tag">One-time purchase</span>
   <span class="tag tag--ghost">Delivered as .xlsx</span>
   <span class="tag tag--ghost">5–10 working days</span>
  </div>
 </div>
</section>

<section class="section" style="padding-top:clamp(24px,3vw,40px)">
 <div class="container">
  <div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;margin-bottom:24px">
   <div class="tabs" role="tablist" aria-label="Filter systems" data-filter-bar>
    <button role="tab" aria-selected="true" data-filter="all">All systems</button>
    <button role="tab" aria-selected="false" data-filter="retail">Retail</button>
    <button role="tab" aria-selected="false" data-filter="wholesale">Wholesale</button>
    <button role="tab" aria-selected="false" data-filter="reporting">Reporting</button>
   </div>
   <a class="link-arrow" href="demo.html">{ico('play', sw=2)} Try the logic in a live demo</a>
  </div>
  <div class="grid grid--2">{''.join(cards)}</div>
  <p hidden data-filter-empty class="muted" style="padding:30px 0">No systems in this category yet.</p>
 </div>
</section>

<section class="section section--tight">
 <div class="container">
  <div class="fact-strip reveal">
   <div class="fact-strip__cell"><div class="fact-strip__k">.xlsx</div><div class="fact-strip__v">Native Excel file — no add-ins required</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">One-time</div><div class="fact-strip__v">Purchase, not a subscription</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">Documented</div><div class="fact-strip__v">Manual + walkthrough on every build</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">Yours</div><div class="fact-strip__v">The file and its logic belong to you</div></div>
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head">
   <div class="kicker-row reveal"><span>Not sure which one</span><span class="rule"></span></div>
   <h2 style="margin-top:16px">A quick way to choose.</h2>
  </div>
  <div class="grid grid--3">
   <div class="card reveal"><span class="icon">{ico('box')}</span><h3 style="font-size:17px;margin:14px 0 8px">“I never know what to reorder.”</h3><p style="font-size:13.6px;color:var(--muted)">Start with the Inventory Command Center. It is the system that most often pays for itself in the first month.</p><a class="link-arrow" href="products/inventory.html" style="margin-top:14px">Inventory system {ico('arrow', sw=2)}</a></div>
   <div class="card reveal" data-d="1"><span class="icon">{ico('truck')}</span><h3 style="font-size:17px;margin:14px 0 8px">“Wholesale orders live in my inbox.”</h3><p style="font-size:13.6px;color:var(--muted)">The Wholesale Order Hub gives purchase orders, fill rates and receivables one honest home.</p><a class="link-arrow" href="products/wholesale.html" style="margin-top:14px">Wholesale system {ico('arrow', sw=2)}</a></div>
   <div class="card reveal" data-d="2"><span class="icon">{ico('chart')}</span><h3 style="font-size:17px;margin:14px 0 8px">“I rebuild the same report every month.”</h3><p style="font-size:13.6px;color:var(--muted)">The Executive Reporting Suite consolidates your files into one scorecard and a printable board pack.</p><a class="link-arrow" href="products/reporting.html" style="margin-top:14px">Reporting system {ico('arrow', sw=2)}</a></div>
  </div>
 </div>
</section>

{cta_band('', 'Need something the catalog does not cover?', 'Custom work is the other half of the studio: messy-data cleanups, multi-company consolidation, bespoke pricing logic, VBA tools and one-off automation jobs.',
          primary=(('contact.html', 'Describe your project'),), secondary=('services.html', 'See custom services'))}
</main>"""
    page("products.html", "Excel Systems Catalog — Inventory, Sales, Wholesale, Expenses, Reporting",
         "Five professional Excel automation systems for small businesses: inventory control, sales performance, wholesale purchase orders, expense budgets and executive reporting.",
         body, base="", active="products", canonical=SITE_URL + "/products.html")


# =========================================================== product pages
def build_product(p):
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    idx = PRODUCTS.index(p)
    prev_p = PRODUCTS[(idx - 1) % len(PRODUCTS)]
    next_p = PRODUCTS[(idx + 1) % len(PRODUCTS)]

    deliverables = "".join(f'<li>{ico("check", sw=2.2)}<span>{d}</span></li>' for d in p["deliverables"])
    inside = "".join(f'<div class="mini" style="flex-direction:column;gap:6px">'
                     f'<div style="display:flex;align-items:center;gap:9px"><span class="icon icon--sm">{ico("layers")}</span>'
                     f'<h4 style="margin:0;font-family:var(--font-d)">{name}</h4></div>'
                     f'<p>{desc}</p></div>' for name, desc in p["inside"])
    features = "".join(f'<div class="mini"><span class="icon icon--sm">{ico("sparkle")}</span>'
                       f'<div><h4>{t}</h4><p>{d}</p></div></div>' for t, d in p["features"])
    metrics = "".join(f'<div class="fact-strip__cell"><div class="fact-strip__k">{v}</div>'
                      f'<div class="fact-strip__v">{k} · {tag}</div></div>' for k, v, tag in p["metrics"])
    related = "".join(f"""<article class="card product-card reveal" data-d="{i}">
 <a class="product-card__media" href="{q['slug']}.html" aria-label="Open {q['name']}">
  {picture(q['image'], 'Original dashboard mockup of the ' + q['name'], '../', w=1440, h=900)}
 </a>
 <div class="product-card__body">
  <span class="eyebrow eyebrow--plain">{q['short']}</span>
  <h3 class="product-card__title"><a href="{q['slug']}.html">{q['name']}</a></h3>
  <p class="product-card__desc">{q['desc']}</p>
  <div class="product-card__foot">
   <span class="product-card__price">{q['price']}<small>{q['price_note']}</small></span>
   <a class="product-card__link" href="{q['slug']}.html">View system {ico('arrow-up-right', sw=2)}</a>
  </div>
 </div>
</article>""" for i, q in enumerate(others))

    body = f"""<main id="main">
<section class="page-head" style="padding-bottom:clamp(16px,2vw,26px)">
 <div class="page-head__glow" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../products.html">Systems</a><span>/</span><span>{p['short']}</span></nav>
  <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:16px">
   <span class="eyebrow">{p['short']}</span>
   {f'<span class="tag">{p["badge"]}</span>' if p['badge'] else ''}
  </div>
  <h1>{p['name']}</h1>
  <p class="page-head__lede">{p['tagline']}</p>
  <div class="page-head__meta">
   <span class="tag tag--ghost">Best for: {p['best']}</span>
   <span class="tag tag--ghost">Native .xlsx</span>
   <span class="tag tag--ghost">5–10 working days</span>
  </div>
 </div>
</section>

<section class="section" style="padding-top:clamp(10px,2vw,20px)">
 <div class="container">
  <div class="pp">
   <div>
    <div class="pp__shot reveal">
     <div class="hero__chrome"><i></i><i></i><i></i><span>{p['slug']} · dashboard mockup</span></div>
     {picture(p['image'], 'Original mockup of the ' + p['name'] + ' dashboard', '../', w=1440, h=900, priority=True)}
    </div>
    <p class="muted" style="font-size:12px;margin-top:10px">Original dashboard mockup drawn for this catalog. Figures shown are sample data, not customer results.</p>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>What you get</span><span class="rule"></span></div>
     <h2 style="font-size:clamp(24px,3vw,32px);margin:16px 0 10px">Everything in the box.</h2>
     <p class="muted" style="max-width:62ch;margin-bottom:22px">{p['desc']}</p>
     <ul class="feature-list" style="gap:14px">{deliverables}</ul>
    </div>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>Inside the workbook</span><span class="rule"></span></div>
     <h2 style="font-size:clamp(24px,3vw,32px);margin:16px 0 10px">A structure you can actually maintain.</h2>
     <div class="feature-grid" style="margin-top:22px">{inside}</div>
    </div>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>Why it holds up</span><span class="rule"></span></div>
     <h2 style="font-size:clamp(24px,3vw,32px);margin:16px 0 10px">Design decisions that matter at 6pm on a Friday.</h2>
     <div class="feature-grid" style="margin-top:22px">{features}</div>
    </div>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>Sample dashboard figures</span><span class="rule"></span></div>
     <div class="fact-strip reveal" style="margin-top:18px">{metrics}</div>
     <p class="muted" style="font-size:12px;margin-top:10px">Illustrative sample data used in the mockup above. Your system ships with your own data and no demo numbers.</p>
    </div>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>Demonstration</span><span class="rule"></span></div>
     <div class="card reveal" style="margin-top:18px;padding:clamp(22px,3vw,34px);
        background:radial-gradient(120% 130% at 100% 0%,rgba(52,224,161,.12),transparent 60%),var(--surface)">
      <div style="display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:space-between">
       <div style="max-width:52ch">
        <h3 style="font-size:19px">Try the calculation logic right now</h3>
        <p class="muted" style="font-size:13.6px;margin-top:8px">An interactive simulation of this system, running in your browser on sample data. Sell stock, approve expenses or advance a purchase order — the totals respond like the real workbook.</p>
       </div>
       <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn btn--primary" href="../demo.html#{p['demo']}">{ico('play', sw=2)} Open demo</a>
       </div>
      </div>
     </div>
    </div>

    <div style="margin-top:clamp(34px,4vw,50px)">
     <div class="kicker-row"><span>Questions</span><span class="rule"></span></div>
     <div style="margin-top:18px">{faq_block(p['faqs'])}</div>
    </div>
   </div>

   <aside class="pp__aside">
    <div class="panel">
     <span class="price__name" style="font-size:11px">Starting price</span>
     <div style="display:flex;align-items:baseline;gap:8px;margin:10px 0 4px">
      <span style="font-family:var(--font-d);font-size:38px;font-weight:600;letter-spacing:-.04em">{p['price']}</span>
      <span class="muted" style="font-size:12px">one-time</span>
     </div>
     <p class="muted" style="font-size:12.5px">Final price depends on scope. Standard build as listed above: {p['price']}. Customisation is quoted separately.</p>
     <div style="display:grid;gap:9px;margin-top:18px">
      <a class="btn btn--primary btn--block" href="../contact.html" data-select-plan="Business">Request this system {ico('arrow', sw=2)}</a>
      <a class="btn btn--ghost btn--block" href="../demo.html#{p['demo']}">{ico('play', sw=2)} Try the demo</a>
      <a class="btn btn--quiet btn--block" href="mailto:{EMAIL}?subject={p['name'].replace(' ', '%20')}%20enquiry">{ico('mail', sw=2)} Ask a question first</a>
     </div>
     <p class="muted" style="font-size:11.5px;margin-top:14px;text-align:center">Reply within one working day</p>
    </div>

    <div class="panel">
     <h3>At a glance</h3>
     <dl class="spec">
      <div class="spec__row"><dt>Format</dt><dd>Microsoft Excel (.xlsx)</dd></div>
      <div class="spec__row"><dt>Requires</dt><dd>Excel 2016+ / Microsoft 365</dd></div>
      <div class="spec__row"><dt>Macros</dt><dd>Optional</dd></div>
      <div class="spec__row"><dt>Best for</dt><dd>{p['best']}</dd></div>
      <div class="spec__row"><dt>Delivery</dt><dd>5–10 working days</dd></div>
      <div class="spec__row"><dt>Support</dt><dd>30 days included</dd></div>
      <div class="spec__row"><dt>Ownership</dt><dd>Yours, permanently</dd></div>
     </dl>
    </div>

    <div class="panel">
     <h3>Prefer a live walkthrough?</h3>
     <p>A 20-minute screen-share where I open the workbook, use your data shape, and answer questions before you decide.</p>
     <a class="btn btn--ghost btn--block" style="margin-top:14px" href="../contact.html">Book a walkthrough</a>
    </div>
   </aside>
  </div>
 </div>
</section>

<section class="section section--tight">
 <div class="container">
  <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;margin-bottom:22px">
   <h2 style="font-size:clamp(22px,2.6vw,30px)">Other systems</h2>
   <div style="display:flex;gap:10px">
    <a class="btn btn--ghost btn--sm" href="{prev_p['slug']}.html">← {prev_p['short']}</a>
    <a class="btn btn--ghost btn--sm" href="{next_p['slug']}.html">{next_p['short']} →</a>
   </div>
  </div>
  <div class="grid grid--3">{related}</div>
 </div>
</section>
</main>

<div class="sticky-cta">
 <a class="btn btn--primary" href="../contact.html" data-select-plan="Business">Request {p['price']}</a>
 <a class="btn btn--ghost" href="../demo.html#{p['demo']}">{ico('play', sw=2)} Demo</a>
</div>"""

    page(f"products/{p['slug']}.html",
         f"{p['name']} — Excel system for {p['best_title']} | Gridline Systems",
         p['tagline'] + ' ' + p['desc'],
         body, base="../", active="products", canonical=f"{SITE_URL}/products/{p['slug']}.html")


# =========================================================== demo.html
def build_demo():
    tabs = "".join(
        f'<a role="tab" class="demo-tab" href="#{q["demo"]}" data-demo-tab="{q["demo"]}">'
        f'{ico(q["icon"])}<span>{q["short"]}</span></a>' for q in PRODUCTS)

    body = f"""<main id="main">
<section class="page-head" style="padding-bottom:clamp(18px,2vw,28px)">
 <div class="page-head__glow" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Demonstrations</span></nav>
  <span class="eyebrow">Product demonstrations</span>
  <h1 style="margin-top:18px">The logic, running live in your browser.</h1>
  <p class="page-head__lede">These simulations reproduce how each system calculates — reorder flags, revenue totals, fill rates,
  budget usage and consolidation. They run entirely in this page on <strong>sample data</strong>, and they are honest about it:
  the demos show the logic, they are not the workbook itself.</p>
 </div>
</section>

<section class="section" style="padding-top:0">
 <div class="container">
  <div class="tabs demo-tabs" role="tablist" aria-label="Choose a demonstration">{tabs}</div>
  <div class="demo-shell">
   <div class="demo-shell__bar">
    <span class="demo-dot"></span><span class="demo-dot"></span><span class="demo-dot"></span>
    <span class="demo-shell__title" data-demo-title>Inventory System</span>
    <span class="demo-shell__flag">sample data · resets on reload</span>
   </div>
   <div id="demo-app" class="demo-app">
    <noscript><p style="padding:24px;color:#87968f">The demonstrations need JavaScript because they calculate live. The rest of the site works without it.</p></noscript>
   </div>
  </div>
  <div class="grid grid--3" style="margin-top:clamp(26px,3vw,40px)">
   <div class="card reveal"><span class="icon">{ico('shield')}</span><h3 style="font-size:16px;margin:14px 0 6px">What this is</h3><p style="font-size:13.4px;color:var(--muted)">A transparent simulation of the rules inside each workbook, so you can test the behaviour before buying.</p></div>
   <div class="card reveal" data-d="1"><span class="icon">{ico('file')}</span><h3 style="font-size:16px;margin:14px 0 6px">What this is not</h3><p style="font-size:13.4px;color:var(--muted)">A running copy of the product. The delivered system is an Excel file that you own and keep.</p></div>
   <div class="card reveal" data-d="2"><span class="icon">{ico('users')}</span><h3 style="font-size:16px;margin:14px 0 6px">Want the real thing?</h3><p style="font-size:13.4px;color:var(--muted)">Tell me which system you tried and what still feels missing — that is usually the start of a good brief.</p></div>
  </div>
 </div>
</section>

{cta_band('', 'Like how it behaves?', 'Pick the system closest to your problem and send a short brief. You will get a written scope, a fixed price and a delivery date — before any payment.',
          primary=(('contact.html', 'Send a brief'),), secondary=('pricing.html', 'See pricing'))}
</main>"""

    extra = """<script src="js/demo.js" defer></script>
<style>
.demo-tabs{display:flex;gap:6px;padding:6px;border-radius:14px;background:#0a100e;border:1px solid var(--line);overflow-x:auto}
.demo-tab{display:inline-flex;align-items:center;gap:9px;padding:11px 16px;border-radius:10px;font-size:13.5px;font-weight:600;color:var(--muted);white-space:nowrap;transition:.22s}
.demo-tab svg{width:16px;height:16px;color:currentColor}
.demo-tab:hover{color:var(--text);background:rgba(255,255,255,.04)}
.demo-tab.is-active{background:rgba(52,224,161,.13);color:var(--acc);box-shadow:inset 0 0 0 1px rgba(52,224,161,.28)}
.demo-shell{margin-top:18px;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:#080c0a;box-shadow:var(--shadow-2)}
.demo-shell__bar{display:flex;align-items:center;gap:7px;padding:12px 16px;background:#0a0f0d;border-bottom:1px solid var(--line-soft)}
.demo-dot{width:9px;height:9px;border-radius:50%;background:#22302a}
.demo-shell__title{margin-left:10px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:700}
.demo-shell__flag{margin-left:auto;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.demo-app{padding:clamp(16px,3vw,30px)}
.demo-head{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-start;justify-content:space-between;margin-bottom:20px}
.demo-head__kicker{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);font-weight:700}
.demo-head__title{font-size:clamp(20px,2.4vw,27px);margin-top:8px;letter-spacing:-.03em}
.demo-head__lede{color:var(--muted);font-size:13.6px;max-width:62ch;margin-top:8px}
.demo-kpis{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));margin-bottom:18px}
.demo-kpi{padding:15px 16px;border-radius:12px;background:linear-gradient(180deg,rgba(255,255,255,.03),transparent),#0e1513;border:1px solid var(--line)}
.demo-kpi__label{display:block;font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint);font-weight:700}
.demo-kpi__value{display:block;margin-top:8px;font-family:var(--font-d);font-size:22px;font-weight:600;letter-spacing:-.03em;transition:color .3s}
.demo-table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:#0b110f}
.demo-table{width:100%;border-collapse:collapse;font-size:13px;min-width:640px}
.demo-table th{text-align:left;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint);font-weight:700;padding:12px 14px;background:#0e1513;border-bottom:1px solid var(--line);white-space:nowrap}
.demo-table td{padding:12px 14px;border-bottom:1px solid #141d1a;color:var(--text-2);white-space:nowrap}
.demo-table tr:last-child td{border-bottom:0}
.demo-table td.is-key{color:var(--text);font-weight:600;font-family:var(--font-b)}
.demo-table td.is-num{font-variant-numeric:tabular-nums;color:var(--text)}
.demo-table td.is-action{text-align:right}
.demo-badge{display:inline-flex;align-items:center;padding:4px 10px;border-radius:100px;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.demo-badge--ok{background:rgba(52,224,161,.12);color:var(--acc)}
.demo-badge--warn{background:rgba(244,196,100,.13);color:var(--amber)}
.demo-badge--danger{background:rgba(242,114,111,.13);color:var(--danger)}
.demo-badge--info{background:rgba(106,168,246,.13);color:var(--blue)}
.demo-btn{display:inline-flex;align-items:center;justify-content:center;padding:6px 12px;margin-left:6px;border-radius:8px;font-size:11.5px;font-weight:600;
 background:rgba(52,224,161,.14);color:var(--acc);border:1px solid rgba(52,224,161,.26);transition:.2s}
.demo-btn:hover{background:rgba(52,224,161,.24)}
.demo-btn--ghost{background:rgba(255,255,255,.04);color:var(--muted);border-color:var(--line)}
.demo-btn--ghost:hover{background:rgba(255,255,255,.08);color:var(--text)}
.demo-toggle{position:relative;width:34px;height:19px;border-radius:100px;background:#1b2622;border:1px solid var(--line);margin-left:6px;transition:.25s;vertical-align:middle}
.demo-toggle span{position:absolute;top:2px;left:2px;width:13px;height:13px;border-radius:50%;background:#5f6d67;transition:.25s}
.demo-toggle.is-on{background:rgba(52,224,161,.24);border-color:rgba(52,224,161,.4)}
.demo-toggle.is-on span{left:16px;background:var(--acc)}
.demo-table td.is-action em{font-style:normal;font-size:11px;color:var(--faint);margin-left:8px}
.demo-extra{margin-top:18px;padding:18px;border:1px solid var(--line);border-radius:14px;background:#0b110f}
.demo-extra h3{font-size:14px;margin-bottom:14px}
.demo-bar-row{display:grid;grid-template-columns:110px 1fr 80px;gap:12px;align-items:center;font-size:12px;margin-bottom:9px}
.demo-bar-row span{color:var(--muted)}
.demo-bar-row b{text-align:right;color:var(--text);font-weight:600;font-variant-numeric:tabular-nums}
.demo-bar{height:7px;border-radius:4px;background:#16211d;overflow:hidden}
.demo-bar i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#12724f,#34e0a1);transition:width .5s var(--ease)}
.demo-foot{display:grid;gap:14px;margin-top:18px}
@media(min-width:760px){.demo-foot{grid-template-columns:1fr 1fr}}
.demo-schema,.demo-log{padding:18px;border:1px solid var(--line);border-radius:14px;background:#0b110f}
.demo-schema h3,.demo-log h3{font-size:13px;margin-bottom:12px;letter-spacing:.02em}
.demo-schema dl{margin:0;display:grid;gap:0}
.demo-schema dl > div{display:flex;justify-content:space-between;gap:14px;padding:7px 0;border-bottom:1px dashed var(--line-soft);font-size:12px}
.demo-schema dl > div:last-child{border-bottom:0}
.demo-schema dt{color:var(--faint)}
.demo-schema dd{margin:0;color:var(--text-2);text-align:right}
.demo-log ul{display:grid;gap:8px;font-size:12px;color:var(--muted)}
.demo-log li{padding-left:14px;position:relative}
.demo-log li::before{content:"";position:absolute;left:0;top:7px;width:5px;height:5px;border-radius:50%;background:#2b3b34}
.demo-log li.is-new{color:var(--acc)}
.demo-log li.is-new::before{background:var(--acc);box-shadow:0 0 0 3px rgba(52,224,161,.15)}
.demo-disclaimer{margin-top:16px;font-size:11.5px;color:var(--faint);line-height:1.6}
</style>"""

    page("demo.html", "Live Product Demonstrations — Excel Automation Logic | Gridline Systems",
         "Interactive demonstrations of the Gridline inventory, sales, wholesale, expense and reporting systems. Real calculation logic running on sample data in your browser.",
         body, base="", active="", extra_head=extra,
         canonical=SITE_URL + "/demo.html")


if __name__ == "__main__":
    build_catalog()
    for p in PRODUCTS:
        build_product(p)
    build_demo()
