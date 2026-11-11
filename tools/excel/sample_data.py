"""
Sample dataset for Pouria Business — Smart Inventory & Sales Manager.

Everything here is synthetic but internally consistent: sales and purchase
lines are produced by a day-by-day stock simulation over one trading year, so
quantities never go negative, purchase volumes track real demand, and the
dashboard figures are reproducible. The verifier recomputes the expected totals
from this same module, so any drift between the workbook's formulas and the
data shows up as a test failure.

The dataset is deliberately shaped to exercise every branch of the system:
fast movers, dead stock, one product that sells out completely (out-of-stock
alert), one that stays below its minimum (low-stock alert), unpaid and
part-paid invoices, and expenses across eight categories.
"""

from __future__ import annotations

import datetime as dt
import random

RNG_SEED = 20261110

# When False the workbook is built as a clean starter file: every product,
# customer, supplier and transaction list is empty, but all structure, formulas,
# dropdowns and dashboard wiring are identical.
DEMO_MODE = True

# The newest transaction in the sample data. Every date is derived from this,
# so the demo never looks stale.
AS_OF = dt.date(2026, 8, 31)
START = AS_OF - dt.timedelta(days=320)      # trading year starts here

BUSINESS = {
    "name": "Pouria Business — Demo Trading Co.",
    "currency": "USD",
    "tax_rate": 0.09,
    "fiscal_start_month": 1,
    "low_stock_default": 10,
    "logo_text": "POURIA BUSINESS",
}

# ---------------------------------------------------------------------------
# Suppliers
# ---------------------------------------------------------------------------
SUPPLIERS = [
    # id, name, contact, phone, email, city, country, terms, lead time, status
    {"id": "SUP-001", "name": "Nordic Paper Works", "contact": "Elin Dahl",
     "phone": "+46 8 555 0142", "email": "orders@nordicpaper.example",
     "city": "Stockholm", "country": "Sweden", "terms": "Net 30",
     "lead_time": 12, "status": "Active"},
    {"id": "SUP-002", "name": "Baltic Print & Pack", "contact": "Marek Tamm",
     "phone": "+372 6 555 0119", "email": "sales@balticprint.example",
     "city": "Tallinn", "country": "Estonia", "terms": "Net 14",
     "lead_time": 7, "status": "Active"},
    {"id": "SUP-003", "name": "Atlas Metal Goods", "contact": "Sofia Rossi",
     "phone": "+39 02 555 0177", "email": "hello@atlasmetal.example",
     "city": "Milan", "country": "Italy", "terms": "Net 45",
     "lead_time": 21, "status": "Active"},
    {"id": "SUP-004", "name": "Bright Plastics Ltd", "contact": "James Okafor",
     "phone": "+44 161 555 0133", "email": "trade@brightplastics.example",
     "city": "Manchester", "country": "United Kingdom", "terms": "Net 30",
     "lead_time": 18, "status": "Active"},
    {"id": "SUP-005", "name": "Orient Packaging Co.", "contact": "Wei Chen",
     "phone": "+86 21 5555 0188", "email": "export@orientpack.example",
     "city": "Shanghai", "country": "China", "terms": "Prepaid",
     "lead_time": 35, "status": "Active"},
    {"id": "SUP-006", "name": "Caspian Office Supply", "contact": "Reza Kamali",
     "phone": "+98 21 5555 0121", "email": "orders@caspianoffice.example",
     "city": "Tehran", "country": "Iran", "terms": "Net 21",
     "lead_time": 10, "status": "On hold"},
]

CATEGORIES = [
    "Notebooks",
    "Writing Instruments",
    "Desk Accessories",
    "Paper & Stationery",
    "Storage & Filing",
    "Presentation",
    "Packaging",
]

# ---------------------------------------------------------------------------
# Products
# Selling prices run at roughly 1.8x cost, which leaves a realistic gross
# margin for a wholesale stationery business once discounts are applied.
# ---------------------------------------------------------------------------
def _p(pid, name, cat, sku, cost, price, minimum, supplier, opening):
    return {"id": pid, "name": name, "category": cat, "sku": sku,
            "cost": cost, "price": price, "min": minimum,
            "supplier": supplier, "opening": opening}


