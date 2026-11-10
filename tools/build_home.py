#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import *

# ---------------------------------------------------------------- home
def product_cards(base="", feature_first=True):
    out = []
    for i, p in enumerate(PRODUCTS):
        feature = " product-card--feature" if (feature_first and i == 0) else ""
        badge = f'<span class="tag product-card__badge">{p["badge"]}</span>' if p["badge"] else ""
        out.append(f"""<article class="card product-card reveal{feature}" data-category="{p['categories']}" data-d="{min(i,4)}">
 <a href="{base}products/{p['slug']}.html" class="product-card__media" aria-label="Open {p['name']}">
  {badge}
  {picture(p['image'], 'Original dashboard mockup of the ' + p['name'], base, w=1440, h=900)}
 </a>
 <div class="product-card__body">
  <div style="display:flex;align-items:center;gap:10px">
   <span class="icon icon--sm">{ico(p['icon'])}</span>
   <span class="eyebrow eyebrow--plain">{p['short']}</span>
  </div>
  <h3 class="product-card__title"><a href="{base}products/{p['slug']}.html">{p['name']}</a></h3>
  <p class="product-card__desc">{p['desc']}</p>
  <div class="product-card__foot">
   <span class="product-card__price">{p['price']}<small>{p['price_note']}</small></span>
   <a class="product-card__link" href="{base}products/{p['slug']}.html">View system {ico('arrow-up-right', sw=2)}</a>
  </div>
 </div>
</article>""")
    return "".join(out)


