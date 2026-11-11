"""Sheet builders: master data (Products / Customers / Suppliers) and Settings."""

from __future__ import annotations

import datetime as dt

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from theme import *          # noqa: F401,F403
import sample_data as S
from build_workbook import (
    SH_PROD, SH_CUST, SH_SUP, SH_SET, SH_LISTS, SH_SALES, SH_PURCH,
    PRODUCT_ROWS, DATA_ROWS, LAST_DATA_ROW, rng, prng,
)

# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
PRODUCT_COLS = [
    # header, width, kind
    ("Product ID", 12, "in_txt"),
    ("Product Name", 34, "in_txt"),
    ("Category", 20, "in_txt"),
    ("SKU", 14, "in_txt"),
    ("Supplier", 30, "in_txt"),
    ("Cost Price", 12, "in_money"),
    ("Selling Price", 12, "in_money"),
    ("Min Stock", 10, "in_num"),
    ("Opening Stock", 12, "in_num"),
    ("Purchased", 11, "fx_num"),
    ("Sold", 10, "fx_num"),
    ("Current Stock", 12, "fx_num"),
    ("Stock Value", 13, "fx_money"),
    ("Stock Status", 15, "fx_txt"),
    ("Last Sale", 12, "fx_date"),
]


def build_products(wb):
    name = SH_PROD
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    ws.set_row(0, 34)

    ws.merge_range("A1:O1", "", wb.fmt("title"))
    ws.write("A1", "Products", wb.fmt("title"))
    ws.merge_range("A2:O2", "Master list of everything you sell. Add a product here once, then "
                            "it becomes available in the Sales and Purchases forms.", wb.fmt("subtitle"))

    # column widths
    for i, (_, width, _) in enumerate(PRODUCT_COLS):
        ws.set_column(i, i, width)

    # header row (row 4 -> index 3)
    HEADER_ROW = 3
    for i, (header, _, kind) in enumerate(PRODUCT_COLS):
        style = "th_num" if "num" in kind or "money" in kind or "date" in kind else "th"
        ws.write(HEADER_ROW, i, header, wb.fmt(style))
    ws.set_row(HEADER_ROW, 30)

    # product rows
    for r, p in enumerate(S.PRODUCTS):
        row = HEADER_ROW + 1 + r            # 0-based index
        n = row + 1                          # 1-based excel row
        ws.write_string(row, 0, p["id"], wb.fmt("in_txt"))
        ws.write_string(row, 1, p["name"], wb.fmt("in_txt"))
        ws.write_string(row, 2, p["category"], wb.fmt("in_txt"))
        ws.write_string(row, 3, p["sku"], wb.fmt("in_txt"))
        sup = next(s for s in S.SUPPLIERS if s["id"] == p["supplier"])
        ws.write_string(row, 4, f'{sup["id"]} — {sup["name"]}', wb.fmt("in_txt"))
        ws.write_number(row, 5, p["cost"], wb.fmt("in_money"))
        ws.write_number(row, 6, p["price"], wb.fmt("in_money"))
        ws.write_number(row, 7, p["min"], wb.fmt("in_num"))
        ws.write_number(row, 8, p["opening"], wb.fmt("in_num"))

        # ---- live formulas ----
        # Purchased = sum of purchase lines for this product
        ws.write_formula(
            row, 9,
            f'=SUMIF({rng("PurchaseData","C")},$A{n},{rng("PurchaseData","F")})',
            wb.fmt("fx_num"), 0)
        # Sold = sum of sale lines for this product
        ws.write_formula(
            row, 10,
            f'=SUMIF({rng("SalesData","D")},$A{n},{rng("SalesData","G")})',
            wb.fmt("fx_num"), 0)
        # Current Stock = opening + purchased - sold
        ws.write_formula(
            row, 11, f'=I{n}+J{n}-K{n}', wb.fmt("fx_num"), 0)
        # Stock Value = current * cost
        ws.write_formula(
            row, 12, f'=L{n}*F{n}', wb.fmt("fx_money"), 0)
        # Stock Status
        ws.write_formula(
            row, 13,
            f'=IF($A{n}="","",IF(L{n}<=0,"Out of stock",'
            f'IF(L{n}<=H{n},"Low stock","In stock")))',
            wb.fmt("fx_txt"), "")
        # Last Sale
        ws.write_formula(
            row, 14,
            f'=IFERROR(MAXIFS({rng("SalesData","B")},{rng("SalesData","D")},$A{n}),"")',
            wb.fmt("fx_date"), "")

    # blank input rows so the owner can add products
    first_blank = HEADER_ROW + 1 + len(S.PRODUCTS)
    last_row = PRODUCT_ROWS + HEADER_ROW
    blank_styles = {0: "in_txt", 1: "in_txt", 2: "in_txt", 3: "in_txt",
                    4: "in_txt", 5: "in_money", 6: "in_money", 7: "in_num",
                    8: "in_num"}
    for row in range(first_blank, last_row + 1):
        n = row + 1
        for col, style in blank_styles.items():
            ws.write_blank(row, col, None, wb.fmt(style))
        ws.write_formula(row, 9, f'=IF($A{n}="","",SUMIF({rng("PurchaseData","C")},$A{n},{rng("PurchaseData","F")}))', wb.fmt("fx_num"), "")
        ws.write_formula(row, 10, f'=IF($A{n}="","",SUMIF({rng("SalesData","D")},$A{n},{rng("SalesData","G")}))', wb.fmt("fx_num"), "")
        ws.write_formula(row, 11, f'=IF($A{n}="","",I{n}+J{n}-K{n})', wb.fmt("fx_num"), "")
        ws.write_formula(row, 12, f'=IF($A{n}="","",L{n}*F{n})', wb.fmt("fx_money"), "")
        ws.write_formula(row, 13, f'=IF($A{n}="","",IF(L{n}<=0,"Out of stock",IF(L{n}<=H{n},"Low stock","In stock")))', wb.fmt("fx_txt"), "")
        ws.write_formula(row, 14, f'=IF($A{n}="","",IFERROR(MAXIFS({rng("SalesData","B")},{rng("SalesData","D")},$A{n}),""))', wb.fmt("fx_date"), "")

    # data validation: category from the category list, product id text only
    cat_first = 2
    cat_last = 1 + len(S.CATEGORIES) + 30
    ws.data_validation(HEADER_ROW + 1, 2, last_row, 2, {
        "validate": "list",
        "source": f"='{SH_SET}'!$B${cat_first}:$B${cat_last}",
        "error_title": "Pick a category",
        "error_message": "Choose a category from the Settings list, or add a new one there first.",
        "input_title": "Category",
        "input_message": "Pick from the list so reports group correctly.",
    })
    # supplier dropdown from Settings supplier column
    ws.data_validation(HEADER_ROW + 1, 4, last_row, 4, {
        "validate": "list",
        "source": f"='{SH_SET}'!$D${cat_first}:$D${cat_last}",
        "error_title": "Pick a supplier",
        "error_message": "Choose a supplier listed in Settings.",
    })
    # numeric guards
    ws.data_validation(HEADER_ROW + 1, 5, last_row, 8, {
        "validate": "decimal", "criteria": ">=", "value": 0,
        "error_title": "Positive numbers only",
        "error_message": "Prices and stock levels cannot be negative.",
    })
    # unique product id (no duplicates)
    ws.data_validation(HEADER_ROW + 1, 0, last_row, 0, {
        "validate": "custom",
        "value": f'=COUNTIF($A${HEADER_ROW+2}:$A${last_row+1},$A${HEADER_ROW+2})<=1',
        "error_title": "Duplicate product ID",
        "error_message": "Every product needs a unique ID.",
    })

    # conditional formatting on stock status
    status_rng = f"O{HEADER_ROW+2}:O{last_row+1}".replace("O", "N")
    for text, style in (("Out of stock", "pill_out"), ("Low stock", "pill_low"),
                        ("In stock", "pill_ok")):
        ws.conditional_format(status_rng, {
            "type": "text", "criteria": "containing", "value": text,
            "format": wb.fmt(style),
        })

    ws.freeze_panes(HEADER_ROW + 1, 2)
    ws.autofilter(HEADER_ROW, 0, last_row, len(PRODUCT_COLS) - 1)
    ws.set_landscape()
    ws.set_paper(9)
    ws.fit_to_pages(1, 0)
    ws.repeat_rows(HEADER_ROW, HEADER_ROW)
    wb.nav_row(name, len(PRODUCT_COLS), name)
    return ws


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------
def build_customers(wb):
    name = SH_CUST
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    cols = [("Customer ID", 13), ("Customer Name", 30), ("Contact Person", 20),
            ("Email", 30), ("Phone", 20), ("City", 14), ("Country", 18),
            ("Type", 12), ("Credit Limit", 13), ("Customer Since", 14),
            ("Invoices", 10), ("Total Sales", 14), ("Outstanding", 13),
            ("Last Order", 12), ("Status", 14)]
    for i, (_, w) in enumerate(cols):
        ws.set_column(i, i, w)
    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(cols) - 1, "Customers", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(cols) - 1,
                   "Your customer database. The last four columns calculate themselves from the Sales sheet.",
                   wb.fmt("subtitle"))
    H = 3
    for i, (h, _) in enumerate(cols):
        ws.write(H, i, h, wb.fmt("th" if i < 9 else "th_num"))
    ws.set_row(H, 30)

    for r, c in enumerate(S.CUSTOMERS):
        row = H + 1 + r
        n = row + 1
        ws.write_string(row, 0, c["id"], wb.fmt("in_txt"))
        ws.write_string(row, 1, c["name"], wb.fmt("in_txt"))
        ws.write_string(row, 2, c["contact"], wb.fmt("in_txt"))
        ws.write_string(row, 3, c["email"], wb.fmt("in_txt"))
        ws.write_string(row, 4, c["phone"], wb.fmt("in_txt"))
        ws.write_string(row, 5, c["city"], wb.fmt("in_txt"))
        ws.write_string(row, 6, c["country"], wb.fmt("in_txt"))
        ws.write_string(row, 7, c["type"], wb.fmt("in_txt"))
        ws.write_number(row, 8, c["credit_limit"], wb.fmt("in_money"))
        ws.write_datetime(row, 9, dt.datetime.combine(c["since"], dt.time()),
                          wb.fmt("in_date"))
        ws.write_formula(row, 10, f'=COUNTIF(Sales!$C$5:$C${LAST_DATA_ROW + 1},$A{n})',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row, 11, f'=SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","E")})',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 12,
                         f'=SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","E")})'
                         f'-SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","L")})',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 13,
                         f'=IFERROR(MAXIFS({rng("SalesData","B")},{rng("SalesData","C")},$A{n}),"")',
                         wb.fmt("fx_date"), "")
        ws.write_formula(row, 14,
                         f'=IF($A{n}="","",IF(M{n}>0,"Balance due","Up to date"))',
                         wb.fmt("fx_txt"), "")

    # blank rows
    first_blank = H + 1 + len(S.CUSTOMERS)
    last_row = 300 + H - 1
    for row in range(first_blank, last_row + 1):
        n = row + 1
        for col in range(10):
            style = "in_money" if col == 8 else ("in_date" if col == 9 else "in_txt")
            ws.write_blank(row, col, None, wb.fmt(style))
        ws.write_formula(row, 10, f'=IF($A{n}="","",COUNTIF(Sales!$C$5:$C${LAST_DATA_ROW + 1},$A{n}))', wb.fmt("fx_num"), "")
        ws.write_formula(row, 11, f'=IF($A{n}="","",SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","E")}))', wb.fmt("fx_money"), "")
        ws.write_formula(row, 12, f'=IF($A{n}="","",SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","E")})-SUMIF({rng("SalesData","C")},$A{n},{rng("SalesData","L")}))', wb.fmt("fx_money"), "")
        ws.write_formula(row, 13, f'=IF($A{n}="","",IFERROR(MAXIFS({rng("SalesData","B")},{rng("SalesData","C")},$A{n}),""))', wb.fmt("fx_date"), "")
        ws.write_formula(row, 14, f'=IF($A{n}="","",IF(M{n}>0,"Balance due","Up to date"))', wb.fmt("fx_txt"), "")

    ws.data_validation(H + 1, 7, last_row, 7, {"validate": "list",
                                               "source": "='Settings'!$K$2:$K$3"})
    ws.conditional_format(f"O{H+2}:O{last_row+1}",
                          {"type": "text", "criteria": "containing",
                           "value": "Balance due", "format": wb.fmt("pill_low")})
    ws.conditional_format(f"M{H+2}:M{last_row+1}",
                          {"type": "cell", "criteria": ">", "value": 0,
                           "format": wb.fmt("fx_money")})
    ws.freeze_panes(H + 1, 2)
    ws.autofilter(H, 0, last_row, len(cols) - 1)
    ws.set_landscape()
    ws.repeat_rows(H, H)
    wb.nav_row(name, len(cols), name)
    return ws