PRODUCTS = [
    _p("PRD-001", "A5 Dotted Notebook — Charcoal", "Notebooks", "NB-A5-CHR", 4.20, 7.80, 120, "SUP-002", 400),
    _p("PRD-002", "A5 Dotted Notebook — Forest", "Notebooks", "NB-A5-FST", 4.20, 7.80, 120, "SUP-002", 340),
    _p("PRD-003", "A4 Ruled Notebook — Bulk 5-Pack", "Notebooks", "NB-A4-5PK", 12.80, 23.50, 60, "SUP-001", 180),
    _p("PRD-004", "Pocket Memo Pad — 3-Pack", "Notebooks", "NB-PKT-3PK", 1.90, 3.60, 200, "SUP-001", 600),
    _p("PRD-005", "Hardcover Executive Journal", "Notebooks", "NB-EXE-HC", 9.60, 17.90, 40, "SUP-001", 140),
    _p("PRD-006", "Gel Pen 0.5mm — Black (Box of 12)", "Writing Instruments", "WP-GEL-BLK", 5.40, 9.90, 180, "SUP-005", 520),
    _p("PRD-007", "Gel Pen 0.5mm — Blue (Box of 12)", "Writing Instruments", "WP-GEL-BLU", 5.40, 9.90, 160, "SUP-005", 480),
    _p("PRD-008", "Fountain Pen — Matte Black", "Writing Instruments", "WP-FTN-BLK", 18.50, 34.00, 30, "SUP-003", 90),
    _p("PRD-009", "Mechanical Pencil 0.7mm", "Writing Instruments", "WP-MEC-07", 2.10, 4.10, 140, "SUP-005", 420),
    _p("PRD-010", "Highlighter Set — 6 Colours", "Writing Instruments", "WP-HIL-6C", 3.80, 7.40, 95, "SUP-005", 290),
    _p("PRD-011", "Bamboo Desk Organiser", "Desk Accessories", "DA-BAM-ORG", 14.20, 27.50, 48, "SUP-004", 150),
    _p("PRD-012", "Monitor Stand — Walnut", "Desk Accessories", "DA-MON-WAL", 22.00, 42.00, 26, "SUP-004", 84),
    _p("PRD-013", "Cable Clip Set — 10 Pack", "Desk Accessories", "DA-CBL-10", 2.40, 4.90, 150, "SUP-004", 460),
    _p("PRD-014", "Desk Mat — Charcoal Felt", "Desk Accessories", "DA-MAT-CHR", 11.60, 22.50, 44, "SUP-004", 140),
    _p("PRD-015", "A4 Copy Paper — 500 Sheets", "Paper & Stationery", "PS-A4-500", 3.10, 5.60, 260, "SUP-001", 800),
    _p("PRD-016", "Sticky Notes — Assorted 12-Pack", "Paper & Stationery", "PS-STK-12", 2.60, 5.20, 170, "SUP-005", 520),
    _p("PRD-017", "Recycled Envelopes — C5 (50)", "Paper & Stationery", "PS-ENV-C5", 4.10, 7.90, 110, "SUP-002", 340),
    _p("PRD-018", "Arch Lever File — A4 (10)", "Storage & Filing", "ST-LEV-A4", 8.90, 16.50, 70, "SUP-002", 210),
    _p("PRD-019", "Document Wallet — Pack of 5", "Storage & Filing", "ST-WAL-5PK", 3.30, 6.40, 96, "SUP-002", 300),
    _p("PRD-020", "Storage Box — A4 (Set of 4)", "Storage & Filing", "ST-BOX-4ST", 7.40, 14.20, 54, "SUP-006", 170),
    _p("PRD-021", "Whiteboard — 90×60cm", "Presentation", "PR-WB-9060", 16.80, 32.00, 30, "SUP-003", 95),
    _p("PRD-022", "Flipchart Pad — 5 Pack", "Presentation", "PR-FLP-5PK", 9.20, 18.00, 38, "SUP-003", 120),
    # PRD-023 is intentionally never reordered: it sells out and stays at zero
    # so the out-of-stock alert always has something to show.
    _p("PRD-023", "Laser Pointer — USB-C", "Presentation", "PR-LSR-USB", 12.40, 24.50, 24, "SUP-003", 60),
    _p("PRD-024", "Kraft Shipping Box — Medium (20)", "Packaging", "PK-KRT-M20", 11.20, 20.50, 58, "SUP-002", 180),
    _p("PRD-025", "Bubble Wrap Roll — 50m", "Packaging", "PK-BBL-50", 6.80, 12.90, 76, "SUP-005", 240),
]