hero = f"""<main id="main">
<section class="hero">
 <div class="hero__bg" aria-hidden="true">
  <div class="hero__grid"></div>
  <div class="hero__glow"></div>
  <div class="hero__glow hero__glow--2"></div>
  <div class="hero__noise"></div>
 </div>
 <div class="container hero__inner">
  <div class="hero__copy">
   <span class="eyebrow reveal">Excel automation studio · open for projects</span>
   <h1 class="reveal" data-d="1">
    <span class="line">Excel systems that</span>
    <span class="line grad">run your business</span>
    <span class="line">while you sleep.</span>
   </h1>
   <p class="hero__lede reveal" data-d="2">
    <strong>Pouria Business</strong> designs and builds <strong>professional Excel automation systems</strong>
    for small businesses, retailers and wholesalers — inventory, sales, wholesale orders, expenses and reporting.
    Real workbooks, real formulas, no subscriptions and no cloud lock-in.
   </p>
   <div class="hero__cta reveal" data-d="3">
    <a class="btn btn--primary" href="products.html">Explore the systems {ico('arrow', sw=2)}</a>
    <a class="btn btn--ghost" href="demo.html">{ico('play', sw=2)} Try a live demo</a>
   </div>
   <div class="hero__meta reveal" data-d="4">
    <span>{ico('check', sw=2.2)} Five ready-made systems</span>
    <span>{ico('check', sw=2.2)} Custom builds from $325</span>
    <span>{ico('check', sw=2.2)} You own the file, forever</span>
   </div>
   <div class="hero__contact reveal" data-d="5">
    <a class="hero__contact-link" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">
     <span class="icon icon--sm">{ico('instagram', sw=1.9)}</span>
     <span><strong>Instagram</strong><small>{INSTAGRAM_HANDLE}</small></span>
    </a>
    <a class="hero__contact-link" href="mailto:{EMAIL}">
     <span class="icon icon--sm">{ico('mail', sw=1.9)}</span>
     <span><strong>Email</strong><small>{EMAIL}</small></span>
    </a>
   </div>
  </div>
  <div class="hero__stage reveal" data-d="2">
   <div class="hero__frame">
    <div class="hero__chrome"><i></i><i></i><i></i><span>Pouria Business · executive overview</span></div>
    {picture('dash-hero', 'Original mockup of a consolidated Excel executive dashboard with revenue, inventory, wholesale and expense widgets', '', w=1560, h=1040, priority=True)}
   </div>
   <div class="float-card float-card--a">
    <span class="float-card__dot"></span>
    <span><strong>Auto-refresh</strong><small>Inventory synced 02:00</small></span>
   </div>
   <div class="float-card float-card--b">
    <span class="icon icon--sm" style="width:26px;height:26px;border-radius:8px">{ico('chart', sw=2)}</span>
    <span><strong>+18.2% revenue</strong><small>Sample dashboard data</small></span>
   </div>
  </div>
 </div>
 <div class="container">
  <div class="marquee" aria-hidden="true">
   <div class="marquee__track">
    <span>Inventory control</span><span>Sales dashboards</span><span>Wholesale purchase orders</span>
    <span>Expense budgets</span><span>Board-ready reporting</span><span>Power Query automation</span>
    <span>VBA where it earns its place</span><span>Cleaning messy spreadsheets</span>
    <span>Inventory control</span><span>Sales dashboards</span><span>Wholesale purchase orders</span>
    <span>Expense budgets</span><span>Board-ready reporting</span><span>Power Query automation</span>
    <span>VBA where it earns its place</span><span>Cleaning messy spreadsheets</span>
   </div>
  </div>
 </div>
</section>

<!-- ============================ what I build ============================ -->
<section class="section" id="systems">
 <div class="container">
  <div class="section-head section-head--row">
   <div>
    <div class="kicker-row reveal"><span>01 — The catalog</span><span class="rule"></span></div>
    <h2 style="margin-top:16px">Five systems. One habit:<br>the numbers take care of themselves.</h2>
   </div>
   <p class="reveal" data-d="2">Each system is a complete Excel workbook built around one job — stock, sales, wholesale orders, expenses or reporting. Start with the one that hurts most, add the others later.</p>
  </div>
  <div class="grid grid--2">
   {product_cards()}
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;margin-top:28px">
   <p class="muted" style="font-size:13.5px">Every screenshot on this site is an original mockup drawn for this catalog — not a stock image and not someone else's file.</p>
   <a class="link-arrow" href="products.html">Compare all systems {ico('arrow-up-right', sw=2)}</a>
  </div>
 </div>
</section>

<!-- ============================ why it works ============================ -->
<section class="section" style="background:linear-gradient(180deg,transparent,rgba(52,224,161,.03),transparent)">
 <div class="container">
  <div class="grid grid--2" style="align-items:center;gap:clamp(28px,5vw,64px)">
   <div>
    <div class="kicker-row reveal"><span>02 — Why Excel, why automation</span><span class="rule"></span></div>
    <h2 class="reveal" data-d="1" style="font-size:clamp(28px,3.8vw,44px);margin-top:16px">You already trust the spreadsheet. I make it dependable.</h2>
    <p class="reveal" data-d="2" style="color:var(--muted);margin-top:16px;max-width:56ch">
     Most small businesses are not losing money because they lack software. They are losing money to
     the version of the file nobody understands, the stock figure that is three days old, and the
     Sunday evening spent rebuilding a report. A properly built workbook fixes all three.
    </p>
    <ul class="feature-list reveal" data-d="3" style="margin-top:24px">
     <li>{ico('check', sw=2.2)}<span><strong>One input, every view.</strong> Type a sale once; the dashboard, the stock sheet and the monthly report all know about it.</span></li>
     <li>{ico('check', sw=2.2)}<span><strong>Protected structure.</strong> Nobody can accidentally delete a formula or type a date into a number column.</span></li>
     <li>{ico('check', sw=2.2)}<span><strong>No subscription.</strong> It is your file, on your machine or your OneDrive. It keeps working if we never speak again.</span></li>
     <li>{ico('check', sw=2.2)}<span><strong>Documented and handover-ready.</strong> A short guide, a commented formula layer and a walkthrough call.</span></li>
    </ul>
   </div>
   <div class="reveal" data-d="2">
    <div class="card" style="padding:0;overflow:hidden">
     <div class="hero__chrome"><i></i><i></i><i></i><span>inventory · live view</span></div>
     {picture('dash-inventory', 'Original mockup of the Inventory Command Center dashboard with KPI cards, stock movement chart and reorder table')}
    </div>
    <div class="grid grid--2" style="margin-top:16px">
     <div class="card" style="padding:20px">
      <span class="icon icon--sm">{ico('bolt')}</span>
      <h3 style="font-size:15px;margin:12px 0 5px">One click refresh</h3>
      <p style="font-size:12.8px;color:var(--muted)">Power Query pulls your exports in and rebuilds the model.</p>
     </div>
     <div class="card" style="padding:20px">
      <span class="icon icon--sm">{ico('shield')}</span>
      <h3 style="font-size:15px;margin:12px 0 5px">Built to be safe</h3>
      <p style="font-size:12.8px;color:var(--muted)">Validated inputs, protected sheets, a clear backup routine.</p>
     </div>
    </div>
   </div>
  </div>
 </div>
</section>

<!-- ============================ demo teaser ============================ -->
<section class="section">
 <div class="container">
  <div class="card reveal" style="padding:clamp(26px,4vw,54px);background:
     radial-gradient(120% 140% at 100% 0%,rgba(52,224,161,.12),transparent 58%),var(--surface);
     border-color:rgba(52,224,161,.2)">
   <div class="grid grid--2" style="align-items:center;gap:clamp(24px,4vw,52px)">
    <div>
     <span class="eyebrow">Product demonstrations</span>
     <h2 style="font-size:clamp(26px,3.6vw,40px);margin:18px 0 14px">Don't take my word for the logic. Break it yourself.</h2>
     <p style="color:var(--muted);max-width:52ch">
      The demos below are working simulations of the catalog systems, running on sample data.
      Approve an expense, move a purchase order forward, sell ten units of stock — and watch
      every KPI, flag and total recalculate exactly as it does inside the workbook.
     </p>
     <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:24px">
      <a class="btn btn--primary" href="demo.html">Open the demo lab {ico('arrow', sw=2)}</a>
      <a class="btn btn--ghost" href="contact.html">Ask about a custom build</a>
     </div>
     <p class="muted" style="font-size:12px;margin-top:16px">Sample data only — no customer figures, no invented testimonials.</p>
    </div>
    <div class="demo-preview">
     <div class="demo-preview__row"><span>Reorder status</span><b>18 units · reorder 40</b><em class="danger">Critical</em></div>
     <div class="demo-preview__row"><span>Fill rate</span><b>PO-20418</b><em class="ok">96%</em></div>
     <div class="demo-preview__row"><span>Budget used</span><b>$2,480 approved</b><em class="warn">21%</em></div>
     <div class="demo-preview__row"><span>Blended margin</span><b>3 entities</b><em class="ok">36%</em></div>
     <a class="demo-preview__cta" href="demo.html">{ico('play', sw=2)} Launch interactive demo</a>
    </div>
   </div>
  </div>
 </div>
</section>

<!-- ============================ process ============================ -->
<section class="section" id="process">
 <div class="container">
  <div class="section-head section-head--row">
   <div>
    <div class="kicker-row reveal"><span>03 — How a build runs</span><span class="rule"></span></div>
    <h2 style="margin-top:16px">Four steps, no mystery.</h2>
   </div>
   <p class="reveal" data-d="2">Most catalog builds are delivered in 5–10 working days. Custom systems depend on how messy the input is — I will tell you honestly after I have seen your files.</p>
  </div>
  <div class="process">
   <div class="step reveal"><span class="step__num">STEP 01</span><h3>Discovery call</h3><p>A short call and a look at the spreadsheet you use today. We agree what the system must do and what it must not do.</p></div>
   <div class="step reveal" data-d="1"><span class="step__num">STEP 02</span><h3>Blueprint</h3><p>You get a written structure: sheets, tables, rules and the exact deliverables. Nothing is built before you approve it.</p></div>
   <div class="step reveal" data-d="2"><span class="step__num">STEP 03</span><h3>Build & test</h3><p>The workbook is built, protected, documented and stress-tested with your real data shapes and awkward edge cases.</p></div>
   <div class="step reveal" data-d="3"><span class="step__num">STEP 04</span><h3>Handover</h3><p>A walkthrough call, a short manual, and 30 days of support for fixes and questions. The file is yours.</p></div>
  </div>
 </div>
</section>

<!-- ============================ pricing teaser ============================ -->
<section class="section" id="pricing-teaser">
 <div class="container">
  <div class="section-head section-head--row">
   <div>
    <div class="kicker-row reveal"><span>04 — Pricing</span><span class="rule"></span></div>
    <h2 style="margin-top:16px">Fixed prices. Written scope. No surprises.</h2>
   </div>
   <p class="reveal" data-d="2">Catalog systems start at $325 (≈ €290 EUR). Custom work is quoted after the blueprint. Everything is a one-time build — there is no monthly fee to keep using your own file. The final figure depends on your scope, data and requirements, and is confirmed in writing before any work starts.</p>
  </div>
  <div class="price-grid">
   <div class="card price reveal">
    <span class="price__name">Starter system</span>
    <div><span class="price__amount">$325<span>one-time · ≈ €290 EUR</span></span></div>
    <p class="price__desc">One core workbook for a single job — expenses or a clean sales tracker.</p>
    <ul class="price__list">
     <li>{ico('check', sw=2.2)}One catalog system (expenses)</li>
     <li>{ico('check', sw=2.2)}Up to 3 source sheets</li>
     <li>{ico('check', sw=2.2)}Dashboard + printable report</li>
     <li>{ico('check', sw=2.2)}Handover call + manual</li>
     <li>{ico('check', sw=2.2)}14 days of support</li>
    </ul>
    <div class="price__foot"><a class="btn btn--ghost btn--block" href="pricing.html" data-select-plan="Starter">Choose Starter</a></div>
   </div>
   <div class="card price price--feature reveal" data-d="1">
    <span class="tag price__badge">Most chosen</span>
    <span class="price__name">Business system</span>
    <div><span class="price__amount">$660<span>one-time · ≈ €590 EUR</span></span></div>
    <p class="price__desc">A full operating system: inventory, sales or wholesale orders, connected and automated.</p>
    <ul class="price__list">
     <li>{ico('check', sw=2.2)}Any catalog system (inventory, sales, wholesale, reporting)</li>
     <li>{ico('check', sw=2.2)}Up to 8 sheets + dashboard</li>
     <li>{ico('check', sw=2.2)}Automated refreshes (Power Query)</li>
     <li>{ico('check', sw=2.2)}Input validation + sheet protection</li>
     <li>{ico('check', sw=2.2)}Walkthrough recording + manual</li>
     <li>{ico('check', sw=2.2)}30 days of support</li>
    </ul>
    <div class="price__foot"><a class="btn btn--primary btn--block" href="pricing.html" data-select-plan="Business">Choose Business</a></div>
   </div>
   <div class="card price reveal" data-d="2">
    <span class="price__name">Custom build</span>
    <div><span class="price__amount">Quoted<span>from $1,000 · ≈ €895 EUR</span></span></div>
    <p class="price__desc">Something your business needs that no catalog system covers — designed from scratch.</p>
    <ul class="price__list">
     <li>{ico('check', sw=2.2)}Discovery + written blueprint</li>
     <li>{ico('check', sw=2.2)}Unlimited sheets within scope</li>
     <li>{ico('check', sw=2.2)}Power Query, VBA or formulas as needed</li>
     <li>{ico('check', sw=2.2)}Data cleanup included</li>
     <li>{ico('check', sw=2.2)}60 days of support</li>
    </ul>
    <div class="price__foot"><a class="btn btn--ghost btn--block" href="pricing.html" data-select-plan="Custom">Request a quote</a></div>
   </div>
  </div>
  <p class="price__note" style="margin-top:20px">Prices in USD, with EUR shown for reference at ≈ €1 = $1.12. Excluding VAT where applicable. Payment in two parts: 50% to start, 50% on handover. The final quote is confirmed in writing and depends on your scope, data and requirements.</p>
 </div>
</section>

<!-- ============================ about teaser ============================ -->
<section class="section" id="about-teaser">
 <div class="container">
  <div class="grid grid--2" style="gap:clamp(28px,5vw,60px);align-items:center">
   <div class="reveal">
    <div class="portrait-wrap">
     <img src="pouria.jpg" alt="Portrait of the founder of Pouria Business" width="620" height="620" loading="lazy" decoding="async" style="border-radius:24px">
     <div class="portrait-tag">
      <span class="float-card__dot"></span>
      <span><strong>Pouria Asghari</strong><small>Founder · Pouria Business</small></span>
     </div>
    </div>
   </div>
   <div>
    <div class="kicker-row reveal"><span>05 — About</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(28px,3.8vw,44px);margin-top:16px">Pouria Business: one person, one speciality — making Excel do the work.</h2>
    <p class="reveal" data-d="2" style="color:var(--muted);margin-top:16px;max-width:56ch">
     <strong>Pouria Business</strong> is a one-person Excel automation studio. I build systems for small
     businesses — the kind of company where the owner is also the buyer, the accountant and the IT
     department — and every build is handled by me personally, start to finish. Everything I ship is
     built to be opened by a tired person on a Friday afternoon and still make sense.
    </p>
    <p class="reveal" data-d="3" style="color:var(--muted);margin-top:12px;max-width:56ch">
     My background is in code — Python, logic, interactive tools — and that shows in how the
     workbooks are structured: no duplicated formulas, no mystery numbers, no sheets named
     <em>Final_v3_new</em>.
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px" class="reveal" data-d="4">
     <a class="btn btn--primary" href="about.html">More about the studio {ico('arrow', sw=2)}</a>
     <a class="btn btn--ghost" href="contact.html">Talk to me directly</a>
    </div>
   </div>
  </div>
 </div>
</section>

<!-- ============================ faq teaser ============================ -->
<section class="section" id="faq-teaser">
 <div class="container">
  <div class="grid grid--2" style="gap:clamp(28px,5vw,64px);align-items:start">
   <div>
    <div class="kicker-row reveal"><span>06 — Questions</span><span class="rule"></span></div>
    <h2 style="font-size:clamp(28px,3.8vw,44px);margin-top:16px">Straight answers.</h2>
    <p class="reveal" data-d="2" style="color:var(--muted);margin-top:14px;max-width:42ch">The five things people ask before they trust an Excel system with their business.</p>
    <a class="link-arrow reveal" data-d="3" href="faq.html" style="margin-top:22px">Read the full FAQ {ico('arrow-up-right', sw=2)}</a>
   </div>
   <div class="faq reveal" data-d="2">
    <details class="faq__item" open>
     <summary class="faq__q">Is this a real Excel file or an online app?<i></i></summary>
     <div class="faq__a">A real <strong>.xlsx</strong> workbook. It opens in Excel (Microsoft 365 or 2016+) and, where noted, in LibreOffice. You work in a file you own — nothing is hosted, nothing expires.</div>
    </details>
    <details class="faq__item">
     <summary class="faq__q">Do I need macros or a subscription?<i></i></summary>
     <div class="faq__a">No subscription, ever. Most systems run on formulas and Power Query, which need nothing extra. Where a macro genuinely saves time I add it and explain the security setting, but the workbook is designed to keep working without it.</div>
    </details>
    <details class="faq__item">
     <summary class="faq__q">Can it use the spreadsheet I already have?<i></i></summary>
     <div class="faq__a">Yes — that is usually the best starting point. I clean and restructure what you have instead of forcing you onto a new layout, so your product codes, customers and history stay intact.</div>
    </details>
    <details class="faq__item">
     <summary class="faq__q">How long does a build take?<i></i></summary>
     <div class="faq__a">Catalog systems: 5–10 working days. Custom builds: usually 2–4 weeks, depending on data cleanup and how many people need to use it.</div>
    </details>
    <details class="faq__item">
     <summary class="faq__q">What if I break something after handover?<i></i></summary>
     <div class="faq__a">Worst case, you restore a backup — the routine is part of the handover. Support is included (14–60 days depending on the package) and later fixes are quoted as small jobs.</div>
    </details>
   </div>
  </div>
 </div>
</section>

<!-- ============================ contact ============================ -->
<section class="section" id="contact-teaser">
 <div class="container">
  <div class="card reveal" style="padding:clamp(26px,4vw,54px);display:grid;gap:clamp(24px,4vw,48px);
      background:radial-gradient(120% 130% at 0% 0%,rgba(52,224,161,.13),transparent 55%),var(--surface-2);
      border-color:rgba(52,224,161,.18)">
   <div class="grid grid--2" style="gap:clamp(24px,4vw,48px);align-items:center">
    <div>
     <span class="eyebrow">Start here</span>
     <h2 style="font-size:clamp(26px,3.6vw,42px);margin:18px 0 14px">Tell me what your spreadsheet should be doing.</h2>
     <p style="color:var(--muted);max-width:50ch">
      Describe the job in plain words — “I need to know what to reorder every Monday” is a perfectly
      good brief. You will get an honest answer about whether Excel is the right tool, what it
      would cost, and how long it takes.
     </p>
     <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:24px">
      <a class="btn btn--primary" href="contact.html">Send a project brief {ico('send', sw=2)}</a>
      <a class="btn btn--ghost" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{ico('instagram', sw=2)} Instagram</a>
      <a class="btn btn--ghost" href="mailto:{EMAIL}">{ico('mail', sw=2)} {EMAIL}</a>
     </div>
    </div>
    <div class="grid" style="gap:12px">
     <div class="mini"><span class="icon icon--sm">{ico('clock')}</span><div><h4>Reply within one working day</h4><p>Direct messages on Instagram are usually fastest.</p></div></div>
     <div class="mini"><span class="icon icon--sm">{ico('globe')}</span><div><h4>Working in English &amp; Persian</h4><p>Remote delivery, files shared over email or OneDrive.</p></div></div>
     <div class="mini"><span class="icon icon--sm">{ico('lock')}</span><div><h4>Your data stays yours</h4><p>Sample files are deleted after the project unless you ask me to keep them.</p></div></div>
    </div>
   </div>
  </div>
 </div>
</section>
</main>
"""

