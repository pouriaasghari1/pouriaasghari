#!/usr/bin/env python3
"""Services, pricing, about, faq, contact."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import *
from build_parts import cta_band, price_cards, faq_block


def page_head(crumbs, eyebrow, title, lede, tags=None):
    tg = "".join(f'<span class="tag tag--ghost">{t}</span>' for t in (tags or []))
    return f"""<section class="page-head">
 <div class="page-head__glow" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
  <span class="eyebrow">{eyebrow}</span>
  <h1 style="margin-top:18px">{title}</h1>
  <p class="page-head__lede">{lede}</p>
  {f'<div class="page-head__meta">{tg}</div>' if tg else ''}
 </div>
</section>"""


# =========================================================== services.html
def build_services():
    services = [
        ("wrench", "Custom Excel system", "When no catalog system fits, we design from zero: your workflow, your vocabulary, your exceptions. Written blueprint first, build second.", ["Discovery + process mapping", "Data model design", "Protected input forms", "Dashboard and reports"]),
        ("broom", "Spreadsheet rescue & clean-up", "Rescue a workbook that has grown out of control: duplicated sheets, broken formulas, mystery numbers, and one person who is the only one who understands it.", ["Structure audit report", "Formula rebuild", "Named ranges and tables", "Documented handover"]),
        ("database", "Data consolidation", "Pull five exports into one clean model with Power Query — stock, sales, orders, expenses and bank statements that finally agree with each other.", ["Power Query pipelines", "Refresh in one click", "Source mapping", "Validation checks"]),
        ("chart", "Automated reporting", "Monthly board pack, management summary, KPI scorecard — generated from the source data and printed ready, not rebuilt by hand each month.", ["Scorecard layout", "Print-ready PDF", "Month/quarter/year views", "Commentary sheet"]),
        ("bolt", "VBA & automation", "Where a macro genuinely earns its place: one-click imports, PDF exports, form-driven entry, batch invoice generation. Always with a fallback that works without macros.", ["Documented VBA", "Error handling", "No hidden state", "Security guidance"]),
        ("target", "Pricing & margin tools", "Quote builders, discount ladders, landed-cost calculators and margin simulators that stop pricing being guesswork.", ["Cost build-up sheets", "Discount governance", "Scenario comparison", "Approval limits"]),
    ]
    s_cards = "".join(f"""<article class="card reveal" data-d="{min(i,4)}">
 <div class="card__glow"></div>
 <span class="icon">{ico(icon)}</span>
 <h3 style="font-size:18px;margin:16px 0 8px">{title}</h3>
 <p style="font-size:13.8px;color:var(--muted)">{desc}</p>
 <ul class="feature-list" style="margin-top:16px;gap:8px">
  {''.join(f'<li>{ico("check", sw=2.2)}<span style="font-size:12.8px">{d}</span></li>' for d in items)}
 </ul>
</article>""" for i, (icon, title, desc, items) in enumerate(services))

    body = f"""<main id="main">
{page_head('<a href="index.html">Home</a><span>/</span><span>Custom work</span>', "Custom Excel development",
           "Your business, in one well-built workbook.",
           "Catalog systems cover the common problems. This page is about the other problems — the process nobody has written down, the file only one person understands, the report that eats a day every month.",
           ["Remote delivery", "Fixed-price quotes", "English &amp; Persian", "Fortune-500-adjacent standards without the invoice"])}

<section class="section" style="padding-top:clamp(24px,3vw,40px)">
 <div class="container">
  <div class="grid grid--3">{s_cards}</div>
 </div>
</section>