PRODUCT_BY_ID = {p["id"]: p for p in PRODUCTS}

# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
CUSTOMERS = [
    {"id": "CUS-001", "name": "Bluebird Design Studio", "contact": "Maya Lindqvist",
     "email": "maya@bluebirddesign.example", "phone": "+46 8 555 0210",
     "city": "Stockholm", "country": "Sweden", "type": "Retail",
     "credit_limit": 8000, "since": dt.date(2024, 3, 12)},
    {"id": "CUS-002", "name": "Harbour Coffee Roasters", "contact": "Tomas Berg",
     "email": "tom@harbourcoffee.example", "phone": "+46 31 555 0244",
     "city": "Gothenburg", "country": "Sweden", "type": "Retail",
     "credit_limit": 6000, "since": dt.date(2024, 6, 2)},
    {"id": "CUS-003", "name": "Meridian Architects", "contact": "Ana Duarte",
     "email": "ana@meridianarch.example", "phone": "+351 21 555 0188",
     "city": "Lisbon", "country": "Portugal", "type": "Wholesale",
     "credit_limit": 24000, "since": dt.date(2023, 11, 20)},
    {"id": "CUS-004", "name": "Northline Logistics", "contact": "Peter Nagy",
     "email": "peter@northline.example", "phone": "+36 1 555 0166",
     "city": "Budapest", "country": "Hungary", "type": "Wholesale",
     "credit_limit": 32000, "since": dt.date(2023, 4, 8)},
    {"id": "CUS-005", "name": "Studio Fern", "contact": "Chloe Martin",
     "email": "chloe@studiofern.example", "phone": "+33 1 55 55 0142",
     "city": "Paris", "country": "France", "type": "Retail",
     "credit_limit": 10000, "since": dt.date(2025, 1, 15)},
    {"id": "CUS-006", "name": "Kestrel Consulting", "contact": "David Whitmore",
     "email": "david@kestrel.example", "phone": "+44 20 5555 0199",
     "city": "London", "country": "United Kingdom", "type": "Wholesale",
     "credit_limit": 40000, "since": dt.date(2022, 9, 5)},
    {"id": "CUS-007", "name": "Verdant Landscaping", "contact": "Ines Silva",
     "email": "ines@verdant.example", "phone": "+351 22 555 0177",
     "city": "Porto", "country": "Portugal", "type": "Retail",
     "credit_limit": 5000, "since": dt.date(2025, 4, 22)},
    {"id": "CUS-008", "name": "Atelier Noir", "contact": "Lucas Bernard",
     "email": "lucas@ateliernoir.example", "phone": "+33 4 55 55 0121",
     "city": "Lyon", "country": "France", "type": "Retail",
     "credit_limit": 7000, "since": dt.date(2024, 10, 3)},
    {"id": "CUS-009", "name": "Summit Coworking", "contact": "Erik Halvorsen",
     "email": "erik@summitcw.example", "phone": "+47 22 55 55 0110",
     "city": "Oslo", "country": "Norway", "type": "Wholesale",
     "credit_limit": 28000, "since": dt.date(2023, 8, 14)},
    {"id": "CUS-010", "name": "Willow & Sage Studio", "contact": "Nora Fischer",
     "email": "nora@willowsage.example", "phone": "+49 30 5555 0128",
     "city": "Berlin", "country": "Germany", "type": "Retail",
     "credit_limit": 9000, "since": dt.date(2025, 7, 9)},
    {"id": "CUS-011", "name": "Redgate Print Shop", "contact": "Owen Price",
     "email": "owen@redgateprint.example", "phone": "+44 117 555 0154",
     "city": "Bristol", "country": "United Kingdom", "type": "Wholesale",
     "credit_limit": 20000, "since": dt.date(2024, 2, 27)},
    {"id": "CUS-012", "name": "Lumen Events", "contact": "Sara Haddad",
     "email": "sara@lumenevents.example", "phone": "+971 4 555 0193",
     "city": "Dubai", "country": "United Arab Emirates", "type": "Retail",
     "credit_limit": 12000, "since": dt.date(2025, 2, 11)},
]

