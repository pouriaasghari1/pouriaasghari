"""
Builds Pouria Business — Smart Inventory & Sales Manager as a real .xlsx.

Design notes
------------
* Columns hold raw inputs. Every derived column (amounts, stock, status) is a
  live formula, so adding a row on a data sheet immediately flows through the
  inventory, dashboard and reports.
* Formulas reference plain ranges (e.g. SalesData!$F$2:$F$1500) rather than
  table structured references. This is deliberate: it keeps the workbook
  calculable by third-party engines (so the build can be verified
  automatically) and it is what Excel writes anyway once you add a row.
* Input columns are unlocked and tinted; formula columns are locked and greyed.
  Sheet protection is on by default with no password, so a shop assistant
  cannot overwrite a formula but the owner can unprotect in one click.
"""

from __future__ import annotations

import datetime as dt

import xlsxwriter

from theme import *          # noqa: F401,F403  (palette + number formats)
import sample_data as S

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
DATA_ROWS = 1500            # usable record rows on every data sheet
PRODUCT_ROWS = 500          # product master size
FIRST_DATA_ROW = 2          # 1-based row number of the first record (row 2)
LAST_DATA_ROW = DATA_ROWS + 1

# Sheet names (kept short so formulas stay readable)
SH_DASH = "Dashboard"
SH_PROD = "Products"
SH_SALES = "Sales"
SH_PURCH = "Purchases"
SH_INV = "Inventory"
SH_CUST = "Customers"
SH_SUP = "Suppliers"
SH_EXP = "Expenses"
SH_REP = "Reports"
SH_SET = "Settings"

# Settings cell addresses for the business profile block.
# The block header sits in row 5, so the first field is row 6.
SET_NAME = "$C$6"
SET_CURRENCY = "$C$7"
SET_SYMBOL = "$C$8"
SET_TAX = "$C$9"
SET_FISCAL = "$C$10"
SET_LOWSTOCK = "$C$11"
SET_ASOF = "$C$12"
SET_OWNER = "$C$13"

# Hidden calculation sheets
SH_SD = "SalesData"
SH_PD = "PurchaseData"
SH_LISTS = "Lists"


def rng(sheet, col, first=FIRST_DATA_ROW, last=LAST_DATA_ROW):
    """Absolute-range helper, e.g. rng('SalesData','F') -> SalesData!$F$2:$F$1501"""
    return f"{sheet}!${col}${first}:${col}${last}"


def prng(sheet, col):
    """Product-master range (products sheet is smaller)."""
    return f"{sheet}!${col}$2:${col}${PRODUCT_ROWS + 1}"


