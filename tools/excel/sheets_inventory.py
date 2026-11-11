"""Inventory sheet — derived entirely from Products, Purchases and Sales."""

from __future__ import annotations

from theme import *          # noqa: F401,F403
import sample_data as S
from build_workbook import SH_INV, SH_PROD, PRODUCT_ROWS, rng

# The Inventory sheet mirrors the product master but adds operational columns.
INV_COLS = [
    ("Product ID", 12), ("Product Name", 34), ("Category", 19),
    ("Supplier", 26), ("On Hand", 10), ("Min Level", 10),
    ("Reorder Qty", 12), ("Cost Price", 12), ("Stock Value", 13),
    ("Retail Value", 13), ("Status", 15), ("Action", 26),
]


def build_inventory(wb):
    name = SH_INV
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    for i, (_, w) in enumerate(INV_COLS):
        ws.set_column(i, i, w)
    ws.set_row(0, 34)
    ws.merge_range(0, 0, 0, len(INV_COLS) - 1, "Inventory", wb.fmt("title"))
    ws.merge_range(1, 0, 1, len(INV_COLS) - 1,
                   "Live stock position. Nothing on this sheet is typed — it all follows from Products, "
                   "Purchases and Sales.", wb.fmt("subtitle"))

    # summary strip
    # summary strip: labels in row 3, values in row 4 (so both are readable)
    ws.write(3, 0, "SKUs tracked", wb.fmt("kpi_label"))
    ws.write(3, 2, "Low / out of stock", wb.fmt("kpi_label"))
    ws.write(3, 4, "Inventory value", wb.fmt("kpi_label"))
    ws.write(3, 6, "Retail value", wb.fmt("kpi_label"))
    ws.set_row(3, 18)
    ws.set_row(4, 30)
    ws.write_formula(4, 0, f'=COUNTA({SH_PROD}!$A$5:$A${PRODUCT_ROWS + 4})',
                     wb.fmt("kpi_value_int"), 0)
    ws.write_formula(4, 2, f'=COUNTIF({SH_PROD}!$N$5:$N${PRODUCT_ROWS + 4},"Low stock")'
                           f'+COUNTIF({SH_PROD}!$N$5:$N${PRODUCT_ROWS + 4},"Out of stock")',
                     wb.fmt("kpi_value_amber"), 0)
    ws.write_formula(4, 4, f'=SUM({SH_PROD}!$M$5:$M${PRODUCT_ROWS + 4})',
                     wb.fmt("kpi_value"), 0)
    ws.write_formula(4, 6, f'=SUMPRODUCT({SH_PROD}!$L$5:$L${PRODUCT_ROWS + 4},{SH_PROD}!$G$5:$G${PRODUCT_ROWS + 4})',
                     wb.fmt("kpi_value_plain"), 0)

    H = 5
    ws.set_row(H, 30)
    for i, (h, _) in enumerate(INV_COLS):
        style = "th_num" if i >= 4 else "th"
        ws.write(H, i, h, wb.fmt(style))

    # one row per product master row (blank master rows stay blank here)
    for r in range(PRODUCT_ROWS):
        row = H + 1 + r
        pn = 5 + r                     # matching Products row
        n = row + 1
        ws.write_formula(row, 0, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$A${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 1, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$B${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 2, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$C${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 3, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$E${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(row, 4, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$L${pn})',
                         wb.fmt("fx_num"), "")
        ws.write_formula(row, 5, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$H${pn})',
                         wb.fmt("fx_num"), "")
        # reorder qty: bring stock back to twice the minimum
        ws.write_formula(row, 6,
                         f'=IF({SH_PROD}!$A${pn}="","",MAX(0,{SH_PROD}!$H${pn}*2-{SH_PROD}!$L${pn}))',
                         wb.fmt("fx_num"), "")
        ws.write_formula(row, 7, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$F${pn})',
                         wb.fmt("fx_money"), "")
        ws.write_formula(row, 8, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$M${pn})',
                         wb.fmt("fx_money"), "")
        # retail value = on hand * selling price
        ws.write_formula(row, 9,
                         f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$L${pn}*{SH_PROD}!$G${pn})',
                         wb.fmt("fx_money"), "")
        ws.write_formula(row, 10, f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$N${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(
            row, 11,
            f'=IF({SH_PROD}!$A${pn}="","",'
            f'IF(E{n}<=0,"Order now — out of stock",'
            f'IF(E{n}<=F{n},"Reorder "&G{n}&" units","Sufficient")))',
            wb.fmt("fx_txt"), "")

    last = H + PRODUCT_ROWS
    for text, style in (("Out of stock", "pill_out"), ("Low stock", "pill_low"),
                        ("In stock", "pill_ok")):
        ws.conditional_format(f"K{H+2}:K{last}", {
            "type": "text", "criteria": "containing", "value": text,
            "format": wb.fmt(style)})
    ws.conditional_format(f"L{H+2}:L{last}", {
        "type": "text", "criteria": "containing", "value": "Order now",
        "format": wb.fmt("pill_out")})
    ws.conditional_format(f"L{H+2}:L{last}", {
        "type": "text", "criteria": "containing", "value": "Reorder",
        "format": wb.fmt("pill_low")})

    ws.freeze_panes(H + 1, 2)
    ws.autofilter(H, 0, last, len(INV_COLS) - 1)
    ws.set_landscape()
    ws.repeat_rows(H, H)
    wb.nav_row(name, len(INV_COLS), name)
    return ws
