#!/usr/bin/env python3
"""
Generates original Excel-dashboard mockups (SVG -> PNG) for the Gridline Systems site.
All artwork is drawn from scratch (no third-party screenshots).
"""
import math, os, subprocess, json

OUT_SVG = "/home/user/pouriaasghari/site-assets-tmp/svg"
OUT_PNG = "/home/user/pouriaasghari/assets/img"
os.makedirs(OUT_SVG, exist_ok=True)
os.makedirs(OUT_PNG, exist_ok=True)

# ---------- theme ----------
BG        = "#070a09"
APP       = "#0a0f0d"
PANEL     = "#0d1311"
PANEL_2   = "#111816"
BORDER    = "#1b2622"
GRID      = "#16201c"
TXT       = "#e9f0ec"
MUTED     = "#87968f"
FAINT     = "#5c6a64"
ACC       = "#34e0a1"
ACC_SOFT  = "#1c6b4e"
ACC_DARC  = "#123024"
AMBER     = "#f4c464"
RED       = "#f2726f"
BLUE      = "#6aa8f6"
VIOLET    = "#a294f7"

DISP = "Space Grotesk"
UI   = "Inter"

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def build_doc(w, h, body, bg=BG, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-synthesis="none">'
            f'<defs>{defs}</defs>'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')

def text(x, y, s, size=13, fill=TXT, font=UI, weight=400, anchor="start",
         ls="0", opacity=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}" opacity="{opacity}">{esc(s)}</text>')

def rect(x, y, w, h, r=0, fill=PANEL, stroke=None, sw=1, opacity=1, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
            f'fill="{fill}"{st} opacity="{opacity}" {extra}/>')

def line(x1, y1, x2, y2, stroke=GRID, sw=1, dash=None, opacity=1, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d} opacity="{opacity}"/>')

def circle(cx, cy, r, fill=ACC, stroke=None, sw=1, opacity=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{st} opacity="{opacity}"/>'

def pill(x, y, w, h, label, color=ACC, size=10.5, weight=600):
    bg = color + "22"
    return (rect(x, y, w, h, h/2, bg, stroke=color + "44") +
            text(x + w/2, y + h/2 + size*0.36, label, size, color, UI, weight, "middle", "0.2"))

def smooth_path(pts, close_base=None, tension=0.22):
    """Catmull-Rom -> cubic bezier smoothing."""
    if len(pts) < 2:
        return ""
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else pts[i + 1]
        c1x = p1[0] + (p2[0] - p0[0]) * tension
        c1y = p1[1] + (p2[1] - p0[1]) * tension
        c2x = p2[0] - (p3[0] - p1[0]) * tension
        c2y = p2[1] - (p3[1] - p1[1]) * tension
        d += f" C{c1x:.2f},{c1y:.2f} {c2x:.2f},{c2y:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    if close_base is not None:
        d += f" L{pts[-1][0]:.2f},{close_base:.2f} L{pts[0][0]:.2f},{close_base:.2f} Z"
    return d

DEFS = f"""
<linearGradient id="fadeAcc" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{ACC}" stop-opacity="0.30"/>
  <stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="fadeBlue" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0.22"/>
  <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="accLine" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{ACC_SOFT}"/><stop offset="1" stop-color="{ACC}"/>
</linearGradient>
<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0f1614"/><stop offset="1" stop-color="#0a0f0d"/>
</linearGradient>
<linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0">
  <stop offset="0" stop-color="#12724f"/><stop offset="1" stop-color="{ACC}"/>
</linearGradient>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="6" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="14"/>
</filter>
<clipPath id="cardClip"><rect x="0" y="0" width="4000" height="4000" rx="16"/></clipPath>
"""

# ---------- spreadsheet app chrome ----------
def excel_chrome(w, title, tabs, active="Home", ribbon_text=None, subtitle="Excel workbook · autosaved"):
    """Fake spreadsheet-app window chrome (Excel-like, original design)."""
    o = []
    o.append(rect(0, 0, w, 44, 0, "#0b100e"))
    o.append(line(0, 44, w, 44, BORDER))
    # logo tile
    o.append(rect(18, 12, 22, 22, 6, ACC_DARC, stroke="#1f4a38"))
    for i, hh in enumerate([7, 10, 13]):
        o.append(rect(23 + i*5, 29 - hh, 3, hh, 1.4, ACC if i == 2 else "#1c6b4e"))
    o.append(text(50, 25, title, 13, TXT, UI, 600))
    o.append(text(50, 37.5, subtitle, 8, FAINT, UI, 400))
    # sheet tabs
    x = w - 18
    for t in reversed(tabs):
        tw = 12 + len(t) * 6.1
        x -= tw + 6
        on = (t == active)
        o.append(rect(x, 13, tw, 21, 6, ACC + "1f" if on else "#121a17",
                      stroke=ACC + "3d" if on else "#1b2622"))
        o.append(text(x + tw/2, 27.5, t, 9.5, ACC if on else MUTED, UI, 600 if on else 500, "middle", "0.3"))
    return "".join(o)

def sheet_tabs(y, w, labels, active, x0=24):
    o = [line(0, y - 14, w, y - 14, BORDER)]
    x = x0
    for lb in labels:
        on = lb == active
        tw = 16 + len(lb) * 6.6
        if on:
            o.append(rect(x, y - 13, tw, 24, 5, "#0d1311", stroke=ACC + "40"))
            o.append(rect(x, y + 9.5, tw, 2, 1, ACC))
        o.append(text(x + tw/2, y + 3, lb, 10, ACC if on else FAINT, UI, 600 if on else 500, "middle", "0.2"))
        x += tw + 4
    return "".join(o)

# ---------- data widget painters ----------
def kpi(x, y, w, h, label, value, delta, up=True, spark=None, icon=None, accent=ACC):
    o = [rect(x, y, w, h, 14, "url(#panelGrad)", stroke=BORDER)]
    o.append(text(x + 16, y + 22, label.upper(), 8.5, FAINT, UI, 700, "start", "1.4"))
    o.append(text(x + 16, y + 50, value, 24, TXT, DISP, 600, "start", "-0.6"))
    dcol = accent if up else RED
    o.append(text(x + 16, y + 70, delta, 9.5, dcol, UI, 600))
    if spark:
        pts = [(x + w - 84 + i * (68 / (len(spark) - 1)),
                y + h - 20 - (v / max(spark)) * 34) for i, v in enumerate(spark)]
        o.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>')
        o.append(circle(pts[-1][0], pts[-1][1], 2.6, accent))
    return "".join(o)

def area_chart(x, y, w, h, series, labels, ymax=None, ticks=4, color=ACC, grad="fadeAcc", series2=None, series2_color=BLUE):
    o = []
    ymax = ymax or max(series) * 1.18
    # grid + y labels
    for i in range(ticks + 1):
        gy = y + h - (h * i / ticks)
        o.append(line(x, gy, x + w, gy, GRID, 1, "2 4" if i else None, 1 if i == 0 else 0.75))
        val = ymax * i / ticks
        lbl = f"{val:.1f}" if val < 10 else (f"{val:,.0f}" if val < 1000 else f"{val/1000:,.0f}k")
        o.append(text(x - 8, gy + 3, lbl, 8.5, FAINT, UI, 500, "end"))
    step = w / (len(series) - 1)
    pts = [(x + i * step, y + h - (v / ymax) * h) for i, v in enumerate(series)]
    o.append(f'<path d="{smooth_path(pts, close_base=y+h)}" fill="url(#{grad})"/>')
    o.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')
    if series2:
        p2 = [(x + i * step, y + h - (v / ymax) * h) for i, v in enumerate(series2)]
        o.append(f'<path d="{smooth_path(p2)}" fill="none" stroke="{series2_color}" stroke-width="1.8" '
                 f'stroke-dasharray="5 5" stroke-linecap="round" opacity="0.85"/>')
    for i, p in enumerate(pts):
        if i == len(pts) - 1:
            o.append(circle(p[0], p[1], 4.4, color, BG, 2.4))
            o.append(text(p[0] - 4, p[1] - 12, f"{series[-1]:,.0f}", 9.5, color, UI, 700, "end"))
    for i, lb in enumerate(labels):
        o.append(text(x + i * step, y + h + 16, lb, 8.5, FAINT, UI, 500, "middle"))
    return "".join(o)

def bars(x, y, w, h, data, labels, colors=None, gap=0.34, labelsize=8.5, value_size=9):
    o = []
    n = len(data)
    bw = w / n * (1 - gap)
    step = w / n
    ymax = max(data) * 1.12
    for i, v in enumerate(data):
        bh = max(3, (v / ymax) * h)
        bx = x + i * step + (step - bw) / 2
        by = y + h - bh
        c = colors[i] if colors else "url(#barGrad)"
        o.append(rect(bx, by, bw, bh, 4, c, opacity=1))
        o.append(rect(bx, by, bw, min(bh, 3.5), 2, "#ffffff", opacity=0.18))
        o.append(text(bx + bw/2, y + h + 15, labels[i], labelsize, FAINT, UI, 500, "middle"))
    return "".join(o)

def donut(cx, cy, r, thick, segs, track="#151f1b"):
    o = [circle(cx, cy, r, "none", track, thick)]
    total = sum(s[1] for s in segs)
    a0 = -90
    for color, val, *_ in segs:
        sweep = 360 * val / total
        a1 = a0 + sweep - 2.2
        large = 1 if (a1 - a0) > 180 else 0
        rad = math.radians
        x0, y0 = cx + r * math.cos(rad(a0)), cy + r * math.sin(rad(a0))
        x1, y1 = cx + r * math.cos(rad(a1)), cy + r * math.sin(rad(a1))
        o.append(f'<path d="M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f}" '
                 f'stroke="{color}" stroke-width="{thick}" fill="none" stroke-linecap="round"/>')
        a0 += sweep
    return "".join(o)

def table(x, y, w, cols, rows, row_h=30, head=9, sizes=None, aligns=None):
    """cols: [(title, width_frac)] ; rows: [[cell widgets as (text, color, weight)]]"""
    o = []
    widths = [w * c[1] for c in cols]
    o.append(rect(x, y, w, row_h, 8, "#0e1513"))
    cx = x
    for i, (title, _) in enumerate(cols):
        al = (aligns or ["start"] * len(cols))[i]
        tx = cx + 12 if al == "start" else (cx + widths[i] - 12 if al == "end" else cx + widths[i]/2)
        o.append(text(tx, y + row_h/2 + 3.4, title.upper(), head, FAINT, UI, 700, al, "1.1"))
        cx += widths[i]
    ry = y + row_h
    for ri, row in enumerate(rows):
        if ri % 2 == 0:
            o.append(rect(x, ry, w, row_h, 0, "#0b110f", opacity=0.6))
        o.append(line(x, ry, x + w, ry, "#141d1a"))
        cx = x
        for ci, cell in enumerate(row):
            al = (aligns or ["start"] * len(cols))[ci]
            tx = cx + 12 if al == "start" else (cx + widths[ci] - 12 if al == "end" else cx + widths[ci]/2)
            if isinstance(cell, tuple) and cell and cell[0] == "__pill__":
                _, label, color = cell
                pw = 18 + len(label) * 5.4
                px = cx + 12 if al == "start" else cx + widths[ci] - 12 - pw
                o.append(pill(px, ry + row_h/2 - 8.5, pw, 17, label, color, 9.5))
            elif isinstance(cell, tuple) and cell and cell[0] == "__bar__":
                _, frac, color = cell
                bw = widths[ci] - 30
                o.append(rect(cx + 12, ry + row_h/2 - 3, bw, 6, 3, "#16211d"))
                o.append(rect(cx + 12, ry + row_h/2 - 3, bw * frac, 6, 3, color))
                o.append(text(cx + 12 + bw + 8, ry + row_h/2 + 3, f"{int(frac*100)}%", 9, MUTED, UI, 600))
            else:
                if isinstance(cell, tuple):
                    t, c, wt = (list(cell) + [MUTED, 500])[:3]
                else:
                    t, c, wt = (cell, MUTED, 500)
                o.append(text(tx, ry + row_h/2 + 3.6, str(t), (sizes or [10]*len(cols))[ci], c, UI, wt, al))
            cx += widths[ci]
        ry += row_h
    return "".join(o) + line(x, ry, x + w, ry, "#1a2521")

def panel_header(x, y, title, sub=None, right=None, rightcolor=ACC):
    o = [text(x, y, title, 12, TXT, UI, 600)]
    if sub:
        o.append(text(x, y + 15, sub, 9, FAINT, UI, 400))
    if right:
        o.append(text(x + 0, y, right, 9, rightcolor, UI, 600))
    return "".join(o)

def section_label(x, y, s, color=FAINT):
    return text(x, y, s.upper(), 8.5, color, UI, 700, "start", "1.6")

def chip_row(x, y, items, active=0):
    o = []
    for i, it in enumerate(items):
        tw = 14 + len(it) * 6.2
        on = i == active
        o.append(rect(x, y, tw, 22, 11, ACC + "1c" if on else "#101715", stroke=ACC + "3a" if on else BORDER))
        o.append(text(x + tw/2, y + 14.6, it, 9.5, ACC if on else MUTED, UI, 600 if on else 500, "middle"))
        x += tw + 7
    return "".join(o)

def spark_pts(x, y, w, h, vals, color=ACC, fill=False):
    pts = [(x + i * w/(len(vals)-1), y + h - (v/max(vals))*h) for i, v in enumerate(vals)]
    o = []
    if fill:
        o.append(f'<path d="{smooth_path(pts, close_base=y+h)}" fill="{color}" opacity="0.12"/>')
    o.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{color}" stroke-width="1.9" stroke-linecap="round"/>')
    return "".join(o)
