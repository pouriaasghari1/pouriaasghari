"""
Transaction sheets and their hidden line data.

One sales invoice can contain several products, so the workbook keeps two
layers:

    Sales (visible)      one row per invoice — the form the owner fills in
    SalesData (hidden)   one row per invoice line — the source of quantities

Invoice-level money on the visible sheet is a SUMIF over the matching lines.
Adding a row to the visible sheet makes it appear in the dashboard, inventory
and reports immediately, because every one of those reads the same ranges.
"""

from __future__ import annotations

import datetime as dt

from theme import *          # noqa: F401,F403
import sample_data as S
from build_workbook import (
    SH_SALES, SH_PURCH, SH_EXP, SH_SD, SH_PD,
    DATA_ROWS, LAST_DATA_ROW, rng,
)

# ---------------------------------------------------------------------------
# Hidden line sheets
# ---------------------------------------------------------------------------
def build_sales_data(wb):
    """
    Columns (must stay in this order — the formulas depend on them):
      A Line ID   B Date      C Customer  D Product  E Line Total  F Invoice
      G Qty       H Unit Price I Discount% J Line No  K Unit Cost   L Amount Paid
    """
    ws = wb.ws[SH_SD]
    ws.hide_gridlines(2)
    headers = ["Line ID", "Date", "Customer ID", "Product ID", "Line Total",
               "Invoice No", "Qty", "Unit Price", "Discount %", "Line",
               "Unit Cost", "Amount Paid"]
    widths = [10, 11, 12, 12, 13, 14, 8, 12, 10, 6, 12, 13]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.set_column(i, i, w)
        ws.write(0, i, h, wb.fmt("th_sys"))
    ws.set_row(0, 22)

    paid_by_invoice = {s["id"]: s["amount_paid"] for s in S.SALES}
    sub_by_invoice = {s["id"]: s["subtotal"] for s in S.SALES}

    for i, ln in enumerate(S.SALE_LINES, start=1):
        row = i
        n = row + 1
        ws.write_string(row, 0, f"SL-{i:05d}", wb.fmt("fx_txt"))
        ws.write_datetime(row, 1, dt.datetime.combine(ln["date"], dt.time()),
                          wb.fmt("fx_date"))
        ws.write_string(row, 2, ln["customer_id"], wb.fmt("fx_txt"))
        ws.write_string(row, 3, ln["product_id"], wb.fmt("fx_txt"))
        # line total is a live formula so a qty/price correction flows through
        ws.write_formula(row, 4, f"=G{n}*H{n}*(1-I{n}/100)", wb.fmt("fx_money"),
                         ln["line_total"])
        ws.write_string(row, 5, ln["invoice_id"], wb.fmt("fx_txt"))
        ws.write_number(row, 6, ln["qty"], wb.fmt("fx_num"))
        ws.write_number(row, 7, ln["unit_price"], wb.fmt("fx_money"))
        ws.write_number(row, 8, ln["discount_pct"], wb.fmt("fx_num"))
        ws.write_number(row, 9, ln["line"], wb.fmt("fx_num"))
        ws.write_number(row, 10, ln["unit_cost"], wb.fmt("fx_money"))
        share = (ln["line_total"] / sub_by_invoice[ln["invoice_id"]]
                 if sub_by_invoice[ln["invoice_id"]] else 0)
        ws.write_number(row, 11, round(paid_by_invoice[ln["invoice_id"]] * share, 2),
                        wb.fmt("fx_money"))
    return ws


def build_purchase_data(wb):
    """
    Columns:
      A Line ID  B Date  C Product ID  D Supplier ID  E PO No
      F Qty      G Unit Cost  H Line Total  I Line No
    """
    ws = wb.ws[SH_PD]
    ws.hide_gridlines(2)
    headers = ["Line ID", "Date", "Product ID", "Supplier ID", "PO No",
               "Qty", "Unit Cost", "Line Total", "Line"]
    widths = [10, 11, 12, 12, 14, 8, 12, 13, 6]
    for i, (h, w) in enumerate(zip(headers, widths)):
        ws.set_column(i, i, w)
        ws.write(0, i, h, wb.fmt("th_sys"))
    ws.set_row(0, 22)

    for i, ln in enumerate(S.PURCHASE_LINES, start=1):
        row = i
        n = row + 1
        ws.write_string(row, 0, f"PL-{i:05d}", wb.fmt("fx_txt"))
        ws.write_datetime(row, 1, dt.datetime.combine(ln["date"], dt.time()),
                          wb.fmt("fx_date"))
        ws.write_string(row, 2, ln["product_id"], wb.fmt("fx_txt"))
        ws.write_string(row, 3, ln["supplier_id"], wb.fmt("fx_txt"))
        ws.write_string(row, 4, ln["purchase_id"], wb.fmt("fx_txt"))
        ws.write_number(row, 5, ln["qty"], wb.fmt("fx_num"))
        ws.write_number(row, 6, ln["unit_cost"], wb.fmt("fx_money"))
        ws.write_formula(row, 7, f"=F{n}*G{n}", wb.fmt("fx_money"), ln["line_total"])
        ws.write_number(row, 8, ln["line"], wb.fmt("fx_num"))
    return ws


