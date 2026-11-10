#!/usr/bin/env python3
"""Composes the Pouria Business dashboard mockups."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dash import *  # noqa

W, H = 1440, 900
RAIL = 236
MAIN_X = RAIL
PAD = 30
CW = W - RAIL - PAD * 2          # 1144 content width


def rail(active, extra_footer=None):
    o = [rect(0, 44, RAIL, H - 44, 0, "#080c0a"), line(RAIL, 44, RAIL, H, BORDER)]
    # brand
    o.append(rect(24, 74, 38, 38, 11, ACC_DARC, stroke="#1f4a38"))
    for i, hh in enumerate([9, 13, 17]):
        o.append(rect(32 + i * 8, 96 - hh, 5, hh, 2, ACC if i == 2 else "#1c6b4e"))
    o.append(text(74, 91, "POURIA", 14, TXT, DISP, 700, "start", "1.2"))
    o.append(text(74, 105, "BUSINESS", 10, ACC, UI, 700, "start", "3.2"))
    o.append(line(24, 136, RAIL - 24, 136, BORDER))
    o.append(text(26, 158, "WORKSPACE", 7.8, FAINT, UI, 700, "start", "1.6"))
    nav = [("Overview", "grid"), ("Inventory", "box"), ("Sales", "cart"), ("Wholesale", "truck"),
           ("Expenses", "card"), ("Reporting", "chart"), ("Automation", "bolt")]
    y = 170
    for label, icon in nav:
        on = label == active
        if on:
            o.append(rect(16, y, RAIL - 32, 34, 9, ACC + "16", stroke=ACC + "33"))
            o.append(rect(16, y + 9, 2.4, 16, 1.2, ACC))
        col = ACC if on else MUTED
        cx = 36
        # tiny icons
        if icon == "grid":
            for gx in range(2):
                for gy in range(2):
                    o.append(rect(cx - 5 + gx * 7, y + 12 + gy * 7, 5, 5, 1.4, col, opacity=0.85))
        elif icon == "box":
            o.append(f'<path d="M{cx-6},{y+16} l6,-3.4 6,3.4 v7 l-6,3.4 -6,-3.4z" fill="none" stroke="{col}" stroke-width="1.5" stroke-linejoin="round"/>')
        elif icon == "cart":
            o.append(f'<circle cx="{cx-3}" cy="{y+22}" r="1.7" fill="{col}"/><circle cx="{cx+3.5}" cy="{y+22}" r="1.7" fill="{col}"/>'
                     f'<path d="M{cx-6},{y+13} h2.6 l2.2,6 h6.6 l1.8,-4.6 h-9" fill="none" stroke="{col}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"/>')
        elif icon == "truck":
            o.append(f'<path d="M{cx-7},{y+14} h7 v6 h-7z M{cx},{y+16.5} h3.4 l2.6,3.5 v0 h-6z" fill="none" stroke="{col}" stroke-width="1.4" stroke-linejoin="round"/>'
                     f'<circle cx="{cx-4.5}" cy="{y+22}" r="1.6" fill="{col}"/><circle cx="{cx+4}" cy="{y+22}" r="1.6" fill="{col}"/>')
        elif icon == "card":
            o.append(rect(cx - 7, y + 13, 14, 9.5, 2, "none", stroke=col, sw=1.4))
            o.append(rect(cx - 7, y + 15.6, 14, 2, 1, col))
        elif icon == "chart":
            o.append(rect(cx - 6.5, y + 18, 3, 5, 1.2, col))
            o.append(rect(cx - 2, y + 15, 3, 8, 1.2, col))
            o.append(rect(cx + 2.5, y + 12.5, 3, 10.5, 1.2, col))
        else:
            o.append(f'<path d="M{cx+1},{y+11} l-5,7 h4 l-1,5.5 5.5,-7.5 h-4z" fill="{col}"/>')
        o.append(text(56, y + 21, label, 11.5, TXT if on else MUTED, UI, 600 if on else 500))
        y += 40
    o.append(line(24, y + 12, RAIL - 24, y + 12, BORDER))
    o.append(text(26, y + 34, "STATUS", 7.8, FAINT, UI, 700, "start", "1.6"))
    o.append(rect(24, y + 46, RAIL - 48, 62, 12, "#0c1311", stroke=BORDER))
    o.append(text(38, y + 66, "Data health", 9.5, MUTED, UI, 500))
    o.append(text(RAIL - 38, y + 66, "94%", 10.5, ACC, UI, 700, "end"))
    o.append(rect(38, y + 76, RAIL - 76, 5, 2.5, "#16211d"))
    o.append(rect(38, y + 76, (RAIL - 76) * 0.94, 5, 2.5, ACC))
    o.append(text(38, y + 98, "Last refresh · 2 min ago", 8, FAINT, UI, 400))
    o.append(rect(24, H - 78, RAIL - 48, 48, 12, ACC + "10", stroke=ACC + "2e"))
    o.append(circle(44, H - 54, 13, ACC + "22", ACC + "55", 1.2))
    o.append(text(44, H - 50, "PA", 8.5, ACC, UI, 700, "middle"))
    o.append(text(64, H - 58, "Pouria Asghari", 10, TXT, UI, 600))
    o.append(text(64, H - 46, "Owner · full access", 8.2, FAINT, UI, 400))
    return "".join(o)


def header(title, sub, chips=None, date="01 Oct — 31 Oct 2026", search="Search SKU, order, report…"):
    o = [rect(MAIN_X, 44, W - MAIN_X, 96, 0, "#080c0a")]
    o.append(text(MAIN_X + PAD, 82, title, 20, TXT, DISP, 600, "start", "-0.3"))
    o.append(text(MAIN_X + PAD, 100, sub, 9.8, FAINT, UI, 400))
    # search
    sx = W - PAD - 250
    o.append(rect(sx, 62, 250, 32, 9, "#0c1210", stroke=BORDER))
    o.append(circle(sx + 17, 75.5, 5.4, "none", FAINT, 1.4))
    o.append(line(sx + 21, 80, sx + 24.5, 83.5, FAINT, 1.4))
    o.append(text(sx + 34, 79.5, search, 9, FAINT, UI, 400))
    o.append(rect(sx + 214, 69, 26, 18, 6, "#131c19"))
    o.append(text(sx + 227, 81.5, "⌘K", 7.6, MUTED, UI, 600, "middle"))
    # date + export
    o.append(rect(W - PAD - 250, 106, 148, 27, 8, "#0c1210", stroke=BORDER))
    o.append(rect(W - PAD - 236, 113, 12, 12, 3, "none", FAINT, 1.2))
    o.append(text(W - PAD - 218, 123.5, date, 8.8, MUTED, UI, 500))
    o.append(rect(W - PAD - 92, 106, 92, 27, 8, ACC + "1a", stroke=ACC + "44"))
    o.append(text(W - PAD - 46, 123.5, "Export", 9.2, ACC, UI, 700, "middle"))
    o.append(line(MAIN_X, 140, W, 140, BORDER))
    if chips:
        o.append(chip_row(MAIN_X + PAD, 156, chips))
    return "".join(o)


def kpi_row(y, items, h=104, gap=16):
    o = []
    n = len(items)
    w = (CW - gap * (n - 1)) / n
    for i, it in enumerate(items):
        x = MAIN_X + PAD + i * (w + gap)
        o.append(kpi(x, y, w, h, *it))
    return "".join(o)


def frame(title, sub, active, tabs, chips, body, sheet="Overview"):
    o = [excel_chrome(W, "Pouria Business · Dashboard App", ["Data", "Reports", "Settings"], "Data",
                      subtitle="Connected to workbook · auto-saved 2 min ago")]
    o.append(rail(active))
    o.append(header(title, sub, chips))
    o.append(body)
    o.append(sheet_tabs(H - 26, W, tabs, sheet, MAIN_X + PAD))
    return build_doc(W, H, "".join(o), BG, DEFS)


# ============ INVENTORY ============
def inventory():
    b = []
    ky = 158
    b.append(kpi_row(ky, [
        ("Inventory value", "$1,428,900", "▲ 6.8% vs Sep", True, [3, 4, 3.6, 5, 4.6, 6, 7]),
        ("Active SKUs", "2,486", "▲ 124 this month", True, [2, 2.4, 3, 3.2, 3.8, 4.2, 4.6]),
        ("Low-stock alerts", "37", "▼ 12 fewer than Sep", True, [9, 8, 7.4, 6, 5.2, 5, 4.2]),
        ("Stock turns", "7.4×", "▲ 0.6× YoY", True, [3, 4, 3.8, 5, 5.4, 6, 7.4]),
    ], h=100))
    # main chart
    cy = 274
    ch = 300
    lw = 700
    b.append(rect(MAIN_X + PAD, cy, lw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, cy + 26, "Stock movement"))
    b.append(text(MAIN_X + PAD + 20, cy + 48, "Units in · units out · closing balance", 9, FAINT))
    b.append(pill(MAIN_X + PAD + lw - 106, cy + 16, 86, 20, "12 months", ACC, 9))
    # legend
    lx = MAIN_X + PAD + 20
    for label, color in [("Closing balance", ACC), ("Units received", BLUE)]:
        b.append(circle(lx + 4, cy + 74, 3.4, color))
        b.append(text(lx + 13, cy + 77, label, 9, MUTED))
        lx += 108
    months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    b.append(area_chart(MAIN_X + PAD + 56, cy + 96, lw - 86, 168,
                        [182, 210, 196, 240, 268, 254, 296, 312, 340, 328, 372, 404],
                        months, series2=[120, 150, 132, 168, 190, 176, 214, 226, 248, 240, 286, 318], ticks=4))
    # right: category donut
    rx = MAIN_X + PAD + lw + 16
    rw = CW - lw - 16
    b.append(rect(rx, cy, rw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Category mix"))
    b.append(text(rx + 20, cy + 48, "Share of stock value", 9, FAINT))
    segs = [(ACC, 42), ("#2f9e77", 26), (BLUE, 18), ("#3b4f47", 14)]
    b.append(donut(rx + rw/2, cy + 148, 62, 17, segs))
    b.append(text(rx + rw/2, cy + 143, "$1.42M", 19, TXT, DISP, 600, "middle"))
    b.append(text(rx + rw/2, cy + 158, "total value", 8.2, FAINT, UI, 500, "middle"))
    legend = [("Electronics", "42%", ACC), ("Apparel", "26%", "#2f9e77"),
              ("Home & Living", "18%", BLUE), ("Consumables", "14%", "#3b4f47")]
    ly = cy + 236
    for i, (name, val, col) in enumerate(legend):
        xx = rx + 24 + (i % 2) * (rw / 2 - 12)
        yy = ly + (i // 2) * 22
        b.append(rect(xx, yy - 7, 7, 7, 2, col))
        b.append(text(xx + 12, yy, name, 8.8, MUTED))
        b.append(text(xx + rw/2 - 32, yy, val, 8.8, TXT, UI, 600, "end"))
    # bottom table
    ty = 592
    b.append(rect(MAIN_X + PAD, ty, CW, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(MAIN_X + PAD + 20, ty + 30, "Reorder pipeline", 12, TXT, UI, 600))
    b.append(text(MAIN_X + PAD + 126, ty + 30, "37 items need attention", 9, FAINT))
    b.append(pill(MAIN_X + PAD + CW - 118, ty + 16, 98, 22, "Auto-generated", ACC, 9))
    rows = [
        [("SKU-10482", MUTED, 500), ("Arctic Pro Headphones", TXT, 600), ("18", TXT, 600), ("40", MUTED, 500),
         ("__pill__", "Critical", RED), ("4 days", MUTED, 500), ("$6,420", TXT, 600)],
        [("SKU-20915", MUTED, 500), ("Linen Blend Overshirt", TXT, 600), ("64", TXT, 600), ("90", MUTED, 500),
         ("__pill__", "Low stock", AMBER), ("9 days", MUTED, 500), ("$4,180", TXT, 600)],
        [("SKU-33107", MUTED, 500), ("Ceramic Pour-Over Set", TXT, 600), ("142", TXT, 600), ("80", MUTED, 500),
         ("__pill__", "Healthy", ACC), ("21 days", MUTED, 500), ("$2,940", TXT, 600)],
        [("SKU-41860", MUTED, 500), ("Everyday Cotton Tote", TXT, 600), ("9", TXT, 600), ("120", MUTED, 500),
         ("__pill__", "Critical", RED), ("2 days", MUTED, 500), ("$8,760", TXT, 600)],
        [("SKU-52240", MUTED, 500), ("Walnut Desk Organiser", TXT, 600), ("88", TXT, 600), ("60", MUTED, 500),
         ("__pill__", "Healthy", ACC), ("17 days", MUTED, 500), ("$3,320", TXT, 600)],
    ]
    b.append(table(MAIN_X + PAD + 12, ty + 44, CW - 24,
                   [("SKU", .13), ("Product", .30), ("On hand", .11), ("Reorder at", .12),
                    ("Status", .15), ("Lead time", .10), ("Value", .09)],
                   rows, row_h=31, aligns=["start", "start", "end", "end", "start", "end", "end"]))
    return frame("Inventory Command Center", "Northline Distribution · 2 warehouses · real-time sync",
                 "Inventory", ["Overview", "Inventory", "Reorder", "Valuation", "Suppliers"],
                 ["All warehouses", "Fast movers", "Dead stock"], "".join(b))


# ============ SALES ============
def sales():
    b = []
    ky = 158
    b.append(kpi_row(ky, [
        ("Net revenue", "$286,430", "▲ 18.2% vs Sep", True, [3, 3.4, 4.2, 4, 5.2, 5.8, 6.6]),
        ("Orders", "3,742", "▲ 312 this month", True, [2, 2.8, 2.6, 3.4, 3.6, 4.2, 4.6]),
        ("Avg order value", "$76.54", "▲ 4.1%", True, [3, 3.2, 3.6, 3.4, 4, 4.4, 4.6]),
        ("Return rate", "2.1%", "▼ 0.7 pts", True, [7, 6.4, 6, 5.6, 5, 4.6, 4.2]),
    ], h=100))
    cy, ch, lw = 274, 300, 700
    b.append(rect(MAIN_X + PAD, cy, lw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, cy + 26, "Revenue vs target"))
    b.append(text(MAIN_X + PAD + 20, cy + 48, "Net of returns · USD", 9, FAINT))
    lx = MAIN_X + PAD + 20
    for label, color in [("Net revenue", ACC), ("Target", BLUE)]:
        b.append(circle(lx + 4, cy + 74, 3.4, color))
        b.append(text(lx + 13, cy + 77, label, 9, MUTED))
        lx += 96
    b.append(area_chart(MAIN_X + PAD + 56, cy + 96, lw - 86, 168,
                        [12.4, 14.1, 13.2, 16.8, 18.4, 17.2, 20.6, 22.4, 21.8, 24.6, 26.2, 28.6],
                        ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
                        ymax=32, series2=[13, 14.5, 15.5, 17, 18, 19, 21, 22, 23, 25, 26, 28]))
    # right panels
    rx = MAIN_X + PAD + lw + 16
    rw = CW - lw - 16
    b.append(rect(rx, cy, rw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Channel mix"))
    b.append(text(rx + 20, cy + 48, "Revenue by sales channel", 9, FAINT))
    b.append(donut(rx + rw/2, cy + 146, 58, 16,
                   [(ACC, 48), ("#2f9e77", 27), (BLUE, 16), ("#3b4f47", 9)]))
    b.append(text(rx + rw/2, cy + 142, "$286K", 18, TXT, DISP, 600, "middle"))
    b.append(text(rx + rw/2, cy + 157, "this month", 8.2, FAINT, UI, 500, "middle"))
    ly = cy + 230
    for i, (name, val, col) in enumerate([("Retail", "48%", ACC), ("Online", "27%", "#2f9e77"),
                                          ("Marketplace", "16%", BLUE), ("Phone", "9%", "#3b4f47")]):
        xx = rx + 24 + (i % 2) * (rw / 2 - 12)
        yy = ly + (i // 2) * 22
        b.append(rect(xx, yy - 7, 7, 7, 2, col))
        b.append(text(xx + 12, yy, name, 8.8, MUTED))
        b.append(text(xx + rw/2 - 32, yy, val, 8.8, TXT, UI, 600, "end"))
    # bottom: bars + table
    ty = 592
    bw_ = 380
    b.append(rect(MAIN_X + PAD, ty, bw_, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, ty + 26, "Revenue by weekday"))
    b.append(bars(MAIN_X + PAD + 30, ty + 62, bw_ - 60, 130,
                  [6, 8, 9.5, 12, 14, 18, 11], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
    b.append(text(MAIN_X + PAD + 20, ty + 226, "Weekend peaks driven by retail walk-ins", 8.6, FAINT))
    tx = MAIN_X + PAD + bw_ + 16
    tw = CW - bw_ - 16
    b.append(rect(tx, ty, tw, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(tx + 20, ty + 30, "Top products", 12, TXT, UI, 600))
    b.append(text(tx + 112, ty + 30, "by net revenue", 9, FAINT))
    b.append(pill(tx + tw - 104, ty + 16, 84, 22, "View all", ACC, 9))
    rows = [
        [("Arctic Pro Headphones", TXT, 600), ("412", MUTED, 500), ("__bar__", 1.0, ACC), ("$42,180", TXT, 600)],
        [("Linen Blend Overshirt", TXT, 600), ("388", MUTED, 500), ("__bar__", .74, ACC), ("$31,240", TXT, 600)],
        [("Ceramic Pour-Over Set", TXT, 600), ("264", MUTED, 500), ("__bar__", .55, "#2f9e77"), ("$23,460", TXT, 600)],
        [("Walnut Desk Organiser", TXT, 600), ("197", MUTED, 500), ("__bar__", .41, "#2f9e77"), ("$17,320", TXT, 600)],
        [("Everyday Cotton Tote", TXT, 600), ("152", MUTED, 500), ("__bar__", .28, "#2f9e77"), ("$11,980", TXT, 600)],
    ]
    b.append(table(tx + 8, ty + 46, tw - 16,
                   [("Product", .38), ("Units", .13), ("Share", .34), ("Revenue", .15)],
                   rows, row_h=30, aligns=["start", "end", "start", "end"]))
    return frame("Sales Performance Studio", "Retail + online channels · daily refresh at 06:00",
                 "Sales", ["Overview", "Sales", "Products", "Channels", "Returns"],
                 ["This month", "Last 90 days", "Year to date"], "".join(b))


# ============ WHOLESALE ============
def wholesale():
    b = []
    b.append(kpi_row(158, [
        ("Open purchase orders", "148", "▲ 22 this week", True, [3, 3.4, 4, 4.2, 5, 5.4, 6]),
        ("Fulfilled value", "$412,900", "▲ 9.4% vs Sep", True, [3, 4, 3.6, 5, 5.4, 6, 6.4]),
        ("Average fill rate", "96.4%", "▲ 1.2 pts", True, [4, 4.4, 4.2, 5, 5.2, 5.6, 6]),
        ("Backorders", "12", "▼ 5 fewer", True, [8, 7, 7.4, 6, 5.4, 4.6, 4.2]),
    ], h=100))
    cy, ch = 274, 300
    lw = 700
    b.append(rect(MAIN_X + PAD, cy, lw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, cy + 26, "Order volume by week"))
    b.append(text(MAIN_X + PAD + 20, cy + 48, "Purchase orders received vs fulfilled", 9, FAINT))
    lx = MAIN_X + PAD + 20
    for label, color in [("Received", "#2b6b55"), ("Fulfilled", ACC)]:
        b.append(rect(lx, cy + 70, 8, 8, 2.5, color))
        b.append(text(lx + 14, cy + 77, label, 9, MUTED))
        lx += 86
    weeks = ["W36", "W37", "W38", "W39", "W40", "W41", "W42", "W43"]
    bx = MAIN_X + PAD + 50
    bw_full = lw - 80
    group = bw_full / len(weeks)
    for i, wk in enumerate(weeks):
        recv = [42, 56, 48, 64, 58, 72, 66, 78][i]
        ful = [38, 50, 46, 58, 54, 68, 62, 74][i]
        gx = bx + i * group + group * 0.18
        bwide = group * 0.28
        hh1 = recv / 84 * 168
        hh2 = ful / 84 * 168
        b.append(rect(gx, cy + 250 - hh1, bwide, hh1, 3.5, "#1d4a3a"))
        b.append(rect(gx + bwide + 3, cy + 250 - hh2, bwide, hh2, 3.5, "url(#barGrad)"))
        b.append(text(gx + bwide, cy + 270, wk, 8.4, FAINT, UI, 500, "middle"))
    for i in range(5):
        gy = cy + 250 - (168 * i / 4)
        b.append(line(bx, gy, bx + bw_full, gy, GRID, 1, "2 4" if i else None, .8))
        b.append(text(bx - 8, gy + 3, f"{21*i}", 8.4, FAINT, UI, 500, "end"))
    # right: receivables aging
    rx = MAIN_X + PAD + lw + 16
    rw = CW - lw - 16
    b.append(rect(rx, cy, rw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Receivables aging"))
    b.append(text(rx + 20, cy + 48, "Outstanding balance by bucket", 9, FAINT))
    segs = [("Current", .58, ACC), ("1–30 days", .24, "#2f9e77"), ("31–60 days", .12, AMBER), ("60+ days", .06, RED)]
    yy = cy + 74
    for name, frac, col in segs:
        b.append(text(rx + 20, yy, name, 9.2, MUTED))
        b.append(text(rx + rw - 20, yy, f"${frac*186000:,.0f}", 9.4, TXT, UI, 600, "end"))
        b.append(rect(rx + 20, yy + 7, rw - 40, 6, 3, "#16211d"))
        b.append(rect(rx + 20, yy + 7, (rw - 40) * frac, 6, 3, col))
        yy += 34
    b.append(line(rx + 20, yy + 4, rx + rw - 20, yy + 4, BORDER))
    b.append(text(rx + 20, yy + 26, "Total outstanding", 9.4, MUTED))
    b.append(text(rx + rw - 20, yy + 26, "$186,400", 13, ACC, DISP, 600, "end"))
    b.append(rect(rx + 20, yy + 40, rw - 40, 42, 10, ACC + "0e", stroke=ACC + "2a"))
    b.append(text(rx + 34, yy + 57, "Collection score", 8.6, MUTED))
    b.append(text(rx + 34, yy + 71, "Excellent · avg 21 days to pay", 9, ACC, UI, 600))
    # table
    ty = 592
    b.append(rect(MAIN_X + PAD, ty, CW, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(MAIN_X + PAD + 20, ty + 30, "Purchase order pipeline", 12, TXT, UI, 600))
    b.append(text(MAIN_X + PAD + 160, ty + 30, "148 open · $412.9K in flight", 9, FAINT))
    b.append(pill(MAIN_X + PAD + CW - 126, ty + 16, 106, 22, "Sync with ERP", ACC, 9))
    rows = [
        [("PO-20418", MUTED, 500), ("Marlow & Co.", TXT, 600), ("42 SKUs", MUTED, 500), ("$48,260", TXT, 600),
         ("__pill__", "In transit", BLUE), ("14 Nov", MUTED, 500), ("96%", ACC, 600)],
        [("PO-20417", MUTED, 500), ("Brightline Retail", TXT, 600), ("18 SKUs", MUTED, 500), ("$22,910", TXT, 600),
         ("__pill__", "Picking", AMBER), ("12 Nov", MUTED, 500), ("88%", TXT, 600)],
        [("PO-20412", MUTED, 500), ("Harbor Wholesale", TXT, 600), ("64 SKUs", MUTED, 500), ("$81,430", TXT, 600),
         ("__pill__", "Confirmed", ACC), ("19 Nov", MUTED, 500), ("—", FAINT, 500)],
        [("PO-20405", MUTED, 500), ("Westgate Supply", TXT, 600), ("9 SKUs", MUTED, 500), ("$9,640", TXT, 600),
         ("__pill__", "Backorder", RED), ("27 Nov", MUTED, 500), ("—", FAINT, 500)],
        [("PO-20398", MUTED, 500), ("Nordvik Trading", TXT, 600), ("31 SKUs", MUTED, 500), ("$36,120", TXT, 600),
         ("__pill__", "Delivered", "#7d8f87"), ("08 Nov", MUTED, 500), ("100%", ACC, 600)],
    ]
    b.append(table(MAIN_X + PAD + 12, ty + 44, CW - 24,
                   [("PO number", .13), ("Customer", .22), ("Lines", .11), ("Value", .13),
                    ("Status", .16), ("Due", .11), ("Fill", .10)],
                   rows, row_h=31, aligns=["start", "start", "end", "end", "start", "end", "end"]))
    return frame("Wholesale Order Hub", "B2B order desk · 34 active trade accounts",
                 "Wholesale", ["Dashboard", "Orders", "Accounts", "Backorders", "Credit"],
                 ["All accounts", "At risk", "Top volume"], "".join(b))


# ============ EXPENSES ============
def expenses():
    b = []
    b.append(kpi_row(158, [
        ("Monthly spend", "$84,260", "▲ 5.1% vs budget", True, [3, 3.6, 3.2, 4.4, 4.8, 5.2, 5.6]),
        ("Budget used", "72%", "▲ within plan", True, [4, 4.4, 5, 4.6, 5.4, 6, 6.4]),
        ("Pending approval", "9", "▼ 3 fewer", True, [8, 7.4, 7, 6.4, 6, 5.2, 4.6]),
        ("Cost per order", "$22.52", "▼ 3.4%", True, [7, 6.6, 6.4, 6, 5.6, 5.2, 4.8]),
    ], h=100))
    cy, ch, lw = 274, 300, 700
    b.append(rect(MAIN_X + PAD, cy, lw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, cy + 26, "Spend vs budget"))
    b.append(text(MAIN_X + PAD + 20, cy + 48, "Operating expenses · rolling 12 months", 9, FAINT))
    lx = MAIN_X + PAD + 20
    for label, color in [("Actual spend", ACC), ("Budget", BLUE)]:
        b.append(circle(lx + 4, cy + 74, 3.4, color))
        b.append(text(lx + 13, cy + 77, label, 9, MUTED))
        lx += 84
    b.append(area_chart(MAIN_X + PAD + 56, cy + 96, lw - 86, 168,
                        [58, 62, 60, 68, 72, 70, 76, 79, 74, 81, 83, 84.3],
                        ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
                        ymax=100, series2=[60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 82, 88]))
    rx = MAIN_X + PAD + lw + 16
    rw = CW - lw - 16
    b.append(rect(rx, cy, rw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Where money goes"))
    b.append(text(rx + 20, cy + 48, "Expense categories this month", 9, FAINT))
    cats = [("Suppliers", 38, ACC), ("Payroll", 26, "#2f9e77"), ("Logistics", 16, BLUE),
            ("Marketing", 12, VIOLET), ("Other", 8, "#3b4f47")]
    yy = cy + 74
    for name, pct, col in cats:
        b.append(text(rx + 20, yy, name, 9.2, MUTED))
        b.append(text(rx + rw - 20, yy, f"{pct}%", 9.4, TXT, UI, 600, "end"))
        b.append(rect(rx + 20, yy + 7, rw - 40, 6, 3, "#16211d"))
        b.append(rect(rx + 20, yy + 7, (rw - 40) * pct / 42, 6, 3, col))
        yy += 31
    b.append(line(rx + 20, yy + 2, rx + rw - 20, yy + 2, BORDER))
    b.append(text(rx + 20, yy + 24, "Remaining budget", 9.4, MUTED))
    b.append(text(rx + rw - 20, yy + 24, "$32,740", 14, ACC, DISP, 600, "end"))
    b.append(rect(rx + 20, yy + 38, rw - 40, 40, 10, "#0f1714", stroke=BORDER))
    b.append(text(rx + 34, yy + 55, "Run-rate projection", 8.6, FAINT))
    b.append(text(rx + 34, yy + 68, "$84.9K · 9 days left", 9.4, TXT, UI, 600))
    # budget vs actual grouped bars
    ty = 592
    bw_ = 470
    b.append(rect(MAIN_X + PAD, ty, bw_, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, ty + 26, "Budget vs actual by team"))
    groups = ["Ops", "Sales", "Retail", "Logistics"]
    actual = [22, 18, 26, 18]
    budget = [24, 22, 28, 20]
    gx0 = MAIN_X + PAD + 40
    gw = bw_ - 70
    gg = gw / len(groups)
    for i, g in enumerate(groups):
        bwide = gg * 0.22
        h1 = actual[i] / 32 * 128
        h2 = budget[i] / 32 * 128
        bx0 = gx0 + i * gg + gg * 0.22
        b.append(rect(bx0, ty + 210 - h1, bwide, h1, 3.5, "url(#barGrad)"))
        b.append(rect(bx0 + bwide + 4, ty + 210 - h2, bwide, h2, 3.5, "#1d2b26"))
        b.append(text(bx0 + bwide + 2, ty + 226, g, 8.4, FAINT, UI, 500, "middle"))
        b.append(text(bx0 + bwide + 2, ty + 204 - max(h1, h2) - 6, f"${actual[i]}K", 8, MUTED, UI, 600, "middle"))
    b.append(text(MAIN_X + PAD + 20, ty + 70, "■ Actual", 8, MUTED))
    b.append(text(MAIN_X + PAD + 80, ty + 70, "■ Budget", 8, FAINT))
    # table
    tx = MAIN_X + PAD + bw_ + 16
    tw = CW - bw_ - 16
    b.append(rect(tx, ty, tw, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(tx + 20, ty + 30, "Recent expenses", 12, TXT, UI, 600))
    b.append(text(tx + 140, ty + 30, "auto-coded", 9, FAINT))
    rows = [
        [("INV-8841", MUTED, 500), ("Marlow & Co.", TXT, 600), ("$12,480", TXT, 600), ("__pill__", "Approved", ACC)],
        [("INV-8839", MUTED, 500), ("Freight · Nordvik", TXT, 600), ("$3,260", TXT, 600), ("__pill__", "Pending", AMBER)],
        [("INV-8834", MUTED, 500), ("Studio light rebuild", TXT, 600), ("$1,180", TXT, 600), ("__pill__", "Approved", ACC)],
        [("INV-8830", MUTED, 500), ("Ad spend · October", TXT, 600), ("$6,900", TXT, 600), ("__pill__", "Review", BLUE)],
        [("INV-8826", MUTED, 500), ("Warehouse utilities", TXT, 600), ("$2,140", TXT, 600), ("__pill__", "Approved", ACC)],
    ]
    b.append(table(tx + 8, ty + 46, tw - 16,
                   [("Ref", .22), ("Vendor", .38), ("Amount", .22), ("Status", .18)],
                   rows, row_h=30, aligns=["start", "start", "end", "start"]))
    return frame("Expense Control Center", "Operating spend · receipts captured in 4 clicks",
                 "Expenses", ["Overview", "Expenses", "Budgets", "Approvals", "Vendors"],
                 ["This month", "By category", "Unapproved"], "".join(b))


# ============ REPORTING ============
def reporting():
    b = []
    b.append(kpi_row(158, [
        ("Reports delivered", "128", "▲ 26 this quarter", True, [3, 3.6, 4, 4.4, 5, 5.4, 6]),
        ("Scheduled refreshes", "24", "▲ all succeeded", True, [4, 4.2, 4.6, 4.6, 5, 5.4, 5.6]),
        ("Connected sources", "6", "Files, ERP, POS", True, [3, 3, 3.6, 3.6, 4, 4, 4.6]),
        ("Refresh time", "38s", "▼ 22s faster", True, [8, 7.4, 6.8, 6.4, 6, 5.4, 5]),
    ], h=100))
    cy, ch, lw = 274, 300, 660
    b.append(rect(MAIN_X + PAD, cy, lw, ch, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(MAIN_X + PAD + 20, cy + 26, "Consolidated performance"))
    b.append(text(MAIN_X + PAD + 20, cy + 48, "Revenue, gross margin and cash position", 9, FAINT))
    lx = MAIN_X + PAD + 20
    for label, color in [("Revenue", ACC), ("Margin", BLUE)]:
        b.append(circle(lx + 4, cy + 74, 3.4, color))
        b.append(text(lx + 13, cy + 77, label, 9, MUTED))
        lx += 78
    b.append(area_chart(MAIN_X + PAD + 56, cy + 96, lw - 86, 168,
                        [14, 16, 15, 19, 21, 20, 24, 26, 25, 28, 30, 33],
                        ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
                        ymax=40, series2=[6, 7, 6.6, 8, 9, 8.6, 10, 11, 10.4, 11.6, 12.4, 13.6]))
    # right top: gauge / score
    rx = MAIN_X + PAD + lw + 16
    rw = CW - lw - 16
    b.append(rect(rx, cy, rw, 144, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Business health"))
    b.append(text(rx + 20, cy + 48, "Weighted score across 5 pillars", 9, FAINT))
    b.append(donut(rx + 78, cy + 104, 38, 11, [(ACC, 86), ("#2f9e77", 8), ("#1d2b26", 6)]))
    b.append(text(rx + 78, cy + 101, "86", 20, TXT, DISP, 600, "middle"))
    b.append(text(rx + 78, cy + 114, "/100", 7.6, FAINT, UI, 500, "middle"))
    facts = [("Cash runway", "8.4 mo"), ("Gross margin", "41.2%"), ("On-time delivery", "96.4%")]
    fy = cy + 82
    for label, val in facts:
        b.append(text(rx + 136, fy, label, 8.8, FAINT))
        b.append(text(rx + rw - 20, fy, val, 9.6, TXT, UI, 600, "end"))
        b.append(line(rx + 136, fy + 6, rx + rw - 20, fy + 6, GRID, 1, None, .8))
        fy += 24
    # right bottom: source list
    b.append(rect(rx, cy + 160, rw, 140, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 186, "Data sources"))
    srcs = [("inventory_master.xlsx", "12 sheets", ACC), ("sales_ledger_2026.csv", "38k rows", ACC),
            ("wholesale_POs.xlsx", "live", BLUE), ("expenses_receipts/", "416 files", AMBER)]
    sy = cy + 208
    for name, meta, col in srcs:
        b.append(rect(rx + 20, sy - 9, 7, 7, 2, col))
        b.append(text(rx + 34, sy, name, 8.6, MUTED))
        b.append(text(rx + rw - 20, sy, meta, 8.2, FAINT, UI, 500, "end"))
        sy += 21
    # bottom: kpi matrix + actions
    ty = 592
    b.append(rect(MAIN_X + PAD, ty, CW, 250, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(MAIN_X + PAD + 20, ty + 30, "Monthly scorecard", 12, TXT, UI, 600))
    b.append(text(MAIN_X + PAD + 150, ty + 30, "October 2026 · all entities", 9, FAINT))
    b.append(pill(MAIN_X + PAD + CW - 138, ty + 16, 118, 22, "Power Query refresh", ACC, 9))
    rows = [
        [("Revenue", TXT, 600), ("$286,430", TXT, 600), ("$242,180", MUTED, 500), ("+18.2%", ACC, 600), ("On track", ACC)],
        [("Gross margin", TXT, 600), ("41.2%", TXT, 600), ("38.6%", MUTED, 500), ("+2.6 pts", ACC, 600), ("On track", ACC)],
        [("Inventory value", TXT, 600), ("$1,428,900", TXT, 600), ("$1,338,000", MUTED, 500), ("+6.8%", ACC, 600), ("Watch", AMBER)],
        [("Operating spend", TXT, 600), ("$84,260", TXT, 600), ("$80,180", MUTED, 500), ("+5.1%", AMBER, 600), ("Within budget", ACC)],
        [("Backorders", TXT, 600), ("12", TXT, 600), ("17", MUTED, 500), ("-29.4%", ACC, 600), ("On track", ACC)],
    ]
    b.append(table(MAIN_X + PAD + 12, ty + 44, CW - 24,
                   [("Metric", .28), ("October", .19), ("Previous", .19), ("Change", .17), ("Status", .17)],
                   rows, row_h=33, aligns=["start", "end", "end", "end", "start"]))
    return frame("Executive Reporting Suite", "One-page board pack · 6 sources consolidated",
                 "Reporting", ["Summary", "Scorecard", "Charts", "Sources", "Notes"],
                 ["October", "Q3", "Board pack"], "".join(b))


# ============ HERO (wide, rich) ============
def hero():
    W_, H_ = 1560, 1040
    b = [excel_chrome(W_, "Pouria Business · Dashboard App", ["Data", "Reports", "Settings"], "Data",
                      subtitle="Northline_Group_Master.xlsx · auto-saved 2 min ago")]
    # rail
    o = [rect(0, 44, 250, H_ - 44, 0, "#080c0a"), line(250, 44, 250, H_, BORDER)]
    o.append(rect(24, 74, 38, 38, 11, ACC_DARC, stroke="#1f4a38"))
    for i, hh in enumerate([9, 13, 17]):
        o.append(rect(32 + i * 8, 96 - hh, 5, hh, 2, ACC if i == 2 else "#1c6b4e"))
    o.append(text(74, 91, "POURIA", 14, TXT, DISP, 700, "start", "1.2"))
    o.append(text(74, 105, "BUSINESS", 10, ACC, UI, 700, "start", "3.2"))
    o.append(line(24, 136, 226, 136, BORDER))
    o.append(text(26, 158, "LIVE DASHBOARD", 7.8, FAINT, UI, 700, "start", "1.6"))
    o.append(rect(18, 168, 214, 46, 10, "#0e1613", stroke=BORDER))
    o.append(circle(40, 191, 5, ACC))
    o.append(circle(40, 191, 9, "none", ACC, 1, 0.35))
    o.append(text(56, 188, "All systems synced", 9.6, TXT, UI, 600))
    o.append(text(56, 201, "2 min ago · 0 errors", 8.2, FAINT))
    yy = 238
    for label, val, pct, col in [("Inventory", "$1.43M", .82, ACC), ("Sales", "$286K", .64, "#2f9e77"),
                                 ("Wholesale", "$413K", .71, BLUE), ("Expenses", "$84K", .38, AMBER)]:
        o.append(text(26, yy, label, 9.4, MUTED))
        o.append(text(226, yy, val, 9.6, TXT, UI, 600, "end"))
        o.append(rect(26, yy + 7, 200, 5, 2.5, "#16211d"))
        o.append(rect(26, yy + 7, 200 * pct, 5, 2.5, col))
        yy += 38
    o.append(line(24, yy + 4, 226, yy + 4, BORDER))
    o.append(text(26, yy + 26, "AUTOMATION RUNS", 7.8, FAINT, UI, 700, "start", "1.6"))
    runs = [("Nightly stock sync", "02:00", ACC), ("Invoice import", "06:00", ACC),
            ("PO reminder emails", "08:30", ACC), ("Board pack export", "Fri 17:00", AMBER)]
    ry = yy + 46
    for name, t, col in runs:
        o.append(circle(30, ry - 3, 3, col))
        o.append(text(40, ry, name, 8.6, MUTED))
        o.append(text(226, ry, t, 8, FAINT, UI, 500, "end"))
        ry += 22
    o.append(rect(24, H_ - 96, 202, 64, 12, ACC + "10", stroke=ACC + "2e"))
    o.append(text(40, H_ - 72, "Automation health", 8.6, MUTED))
    o.append(text(40, H_ - 52, "100% · 0 failures", 10.5, ACC, UI, 600))
    b.append("".join(o))
    # header
    o = [rect(250, 44, W_ - 250, 104, 0, "#080c0a")]
    o.append(text(280, 84, "Executive Overview", 23, TXT, DISP, 600, "start", "-0.4"))
    o.append(text(280, 104, "Northline Group · retail, wholesale & distribution", 10, FAINT))
    o.append(rect(W_ - 490, 64, 190, 32, 9, "#0c1210", stroke=BORDER))
    o.append(circle(W_ - 473, 79, 5.4, "none", FAINT, 1.4))
    o.append(text(W_ - 458, 83, "Search anything…", 9, FAINT))
    o.append(rect(W_ - 286, 64, 122, 32, 9, "#0c1210", stroke=BORDER))
    o.append(text(W_ - 225, 83.5, "Oct 2026", 9, MUTED, UI, 500, "middle"))
    o.append(rect(W_ - 152, 64, 122, 32, 9, ACC, None))
    o.append(text(W_ - 91, 83.5, "Export PDF", 9.4, "#04140d", UI, 700, "middle"))
    o.append(line(250, 148, W_, 148, BORDER))
    o.append(text(280, 174, "TODAY", 8, FAINT, UI, 700, "start", "1.6"))
    o.append(chip_row(330, 162, ["Overview", "Inventory", "Sales", "Wholesale", "Expenses"], 0))
    b.append("".join(o))
    # KPI row 4
    cw = (W_ - 250 - 56 - 3 * 16) / 4
    kx = 278
    items = [("Revenue this month", "$286,430", "▲ 18.2%", [3, 3.4, 4.2, 4, 5.2, 5.8, 6.6]),
             ("Inventory value", "$1,428,900", "▲ 6.8%", [3, 4, 3.6, 5, 4.6, 6, 7]),
             ("Open orders", "148", "▲ 22", [3, 3.4, 4, 4.2, 5, 5.4, 6]),
             ("Gross margin", "41.2%", "▲ 2.6 pts", [3, 3.6, 3.4, 4.4, 4.8, 5, 5.6])]
    for i, it in enumerate(items):
        b.append(kpi(kx + i * (cw + 16), 194, cw, 116, *it))
    # big chart
    cy = 330
    lw = 830
    b.append(rect(278, cy, lw, 330, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(298, cy + 28, "Consolidated revenue"))
    b.append(text(298, cy + 50, "Retail + wholesale + online · USD thousands", 9, FAINT))
    for i, (lb, col) in enumerate([("2026", ACC), ("2025", BLUE)]):
        b.append(circle(298 + i * 76, cy + 76, 3.4, col))
        b.append(text(307 + i * 76, cy + 79, lb, 9, MUTED))
    b.append(area_chart(334, cy + 100, lw - 78, 190,
                        [14, 16, 15, 19, 21, 20, 24, 26, 25, 28, 30, 33],
                        ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
                        ymax=40, ticks=4, series2=[11, 12.4, 12, 13.5, 15, 14.6, 16.5, 18, 17.4, 19, 20.4, 22]))
    b.append(pill(278 + lw - 118, cy + 16, 98, 22, "12 months", ACC, 9))
    # right: donut + bars
    rx = 278 + lw + 16
    rw = W_ - rx - 28
    b.append(rect(rx, cy, rw, 158, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 26, "Revenue split"))
    b.append(donut(rx + 76, cy + 92, 42, 13, [(ACC, 46), ("#2f9e77", 28), (BLUE, 17), ("#3b4f47", 9)]))
    b.append(text(rx + 76, cy + 89, "$286K", 14, TXT, DISP, 600, "middle"))
    b.append(text(rx + 76, cy + 102, "month", 7.6, FAINT, UI, 500, "middle"))
    fy = cy + 58
    for label, val, col in [("Retail", "46%", ACC), ("Online", "28%", "#2f9e77"),
                            ("Wholesale", "17%", BLUE), ("Other", "9%", "#3b4f47")]:
        b.append(rect(rx + 142, fy - 7, 7, 7, 2, col))
        b.append(text(rx + 155, fy, label, 8.8, MUTED))
        b.append(text(rx + rw - 20, fy, val, 9, TXT, UI, 600, "end"))
        fy += 24
    b.append(rect(rx, cy + 174, rw, 156, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(rx + 20, cy + 200, "Weekly orders"))
    b.append(bars(rx + 24, cy + 212, rw - 48, 76, [42, 56, 48, 64, 72, 58, 66],
                  ["M", "T", "W", "T", "F", "S", "S"], labelsize=8))
    b.append(text(rx + 20, cy + 322, "5,180 orders", 12, TXT, DISP, 600))
    b.append(text(rx + rw - 20, cy + 322, "▲ 12.4%", 9.4, ACC, UI, 600, "end"))
    # bottom: table + activity
    ty = 678
    tw = 830
    b.append(rect(278, ty, tw, 300, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(text(298, ty + 32, "Reorder pipeline", 13, TXT, UI, 600))
    b.append(text(432, ty + 32, "auto-flagged by the inventory system", 9, FAINT))
    b.append(pill(278 + tw - 122, ty + 18, 102, 22, "Open sheet", ACC, 9))
    rows = [
        [("SKU-10482", MUTED, 500), ("Arctic Pro Headphones", TXT, 600), ("18 / 40", TXT, 600),
         ("__pill__", "Critical", RED), ("$6,420", TXT, 600)],
        [("SKU-41860", MUTED, 500), ("Everyday Cotton Tote", TXT, 600), ("9 / 120", TXT, 600),
         ("__pill__", "Critical", RED), ("$8,760", TXT, 600)],
        [("SKU-20915", MUTED, 500), ("Linen Blend Overshirt", TXT, 600), ("64 / 90", TXT, 600),
         ("__pill__", "Low stock", AMBER), ("$4,180", TXT, 600)],
        [("SKU-33107", MUTED, 500), ("Ceramic Pour-Over Set", TXT, 600), ("142 / 80", TXT, 600),
         ("__pill__", "Healthy", ACC), ("$2,940", TXT, 600)],
        [("SKU-52240", MUTED, 500), ("Walnut Desk Organiser", TXT, 600), ("88 / 60", TXT, 600),
         ("__pill__", "Healthy", ACC), ("$3,320", TXT, 600)],
    ]
    b.append(table(290, ty + 50, tw - 24,
                   [("SKU", .16), ("Product", .34), ("On hand / reorder", .21), ("Status", .17), ("Value", .12)],
                   rows, row_h=38, aligns=["start", "start", "end", "start", "end"]))
    # activity feed
    ax = 278 + tw + 16
    aw = W_ - ax - 28
    b.append(rect(ax, ty, aw, 300, 16, "url(#panelGrad)", stroke=BORDER))
    b.append(section_label(ax + 20, ty + 30, "Automation activity"))
    acts = [("Stock sync completed", "1,204 rows updated", "02:00", ACC),
            ("Invoice batch imported", "38 invoices matched", "06:12", ACC),
            ("Low-stock alert sent", "12 items emailed", "08:30", AMBER),
            ("PO reminder queued", "6 suppliers flagged", "08:31", ACC),
            ("Board pack exported", "PDF · 14 pages", "Fri 17:00", BLUE),
            ("Valuation snapshot saved", "version 4.2", "Fri 17:02", ACC)]
    ay = ty + 62
    for i, (title, meta, time_, col) in enumerate(acts):
        b.append(circle(ax + 26, ay - 4, 4, col))
        if i < len(acts) - 1:
            b.append(line(ax + 26, ay + 3, ax + 26, ay + 26, "#1a2521", 1))
        b.append(text(ax + 40, ay, title, 9.4, TXT, UI, 600))
        b.append(text(ax + 40, ay + 12, meta, 8.2, FAINT))
        b.append(text(ax + aw - 20, ay, time_, 8, FAINT, UI, 500, "end"))
        ay += 38
    b.append(sheet_tabs(H_ - 28, W_, ["Overview", "Inventory", "Sales", "Wholesale", "Expenses", "Reporting"],
                        "Overview", 278))
    return build_doc(W_, H_, "".join(b), BG, DEFS)


# ============ OG image ============
def og():
    W_, H_ = 1200, 630
    b = [f'<rect width="{W_}" height="{H_}" fill="#070a09"/>']
    b.append(circle(1050, 90, 240, ACC, None, 0, 0.07))
    b.append(circle(1050, 90, 240, "none", ACC, 1, 0.12))
    b.append(rect(72, 64, 46, 46, 13, ACC_DARC, stroke="#1f4a38"))
    for i, hh in enumerate([11, 16, 21]):
        b.append(rect(82 + i * 10, 92 - hh, 6, hh, 2.4, ACC if i == 2 else "#1c6b4e"))
    b.append(text(134, 86, "POURIA BUSINESS", 17, TXT, DISP, 700, "start", "1.5"))
    b.append(text(134, 104, "EXCEL AUTOMATION", 9.5, ACC, UI, 700, "start", "3"))
    b.append(text(72, 250, "Excel systems that", 58, TXT, DISP, 600, "start", "-1.4"))
    b.append(text(72, 316, "run your business.", 58, TXT, DISP, 600, "start", "-1.4"))
    b.append(text(72, 380, "Inventory · Sales · Wholesale · Expenses · Reporting", 17, MUTED))
    b.append(rect(72, 434, 250, 52, 12, ACC))
    b.append(text(197, 466, "Explore systems", 14, "#04140d", UI, 700, "middle"))
    b.append(rect(338, 434, 210, 52, 12, "none", "#2a3a34"))
    b.append(text(443, 466, "Book a call", 14, TXT, UI, 600, "middle"))
    # mini chart card
    b.append(rect(760, 176, 372, 232, 18, "url(#panelGrad)", stroke=BORDER))
    b.append(text(784, 208, "Monthly revenue", 10, FAINT, UI, 700, "start", "1.2"))
    b.append(text(784, 244, "$286,430", 30, TXT, DISP, 600))
    b.append(text(940, 244, "▲ 18.2%", 12, ACC, UI, 600))
    b.append(area_chart(796, 268, 306, 112, [12, 15, 13, 19, 18, 24, 22, 27, 29, 33],
                        ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O"], ymax=38, ticks=2))
    b.append(text(72, 560, "pouriaasghari1.github.io/pouriaasghari", 12, FAINT, UI, 500))
    return build_doc(W_, H_, "".join(b), BG, DEFS)


if __name__ == "__main__":
    jobs = {
        "dash-inventory": inventory,
        "dash-sales": sales,
        "dash-wholesale": wholesale,
        "dash-expenses": expenses,
        "dash-reporting": reporting,
        "dash-hero": hero,
        "og-image": og,
    }
    for name, fn in jobs.items():
        svg = fn()
        with open(f"{OUT_SVG}/{name}.svg", "w") as f:
            f.write(svg)
        print("wrote", name, len(svg))