CUSTOMER_BY_ID = {c["id"]: c for c in CUSTOMERS}

# ---------------------------------------------------------------------------
# Expenses — sized so the year lands at a believable net margin (~10-14%)
# ---------------------------------------------------------------------------
EXPENSE_CATEGORIES = [
    "Rent", "Utilities", "Salaries", "Marketing",
    "Software", "Logistics", "Office", "Insurance",
]

PAYMENT_METHODS = ["Bank transfer", "Card", "Cash", "PayPal"]

EXPENSE_ROWS = [
    # day offset, category, description, payee, amount, method, tax deductible
    (310, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (300, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (296, "Utilities", "Electricity and heating", "City Power", 190.00, "Bank transfer", "Yes"),
    (288, "Software", "Accounting suite (annual)", "Ledgerly", 220.00, "Card", "Yes"),
    (282, "Marketing", "Instagram ads — spring campaign", "Meta", 380.00, "Card", "Yes"),
    (280, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (272, "Logistics", "Courier account — month 1", "Swiftline", 440.00, "Bank transfer", "Yes"),
    (268, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (260, "Office", "Packaging supplies and tape", "Baltic Print & Pack", 290.00, "Card", "Yes"),
    (250, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (242, "Insurance", "Stock and liability insurance", "SafeGuard", 350.00, "Bank transfer", "Yes"),
    (238, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (230, "Logistics", "Courier account — month 2", "Swiftline", 490.00, "Bank transfer", "Yes"),
    (226, "Marketing", "Trade fair booth and materials", "Expo Nordic", 720.00, "Bank transfer", "Yes"),
    (220, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (212, "Utilities", "Water and waste", "City Water", 90.00, "Bank transfer", "Yes"),
    (208, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (200, "Software", "Inventory scanner licences", "ScanWorks", 140.00, "Card", "Yes"),
    (190, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (184, "Logistics", "Courier account — month 3", "Swiftline", 460.00, "Bank transfer", "Yes"),
    (178, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (170, "Office", "Racking and shelving", "Bright Plastics Ltd", 570.00, "Card", "Yes"),
    (160, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (152, "Marketing", "Website photography", "Studio Fern", 440.00, "Card", "Yes"),
    (148, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (140, "Utilities", "Electricity and heating", "City Power", 170.00, "Bank transfer", "Yes"),
    (132, "Logistics", "Courier account — month 4", "Swiftline", 520.00, "Bank transfer", "Yes"),
    (130, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (120, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (112, "Software", "Email and design tools", "Ledgerly", 60.00, "Card", "Yes"),
    (104, "Office", "Printer toner and paper", "Caspian Office Supply", 190.00, "Card", "Yes"),
    (100, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 960.00, "Bank transfer", "Yes"),
    (94, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (86, "Logistics", "Courier account — month 5", "Swiftline", 540.00, "Bank transfer", "Yes"),
    (80, "Marketing", "Instagram ads — summer campaign", "Meta", 410.00, "Card", "Yes"),
    (72, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 1020.00, "Bank transfer", "Yes"),
    (66, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1620.00, "Bank transfer", "Yes"),
    (58, "Utilities", "Water and waste", "City Water", 90.00, "Bank transfer", "Yes"),
    (50, "Insurance", "Stock and liability insurance", "SafeGuard", 350.00, "Bank transfer", "Yes"),
    (44, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 1020.00, "Bank transfer", "Yes"),
    (38, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1680.00, "Bank transfer", "Yes"),
    (30, "Logistics", "Courier account — month 6", "Swiftline", 580.00, "Bank transfer", "Yes"),
    (22, "Software", "Inventory scanner licences", "ScanWorks", 140.00, "Card", "Yes"),
    (16, "Rent", "Warehouse unit B4 — monthly rent", "Harbour Properties", 1020.00, "Bank transfer", "Yes"),
    (10, "Marketing", "Newsletter sponsorship", "Indie Trade Weekly", 190.00, "Card", "Yes"),
    (4, "Salaries", "Warehouse team — monthly payroll", "Payroll", 1680.00, "Bank transfer", "Yes"),
]


# ---------------------------------------------------------------------------
# Trading simulation
# ---------------------------------------------------------------------------
OPENING_STOCK = {}


def _sales_plan():
    """Two to three invoices per week across the trading year, cycling customers."""
    rng = random.Random(RNG_SEED + 1)
    plan = []
    seq = 0
    day = 318
    while day >= 2:
        seq += 1
        cust = CUSTOMERS[(seq * 7) % len(CUSTOMERS)]["id"]
        roll = rng.random()
        if roll < 0.74:
            status, ratio = "Paid", 1.0
        elif roll < 0.88:
            status, ratio = "Part paid", rng.choice([0.3, 0.4, 0.5, 0.6])
        else:
            status, ratio = "Unpaid", 0.0
        plan.append({"seq": seq, "day": day, "customer_id": cust,
                     "status": status, "ratio": ratio})
        day -= rng.choice([2, 2, 3, 3, 4, 5])
    return plan


SALES_PLAN = _sales_plan()


def _build_tables():
    """
    Day-by-day simulation over the trading year.

      * Purchase run every 7 days: a product is reordered when stock drops
        below twice its minimum level, topping it back up to six times the
        minimum. PRD-023 is excluded so it sells out and stays at zero.
      * Sales are capped by available stock, so the position never goes
        negative and no invoice can oversell.
    """
    rng = random.Random(RNG_SEED)
    NEVER_REORDER = {"PRD-023"}
    # Reordering stops partway through the year for these, so they end up
    # either below their minimum (low stock) or at zero (out of stock).
    STOP_AFTER = {"PRD-005": 285, "PRD-008": 250, "PRD-012": 270, "PRD-021": 265, "PRD-022": 315}
    RUN_EVERY = 7

    stock = {p["id"]: float(p["opening"]) for p in PRODUCTS}
    OPENING_STOCK.update(stock)

    purchases, purchase_lines, sales, sale_lines = [], [], [], []
    po_seq = 0

    plan_by_day = {}
    for inv in SALES_PLAN:
        plan_by_day.setdefault(inv["day"], []).append(inv)

    for day in range(0, 321):
        date = START + dt.timedelta(days=day)

        # ---------------- purchase run ----------------
        if day % RUN_EVERY == 0:
            for sup_id in sorted({p["supplier"] for p in PRODUCTS}):
                lines = []
                for p in PRODUCTS:
                    if p["supplier"] != sup_id or p["id"] in NEVER_REORDER:
                        continue
                    if day > STOP_AFTER.get(p["id"], 999):
                        continue
                    pid = p["id"]
                    if stock[pid] >= p["min"] * 2.6:
                        continue
                    target = p["min"] * 5.6
                    qty = int(max(10, -(-(target - stock[pid]) // 10) * 10))
                    unit_cost = round(p["cost"] * rng.choice([1.0, 1.0, 1.0, 1.02]), 2)
                    lines.append((p, qty, unit_cost))
                if not lines:
                    continue
                po_seq += 1
                pid_str = f"PO-{date.year}-{po_seq:04d}"
                total = 0.0
                for line_no, (p, qty, unit_cost) in enumerate(lines, start=1):
                    line_total = round(qty * unit_cost, 2)
                    total += line_total
                    stock[p["id"]] += qty
                    purchase_lines.append({
                        "purchase_id": pid_str, "date": date, "supplier_id": sup_id,
                        "product_id": p["id"], "qty": qty, "unit_cost": unit_cost,
                        "line_total": line_total, "line": line_no,
                    })
                purchases.append({
                    "id": pid_str, "date": date, "supplier_id": sup_id,
                    "total": round(total, 2),
                    "status": "Unpaid" if date > AS_OF - dt.timedelta(days=30) else "Paid",
                })

        # ---------------- sales ----------------
        for inv in plan_by_day.get(day, []):
            picks = rng.sample(PRODUCTS, rng.choice([2, 2, 3, 3, 4]))
            kept = []
            for p in picks:
                pid = p["id"]
                want = rng.choice([10, 15, 20, 25, 30, 40, 50, 60, 80])
                qty = int(min(want, stock[pid]))
                if qty <= 0:
                    continue
                stock[pid] -= qty
                disc = rng.choice([0, 0, 0, 5, 5, 10]) if qty >= 30 else 0
                gross = round(qty * p["price"], 2)
                discount = round(gross * disc / 100.0, 2)
                kept.append({
                    "product_id": pid, "qty": qty, "unit_price": p["price"],
                    "discount_pct": disc, "line_total": round(gross - discount, 2),
                    "line": len(kept) + 1, "unit_cost": p["cost"],
                })
            if not kept:
                continue
            sid = f"INV-{date.year}-{inv['seq']:04d}"
            subtotal = round(sum(k["line_total"] for k in kept), 2)
            for k in kept:
                k.update({"invoice_id": sid, "date": date,
                          "customer_id": inv["customer_id"]})
                sale_lines.append(k)
            sales.append({
                "id": sid, "date": date, "customer_id": inv["customer_id"],
                "subtotal": subtotal,
                "status": inv["status"],
                "amount_paid": round(subtotal * inv["ratio"], 2),
                "due_date": date + dt.timedelta(days=30),
            })

    sales.sort(key=lambda r: (r["date"], r["id"]))
    sale_lines.sort(key=lambda r: (r["date"], r["invoice_id"], r["line"]))
    purchases.sort(key=lambda r: (r["date"], r["id"]))
    purchase_lines.sort(key=lambda r: (r["date"], r["purchase_id"], r["line"]))
    return purchases, purchase_lines, sales, sale_lines


PURCHASES, PURCHASE_LINES, SALES, SALE_LINES = _build_tables()


def stock_movement():
    """Opening + purchases - sales per product."""
    stock = {p["id"]: OPENING_STOCK.get(p["id"], p["opening"]) for p in PRODUCTS}
    for line in PURCHASE_LINES:
        stock[line["product_id"]] += line["qty"]
    for line in SALE_LINES:
        stock[line["product_id"]] -= line["qty"]
    return stock


def expected_totals():
    """The numbers the workbook's dashboard must reproduce."""
    stock = stock_movement()
    revenue = round(sum(s["subtotal"] for s in SALES), 2)
    cogs = round(sum(l["qty"] * l["unit_cost"] for l in SALE_LINES), 2)
    expenses = round(sum(e[4] for e in EXPENSE_ROWS), 2)
    purchases = round(sum(p["total"] for p in PURCHASES), 2)
    inv_value = round(sum(stock[p["id"]] * p["cost"] for p in PRODUCTS), 2)
    return {
        "revenue": revenue,
        "cogs": cogs,
        "gross_profit": round(revenue - cogs, 2),
        "expenses": expenses,
        "net_profit": round(revenue - cogs - expenses, 2),
        "purchases": purchases,
        "inventory_value": inv_value,
        "product_count": len(PRODUCTS),
        "low_stock": sum(1 for p in PRODUCTS
                         if 0 < stock[p["id"]] <= p["min"]),
        "out_of_stock": sum(1 for p in PRODUCTS if stock[p["id"]] <= 0),
        "invoice_count": len(SALES),
        "sale_lines": len(SALE_LINES),
        "purchase_lines": len(PURCHASE_LINES),
        "receivable": round(sum(s["subtotal"] - s["amount_paid"] for s in SALES), 2),
        "stock": stock,
    }


if __name__ == "__main__":
    t = expected_totals()
    print(f"products={t['product_count']} invoices={t['invoice_count']} "
          f"lines={t['sale_lines']} purchase_lines={t['purchase_lines']}")
    print(f"revenue={t['revenue']:,.2f} cogs={t['cogs']:,.2f} "
          f"gross={t['gross_profit']:,.2f} ({t['gross_profit']/t['revenue']:.1%})")
    print(f"expenses={t['expenses']:,.2f} net={t['net_profit']:,.2f} "
          f"({t['net_profit']/t['revenue']:.1%})")
    print(f"purchases={t['purchases']:,.2f} inventory={t['inventory_value']:,.2f}")
    print(f"low_stock={t['low_stock']} out_of_stock={t['out_of_stock']} "
          f"receivable={t['receivable']:,.2f}")