# ---------------------------------------------------------------------------
# Sales — invoice form
# ---------------------------------------------------------------------------
def build_sales(wb):
    name = SH_SALES
    ws = wb.ws[name]
    ws.hide_gridlines(2)

    # A invoice  B date  C customer  D items  E subtotal  F tax  G total
    # H paid     I balance  J status  K due date  L days overdue  M profit  N margin
    cols = [
        ("Invoice No", 15, "th"), ("Date", 11, "th"), ("Customer", 30, "th"),
        ("Items", 7, "th_num"), ("Subtotal", 13, "th_num"), ("Tax", 11, "th_num"),
        ("Invoice Total", 14, "th_num"), ("Paid", 12, "th_num"),
        ("Balance", 12, "th_num"), ("Payment Status", 14, "th_num"),
        ("Due Date", 12, "th_num"), ("Days Overdue", 12, "th_num"),
        ("Profit", 12, "th_num"), ("Margin", 9, "th_num"),
    ]
    for i, (_, w, _) in enumerate(cols):
        ws.set_column(i, i, w)

    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(cols) - 1, "Sales", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(cols) - 1,
                   "One row per invoice. Enter the invoice number, date, customer and what was sold — "
                   "subtotal, tax, profit and payment status all calculate themselves.",
                   wb.fmt("subtitle"))

    H = 3
    ws.set_row(H, 32)
    for i, (h, _, style) in enumerate(cols):
        ws.write(H, i, h, wb.fmt(style))

    def formulas(row, n, invoice_total_hint=None):
        ws.write_formula(row, 3, f'=IF($A{n}="","",COUNTIF({rng("SalesData","F")},$A{n}))',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row, 4, f'=IF($A{n}="","",SUMIF({rng("SalesData","F")},$A{n},{rng("SalesData","E")}))',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 5, f'=IF($A{n}="","",E{n}*TaxRate)', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 6, f'=IF($A{n}="","",E{n}+F{n})', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 7, f'=IF($A{n}="","",SUMIF({rng("SalesData","F")},$A{n},{rng("SalesData","L")}))',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 8, f'=IF($A{n}="","",G{n}-H{n})', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 9,
                         f'=IF($A{n}="","",IF(H{n}<=0,"Unpaid",IF(I{n}<=0.01,"Paid","Part paid")))',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 10, f'=IF($A{n}="","",B{n}+30)', wb.fmt("fx_date"), "")
        ws.write_formula(row, 11,
                         f'=IF($A{n}="","",IF(I{n}>0.01,MAX(0,TODAY()-K{n}),0))',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(
            row, 12,
            f'=IF($A{n}="","",'
            f'SUMIF({rng("SalesData","F")},$A{n},{rng("SalesData","E")})'
            f'-SUMPRODUCT(({rng("SalesData","F")}=$A{n})*{rng("SalesData","G")}*{rng("SalesData","K")}))',
            wb.fmt("fx_money"), 0)
        ws.write_formula(row, 13, f'=IFERROR(IF($A{n}="","",M{n}/E{n}),"")',
                         wb.fmt("fx_num"), 0)

    # ---- filled sample invoices ---------------------------------------
    for r, inv in enumerate(S.SALES):
        row = H + 1 + r
        n = row + 1
        ws.write_string(row, 0, inv["id"], wb.fmt("in_txt"))
        ws.write_datetime(row, 1, dt.datetime.combine(inv["date"], dt.time()),
                          wb.fmt("in_date"))
        ws.write_string(row, 2, inv["customer_id"], wb.fmt("in_txt"))
        formulas(row, n)

    # ---- blank rows ready for new invoices ----------------------------
    first_blank = H + 1 + len(S.SALES)
    for row in range(first_blank, LAST_DATA_ROW):
        n = row + 1
        ws.write_blank(row, 0, None, wb.fmt("in_txt"))
        ws.write_blank(row, 1, None, wb.fmt("in_date"))
        ws.write_blank(row, 2, None, wb.fmt("in_txt"))
        formulas(row, n)

    last = LAST_DATA_ROW
    # dropdowns: customers come from the Customers sheet so names stay canonical
    ws.data_validation(H + 1, 2, last - 1, 2, {
        "validate": "list",
        "source": f"='Customers'!$A$5:$A$300",
        "input_title": "Customer",
        "input_message": "Pick a customer ID. Add new customers on the Customers sheet first.",
        "error_title": "Unknown customer",
        "error_message": "Choose a customer that exists on the Customers sheet.",
    })
    ws.data_validation(H + 1, 1, last - 1, 1, {
        "validate": "date", "criteria": ">=", "value": dt.date(2000, 1, 1),
        "error_title": "Check the date",
        "error_message": "Enter a real invoice date (dd/mm/yyyy).",
    })
    ws.data_validation(H + 1, 0, last - 1, 0, {
        "validate": "custom",
        "value": f'=COUNTIF($A$4:$A${last},$A5)<=1',
        "error_title": "Duplicate invoice",
        "error_message": "This invoice number is already used.",
    })
    # conditional formatting on payment status
    for text, style in (("Paid", "pill_ok"), ("Part paid", "pill_low"),
                        ("Unpaid", "pill_out")):
        ws.conditional_format(f"J{H+2}:J{last}", {
            "type": "text", "criteria": "containing", "value": text,
            "format": wb.fmt(style)})
    # overdue rows turn red on the days-overdue column
    ws.conditional_format(f"L{H+2}:L{last}", {
        "type": "cell", "criteria": ">", "value": 0,
        "format": wb.fmt("kpi_value_r")})

    ws.freeze_panes(H + 1, 3)
    ws.autofilter(H, 0, last - 1, len(cols) - 1)
    ws.set_landscape()
    ws.repeat_rows(H, H)
    wb.nav_row(name, len(cols), name)
    return ws


# ---------------------------------------------------------------------------
# Purchases — delivery form
# ---------------------------------------------------------------------------
def build_purchases(wb):
    name = SH_PURCH
    ws = wb.ws[name]
    ws.hide_gridlines(2)

    # A po  B date  C supplier  D items  E subtotal  F tax  G total  H status  I lead days
    cols = [
        ("PO Number", 15, "th"), ("Date", 11, "th"), ("Supplier", 30, "th"),
        ("Items", 7, "th_num"), ("Subtotal", 13, "th_num"), ("Tax", 11, "th_num"),
        ("PO Total", 14, "th_num"), ("Payment Status", 14, "th_num"),
        ("Balance", 12, "th_num"),
    ]
    for i, (_, w, _) in enumerate(cols):
        ws.set_column(i, i, w)

    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(cols) - 1, "Purchases", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(cols) - 1,
                   "Every delivery you receive. Recording a purchase raises stock automatically on the "
                   "Products and Inventory sheets.", wb.fmt("subtitle"))
    H = 3
    ws.set_row(H, 32)
    for i, (h, _, style) in enumerate(cols):
        ws.write(H, i, h, wb.fmt(style))

    def formulas(row, n):
        ws.write_formula(row, 3, f'=IF($A{n}="","",COUNTIF({rng("PurchaseData","E")},$A{n}))',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row, 4, f'=IF($A{n}="","",SUMIF({rng("PurchaseData","E")},$A{n},{rng("PurchaseData","H")}))',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 5, f'=IF($A{n}="","",E{n}*TaxRate)', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 6, f'=IF($A{n}="","",E{n}+F{n})', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 7, f'=IF($A{n}="","",IF(G{n}>0,"Unpaid","Paid"))',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 8, f'=IF($A{n}="","",G{n})', wb.fmt("fx_money"), 0)

    for r, po in enumerate(S.PURCHASES):
        row = H + 1 + r
        n = row + 1
        ws.write_string(row, 0, po["id"], wb.fmt("in_txt"))
        ws.write_datetime(row, 1, dt.datetime.combine(po["date"], dt.time()),
                          wb.fmt("in_date"))
        ws.write_string(row, 2, po["supplier_id"], wb.fmt("in_txt"))
        formulas(row, n)
        # purchases recorded as already paid carry their PO total as paid
        if po["status"] == "Paid":
            ws.write_formula(row, 6, f'=IF($A{n}="","",E{n}+F{n})', wb.fmt("fx_money"), 0)

    first_blank = H + 1 + len(S.PURCHASES)
    for row in range(first_blank, LAST_DATA_ROW):
        n = row + 1
        ws.write_blank(row, 0, None, wb.fmt("in_txt"))
        ws.write_blank(row, 1, None, wb.fmt("in_date"))
        ws.write_blank(row, 2, None, wb.fmt("in_txt"))
        formulas(row, n)

    last = LAST_DATA_ROW
    ws.data_validation(H + 1, 2, last - 1, 2, {
        "validate": "list",
        "source": f"='Suppliers'!$A$5:$A$120",
        "input_title": "Supplier",
        "input_message": "Pick a supplier ID from the Suppliers sheet.",
        "error_title": "Unknown supplier",
        "error_message": "Choose a supplier that exists on the Suppliers sheet.",
    })
    ws.data_validation(H + 1, 1, last - 1, 1, {
        "validate": "date", "criteria": ">=", "value": dt.date(2000, 1, 1),
        "error_title": "Check the date",
        "error_message": "Enter a real delivery date.",
    })
    ws.freeze_panes(H + 1, 3)
    ws.autofilter(H, 0, last - 1, len(cols) - 1)
    ws.set_landscape()
    ws.repeat_rows(H, H)
    wb.nav_row(name, len(cols), name)
    return ws


