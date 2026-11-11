# Pouria Business — Smart Inventory & Sales Manager

A complete, commercial-quality Excel workbook that lets a small business run products, stock,
purchases, sales, customers, suppliers, expenses and reporting from one file.

- **Real product, not a mockup.** Every figure is a live formula. Change a quantity and the
  inventory, dashboard, customer balance and monthly reports all move.
- **No macros, no add-ins, no external links.** Standard Excel formulas only, so it works in
  Microsoft Excel 2016+ on Windows and macOS, and survives email filters that strip `.xlsm`.
- **Ten working sheets plus three hidden data sheets**, in a dark-navy and emerald interface with
  a consistent type scale, KPI cards and two charts.

---

## Files

| File | What it is |
| --- | --- |
| `Pouria_Business_Inventory_Manager.xlsx` | The product, filled with one trading year of demo data (25 products, 100 invoices, 47 purchase lines, 47 expenses) so every feature is visibly working |
| `Sample_Data.xlsx` | The same workbook with **no records** — use this to start a real business |
| `User_Guide.pdf` | 9-page guide: setup, daily use, dashboard reference, troubleshooting |

---

## The ten sheets

| Sheet | Purpose |
| --- | --- |
| **Dashboard** | 12 KPI cards, monthly sales chart, top-5 products, 8 most recent invoices, live reorder list |
| **Products** | Catalogue with cost, price, minimum level, opening stock and five calculated columns |
| **Sales** | One row per invoice: items, subtotal, tax, total, paid, balance, status, due date, days overdue, profit, margin |
| **Purchases** | One row per purchase order, with calculated totals and payment status |
| **Inventory** | Live stock per product, reorder quantity, stock value at cost and at retail, status and next action |
| **Customers** | Customer database with invoice count, lifetime value, outstanding balance, last order |
| **Suppliers** | Supplier database with order count, total spend, last order |
| **Expenses** | Operating costs by category, date, payee and payment method, with tax |
| **Reports** | Month-by-month sales/profit/expenses, sales-vs-profit chart, sales by category, expenses by category, annual summary |
| **Settings** | Business name, currency, tax rate, fiscal year, and every dropdown source list |

Hidden sheets: `SalesData` (one row per invoice line), `PurchaseData` (one row per purchase line),
`Lists` (dropdown sources). Hidden on purpose — see "Design notes" below.

---

## What is calculated (nothing is hard-coded)

| Figure | Formula basis |
| --- | --- |
| Product stock | `Opening + SUMIF(purchases) − SUMIF(sales)` |
| Stock status | `Out of stock` when ≤ 0, `Low stock` when ≤ minimum, else `In stock` |
| Stock value | Current stock × cost price |
| Invoice subtotal | `SUMIF` of its lines on `SalesData` |
| Tax / total / balance | Subtotal × tax rate; subtotal + tax; total − paid |
| Payment status | Derived from paid vs total — never typed |
| Invoice profit | Line revenue − (quantity × unit cost at time of sale) |
| Dashboard KPIs | Aggregates over `SalesData`, `PurchaseData`, `Products`, `Expenses` |
| Monthly reports | `MONTH(date)` bucketing, so month boundaries follow the invoice date |
| Top products | `LARGE()` over a revenue + `ROW()/100000` key, so ties never collapse |

---

## Validation and error prevention

- **Dropdowns** for category, supplier, customer, expense category, payment method, payment status,
  supplier status, customer type and currency — all sourced from Settings or the ID columns.
- **Unique guards** on product ID and invoice number (`COUNTIF ≤ 1`), so a duplicate cannot be typed.
- **Numeric guards**: prices, stock, quantities and expense amounts must be ≥ 0.
- **Date guards** on the transaction sheets.
- **Conditional formatting** turns stock status, payment status and overdue days into green / amber /
  red automatically.
- **Sheet protection** (no password) locks every formula cell while leaving input cells editable.

---

## Design notes

**Why the line data is on hidden sheets.** A four-product invoice is one row on the Sales sheet but
four rows of quantities. Putting quantities on a separate line sheet is how real accounting systems
are built: the invoice stays readable, the detail stays complete, and the visible amounts are `SUMIF`s
over those lines so the two can never disagree.

**Why plain ranges instead of table structured references.** Formulas use normal ranges such as
`SalesData!$E$2:$E$1501`. This keeps the workbook calculable by standard formula engines — which is
what let it be verified automatically (see below) — and it is what Excel writes anyway once you add a
row. Each sheet still has a real Excel Table (with filter buttons and banded styling) over its data.