class Workbook:
    def __init__(self, path: str):
        self.path = path
        self.wb = xlsxwriter.Workbook(path, {"default_date_format": DATE_FMT})
        self._formats = {}
        self._define_formats()
        self.sheets = {}
        self._create_sheets()

    # ------------------------------------------------------------------
    # formats
    # ------------------------------------------------------------------
    def _define_formats(self):
        f = self._formats

        def add(name, **kw):
            base = {"font_name": FONT, "font_size": 11, "font_color": TEXT,
                    "bg_color": NAVY_800, "valign": "vcenter"}
            base.update(kw)
            f[name] = self.wb.add_format(base)

        # --- typography -------------------------------------------------
        add("title", font_name=FONT_DISPLAY, font_size=26, bold=True,
            font_color=WHITE, bg_color=NAVY_900)
        add("subtitle", font_size=11, font_color=MUTED, bg_color=NAVY_900)
        add("h1", font_name=FONT_DISPLAY, font_size=16, bold=True, font_color=WHITE)
        add("h2", font_size=12, bold=True, font_color=WHITE)
        add("label", font_size=9, bold=True, font_color=FAINT)
        add("body", font_size=10.5, font_color=TEXT)
        add("muted", font_size=10.5, font_color=MUTED)
        add("faint", font_size=9.5, font_color=FAINT)
        add("link", font_size=10.5, font_color=EMERALD, underline=1)

        # --- table head / cells -----------------------------------------
        add("th", bold=True, font_size=10, font_color=NAVY_900,
            bg_color=EMERALD, align="left", border=1, border_color=NAVY_900,
            text_wrap=True, valign="vcenter")
        add("th_num", bold=True, font_size=10, font_color=NAVY_900,
            bg_color=EMERALD, align="right", border=1, border_color=NAVY_900,
            text_wrap=True, valign="vcenter")
        add("th_sys", bold=True, font_size=10, font_color=TEXT,
            bg_color=NAVY_600, align="left", border=1, border_color=NAVY_500,
            text_wrap=True)

        # input cells (owner can type here)
        add("in_txt", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, align="left")
        add("in_num", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, num_format=INT_FMT)
        add("in_money", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, num_format=CURRENCY_FMT)
        add("in_pct", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, num_format="0.0")
        add("in_date", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, num_format=DATE_FMT, align="left")

        # formula cells (locked, visually distinct)
        add("fx_txt", font_size=10.5, font_color=MUTED, bg_color=NAVY_800,
            border=1, border_color=LINE, align="left")
        add("fx_num", font_size=10.5, font_color=TEXT, bg_color=NAVY_800,
            border=1, border_color=LINE, num_format=INT_FMT)
        add("fx_money", font_size=10.5, font_color=TEXT, bg_color=NAVY_800,
            border=1, border_color=LINE, num_format=CURRENCY_FMT)
        add("fx_date", font_size=10.5, font_color=MUTED, bg_color=NAVY_800,
            border=1, border_color=LINE, num_format=DATE_FMT, align="left")
        add("fx_bold", font_size=10.5, bold=True, font_color=WHITE,
            bg_color=NAVY_800, border=1, border_color=LINE, align="left")

        # --- KPI cards ---------------------------------------------------
        add("kpi_label", font_size=9, bold=True, font_color=FAINT,
            bg_color=NAVY_700, align="left", top=1, left=1, right=1,
            top_color=NAVY_500, left_color=NAVY_500, right_color=NAVY_500)
        add("kpi_value", font_name=FONT_DISPLAY, font_size=21, bold=True,
            font_color=EMERALD, bg_color=NAVY_700, align="left",
            left=1, right=1, left_color=NAVY_500, right_color=NAVY_500,
            num_format=CURRENCY_FMT_0)
        add("kpi_value_int", font_name=FONT_DISPLAY, font_size=21, bold=True,
            font_color=WHITE, bg_color=NAVY_700, align="left",
            left=1, right=1, left_color=NAVY_500, right_color=NAVY_500,
            num_format=INT_FMT)
        add("kpi_value_plain", font_name=FONT_DISPLAY, font_size=21, bold=True,
            font_color=WHITE, bg_color=NAVY_700, align="left",
            left=1, right=1, left_color=NAVY_500, right_color=NAVY_500)
        add("kpi_foot", font_size=9, font_color=MUTED, bg_color=NAVY_700,
            align="left", bottom=1, left=1, right=1,
            bottom_color=NAVY_500, left_color=NAVY_500, right_color=NAVY_500)
        add("kpi_value_r", font_name=FONT_DISPLAY, font_size=21, bold=True,
            font_color=RED, bg_color=NAVY_700, align="left",
            left=1, right=1, left_color=NAVY_500, right_color=NAVY_500,
            num_format=INT_FMT)
        add("kpi_value_amber", font_name=FONT_DISPLAY, font_size=21, bold=True,
            font_color=AMBER, bg_color=NAVY_700, align="left",
            left=1, right=1, left_color=NAVY_500, right_color=NAVY_500,
            num_format=INT_FMT)

        # --- sections / nav ---------------------------------------------
        add("nav", font_size=10.5, font_color=TEXT, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, align="center")
        add("nav_active", font_size=10.5, bold=True, font_color=NAVY_900,
            bg_color=EMERALD, border=1, border_color=EMERALD, align="center")
        add("section", font_name=FONT_DISPLAY, font_size=13, bold=True,
            font_color=WHITE, bg_color=NAVY_800, align="left")
        add("card_head", font_size=10, bold=True, font_color=NAVY_900,
            bg_color=TEXT, align="left", border=1, border_color=NAVY_500)
        add("band", font_size=10, bold=True, font_color=WHITE, bg_color=NAVY_600,
            align="left", border=1, border_color=NAVY_500)
        add("note", font_size=9, font_color=FAINT, bg_color=NAVY_800, align="left",
            text_wrap=True)
        add("note_box", font_size=9.5, font_color=MUTED, bg_color=NAVY_700,
            align="left", text_wrap=True, valign="top",
            border=1, border_color=NAVY_500)

        # --- status pills ------------------------------------------------
        add("pill_ok", font_size=9.5, bold=True, font_color="#0B2A20",
            bg_color=EMERALD, align="center", border=1, border_color=EMERALD)
        add("pill_low", font_size=9.5, bold=True, font_color="#3A2A05",
            bg_color=AMBER, align="center", border=1, border_color=AMBER)
        add("pill_out", font_size=9.5, bold=True, font_color="#3A0F0E",
            bg_color=RED, align="center", border=1, border_color=RED)

        # plain variants of the numeric cells for report sheets
        add("fx_pct", font_size=10.5, font_color=TEXT, bg_color=NAVY_800,
            border=1, border_color=LINE, num_format="0.0%")
        add("in_pct_cell", font_size=10.5, font_color=WHITE, bg_color=NAVY_700,
            border=1, border_color=NAVY_500, num_format="0.0%")
        add("fx_money_plain", font_size=10.5, font_color=TEXT,
            num_format=CURRENCY_FMT)
        add("fx_num_plain", font_size=10.5, font_color=TEXT, num_format=INT_FMT)

    def fmt(self, name):
        return self._formats[name]

    def pct_format(self):
        return self._formats["in_pct_cell"]

    # ------------------------------------------------------------------
    # sheets
    # ------------------------------------------------------------------
    def _create_sheets(self):
        wb = self.wb
        self.ws = {}
        for name in [SH_DASH, SH_PROD, SH_SALES, SH_PURCH, SH_INV,
                     SH_CUST, SH_SUP, SH_EXP, SH_REP, SH_SET]:
            self.ws[name] = wb.add_worksheet(name)
        # hidden working sheets
        self.ws[SH_SD] = wb.add_worksheet(SH_SD)
        self.ws[SH_PD] = wb.add_worksheet(SH_PD)
        self.ws[SH_LISTS] = wb.add_worksheet(SH_LISTS)
        for name in (SH_SD, SH_PD, SH_LISTS):
            self.ws[name].hide()

        # Named ranges are declared here, before any sheet writes a formula that
        # uses them. Excel resolves names at load time, but a calculation engine
        # (and any third-party tool) needs them to exist when it parses.
        wb.define_name("TaxRate", f"='{SH_SET}'!{SET_TAX}")
        wb.define_name("BusinessName", f"='{SH_SET}'!{SET_NAME}")
        wb.define_name("CurrencyCode", f"='{SH_SET}'!{SET_CURRENCY}")
        wb.define_name("CurrencySymbol", f"='{SH_SET}'!{SET_SYMBOL}")
        wb.define_name("LowStockDefault", f"='{SH_SET}'!{SET_LOWSTOCK}")
        wb.define_name("DataAsOf", f"='{SH_SET}'!{SET_ASOF}")

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def sheet_bg(self, name, last_col, last_row):
        """Paint the dark background across a range so the sheet looks designed."""
        ws = self.ws[name]
        ws.set_column(0, last_col, 12)
        blank = self.wb.add_format({"bg_color": NAVY_800, "font_name": FONT})
        # only paint the visible block; keeps file size sane
        for r in range(0, last_row):
            ws.write_blank(r, last_col, None, blank)

    def header_block(self, name, kicker, title, subtitle, last_col):
        ws = self.ws[name]
        ws.hide_gridlines(2)
        ws.set_row(0, 44)
        ws.set_row(1, 6)
        ws.merge_range(0, 0, 0, last_col, "", self.fmt("title"))
        ws.write(0, 0, title, self.fmt("title"))
        ws.write(0, last_col - 2, kicker, self.fmt("label"))
        ws.merge_range(2, 0, 2, last_col, subtitle, self.fmt("subtitle"))

    def nav_row(self, name, last_col, active):
        """Navigation strip that links every sheet — the workbook's 'menu'."""
        ws = self.ws[name]
        order = [SH_DASH, SH_PROD, SH_SALES, SH_PURCH, SH_INV,
                 SH_CUST, SH_SUP, SH_EXP, SH_REP, SH_SET]
        # place nav starting at column 0, one column per sheet, 2 cols apart
        col = 0
        for sh in order:
            style = "nav_active" if sh == active else "nav"
            ws.merge_range(3, col, 3, col + 1, "", self.fmt(style))
            ws.write_url(3, col, f"internal:'{sh}'!A1", self.fmt(style), sh)
            col += 2
        ws.set_row(3, 24)

    def data_validation_helpers(self):
        """Named ranges used by dropdowns across the workbook."""
        ws = self.ws[SH_LISTS]
        ws.write_column(0, 0, ["Products"] + [p["id"] + " — " + p["name"] for p in S.PRODUCTS])
        ws.write_column(0, 1, ["Categories"] + S.CATEGORIES)
        ws.write_column(0, 2, ["Customers"] + [c["id"] + " — " + c["name"] for c in S.CUSTOMERS])
        ws.write_column(0, 3, ["Suppliers"] + [s["id"] + " — " + s["name"] for s in S.SUPPLIERS])
        ws.write_column(0, 4, ["Expense Categories"] + S.EXPENSE_CATEGORIES)
        ws.write_column(0, 5, ["Payment Methods"] + S.PAYMENT_METHODS)
        ws.write_column(0, 6, ["Payment Status"] + ["Paid", "Part paid", "Unpaid"])
        ws.write_column(0, 7, ["Supplier Status"] + ["Active", "On hold", "Inactive"])
        ws.write_column(0, 8, ["Customer Type"] + ["Retail", "Wholesale"])
        ws.write_column(0, 9, ["Yes No"] + ["Yes", "No"])
        ws.write_column(0, 10, ["Currencies"] + ["USD", "EUR", "GBP", "AED", "SEK"])
        ws.write_column(0, 11, ["Months (names)"] + [dt.date(2026, m, 1).strftime("%B") for m in range(1, 13)])
