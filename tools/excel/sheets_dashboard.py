"""
Dashboard and Reports.

Dashboard layout (columns A..N, each KPI card is 2 columns wide):

    row 5   KPI labels        row 6  values        row 7  footers
    row 9   KPI labels        row 10 values        row 11 footers
    row 13  KPI labels        row 14 values        row 15 footers
    row 17+ monthly chart              row 17+ top products
    row 32+ recent invoices            row 32+ reorder list

Every value is a formula over the data ranges; nothing is hard-coded. Ranking
uses a hidden helper block (a revenue + ROW()/100000 key) so ties never
collapse two products into one row.
"""

from __future__ import annotations

from theme import *          # noqa: F401,F403
import sample_data as S
from build_workbook import (
    SH_DASH, SH_REP, SH_SALES, SH_PROD,
    PRODUCT_ROWS, LAST_DATA_ROW,
)

MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

SALES_LAST = 1501          # last usable row of SalesData
PURCH_LAST = 1501
EXP_LAST = 600


def _kpi(ws, wb, row, col1, col2, label, formula, value_style, foot, num_format=None):
    """One KPI card: label / value / footer, merged across two columns."""
    ws.merge_range(row, col1, row, col2, label, wb.fmt("kpi_label"))
    ws.merge_range(row + 1, col1, row + 1, col2, "", wb.fmt(value_style))
    ws.write_formula(row + 1, col1, formula, wb.fmt(value_style), 0)
    ws.merge_range(row + 2, col1, row + 2, col2, foot, wb.fmt("kpi_foot"))