<section class="section" style="background:linear-gradient(180deg,transparent,rgba(52,224,161,.028),transparent)">
 <div class="container">
  <div class="grid grid--2" style="gap:clamp(28px,5vw,60px);align-items:start">
   <div>
    <div class="kicker-row reveal"><span>The build process</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(26px,3.6vw,40px);margin-top:16px">You always know what happens next.</h2>
    <p class="reveal" data-d="2" class="muted" style="color:var(--muted);margin-top:14px;max-width:56ch">No hourly mystery, no scope creep, no invoices that appear from nowhere. Every stage has a deliverable you approve before the next one begins.</p>
    <div class="process reveal" data-d="3" style="grid-template-columns:1fr;gap:0;margin-top:30px">
     <div class="step" style="padding:18px 0 18px 0"><span class="step__num">01 — DISCOVERY</span><h3 style="margin:8px 0 6px">We look at what you use now</h3><p>A 30–45 minute call plus your current file. I write down the workflow, the exceptions and the reporting you actually need — not the one a template assumes.</p></div>
     <div class="step" style="padding:18px 0"><span class="step__num">02 — BLUEPRINT</span><h3 style="margin:8px 0 6px">A written scope, a fixed price</h3><p>Sheets, tables, rules, deliverables and a date. You approve the blueprint in writing; anything outside it is a separate, clearly priced change.</p></div>
     <div class="step" style="padding:18px 0"><span class="step__num">03 — BUILD</span><h3 style="margin:8px 0 6px">Built, protected, tested</h3><p>You get progress previews. Testing uses your real data shapes — including the awkward cases: duplicate codes, refunds, half-empty rows.</p></div>
     <div class="step" style="padding:18px 0"><span class="step__num">04 — HANDOVER</span><h3 style="margin:8px 0 6px">Training and support</h3><p>A walkthrough call (recorded if you like), a written manual, a backup routine and a support window for fixes.</p></div>
    </div>
   </div>
   <div class="reveal" data-d="2">
    <div class="card" style="padding:0;overflow:hidden">
     <div class="hero__chrome"><i></i><i></i><i></i><span>reporting · board pack mockup</span></div>
     {picture('dash-reporting', 'Original mockup of an executive reporting dashboard with scorecard, health gauge and consolidated chart')}
    </div>
    <div class="panel" style="margin-top:16px">
     <h3>What I will not do</h3>
     <ul class="feature-list" style="gap:10px;margin-top:6px">
      <li>{ico('close', sw=2.2)}<span style="font-size:13px">Pretend a workbook is a certified accounting or e-invoicing system — it is neither.</span></li>
      <li>{ico('close', sw=2.2)}<span style="font-size:13px">Sell you a subscription for a file you can own.</span></li>
      <li>{ico('close', sw=2.2)}<span style="font-size:13px">Deliver something with no documentation, so you depend on me forever.</span></li>
      <li>{ico('close', sw=2.2)}<span style="font-size:13px">Promise integrations I have not verified against your actual tools.</span></li>
     </ul>
    </div>
   </div>
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="section-head section-head--row">
   <div>
    <div class="kicker-row reveal"><span>Good fits</span><span class="rule"></span></div>
    <h2 style="margin-top:16px">Projects this studio does well.</h2>
   </div>
   <p class="reveal" data-d="2">If your project looks like one of these, the conversation will be short and useful.</p>
  </div>
  <div class="grid grid--2">
   <div class="card reveal"><h3 style="font-size:16px">A retailer with stock spread over two locations</h3><p style="font-size:13.6px;color:var(--muted);margin-top:8px">Needs: one stock truth, reorder suggestions, monthly valuation for the accountant.</p></div>
   <div class="card reveal" data-d="1"><h3 style="font-size:16px">A wholesaler drowning in purchase orders</h3><p style="font-size:13.6px;color:var(--muted);margin-top:8px">Needs: PO pipeline, fill-rate tracking, receivables ageing, delivery planner.</p></div>
   <div class="card reveal" data-d="2"><h3 style="font-size:16px">A small business with messy monthly reporting</h3><p style="font-size:13.6px;color:var(--muted);margin-top:8px">Needs: consolidation of sales/expenses/stock into one page a bank will accept.</p></div>
   <div class="card reveal" data-d="3"><h3 style="font-size:16px">An owner who is the only Excel person</h3><p style="font-size:13.6px;color:var(--muted);margin-top:8px">Needs: documentation, protection and a file a colleague can open without fear.</p></div>
  </div>
 </div>
</section>

{cta_band('', 'Send the messy file. I have seen worse.', 'A short description plus a sample export is enough to start. If Excel is the wrong tool for your problem, I will say so in the first reply.',
          primary=(('contact.html', 'Brief me on the project'),), secondary=('pricing.html', 'Pricing and packages'))}
</main>"""
    page("services.html", "Custom Excel Development Services | Pouria Business",
         "Custom Excel development: bespoke business workbooks, spreadsheet rescue, Power Query data consolidation, automated reporting, VBA automation and pricing tools.",
         body, base="", active="services", canonical=SITE_URL + "/services.html")


# =========================================================== pricing.html
def build_pricing():
    compare = [
        ("Catalog system included", "Expenses", "Any one", "Custom design"),
        ("Source sheets consolidated", "Up to 3", "Up to 8", "As scoped"),
        ("Dashboard with KPI cards", "Basic", "Full", "Full + custom"),
        ("Power Query automation", "—", "Yes", "Yes"),
        ("VBA macros", "—", "Where needed", "Where needed"),
        ("Input validation &amp; protection", "Yes", "Yes", "Yes"),
        ("Written manual", "Yes", "Yes", "Yes"),
        ("Recorded walkthrough", "—", "Yes", "Yes"),
        ("Support after handover", "14 days", "30 days", "60 days"),
        ("Delivery time", "5–7 days", "5–10 days", "2–4 weeks"),
        ("Price", "€290", "€590", "from €900"),
    ]
    rows = "".join(f"""<tr>
 <td>{a}</td><td>{b}</td><td class="is-feature">{c}</td><td>{d}</td></tr>""" for a, b, c, d in compare)

    body = f"""<main id="main">
{page_head('<a href="index.html">Home</a><span>/</span><span>Pricing</span>', "Pricing",
           "Clear prices. Written scope. No monthly fee.",
           "Every system is a one-time build. You pay half to start and half on handover. There is no subscription, no per-user fee, and no charge for keeping the file you paid for.",
           ["EUR · excl. VAT", "50% / 50% payment", "Fixed-price quotes"])}