# ---------------------------------------------------------------------------
# Suppliers
# ---------------------------------------------------------------------------
def build_suppliers(wb):
    name = SH_SUP
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    cols = [("Supplier ID", 13), ("Supplier Name", 28), ("Contact Person", 18),
            ("Email", 30), ("Phone", 18), ("City", 14), ("Country", 18),
            ("Payment Terms", 14), ("Lead Time (days)", 12), ("Status", 12),
            ("Orders", 9), ("Total Purchased", 15), ("Last Order", 12)]
    for i, (_, w) in enumerate(cols):
        ws.set_column(i, i, w)
    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(cols) - 1, "Suppliers", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(cols) - 1,
                   "Who you buy from. Order counts and spend are calculated from the Purchases sheet.",
                   wb.fmt("subtitle"))
    H = 3
    for i, (h, _) in enumerate(cols):
        ws.write(H, i, h, wb.fmt("th" if i < 10 else "th_num"))
    ws.set_row(H, 30)

    for r, s in enumerate(S.SUPPLIERS):
        row = H + 1 + r
        n = row + 1
        ws.write_string(row, 0, s["id"], wb.fmt("in_txt"))
        ws.write_string(row, 1, s["name"], wb.fmt("in_txt"))
        ws.write_string(row, 2, s["contact"], wb.fmt("in_txt"))
        ws.write_string(row, 3, s["email"], wb.fmt("in_txt"))
        ws.write_string(row, 4, s["phone"], wb.fmt("in_txt"))
        ws.write_string(row, 5, s["city"], wb.fmt("in_txt"))
        ws.write_string(row, 6, s["country"], wb.fmt("in_txt"))
        ws.write_string(row, 7, s["terms"], wb.fmt("in_txt"))
        ws.write_number(row, 8, s["lead_time"], wb.fmt("in_num"))
        ws.write_string(row, 9, s["status"], wb.fmt("in_txt"))
        ws.write_formula(row, 10, f'=COUNTIF(Purchases!$C$5:$C${LAST_DATA_ROW + 1},$A{n})',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row, 11,
                         f'=SUMIF({rng("PurchaseData","E")},$A{n},{rng("PurchaseData","H")})',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 12,
                         f'=IFERROR(MAXIFS({rng("PurchaseData","B")},{rng("PurchaseData","E")},$A{n}),"")',
                         wb.fmt("fx_date"), "")

    first_blank = H + 1 + len(S.SUPPLIERS)
    last_row = 120 + H - 1
    for row in range(first_blank, last_row + 1):
        n = row + 1
        for col in range(10):
            style = "in_num" if col == 8 else "in_txt"
            ws.write_blank(row, col, None, wb.fmt(style))
        ws.write_formula(row, 10, f'=IF($A{n}="","",COUNTIF(Purchases!$C$5:$C${LAST_DATA_ROW + 1},$A{n}))', wb.fmt("fx_num"), "")
        ws.write_formula(row, 11, f'=IF($A{n}="","",SUMIF({rng("PurchaseData","E")},$A{n},{rng("PurchaseData","H")}))', wb.fmt("fx_money"), "")
        ws.write_formula(row, 12, f'=IF($A{n}="","",IFERROR(MAXIFS({rng("PurchaseData","B")},{rng("PurchaseData","E")},$A{n}),""))', wb.fmt("fx_date"), "")

    ws.data_validation(H + 1, 7, last_row, 7, {"validate": "list",
                                               "source": "='Settings'!$F$2:$F$5"})
    ws.data_validation(H + 1, 9, last_row, 9, {"validate": "list",
                                               "source": "='Settings'!$H$2:$H$4"})
    ws.conditional_format(f"J{H+2}:J{last_row+1}",
                          {"type": "text", "criteria": "containing",
                           "value": "On hold", "format": wb.fmt("pill_low")})
    ws.freeze_panes(H + 1, 2)
    ws.autofilter(H, 0, last_row, len(cols) - 1)
    ws.set_landscape()
    wb.nav_row(name, len(cols), name)
    return ws


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
def build_settings(wb):
    """
    Settings layout (columns A..N):
        B:C  business profile         D:E  product categories
        F    payment terms            G    statuses         H  customer types
        J    expense categories       K    payment methods  L  payment status
    """
    name = SH_SET
    ws = wb.ws[name]
    ws.hide_gridlines(2)

    widths = {"A": 2.5, "B": 24, "C": 22, "D": 3, "E": 24, "F": 18,
              "G": 16, "H": 18, "I": 3, "J": 22, "K": 20, "L": 20, "M": 22}
    for col, w in widths.items():
        ws.set_column(f"{col}:{col}", w)

    ws.set_row(0, 40)
    ws.merge_range("B1:L1", "", wb.fmt("title"))
    ws.write("B1", "Settings", wb.fmt("title"))
    ws.merge_range("B2:L2",
                   "Business details, currency, tax and every dropdown list used in the workbook.",
                   wb.fmt("subtitle"))

    def panel(row, c1, c2, title):
        ws.merge_range(row, c1, row, c2, title, wb.fmt("band"))

    # ---- business profile (rows 5-12) ----
    panel(4, 1, 2, "Business profile")
    details = [
        ("Business name", "string", S.BUSINESS["name"]),
        ("Currency code", "string", S.BUSINESS["currency"]),
        ("Currency symbol", "string", "$"),
        ("Tax rate", "number", 0.09),
        ("Fiscal year starts", "string", "January"),
        ("Low stock default", "number", S.BUSINESS["low_stock_default"]),
        ("Data as of", "date", dt.datetime(2026, 8, 31)),
        ("Owner", "string", "Pouria Asghari"),
    ]
    for i, (label, kind, value) in enumerate(details):
        r = 5 + i
        ws.write(r, 1, label, wb.fmt("body"))
        if kind == "date":
            ws.write_datetime(r, 2, value, wb.fmt("in_date"))
        elif kind == "number":
            pct = label.startswith("Tax rate")
            ws.write_number(r, 2, value,
                            wb.pct_format() if pct else wb.fmt("in_num"))
        else:
            ws.write_string(r, 2, value, wb.fmt("in_txt"))

    # ---- product categories (rows 5-34, col E) ----
    panel(4, 4, 4, "Product categories")
    for i, cat in enumerate(S.CATEGORIES):
        ws.write(5 + i, 4, cat, wb.fmt("in_txt"))
    for i in range(len(S.CATEGORIES), 30):
        ws.write_blank(5 + i, 4, None, wb.fmt("in_txt"))

    # ---- small lists (row 4 headers, values from row 5) ----
    panel(4, 5, 5, "Payment terms")
    for i, t in enumerate(["Net 7", "Net 14", "Net 21", "Net 30", "Net 45", "Prepaid"]):
        ws.write(5 + i, 5, t, wb.fmt("in_txt"))
    panel(4, 6, 6, "Supplier status")
    for i, t in enumerate(["Active", "On hold", "Inactive"]):
        ws.write(5 + i, 6, t, wb.fmt("in_txt"))
    panel(4, 7, 7, "Customer types")
    for i, t in enumerate(["Retail", "Wholesale"]):
        ws.write(5 + i, 7, t, wb.fmt("in_txt"))

    # ---- right-hand column group ----
    panel(4, 9, 9, "Expense categories")
    for i, t in enumerate(S.EXPENSE_CATEGORIES):
        ws.write(5 + i, 9, t, wb.fmt("in_txt"))
    for i in range(len(S.EXPENSE_CATEGORIES), 20):
        ws.write_blank(5 + i, 9, None, wb.fmt("in_txt"))
    panel(4, 10, 10, "Payment methods")
    for i, t in enumerate(S.PAYMENT_METHODS):
        ws.write(5 + i, 10, t, wb.fmt("in_txt"))
    panel(4, 11, 11, "Payment status")
    for i, t in enumerate(["Paid", "Part paid", "Unpaid"]):
        ws.write(5 + i, 11, t, wb.fmt("in_txt"))
    panel(4, 12, 12, "Currencies")
    for i, t in enumerate(["USD", "EUR", "GBP", "AED", "SEK"]):
        ws.write(5 + i, 12, t, wb.fmt("in_txt"))

    # ---- how it works ----
    ws.merge_range(36, 1, 36, 7, "How this workbook works", wb.fmt("band"))
    guide = (
        "1.  Enter your products on the Products sheet — one row per product.\n"
        "2.  Record every delivery on the Purchases sheet.\n"
        "3.  Record every invoice on the Sales sheet. Stock, profit and the dashboard update themselves.\n"
        "4.  The Inventory sheet shows what is left and what to reorder.\n"
        "5.  Dashboard and Reports need no input at all.\n\n"
        "Amber-bordered cells accept typing. Grey cells contain formulas and are locked so they cannot be "
        "overwritten by accident. To unlock a sheet choose Review > Unprotect Sheet (there is no password). "
        "Formulas use normal ranges (for example SalesData!$E$2:$E$1501), so you can copy a row down and the "
        "new record is counted immediately."
    )
    ws.merge_range(37, 1, 48, 7, guide, wb.fmt("note_box"))

    # ---- what each hidden sheet is ----
    ws.merge_range(36, 9, 36, 12, "Sheets behind the scenes", wb.fmt("band"))
    behind = [
        ("SalesData", "One row per invoice line — the quantities behind each invoice."),
        ("PurchaseData", "One row per purchase line — the quantities behind each PO."),
        ("Lists", "Dropdown source lists."),
        ("", ""),
        ("Changing a product price does not rewrite history:", "existing sale lines keep the price they sold at."),
    ]
    for i, (a, b) in enumerate(behind):
        ws.merge_range(37 + i, 9, 37 + i, 12, f"{a}  {b}".strip(), wb.fmt("note"))
        ws.set_row(37 + i, 30)

    ws.set_landscape()
    wb.nav_row(name, 12, name)
    return ws