# ---------------------------------------------------------------------------
# Expenses
# ---------------------------------------------------------------------------
def build_expenses(wb):
    name = SH_EXP
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    cols = [
        ("Date", 11, "th"), ("Category", 16, "th"), ("Description", 36, "th"),
        ("Paid To", 24, "th"), ("Amount", 13, "th_num"), ("Tax", 11, "th_num"),
        ("Total", 13, "th_num"), ("Method", 14, "th_num"),
        ("Tax Deductible", 14, "th_num"), ("Month", 13, "th_num"),
    ]
    for i, (_, w, _) in enumerate(cols):
        ws.set_column(i, i, w)
    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(cols) - 1, "Expenses", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(cols) - 1,
                   "Operating costs by category and date. These feed the Reports sheet and reduce net profit.",
                   wb.fmt("subtitle"))
    H = 3
    ws.set_row(H, 32)
    for i, (h, _, style) in enumerate(cols):
        ws.write(H, i, h, wb.fmt(style))

    for r, e in enumerate(S.EXPENSE_ROWS):
        off, cat, desc, payee, amount, method, deductible = e
        row = H + 1 + r
        n = row + 1
        date = S.AS_OF - dt.timedelta(days=off)
        ws.write_datetime(row, 0, dt.datetime.combine(date, dt.time()),
                          wb.fmt("in_date"))
        ws.write_string(row, 1, cat, wb.fmt("in_txt"))
        ws.write_string(row, 2, desc, wb.fmt("in_txt"))
        ws.write_string(row, 3, payee, wb.fmt("in_txt"))
        ws.write_number(row, 4, amount, wb.fmt("in_money"))
        ws.write_formula(row, 5, f'=E{n}*TaxRate', wb.fmt("fx_money"), 0)
        ws.write_formula(row, 6, f'=E{n}+F{n}', wb.fmt("fx_money"), 0)
        ws.write_string(row, 7, method, wb.fmt("in_txt"))
        ws.write_string(row, 8, deductible, wb.fmt("in_txt"))
        ws.write_formula(row, 9, f'=IF($A{n}="","",TEXT($A{n},"mmm yyyy"))',
                         wb.fmt("fx_txt"), "")

    first_blank = H + 1 + len(S.EXPENSE_ROWS)
    last_row = 600 + H
    for row in range(first_blank, last_row):
        n = row + 1
        ws.write_blank(row, 0, None, wb.fmt("in_date"))
        for c in (1, 2, 3):
            ws.write_blank(row, c, None, wb.fmt("in_txt"))
        ws.write_blank(row, 4, None, wb.fmt("in_money"))
        ws.write_formula(row, 5, f'=IF($A{n}="","",E{n}*TaxRate)', wb.fmt("fx_money"), "")
        ws.write_formula(row, 6, f'=IF($A{n}="","",E{n}+F{n})', wb.fmt("fx_money"), "")
        ws.write_blank(row, 7, None, wb.fmt("in_txt"))
        ws.write_blank(row, 8, None, wb.fmt("in_txt"))
        ws.write_formula(row, 9, f'=IF($A{n}="","",TEXT($A{n},"mmm yyyy"))', wb.fmt("fx_txt"), "")

    last = last_row
    ws.data_validation(H + 1, 1, last - 1, 1, {
        "validate": "list",
        "source": f"='Settings'!$J$6:$J${6 + len(S.EXPENSE_CATEGORIES) + 15}",
        "error_title": "Pick a category",
        "error_message": "Choose an expense category from the Settings list.",
    })
    ws.data_validation(H + 1, 7, last - 1, 7, {
        "validate": "list",
        "source": f"='Settings'!$K$6:$K${6 + len(S.PAYMENT_METHODS)}",
    })
    ws.data_validation(H + 1, 8, last - 1, 8, {
        "validate": "list", "source": "='Settings'!$K$2:$K$3"})
    ws.data_validation(H + 1, 4, last - 1, 4, {
        "validate": "decimal", "criteria": ">", "value": 0,
        "error_title": "Amount", "error_message": "Expenses must be a positive amount."})
    ws.conditional_format(f"E{H+2}:E{last}", {
        "type": "cell", "criteria": ">=", "value": 500,
        "format": wb.fmt("fx_money")})
    ws.freeze_panes(H + 1, 2)
    ws.autofilter(H, 0, last - 1, len(cols) - 1)
    ws.set_landscape()
    ws.repeat_rows(H, H)
    wb.nav_row(name, len(cols), name)
    return ws