<section class="section" style="padding-top:clamp(20px,3vw,34px)">
 <div class="container">
  {price_cards('')}
  <p class="price__note" style="margin-top:20px">Prices are starting points for the standard scope described. Extra sites, additional companies, unusual data cleanup or ongoing support are quoted separately and always in writing first.</p>
 </div>
</section>

<section class="section" style="background:linear-gradient(180deg,transparent,rgba(52,224,161,.028),transparent)">
 <div class="container">
  <div class="section-head">
   <div class="kicker-row reveal"><span>Compare</span><span class="rule"></span></div>
   <h2 style="margin-top:16px">What is actually different.</h2>
  </div>
  <div class="card reveal" style="padding:0;overflow:hidden">
   <div style="overflow-x:auto">
    <table class="compare">
     <thead><tr><th scope="col">Included</th><th scope="col">Starter · €290</th><th scope="col" class="is-feature">Business · €590</th><th scope="col">Custom · from €900</th></tr></thead>
     <tbody>{rows}</tbody>
    </table>
   </div>
  </div>
 </div>
</section>

<section class="section">
 <div class="container">
  <div class="grid grid--2" style="gap:clamp(28px,5vw,60px);align-items:start">
   <div>
    <div class="kicker-row reveal"><span>Add-ons</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(26px,3.4vw,38px);margin-top:16px">Optional extras.</h2>
    <p class="reveal" data-d="2" style="color:var(--muted);margin-top:14px;max-width:52ch">Only when they are genuinely useful. Nothing is bundled to inflate the invoice.</p>
    <div class="grid" style="gap:12px;margin-top:24px">
     <div class="mini"><span class="icon icon--sm">{ico('refresh')}</span><div><h4>Second system integration <span class="acc">+€150</span></h4><p>Link two catalog systems so sales update stock automatically.</p></div></div>
     <div class="mini"><span class="icon icon--sm">{ico('users')}</span><div><h4>Multi-user layout <span class="acc">+€120</span></h4><p>Split entry and reporting for OneDrive/SharePoint co-authoring.</p></div></div>
     <div class="mini"><span class="icon icon--sm">{ico('database')}</span><div><h4>Data migration <span class="acc">from €90</span></h4><p>Clean and import existing history, with a reconciliation sheet.</p></div></div>
     <div class="mini"><span class="icon icon--sm">{ico('clock')}</span><div><h4>Extended support <span class="acc">€60 / month</span></h4><p>Optional, cancellable any time. Fixes, small changes and a quarterly review.</p></div></div>
    </div>
   </div>
   <div>
    <div class="kicker-row reveal"><span>Logistics</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(26px,3.4vw,38px);margin-top:16px">How payment works.</h2>
    <div style="margin-top:22px">
     {faq_block([
        ("When do I pay?", "50% when you approve the written blueprint, 50% on handover. Custom builds over €1,500 can be split into three payments."),
        ("What payment methods?", "Bank transfer (SEPA) or a payment link. An invoice is issued for every payment."),
        ("What if I need changes later?", "Small adjustments are quoted as separate mini-jobs. Extended support (€60/month) covers fixes and small changes without a new quote each time."),
        ("Is there a refund policy?", "If the delivered workbook does not match the approved blueprint, I fix it. Beyond that, custom work is not refundable once the build starts — which is why the blueprint step exists."),
        ("Do you work with businesses outside the EU?", "Yes. Prices stay in EUR; payment links handle most currencies."),
     ], open_first=True)}
    </div>
   </div>
  </div>
 </div>
</section>

{cta_band('', 'Not sure which package you need?', 'Send a two-line description of the problem. I will tell you which package fits — and if the cheapest one genuinely works, that is the one I will quote.',
          primary=(('contact.html', 'Ask for a recommendation'),), secondary=('services.html', 'See custom services'))}
