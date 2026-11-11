"""
Design system for the workbook.

Dark navy + emerald theme, consistent typography and one source of truth for
every colour, so all ten sheets look like one product rather than ten files.
xlsxwriter colours are #RRGGBB.
"""

# ---------------------------------------------------------------------------
# palette
# ---------------------------------------------------------------------------
NAVY_900 = "#0B1220"      # deepest background
NAVY_800 = "#111B2E"      # sheet background
NAVY_700 = "#16233A"      # card / panel
NAVY_600 = "#1D2D47"      # input header band
NAVY_500 = "#243754"      # hover / border

EMERALD = "#2FE0A0"       # primary accent
EMERALD_DK = "#1FA97A"
EMERALD_LT = "#153A30"    # accent wash

AMBER = "#F4C464"
RED = "#F2726F"
BLUE = "#6AA8F6"

WHITE = "#FFFFFF"
TEXT = "#E8EEF7"          # primary text on dark
MUTED = "#9FB0C9"         # secondary text
FAINT = "#6B7E99"         # labels, captions
LINE = "#22334E"          # hairline borders

# Print / light surfaces (a couple of report sheets stay light for printing)
LIGHT_BG = "#FFFFFF"
LIGHT_LINE = "#D9E2EC"
LIGHT_TEXT = "#1B2733"

FONT = "Calibri"
FONT_DISPLAY = "Segoe UI Semibold"

# money / date formats are pulled from Settings via named formats
CURRENCY_FMT = '"$"#,##0.00'
CURRENCY_FMT_0 = '"$"#,##0'
PERCENT_FMT = "0.0%"
INT_FMT = "#,##0"
DATE_FMT = "yyyy-mm-dd"
DATE_FMT_LONG = "dd mmm yyyy"
QTY_FMT = "#,##0"