def build_dashboard(wb):
    name = SH_DASH
    ws = wb.ws[name]
    ws.hide_gridlines(2)

    ws.set_column("A:A", 2.5)
    ws.set_column("B:M", 12.5)
    ws.set_column("N:N", 2.5)
    ws.set_column("O:Z", 11)

    # ---------------- title ----------------
    ws.set_row(0, 46)
    ws.merge_range("B2:M2", "", wb.fmt("title"))
    ws.write("B2", "Pouria Business", wb.fmt("title"))
    ws.merge_range("B3:M3",
                   "Smart Inventory & Sales Manager   ·   live management dashboard",
                   wb.fmt("subtitle"))

    # ---------------- KPI grid ----------------
    for r, h in [(5, 20), (6, 34), (7, 17), (9, 20), (10, 34), (11, 17),
                 (13, 20), (14, 34), (15, 17)]:
        ws.set_row(r, h)

    sales_sum = f"SUM(SalesData!$E$2:$E${SALES_LAST})"
    cogs_sum = f"SUMPRODUCT(SalesData!$G$2:$G${SALES_LAST},SalesData!$K$2:$K${SALES_LAST})"
    gross = f"{sales_sum}-{cogs_sum}"
    exp_sum = 'SUMIFS(Expenses!$E$5:$E$600,Expenses!$A$5:$A$600,">0")'
    net = f"{gross}-{exp_sum}"

    # band 1
    _kpi(ws, wb, 5, 1, 2, "TOTAL SALES", f"={sales_sum}", "kpi_value",
         "All invoices, excluding tax")
    _kpi(ws, wb, 5, 3, 4, "GROSS PROFIT", f"={gross}", "kpi_value",
         "Sales less cost of goods sold")
    _kpi(ws, wb, 5, 5, 6, "NET PROFIT", f"={net}", "kpi_value",
         "After operating expenses")
    _kpi(ws, wb, 5, 7, 8, "PURCHASES", f"=SUM(PurchaseData!$H$2:$H${PURCH_LAST})",
         "kpi_value_plain", "Total supplier spend")
    _kpi(ws, wb, 5, 9, 10, "EXPENSES", f"={exp_sum}", "kpi_value_plain",
         "All operating costs")
    _kpi(ws, wb, 5, 11, 12, "INVENTORY VALUE",
         f"=SUM({SH_PROD}!$M$5:$M${PRODUCT_ROWS + 4})", "kpi_value",
         "Stock at cost price")

    # band 2 — counts and receivables
    _kpi(ws, wb, 9, 1, 2, "PRODUCTS",
         f"=COUNTA({SH_PROD}!$A$5:$A${PRODUCT_ROWS + 4})", "kpi_value_int",
         "Active SKUs in the catalogue")
    _kpi(ws, wb, 9, 3, 4, "LOW STOCK",
         f'=COUNTIF({SH_PROD}!$N$5:$N${PRODUCT_ROWS + 4},"Low stock")',
         "kpi_value_amber", "At or below minimum level")
    _kpi(ws, wb, 9, 5, 6, "OUT OF STOCK",
         f'=COUNTIF({SH_PROD}!$N$5:$N${PRODUCT_ROWS + 4},"Out of stock")',
         "kpi_value_r", "Nothing left to sell")
    _kpi(ws, wb, 9, 7, 8, "RECEIVABLES",
         f'=SUM(Sales!$E$5:$E${LAST_DATA_ROW})-SUM(Sales!$H$5:$H${LAST_DATA_ROW})', "kpi_value_plain",
         "Invoiced but not yet paid")
    _kpi(ws, wb, 9, 9, 10, "INVOICES",
         f"=COUNTA(Sales!$A$5:$A${LAST_DATA_ROW - 1})", "kpi_value_int",
         "Sales documents issued")
    _kpi(ws, wb, 9, 11, 12, "AVERAGE INVOICE",
         f"=IFERROR({sales_sum}/COUNTA(Sales!$A$5:$A${LAST_DATA_ROW - 1}),0)",
         "kpi_value_plain", "Mean value per invoice")

    # band 3 — margin and alerts
    _kpi(ws, wb, 13, 1, 2, "GROSS MARGIN",
         f"=IFERROR({gross}/{sales_sum},0)", "kpi_value", "Gross profit as % of sales")
    _kpi(ws, wb, 13, 3, 4, "NET MARGIN",
         f"=IFERROR({net}/{sales_sum},0)", "kpi_value", "Net profit as % of sales")
    _kpi(ws, wb, 13, 5, 6, "STOCK ON HAND",
         f"=SUM({SH_PROD}!$L$5:$L${PRODUCT_ROWS + 4})", "kpi_value_int",
         "Units across all products")
    _kpi(ws, wb, 13, 7, 8, "UNPAID INVOICES",
         f'=COUNTIFS(Sales!$J$5:$J${LAST_DATA_ROW - 1},"<>Paid",'
         f'Sales!$A$5:$A${LAST_DATA_ROW - 1},"<>")',
         "kpi_value_amber", "Awaiting payment")
    _kpi(ws, wb, 13, 9, 10, "PURCHASE ORDERS",
         f"=COUNTA(Purchases!$A$5:$A${LAST_DATA_ROW - 1})", "kpi_value_int",
         "Deliveries recorded")
    _kpi(ws, wb, 13, 11, 12, "EXPENSE ENTRIES",
         f"=COUNTA(Expenses!$A$5:$A${EXP_LAST})", "kpi_value_int",
         "Cost records logged")

    # Percentage-formatted margin cards. Written directly (not through the
    # _kpi helper) so the number format is a real percentage.
    pct_fmt = wb.wb.add_format({
        "num_format": "0.0%", "font_name": FONT, "font_size": 21, "bold": True,
        "font_color": EMERALD, "bg_color": NAVY_700, "align": "left",
        "left": 1, "right": 1, "left_color": NAVY_500,
        "right_color": NAVY_500,
    })
    ws.write_formula(14, 1, f"=IFERROR(({gross})/({sales_sum}),0)", pct_fmt, 0)
    ws.write_formula(14, 3, f"=IFERROR(({net})/({sales_sum}),0)", pct_fmt, 0)

    # ---------------- charts & lists ----------------
    ws.merge_range("B18:G18", "Monthly sales", wb.fmt("section"))

    # helper block for the monthly series (hidden columns O/P)
    ws.write(18, 14, "Month", wb.fmt("th_sys"))
    ws.write(18, 15, "Sales", wb.fmt("th_sys"))
    for i, m in enumerate(MONTH_ABBR):
        r = 19 + i
        ws.write(r, 14, m, wb.fmt("fx_txt"))
        ws.write_formula(
            r, 15,
            f'=SUMPRODUCT((MONTH(SalesData!$B$2:$B${SALES_LAST})={i + 1})'
            f'*(SalesData!$B$2:$B${SALES_LAST}<>"")*SalesData!$E$2:$E${SALES_LAST})',
            wb.fmt("fx_money"), 0)

    chart = wb.wb.add_chart({"type": "column"})
    chart.add_series({
        "name": "Monthly sales",
        "categories": [SH_DASH, 19, 14, 30, 14],
        "values": [SH_DASH, 19, 15, 30, 15],
        "fill": {"color": EMERALD},
        "border": {"none": True},
        "gap": 40,
    })
    chart.set_title({"name": "Sales by month",
                     "name_font": {"size": 11, "color": WHITE}})
    chart.set_legend({"none": True})
    chart.set_y_axis({"num_format": '"$"#,##0',
                      "major_gridlines": {"visible": True,
                                          "line": {"color": LINE}},
                      "font": {"size": 9, "color": MUTED},
                      "line": {"none": True}})
    chart.set_x_axis({"font": {"size": 9, "color": MUTED},
                      "line": {"color": LINE}})
    chart.set_chartarea({"fill": {"color": NAVY_700}, "border": {"none": True}})
    chart.set_plotarea({"fill": {"none": True}})
    chart.set_size({"width": 520, "height": 280})
    ws.insert_chart("B19", chart, {"x_offset": 4, "y_offset": 2})

    # ---------------- top products ----------------
    ws.merge_range("H18:M18", "Top 5 products by revenue", wb.fmt("section"))
    hdr = {7: "#", 8: "Product", 11: "Revenue", 12: "Units"}
    for col, text in hdr.items():
        pass
    ws.write(18, 7, "Rank", wb.fmt("th_sys"))
    ws.merge_range(18, 8, 18, 10, "Product", wb.fmt("th_sys"))
    ws.write(18, 11, "Revenue", wb.fmt("th_sys"))
    ws.write(18, 12, "Units", wb.fmt("th_sys"))

    # helper: product / revenue / key  (columns Q,R,S)
    hq = 16
    ws.write(17, hq, "Product", wb.fmt("th_sys"))
    ws.write(17, hq + 1, "Revenue", wb.fmt("th_sys"))
    ws.write(17, hq + 2, "Key", wb.fmt("th_sys"))
    for r in range(PRODUCT_ROWS):
        pn = 5 + r
        row0 = 18 + r
        ws.write_formula(row0, hq,
                         f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$B${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(
            row0, hq + 1,
            f'=IF({SH_PROD}!$A${pn}="","",SUMIF(SalesData!$D$2:$D${SALES_LAST},'
            f'{SH_PROD}!$A${pn},SalesData!$E$2:$E${SALES_LAST}))',
            wb.fmt("fx_money"), 0)
        ws.write_formula(row0, hq + 2,
                         f'=IF({SH_PROD}!$A${pn}="","",R{row0+1}+ROW()/100000)',
                         wb.fmt("fx_num"), 0)
    key_first, key_last = 19, 18 + PRODUCT_ROWS
    for i in range(5):
        row = 19 + i
        n = row + 1
        ws.write(row, 7, i + 1, wb.fmt("fx_num"))
        ws.merge_range(row, 8, row, 10, "", wb.fmt("fx_txt"))
        ws.write_formula(
            row, 8,
            f'=IFERROR(INDEX($Q${key_first}:$Q${key_last},'
            f'MATCH(LARGE($S${key_first}:$S${key_last},{i+1}),$S${key_first}:$S${key_last},0)),"")',
            wb.fmt("fx_txt"), "")
        ws.write_formula(
            row, 11,
            f'=IFERROR(INDEX($R${key_first}:$R${key_last},'
            f'MATCH(LARGE($S${key_first}:$S${key_last},{i+1}),$S${key_first}:$S${key_last},0)),"")',
            wb.fmt("fx_money"), 0)
        ws.write_formula(
            row, 12,
            f'=IFERROR(SUMPRODUCT((SalesData!$D$2:$D${SALES_LAST}=$H{n})*SalesData!$G$2:$G${SALES_LAST}),0)',
            wb.fmt("fx_num"), 0)

    # ---------------- recent invoices ----------------
    # Rank by date rather than "last rows", so the list stays correct whether
    # the data sits in rows 5-104 or 5-900. A tiny ROW()/100000 offset keeps
    # same-day invoices from collapsing into one match.
    ws.merge_range("B33:G33", "Recent invoices", wb.fmt("section"))
    ws.write(33, 1, "Invoice", wb.fmt("th_sys"))
    ws.merge_range(33, 2, 33, 3, "Customer", wb.fmt("th_sys"))
    ws.write(33, 4, "Date", wb.fmt("th_sys"))
    ws.write(33, 5, "Total", wb.fmt("th_sys"))
    ws.write(33, 6, "Status", wb.fmt("th_sys"))

    hz = 25                      # helper block in columns Z, AA
    ws.write(31, hz, "DateKey", wb.fmt("th_sys"))
    for r in range(LAST_DATA_ROW):
        n = 5 + r
        ws.write_formula(
            r + 31, hz,
            f'=IF(Sales!$A${n}="",0,Sales!$B${n}+ROW()/100000)',
            wb.fmt("fx_num"), 0)
    z_first, z_last = 32, 31 + LAST_DATA_ROW

    for i in range(8):
        row = 34 + i
        ws.merge_range(row, 2, row, 3, "", wb.fmt("fx_txt"))
        for col, src_col, style in ((1, "A", "fx_txt"), (2, "C", "fx_txt"),
                                    (4, "B", "fx_date"), (5, "G", "fx_money"),
                                    (6, "J", "fx_txt")):
            ws.write_formula(
                row, col,
                f'=IFERROR(IF(LARGE($Z${z_first}:$Z${z_last},{i+1})=0,"",'
                f'INDEX(Sales!${src_col}$5:${src_col}${LAST_DATA_ROW},'
                f'MATCH(LARGE($Z${z_first}:$Z${z_last},{i+1}),$Z${z_first}:$Z${z_last},0))),"")',
                wb.fmt(style), "")

    # ---------------- reorder list ----------------
    ws.merge_range("H33:M33", "Reorder now", wb.fmt("section"))
    ws.merge_range(33, 7, 33, 9, "Product", wb.fmt("th_sys"))
    ws.write(33, 10, "On hand", wb.fmt("th_sys"))
    ws.write(33, 11, "Minimum", wb.fmt("th_sys"))
    ws.write(33, 12, "Order", wb.fmt("th_sys"))

    # helper: product / need / key  (columns U,V,W)
    hu = 20
    ws.write(32, hu, "Product", wb.fmt("th_sys"))
    ws.write(32, hu + 1, "Need", wb.fmt("th_sys"))
    ws.write(32, hu + 2, "Key", wb.fmt("th_sys"))
    ws.write(32, hu + 3, "On hand", wb.fmt("th_sys"))
    ws.write(32, hu + 4, "Minimum", wb.fmt("th_sys"))
    for r in range(PRODUCT_ROWS):
        pn = 5 + r
        row0 = 33 + r
        ws.write_formula(row0, hu,
                         f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$B${pn})',
                         wb.fmt("fx_txt"), "")
        ws.write_formula(
            row0, hu + 1,
            f'=IF({SH_PROD}!$A${pn}="","",IF({SH_PROD}!$L${pn}<={SH_PROD}!$H${pn},'
            f'MAX(1,{SH_PROD}!$H${pn}*2-{SH_PROD}!$L${pn}),0))',
            wb.fmt("fx_num"), 0)
        ws.write_formula(row0, hu + 2,
                         f'=IF({SH_PROD}!$A${pn}="","",V{row0+1}+ROW()/100000)',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row0, hu + 3,
                         f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$L${pn})',
                         wb.fmt("fx_num"), "")
        ws.write_formula(row0, hu + 4,
                         f'=IF({SH_PROD}!$A${pn}="","",{SH_PROD}!$H${pn})',
                         wb.fmt("fx_num"), "")
    rk_first, rk_last = 34, 33 + PRODUCT_ROWS
    for i in range(6):
        row = 34 + i
        ws.merge_range(row, 7, row, 9, "", wb.fmt("fx_txt"))
        ws.write_formula(
            row, 7,
            f'=IFERROR(INDEX($U${rk_first}:$U${rk_last},MATCH(LARGE($W${rk_first}:$W${rk_last},{i+1}),$W${rk_first}:$W${rk_last},0)),"—")',
            wb.fmt("fx_txt"), "")
        ws.write_formula(
            row, 10,
            f'=IFERROR(INDEX($X${rk_first}:$X${rk_last},MATCH(LARGE($W${rk_first}:$W${rk_last},{i+1}),$W${rk_first}:$W${rk_last},0)),"")',
            wb.fmt("fx_num"), "")
        ws.write_formula(
            row, 11,
            f'=IFERROR(INDEX($Y${rk_first}:$Y${rk_last},MATCH(LARGE($W${rk_first}:$W${rk_last},{i+1}),$W${rk_first}:$W${rk_last},0)),"")',
            wb.fmt("fx_num"), "")
        ws.write_formula(
            row, 12,
            f'=IFERROR(INDEX($V${rk_first}:$V${rk_last},MATCH(LARGE($W${rk_first}:$W${rk_last},{i+1}),$W${rk_first}:$W${rk_last},0)),"")',
            wb.fmt("fx_num"), "")

    # ---------------- conditional formatting ----------------
    for text, style in (("Paid", "pill_ok"), ("Part paid", "pill_low"),
                        ("Unpaid", "pill_out")):
        ws.conditional_format(f"G35:G42", {
            "type": "text", "criteria": "containing", "value": text,
            "format": wb.fmt(style)})
    ws.conditional_format("D10:F10", {"type": "cell", "criteria": ">", "value": 0,
                                      "format": wb.fmt("kpi_value_amber")})
    ws.conditional_format("K36:K41", {"type": "cell", "criteria": ">", "value": 0,
                                      "format": wb.fmt("kpi_value_amber")})

    # group + hide the helper columns
    for col in range(14, 27):
        ws.set_column(col, col, 12, None, {"level": 1, "hidden": True})

    ws.set_tab_color(EMERALD)
    ws.set_landscape()
    ws.set_paper(9)
    ws.fit_to_pages(1, 1)
    ws.activate()
    wb.nav_row(name, 13, name)
    return ws


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
def build_reports(wb):
    name = SH_REP
    ws = wb.ws[name]
    ws.hide_gridlines(2)
    ws.set_column("A:A", 2.5)
    ws.set_column("B:B", 15)
    ws.set_column("C:G", 15)
    ws.set_column("H:H", 2.5)
    ws.set_column("I:I", 15)
    ws.set_column("J:M", 14)

    ws.set_row(0, 44)
    ws.merge_range("B2:M2", "", wb.fmt("title"))
    ws.write("B2", "Reports", wb.fmt("title"))
    ws.merge_range("B3:M3",
                   "Monthly and annual performance, recalculated from the data sheets every time the file opens.",
                   wb.fmt("subtitle"))

    # ---------------- monthly performance ----------------
    ws.merge_range("B5:G5", "Monthly performance", wb.fmt("section"))
    head = ["Month", "Invoices", "Sales", "Cost of goods", "Gross profit",
            "Expenses"]
    for i, h in enumerate(head):
        ws.write(5, 1 + i, h, wb.fmt("th_num" if i else "th"))

    for i, m in enumerate(MONTH_ABBR):
        row = 6 + i
        n = row + 1
        ws.write(row, 1, m, wb.fmt("fx_txt"))
        ws.write_formula(
            row, 2,
            f'=SUMPRODUCT((MONTH(SalesData!$B$2:$B${SALES_LAST})={i + 1})'
            f'*(SalesData!$B$2:$B${SALES_LAST}<>""))',
            wb.fmt("fx_num"), 0)
        ws.write_formula(
            row, 3,
            f'=SUMPRODUCT((MONTH(SalesData!$B$2:$B${SALES_LAST})={i + 1})'
            f'*(SalesData!$B$2:$B${SALES_LAST}<>"")*SalesData!$E$2:$E${SALES_LAST})',
            wb.fmt("fx_money"), 0)
        ws.write_formula(
            row, 4,
            f'=SUMPRODUCT((MONTH(SalesData!$B$2:$B${SALES_LAST})={i + 1})'
            f'*(SalesData!$B$2:$B${SALES_LAST}<>"")*'
            f'SalesData!$G$2:$G${SALES_LAST}*SalesData!$K$2:$K${SALES_LAST})',
            wb.fmt("fx_money"), 0)
        ws.write_formula(row, 5, f'=D{n}-E{n}', wb.fmt("fx_money"), 0)
        ws.write_formula(
            row, 6,
            f'=SUMIFS(Expenses!$E$5:$E${EXP_LAST},'
            f'Expenses!$A$5:$A${EXP_LAST},">="&DATE(2026,{i + 1},1),'
            f'Expenses!$A$5:$A${EXP_LAST},"<"&DATE(2026,{i + 2},1))',
            wb.fmt("fx_money"), 0)

    total_row = 18
    ws.write(total_row, 1, "Total", wb.fmt("band"))
    for col in range(2, 7):
        letter = chr(ord("A") + col)
        ws.write_formula(total_row, col, f'=SUM({letter}7:{letter}18)',
                         wb.fmt("band"), 0)

    # ---------------- chart ----------------
    chart = wb.wb.add_chart({"type": "line"})
    chart.add_series({
        "name": "Sales",
        "categories": [SH_REP, 6, 1, 17, 1],
        "values": [SH_REP, 6, 3, 17, 3],
        "line": {"color": EMERALD, "width": 2.5},
        "marker": {"type": "circle", "size": 4,
                   "fill": {"color": EMERALD}, "border": {"none": True}},
    })
    chart.add_series({
        "name": "Gross profit",
        "categories": [SH_REP, 6, 1, 17, 1],
        "values": [SH_REP, 6, 5, 17, 5],
        "line": {"color": BLUE, "width": 2.5, "dash_type": "dash"},
        "marker": {"type": "circle", "size": 3,
                   "fill": {"color": BLUE}, "border": {"none": True}},
    })
    chart.set_title({"name": "Sales vs gross profit by month",
                     "name_font": {"size": 12, "color": WHITE}})
    chart.set_legend({"position": "bottom", "font": {"size": 9, "color": MUTED}})
    chart.set_y_axis({"num_format": '"$"#,##0',
                      "major_gridlines": {"visible": True,
                                          "line": {"color": LINE}},
                      "font": {"size": 9, "color": MUTED}})
    chart.set_x_axis({"font": {"size": 9, "color": MUTED}})
    chart.set_chartarea({"fill": {"color": NAVY_700}, "border": {"none": True}})
    chart.set_plotarea({"fill": {"none": True}})
    chart.set_size({"width": 620, "height": 300})
    ws.insert_chart("B21", chart, {"x_offset": 4, "y_offset": 4})

    # ---------------- sales by category ----------------
    ws.merge_range("I5:M5", "Sales by category", wb.fmt("section"))
    for i, h in enumerate(["Category", "Revenue", "Units", "Share"]):
        ws.write(5, 8 + i, h, wb.fmt("th_num" if i else "th"))
    cat_first, cat_last = 7, 6 + len(S.CATEGORIES)
    for i, cat in enumerate(S.CATEGORIES):
        row = 6 + i
        n = row + 1
        ws.write(row, 8, cat, wb.fmt("fx_txt"))
        ws.write_formula(
            row, 9,
            f'=SUMPRODUCT(({SH_PROD}!$C$5:$C${PRODUCT_ROWS + 4}=$I{n})*'
            f'SUMIF(SalesData!$D$2:$D${SALES_LAST},{SH_PROD}!$A$5:$A${PRODUCT_ROWS + 4},'
            f'SalesData!$E$2:$E${SALES_LAST}))',
            wb.fmt("fx_money"), 0)
        ws.write_formula(
            row, 10,
            f'=SUMPRODUCT(({SH_PROD}!$C$5:$C${PRODUCT_ROWS + 4}=$I{n})*'
            f'SUMIF(SalesData!$D$2:$D${SALES_LAST},{SH_PROD}!$A$5:$A${PRODUCT_ROWS + 4},'
            f'SalesData!$G$2:$G${SALES_LAST}))',
            wb.fmt("fx_num"), 0)
        ws.write_formula(row, 11, f'=IFERROR(J{n}/SUM($J${cat_first}:$J${cat_last}),0)',
                         wb.fmt("fx_num"), 0)

    # ---------------- expenses by category ----------------
    ws.merge_range("I15:M15", "Expenses by category", wb.fmt("section"))
    for i, h in enumerate(["Category", "Amount", "Entries", "Share"]):
        ws.write(15, 8 + i, h, wb.fmt("th_num" if i else "th"))
    ec_first, ec_last = 17, 16 + len(S.EXPENSE_CATEGORIES)
    for i, cat in enumerate(S.EXPENSE_CATEGORIES):
        row = 16 + i
        n = row + 1
        ws.write(row, 8, cat, wb.fmt("fx_txt"))
        ws.write_formula(row, 9, f'=SUMIF(Expenses!$B$5:$B${EXP_LAST},$I{n},Expenses!$E$5:$E${EXP_LAST})',
                         wb.fmt("fx_money"), 0)
        ws.write_formula(row, 10, f'=COUNTIF(Expenses!$B$5:$B${EXP_LAST},$I{n})',
                         wb.fmt("fx_num"), 0)
        ws.write_formula(row, 11, f'=IFERROR(J{n}/SUM($J${ec_first}:$J${ec_last}),0)',
                         wb.fmt("fx_num"), 0)

    # ---------------- annual summary ----------------
    EXP_SUM = 'SUMIFS(Expenses!$E$5:$E$600,Expenses!$A$5:$A$600,">0")'
    ws.merge_range("B28:G28", "Annual summary", wb.fmt("section"))
    summary = [
        ("Total sales", f"=SUM(SalesData!$E$2:$E${SALES_LAST})", "0"),
        ("Total purchases", f"=SUM(PurchaseData!$H$2:$H${PURCH_LAST})", "0"),
        ("Total expenses", f'=SUMPRODUCT({EXP_SUM})', "0"),
        ("Gross profit",
         f"=SUM(SalesData!$E$2:$E${SALES_LAST})"
         f"-SUMPRODUCT(SalesData!$G$2:$G${SALES_LAST},SalesData!$K$2:$K${SALES_LAST})",
         "0"),
        ("Net profit",
         f"=SUM(SalesData!$E$2:$E${SALES_LAST})"
         f"-SUMPRODUCT(SalesData!$G$2:$G${SALES_LAST},SalesData!$K$2:$K${SALES_LAST})"
         f"-SUMPRODUCT({EXP_SUM})",
         "0"),
        ("Inventory value", f"=SUM({SH_PROD}!$M$5:$M${PRODUCT_ROWS + 4})", "0"),
        ("Outstanding receivables", f'=SUM(Sales!$E$5:$E${LAST_DATA_ROW})-SUM(Sales!$H$5:$H${LAST_DATA_ROW})', "0"),
    ]
    for i, (label, formula, kind) in enumerate(summary):
        row = 29 + i
        ws.write(row, 1, label, wb.fmt("body"))
        ws.merge_range(row, 2, row, 3, "", wb.fmt("fx_money"))
        ws.write_formula(row, 2, formula, wb.fmt("fx_money"), 0)

    # margin lines
    ws.write(36, 1, "Gross margin", wb.fmt("body"))
    ws.merge_range(36, 2, 36, 3, "", wb.fmt("fx_num"))
    ws.write_formula(36, 2,
                     f"=IFERROR((SUM(SalesData!$E$2:$E${SALES_LAST})-SUMPRODUCT(SalesData!$G$2:$G${SALES_LAST},SalesData!$K$2:$K${SALES_LAST}))/SUM(SalesData!$E$2:$E${SALES_LAST}),0)",
                     wb.wb.add_format({"num_format": "0.0%", "font_name": FONT,
                                       "font_size": 10.5, "font_color": TEXT,
                                       "bg_color": NAVY_800, "bold": True}), 0)
    ws.write(37, 1, "Net margin", wb.fmt("body"))
    ws.merge_range(37, 2, 37, 3, "", wb.fmt("fx_num"))
    ws.write_formula(37, 2,
                     f"=IFERROR((SUM(SalesData!$E$2:$E${SALES_LAST})"
                     f"-SUMPRODUCT(SalesData!$G$2:$G${SALES_LAST},SalesData!$K$2:$K${SALES_LAST})"
                     f"-SUMPRODUCT({EXP_SUM}))"
                     f"/SUM(SalesData!$E$2:$E${SALES_LAST}),0)",
                     wb.wb.add_format({"num_format": "0.0%", "font_name": FONT,
                                       "font_size": 10.5, "font_color": TEXT,
                                       "bg_color": NAVY_800, "bold": True}), 0)

    ws.set_tab_color(BLUE)
    ws.set_landscape()
    ws.set_paper(9)
    ws.fit_to_pages(1, 1)
    wb.nav_row(name, 13, name)
    return ws