**Why the exchange of precision.** Money cells are formatted to two decimals and calculations are done
on unrounded values, so a 100-invoice year reconciles to the cent against hand-computed totals.

---

## Verification

The workbook ships with the tooling used to test it, in `tools/excel/`:

| Script | What it does |
| --- | --- |
| `sample_data.py` | Deterministic generator: a day-by-day stock simulation produces one trading year. Sales are capped by available stock, so no product can ever go negative, and one product is deliberately never reordered so the out-of-stock alert always has something to show |
| `build_workbook.py`, `sheets_*.py` | The workbook builder |
| `make_workbook.py` | Rebuilds both `.xlsx` files |
| `lint_formulas.py` | Parses all 44,147 formulas — catches malformed syntax in seconds |
| `verify_workbook.py` | **Recalculates the workbook** and compares 29 results against figures computed independently in Python |
| `make_guide.py` | Rebuilds `User_Guide.pdf` |

```
cd tools/excel
python3 make_workbook.py      # build both workbooks
python3 lint_formulas.py      # 44,147 formulas, 0 invalid
python3 verify_workbook.py    # 29 passed, 0 failed
python3 make_guide.py         # rebuild the PDF
```

Requires `xlsxwriter`, `reportlab` and `formulas` (the last one is the calculation engine).

### What the verification actually proves

`verify_workbook.py` does not check syntax — it evaluates every formula and compares the result with
the expected value:

```
[1] Dashboard KPIs          12 checks   total sales, gross/net profit, purchases, expenses,
                                        inventory value, product/low/out counts, receivables, invoices
[2] Margins                  2 checks   gross and net margin to 3 decimal places
[3] Inventory and stock     3 checks   all 25 products' stock and status agree with the simulation;
                                        no negative stock; Inventory total matches Products
[4] Invoice arithmetic      3 checks   subtotal, tax, total and balance on 12 invoices; status values;
                                        per-invoice profit
[5] Customer/supplier       3 checks   invoice counts, lifetime value, order counts
[6] Reports                 2 checks   12 monthly buckets and the annual total
[6b] Dashboard lists        4 checks   newest invoice, second newest, reorder list, top product
[7] Formula integrity       1 check    0 error cells anywhere in 44,147 formulas
```

Current result: **29 passed, 0 failed**. The demo totals of
**$149,483.65 sales / $68,116.15 gross profit / $31,416.15 net profit / $47,353.50 inventory**
reproduce exactly.

---

## Demo data

Everything in the demo workbook is invented: 25 products across 7 categories, 12 customers in 9
countries, 6 suppliers, one trading year (Sep 2025 – Aug 2026) producing 100 invoices, 47 purchase
lines and 47 expense records. There are **no real customers, no invented testimonials and no
fabricated statistics** — the numbers exist only to demonstrate the formulas.

The dataset deliberately includes: one out-of-stock product (`PRD-023`), one product at zero after
being run down (`PRD-012`), one below its minimum (`PRD-008`), and a mix of paid, part-paid and
unpaid invoices, so every conditional format and alert is exercised.

Headline demo figures (as of 31 Aug 2026):

| Metric | Value |
| --- | --- |
| Sales | $149,483.65 |
| Gross profit | $68,116.15 (45.6%) |
| Operating expenses | $36,700.00 |
| Net profit | $31,416.15 (21.0%) |
| Purchases | $88,914.40 |
| Inventory value | $47,353.50 |
| Outstanding receivables | $34,921.79 |

---

## Requirements and limits

- **Excel 2016+ / Microsoft 365** on Windows or macOS. Excel for the web works but is slower on the
  1,500-row ranges.
- Uses `SUMIFS`, `MAXIFS`, `COUNTIFS`, `SUMPRODUCT`, `TEXT`, `LARGE`/`MATCH`/`INDEX` and `IFERROR`
  — all available in Excel 2016 and later. The formula set was checked to avoid anything newer
  (`XLOOKUP`, `LET`, dynamic arrays), so the file opens and calculates on older installations.
- LibreOffice Calc opens the file and calculates most formulas, but charts and some conditional
  formats do not render identically. Excel is the supported environment.
- Not designed for multi-user simultaneous editing through OneDrive co-authoring; it is a single
  owner's file, which is what most small businesses actually need.

---

## Support

Pouria Business — Excel automation for small business.

- Email: [pouriabusines1@gmail.com](mailto:pouriabusines1@gmail.com)
- Instagram: [@pouria_busines](https://www.instagram.com/pouria_busines/)
- Telegram: [@pouria_busines](https://t.me/pouria_busines)

Built by Pouria Asghari.