</main>

<style>
.compare{{width:100%;border-collapse:collapse;font-size:13.5px;min-width:720px}}
.compare th,.compare td{{padding:13px 18px;text-align:left;border-bottom:1px solid var(--line-soft)}}
.compare thead th{{background:#0e1513;font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--faint);font-weight:700;position:sticky;top:0}}
.compare tbody td:first-child{{color:var(--text-2)}}
.compare tbody td{{color:var(--muted)}}
.compare tbody tr:last-child td{{border-bottom:0;color:var(--text);font-weight:600}}
.compare .is-feature{{background:rgba(52,224,161,.05);color:var(--text)!important}}
.compare thead .is-feature{{color:var(--acc)!important}}
</style>"""
    page("pricing.html", "Pricing — Excel Automation Systems from €290 | Pouria Business",
         "Transparent one-time pricing for professional Excel automation systems: Starter €290, Business €590, custom builds from €900. No subscriptions.",
         body, base="", active="pricing", canonical=SITE_URL + "/pricing.html")


# =========================================================== about.html
def build_about():
    body = f"""<main id="main">
{page_head('<a href="index.html">Home</a><span>/</span><span>About</span>', "About the studio",
           "I build the spreadsheet your business should have had from the start.",
           "Pouria Business is a one-person Excel automation studio focused on small businesses, retailers and wholesalers who are tired of guessing their own numbers.",
           [])}

<section class="section" style="padding-top:clamp(16px,2vw,26px)">
 <div class="container">
  <div class="grid grid--2" style="gap:clamp(30px,5vw,64px);align-items:start">
   <div class="reveal">
    <div style="border-radius:26px;padding:10px;background:linear-gradient(160deg,rgba(52,224,161,.22),transparent 55%),var(--surface);border:1px solid var(--line)">
     <img src="pouria.jpg" alt="Portrait of the founder of Pouria Business" width="620" height="620" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:18px;filter:saturate(.92) contrast(1.03)">
    </div>
    <div class="panel" style="margin-top:16px">
     <h3>Pouria Business</h3>
     <p style="margin-top:6px">An Excel automation studio for small businesses, retailers and wholesalers — working remotely with clients worldwide.</p>
     <dl class="spec" style="margin-top:16px">
      <div class="spec__row"><dt>Business</dt><dd>Pouria Business</dd></div>
      <div class="spec__row"><dt>Focus</dt><dd>Excel automation for small business</dd></div>
      <div class="spec__row"><dt>Tools</dt><dd>Excel, Power Query, VBA, Python</dd></div>
      <div class="spec__row"><dt>Languages</dt><dd>English, Persian</dd></div>
      <div class="spec__row"><dt>Email</dt><dd><a href="mailto:{EMAIL}" style="color:var(--acc)">{EMAIL}</a></dd></div>
      <div class="spec__row"><dt>Instagram</dt><dd><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" style="color:var(--acc)">{INSTAGRAM_HANDLE}</a></dd></div>
     </dl>
     <div style="display:flex;gap:9px;margin-top:16px;flex-wrap:wrap">
      <a class="btn btn--primary btn--sm" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{ico('instagram', sw=1.9)} Follow on Instagram</a>
      <a class="btn btn--ghost btn--sm" href="mailto:{EMAIL}">{ico('mail', sw=1.9)} Email</a>
     </div>
    </div>
   </div>
   <div>
    <div class="kicker-row reveal"><span>Why this exists</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(26px,3.6vw,40px);margin-top:16px">Small businesses do not need another platform. They need one file that works.</h2>
    <div class="reveal" data-d="2" style="color:var(--muted);margin-top:16px;display:grid;gap:14px;max-width:60ch">
     <p><strong>Pouria Business</strong> is a one-person studio: you deal with the person who builds the file, not a department. Most of the businesses I talk to already own the right tool. Excel is installed, the staff know it, and the data is already there. What is missing is structure: a data model that holds up, formulas that cannot quietly break, and reporting that builds itself.</p>
     <p>So that is what I build. Not a template downloaded from somewhere — a system designed around the way your business actually operates, including the exceptions nobody documents.</p>
     <p>My background is software: Python, logic, interactive tools. That background is why the workbooks I ship avoid the usual Excel traps — copy-pasted formulas, hard-coded months, five versions of the same sheet, and numbers nobody can trace back to a source.</p>
    </div>

    <div style="margin-top:clamp(28px,4vw,44px)">
     <div class="kicker-row reveal"><span>Principles</span><span class="rule"></span></div>
     <div class="grid grid--2" style="margin-top:18px">
      <div class="card reveal"><span class="icon icon--sm">{ico('target')}</span><h3 style="font-size:15.5px;margin:12px 0 6px">One source of truth</h3><p style="font-size:13.2px;color:var(--muted)">Every number on a dashboard traces back to one row in one table. No typed summaries, no parallel totals.</p></div>
      <div class="card reveal" data-d="1"><span class="icon icon--sm">{ico('shield')}</span><h3 style="font-size:15.5px;margin:12px 0 6px">Make it hard to break</h3><p style="font-size:13.2px;color:var(--muted)">Validated inputs, protected formulas and conditional formatting that shows a mistake before it becomes one.</p></div>
      <div class="card reveal" data-d="2"><span class="icon icon--sm">{ico('file')}</span><h3 style="font-size:15.5px;margin:12px 0 6px">Document everything</h3><p style="font-size:13.2px;color:var(--muted)">A short manual and a readable structure, so the file survives staff changes — not just my memory of it.</p></div>
      <div class="card reveal" data-d="3"><span class="icon icon--sm">{ico('code')}</span><h3 style="font-size:15.5px;margin:12px 0 6px">Honest about limits</h3><p style="font-size:13.2px;color:var(--muted)">If Excel is the wrong tool, you will hear it in the first call. A workbook is not an ERP, and I will not pretend it is.</p></div>
     </div>
    </div>

    <div style="margin-top:clamp(28px,4vw,44px)">
     <div class="kicker-row reveal"><span>Working with me</span><span class="rule"></span></div>
     <h3 style="font-size:clamp(20px,2.4vw,26px);margin-top:14px">Direct, not departmental.</h3>
     <p class="reveal" data-d="2" style="color:var(--muted);margin-top:10px;max-width:60ch">You message one person. You get one voice, one blueprint, one invoice. That is the whole advantage of a studio this small: nothing gets lost in a handover, and nobody builds a feature you did not ask for.</p>
     <div class="grid grid--3" style="margin-top:20px">
      <div class="mini"><span class="icon icon--sm">{ico('clock')}</span><div><h4>Response</h4><p>Within one working day.</p></div></div>
      <div class="mini"><span class="icon icon--sm">{ico('globe')}</span><div><h4>Remote</h4><p>Files by email or OneDrive.</p></div></div>
      <div class="mini"><span class="icon icon--sm">{ico('lock')}</span><div><h4>Confidential</h4><p>Your data is deleted after the job unless you ask otherwise.</p></div></div>
     </div>
    </div>
   </div>
  </div>
 </div>
</section>

<section class="section section--tight">
 <div class="container">
  <div class="fact-strip reveal">
   <div class="fact-strip__cell"><div class="fact-strip__k">5</div><div class="fact-strip__v">Ready catalog systems</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">.xlsx</div><div class="fact-strip__v">Everything ships as a native workbook</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">0</div><div class="fact-strip__v">Subscriptions required</div></div>
   <div class="fact-strip__cell"><div class="fact-strip__k">1</div><div class="fact-strip__v">Person you speak to, start to finish</div></div>
  </div>
  <p class="muted" style="font-size:12px;margin-top:12px">No invented testimonials, no customer counts, no performance claims on this site — only what the studio offers and how it works.</p>
 </div>
</section>

{cta_band('', 'Tell me about the spreadsheet you dread opening.', 'A short message is enough to start. You will get a straight answer about what is possible, what it costs, and how long it takes.',
          primary=(('contact.html', 'Contact the studio'),), secondary=('portfolio.html', 'Personal portfolio'))}
</main>"""
    about_ld = site_identity() + jsonld({
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "About Pouria Business",
        "url": SITE_URL + "/about.html",
        "description": "Pouria Business is a one-person Excel automation studio founded by Pouria Asghari.",
        "mainEntity": {"@id": SITE_URL + "/#person"},
        "isPartOf": {"@id": SITE_URL + "/#website"},
    })

    page("about.html", "About — Excel Automation Studio | Pouria Business",
         "Pouria Business is a one-person Excel automation studio building professional Excel systems for small businesses, retailers and wholesalers.",
         body, base="", active="about", canonical=SITE_URL + "/about.html", structured=about_ld)


# =========================================================== faq.html
def build_faq():
    groups = [
        ("The basics", [
            ("Is this a real Excel file or an online app?", "A real <strong>.xlsx</strong> workbook that opens in Microsoft Excel (2016 or later, or Microsoft 365). The website demos are simulations of the logic; the product itself is a file you download, keep and own."),
            ("Do I need a Microsoft 365 subscription?", "A desktop Excel install is required. Most systems use formulas and Power Query only, both included in Excel 2016+ and Microsoft 365. If your build needs Power Query and you are on a very old version, I will tell you before you pay."),
            ("Does it work on Mac?", "Yes for the formula-driven systems. Power Query works on modern Excel for Mac; VBA behaves slightly differently, so Mac-specific builds are tested on Mac."),
            ("Will it work in Google Sheets or LibreOffice?", "Some systems import into LibreOffice Calc with reduced functionality. Google Sheets is not supported because Power Query and structured tables do not exist there."),
        ]),
        ("Buying and delivery", [
            ("How long does delivery take?", "Catalog systems: 5–10 working days from approved scope. Custom builds: usually 2–4 weeks depending on data cleanup and the number of users."),
            ("What do I receive?", "The workbook (with sample data replaced by yours where relevant), a written manual, a walkthrough call or recording, and a backup routine. Custom builds also include the blueprint document."),
            ("Can I buy more than one system?", "Yes. Buying two or more catalog systems together is discounted — ask for a combined quote. Systems can also be linked so that sales update inventory automatically."),
            ("How is the file transferred?", "Email, or a shared OneDrive/Google Drive folder if the file is large. You get the final file, not a link that expires."),
        ]),
        ("Data and privacy", [
            ("What happens to my business data?", "It is used only to build and test your system on my machine, then deleted once the project is closed — unless you ask me to keep the working copy for support."),
            ("Can you sign a confidentiality agreement?", "Yes. Send yours, or ask for a short mutual NDA before sharing files."),
            ("Is the workbook secure?", "Sheets are protected and inputs validated to prevent accidental damage. That is protection against mistakes, not against a determined person — no Excel file is encrypted unless you set a password, which I recommend."),
        ]),
        ("After handover", [
            ("What if a formula breaks later?", "Every build includes a support window (14–60 days depending on the package). After that, small fixes are quoted as mini-jobs, or covered by optional support at €60/month."),
            ("Can I edit it myself?", "Yes — it is your file. The structure is documented so you can add products, categories or users without breaking anything. Larger structural changes are best done together."),
            ("Do you keep working with the business after delivery?", "Only if you want to. Many clients come back for a second system six months later; nothing requires it."),
            ("What if I outgrow Excel?", "Then you will need a different tool, and that is a good sign. I will happily tell you when a workbook stops being the right answer — the file stays yours either way."),
        ]),
    ]
    blocks = []
    for gi, (title, items) in enumerate(groups):
        blocks.append(f"""<div class="faq-group">
 <h2 class="faq-group__title reveal">{title}</h2>
 {faq_block(items, open_first=(gi == 0))}
</div>""")

    body = f"""<main id="main">
{page_head('<a href="index.html">Home</a><span>/</span><span>FAQ</span>', "Questions",
           "Everything people ask before trusting Excel with the numbers.",
           "Honest answers about formats, versions, delivery, data handling and what happens after handover. If something is missing, ask — the reply comes from me, not a support queue.",
           [])}

<section class="section" style="padding-top:clamp(18px,2.5vw,30px)">
 <div class="container">
  <div class="faq-layout">
   {''.join(blocks)}
  </div>
  <div class="card reveal" style="margin-top:clamp(30px,4vw,50px);padding:clamp(24px,3vw,36px);display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:space-between">
   <div>
    <h3 style="font-size:19px">Still unanswered?</h3>
    <p class="muted" style="font-size:13.6px;margin-top:6px">Write two lines about your situation and get a real answer within one working day.</p>
   </div>
   <div style="display:flex;gap:10px;flex-wrap:wrap">
    <a class="btn btn--primary" href="contact.html">Ask a question {ico('arrow', sw=2)}</a>
    <a class="btn btn--ghost" href="mailto:{EMAIL}">{ico('mail', sw=2)} Email directly</a>
   </div>
  </div>
 </div>
</section>
</main>

<style>
.faq-layout{{display:grid;gap:clamp(26px,4vw,44px);max-width:900px}}
.faq-group__title{{font-size:13px;font-family:var(--font-b);font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:16px}}
</style>"""
    faq_items = []
    for _title, _items in groups:
        for _q, _a in _items:
            import re as _re
            faq_items.append({
                "@type": "Question",
                "name": _q,
                "acceptedAnswer": {"@type": "Answer", "text": _re.sub(r"<[^>]+>", "", _a)},
            })
    faq_ld = site_identity() + jsonld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items,
    }) + jsonld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "FAQ", "item": SITE_URL + "/faq.html"},
        ],
    })

    page("faq.html", "FAQ — Excel Automation Systems | Pouria Business",
         "Frequently asked questions about Pouria Business Excel automation: file format, Excel versions, delivery times, data privacy and post-handover support.",
         body, base="", active="", canonical=SITE_URL + "/faq.html", structured=faq_ld)


# =========================================================== contact.html
def build_contact():
    # Telegram is only rendered once the real handle/link exists.
    telegram_line = (f'<a class="contact-line" href="{TELEGRAM}" target="_blank" rel="noopener noreferrer">'
                     f'<span class="icon icon--sm">{ico("send")}</span>'
                     f'<span><strong>Telegram</strong><small>Direct message</small></span></a>') if TELEGRAM else ""
    form = f"""<form class="form" data-mailto="{EMAIL}" data-subject="Project enquiry — Pouria Business website"
   data-intro="Hello Pouria,&#10;&#10;I would like to discuss an Excel automation project.&#10;&#10;">
 <div class="field--row">
  <div class="field"><label for="name">Your name</label><input id="name" name="Name" type="text" autocomplete="name" required placeholder="Jane Doe"></div>
  <div class="field"><label for="email">Email</label><input id="email" name="Email" type="email" autocomplete="email" required placeholder="you@company.com"></div>
 </div>
 <div class="field--row">
  <div class="field"><label for="company">Business / shop name <span class="muted" style="text-transform:none;letter-spacing:0">(optional)</span></label><input id="company" name="Business" type="text" autocomplete="organization" placeholder="Northline Retail"></div>
  <div class="field">
   <label for="project-type">What do you need?</label>
   <select id="project-type" name="Project type" required>
    <option value="">Choose one…</option>
    <option value="Starter system (€290)">Starter system — €290</option>
    <option value="Business system (€590)">Business system — €590</option>
    <option value="Custom build (from €900)">Custom build — from €900</option>
    <option value="Inventory system">Inventory system</option>
    <option value="Sales system">Sales system</option>
    <option value="Wholesale system">Wholesale system</option>
    <option value="Expense system">Expense system</option>
    <option value="Reporting system">Reporting system</option>
    <option value="Spreadsheet rescue / cleanup">Spreadsheet rescue / cleanup</option>
    <option value="Not sure yet">Not sure yet — advise me</option>
   </select>
  </div>
 </div>
 <div class="field--row">
  <div class="field">
   <label for="size">Business size</label>
   <select id="size" name="Business size">
    <option value="">Prefer not to say</option>
    <option value="Just me">Just me</option>
    <option value="2–5 people">2–5 people</option>
    <option value="6–20 people">6–20 people</option>
    <option value="21–50 people">21–50 people</option>
    <option value="More than 50">More than 50</option>
   </select>
  </div>
  <div class="field">
   <label for="timeline">When do you need it?</label>
   <select id="timeline" name="Timeline">
    <option value="Flexible">Flexible</option>
    <option value="Within 2 weeks">Within 2 weeks</option>
    <option value="This month">This month</option>
    <option value="This quarter">This quarter</option>
    <option value="Just exploring">Just exploring</option>
   </select>
  </div>
 </div>
 <div class="field">
  <label for="message">What should the system do?</label>
  <textarea id="message" name="Project details" required placeholder="Example: I run a small shop and a wholesale side. Every Monday I count stock by hand and still get reorder quantities wrong. I need one file that tells me what to buy and shows me the week's sales."></textarea>
 </div>
 <div class="form__status" role="status" aria-live="polite"></div>
 <div>
  <button class="btn btn--primary btn--block" type="submit">Open pre-filled email {ico('send', sw=2)}</button>
 </div>
 <p class="form__note">This site is static and hosted on GitHub Pages, so the form does not upload anything to a server. Pressing the button composes an email in your own mail app with these details filled in — you can edit it before sending. Prefer to write directly? Use <a href="mailto:{EMAIL}" style="color:var(--acc)">{EMAIL}</a>.</p>
</form>"""

    body = f"""<main id="main">
{page_head('<a href="index.html">Home</a><span>/</span><span>Contact</span>', "Contact",
           "Let's look at your spreadsheet.",
           "Tell me what the file should be doing and what it is doing instead. I answer personally, within one working day, and I will tell you if Excel is the wrong tool for the job.",
           ["English &amp; Persian", "Remote · worldwide", "Reply within 1 working day"])}

<section class="section" style="padding-top:clamp(18px,2.5vw,30px)">
 <div class="container">
  <div class="contact-grid">
   <div class="card reveal" style="padding:clamp(22px,3vw,34px)">
    {form}
   </div>
   <div class="contact-side">
    <div class="panel reveal" data-d="1">
     <h3>Direct channels</h3>
     <div style="display:grid;gap:10px;margin-top:14px">
      <a class="contact-line" href="mailto:{EMAIL}"><span class="icon icon--sm">{ico('mail')}</span><span><strong>Email</strong><small>{EMAIL}</small></span></a>
      <a class="contact-line" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><span class="icon icon--sm">{ico('instagram')}</span><span><strong>Instagram</strong><small>{INSTAGRAM_HANDLE} · direct messages</small></span></a>
      {telegram_line}
      <button class="contact-line" type="button" data-copy="{EMAIL}"><span class="icon icon--sm">{ico('file')}</span><span><strong>Copy email address</strong><small>Click to copy</small></span></button>
     </div>
    </div>

    <div class="panel reveal" data-d="2">
     <h3>What to include</h3>
     <ul class="feature-list" style="gap:10px;margin-top:8px">
      <li>{ico('check', sw=2.2)}<span style="font-size:13px">What you sell, roughly how many products.</span></li>
      <li>{ico('check', sw=2.2)}<span style="font-size:13px">How many people will use the file.</span></li>
      <li>{ico('check', sw=2.2)}<span style="font-size:13px">The report or decision you struggle with today.</span></li>
      <li>{ico('check', sw=2.2)}<span style="font-size:13px">A sample export (no sensitive names needed).</span></li>
     </ul>
     <p class="muted" style="font-size:12px;margin-top:14px">A messy file is fine. Cleaning it is part of the job.</p>
    </div>

    <div class="panel reveal" data-d="3">
     <h3>What happens next</h3>
     <div class="steps-mini">
      <div><span>1</span><p>I read your message and reply with questions or a first read.</p></div>
      <div><span>2</span><p>A short call to confirm scope, then a written blueprint.</p></div>
      <div><span>3</span><p>You approve; I build; you get the file and the manual.</p></div>
     </div>
    </div>

    <div class="panel reveal" data-d="4" style="background:radial-gradient(120% 130% at 0% 0%,rgba(52,224,161,.1),transparent 60%),var(--surface)">
     <h3>Booking a call</h3>
     <p>Calls are arranged by email or Instagram DM — no calendar widget, no booking platform. Send your time zone and two windows that suit you.</p>
     <a class="btn btn--ghost btn--block" style="margin-top:14px" href="mailto:{EMAIL}?subject=Walkthrough%20call%20request">Request a call slot</a>
    </div>
   </div>
  </div>
 </div>
</section>
</main>

"""

    contact_css = """<style>.contact-grid{display:grid;gap:18px}
@media(min-width:980px){.contact-grid{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);align-items:start}}
.contact-side{display:grid;gap:14px}
.contact-line{display:flex;align-items:center;gap:12px;padding:12px;border-radius:12px;border:1px solid var(--line);background:#0b110f;text-align:left;transition:.22s;width:100%}
.contact-line:hover{border-color:rgba(52,224,161,.32);background:rgba(52,224,161,.05)}
.contact-line strong{display:block;font-size:13.2px;font-weight:600;color:var(--text)}
.contact-line small{display:block;font-size:11.5px;color:var(--faint);margin-top:2px;word-break:break-word}
.steps-mini{display:grid;gap:12px;margin-top:14px}
.steps-mini > div{display:flex;gap:12px;align-items:flex-start}
.steps-mini span{flex:none;width:22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:11px;font-weight:700;
 background:rgba(52,224,161,.13);color:var(--acc);border:1px solid rgba(52,224,161,.28)}
.steps-mini p{font-size:13px;color:var(--muted);line-height:1.55}
</style>"""

    contact_ld = site_identity() + jsonld({
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": "Contact Pouria Business",
        "url": SITE_URL + "/contact.html",
        "description": "Contact Pouria Business about a custom Excel automation project.",
        "isPartOf": {"@id": SITE_URL + "/#website"},
        "about": {"@id": SITE_URL + "/#organization"},
        "mainEntity": {
            "@type": "Organization",
            "@id": SITE_URL + "/#organization",
            "name": BRAND,
            "email": EMAIL,
            "url": SITE_URL + "/",
            "contactPoint": [{
                "@type": "ContactPoint",
                "contactType": "sales",
                "email": EMAIL,
                "availableLanguage": ["English", "Persian"],
                "url": SITE_URL + "/contact.html",
            }],
            "sameAs": [INSTAGRAM, GITHUB],
        },
    })

    page("contact.html", "Contact — Start an Excel Automation Project | Pouria Business",
         "Contact Pouria Business to discuss a custom Excel automation project. Personal reply within one working day, in English or Persian.",
         body, base="", active="contact", extra_head=contact_css, canonical=SITE_URL + "/contact.html",
         structured=contact_ld)


if __name__ == "__main__":
    build_services()
    build_pricing()
    build_about()
    build_faq()
    build_contact()