extra = """<style>
.hero__contact{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.hero__contact-link{display:flex;align-items:center;gap:10px;padding:9px 14px 9px 10px;border-radius:12px;
 border:1px solid var(--line);background:rgba(255,255,255,.022);transition:.25s var(--ease)}
.hero__contact-link:hover{border-color:rgba(52,224,161,.34);background:rgba(52,224,161,.06);transform:translateY(-2px)}
.hero__contact-link strong{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:700}
.hero__contact-link small{display:block;font-size:12.5px;color:var(--text);margin-top:2px}
.portrait-wrap{position:relative;border-radius:26px;padding:10px;background:linear-gradient(160deg,rgba(52,224,161,.22),transparent 55%),var(--surface);border:1px solid var(--line)}
.portrait-wrap img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:18px;filter:saturate(.92) contrast(1.03)}
.portrait-tag{position:absolute;left:24px;bottom:24px;display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:12px;
 background:rgba(8,12,10,.9);border:1px solid var(--line);backdrop-filter:blur(14px);font-size:12px}
.portrait-tag strong{display:block;font-family:var(--font-d);font-size:13.5px}
.portrait-tag small{color:var(--faint);font-size:10.5px}
.demo-preview{border-radius:18px;border:1px solid var(--line);background:#0a100e;padding:8px;display:grid;gap:6px}
.demo-preview__row{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:10px;background:#0d1412;font-size:12.5px}
.demo-preview__row span{color:var(--faint);flex:1}
.demo-preview__row b{color:var(--text);font-weight:600;font-size:12px}
.demo-preview__row em{font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:3px 9px;border-radius:100px}
.demo-preview__row em.ok{background:rgba(52,224,161,.12);color:var(--acc)}
.demo-preview__row em.warn{background:rgba(244,196,100,.12);color:var(--amber)}
.demo-preview__row em.danger{background:rgba(242,114,111,.12);color:var(--danger)}
.demo-preview__cta{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:4px;padding:13px;border-radius:10px;
 background:rgba(52,224,161,.1);border:1px solid rgba(52,224,161,.28);color:var(--acc);font-size:13px;font-weight:600;transition:.25s}
.demo-preview__cta:hover{background:rgba(52,224,161,.18)}
.demo-preview__cta svg{width:15px;height:15px}
</style>"""

page("index.html",
     SITE_TITLE,
     SITE_DESCRIPTION,
     hero, base="", active="home", extra_head=extra, canonical=SITE_URL + "/")
