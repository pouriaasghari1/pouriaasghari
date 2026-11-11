#!/usr/bin/env python3
"""
Generate User_Guide.pdf for Pouria Business — Smart Inventory & Sales Manager.

Written with reportlab platypus so the guide is a real, selectable-text PDF
rather than an exported screenshot of the workbook.
"""

from __future__ import annotations

import os
import sys
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, NextPageTemplate,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_DIR = os.path.join(ROOT, "products", "smart-inventory-sales-manager")
OUT = os.path.join(OUT_DIR, "User_Guide.pdf")

# ---------------------------------------------------------------------------
# palette (matches the workbook)
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#0B1220")
NAVY_SOFT = colors.HexColor("#16233A")
EMERALD = colors.HexColor("#1FA97A")
EMERALD_LT = colors.HexColor("#E6F7F0")
TEXT = colors.HexColor("#1B2733")
MUTED = colors.HexColor("#5A6B7B")
LINE = colors.HexColor("#D9E2EC")
AMBER_BG = colors.HexColor("#FFF6E0")
WARN = colors.HexColor("#B8860B")

styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold",
                    fontSize=22, leading=26, textColor=NAVY, spaceAfter=4,
                    alignment=TA_LEFT)
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontName="Helvetica",
                     fontSize=11, leading=15, textColor=MUTED, spaceAfter=14)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13.5, leading=17, textColor=NAVY,
                    spaceBefore=14, spaceAfter=6)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=11, leading=14, textColor=EMERALD,
                    spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=9.6, leading=13.6, textColor=TEXT, spaceAfter=6)
SMALL = ParagraphStyle("SMALL", parent=BODY, fontSize=8.4, leading=11.5,
                       textColor=MUTED)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=11, bulletIndent=2,
                        spaceAfter=3)
CODE = ParagraphStyle("CODE", parent=BODY, fontName="Courier",
                      fontSize=8.2, leading=11, textColor=NAVY_SOFT,
                      backColor=EMERALD_LT, borderPadding=4, spaceAfter=6)


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(path, pagesize=A4,
                         leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=17 * mm, bottomMargin=17 * mm,
                         title="User Guide — Smart Inventory & Sales Manager",
                         author="Pouria Asghari",
                         subject="How to install, set up and use the workbook",
                         creator="Pouria Business", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="body")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=self._cover),
            PageTemplate(id="body", frames=[frame], onPage=self._later),
        ])

    def _cover(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        canvas.setFillColor(EMERALD)
        canvas.rect(0, A4[1] - 6, A4[0], 6, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(18 * mm, A4[1] - 22 * mm, "POURIA BUSINESS")
        canvas.setFillColor(EMERALD)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18 * mm, A4[1] - 27 * mm, "EXCEL AUTOMATION")
        canvas.setFillColor(colors.HexColor("#9FB0C9"))
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(18 * mm, 14 * mm,
                          "Pouria Business  ·  pouriabusines1@gmail.com  ·  @pouria_busines")
        canvas.drawRightString(A4[0] - 18 * mm, 14 * mm, "Version 1.0")
        canvas.restoreState()

    def _later(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, A4[1] - 12 * mm, A4[0] - 18 * mm, A4[1] - 12 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(18 * mm, A4[1] - 10 * mm,
                          "Smart Inventory & Sales Manager — User Guide")
        canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, f"Page {doc.page}")
        canvas.drawString(18 * mm, 11 * mm, "Pouria Business")
        canvas.restoreState()


def table(data, widths, header=True, zebra=True):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY_SOFT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8.6),
        ]
    if zebra:
        for r in range(1, len(data)):
            if r % 2 == 0:
                cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F7FAFC")))
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body):
    t = Table([[Paragraph(f"<b>{title}</b><br/>{body}", SMALL)]],
              colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
        ("BOX", (0, 0), (-1, -1), 0.6, WARN),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = Doc(OUT)
    S = []

    # ---------------- cover ----------------
    S.append(Spacer(1, 62 * mm))
    S.append(Paragraph(
        '<font color="#FFFFFF" size="25"><b>Smart Inventory &amp;<br/>Sales Manager</b></font>',
        ParagraphStyle("cv", parent=BODY, leading=30)))
    S.append(Spacer(1, 6 * mm))
    S.append(Paragraph(
        '<font color="#2FE0A0" size="12">User Guide</font>',
        ParagraphStyle("cv2", parent=BODY)))
    S.append(Spacer(1, 9 * mm))
    S.append(Paragraph(
        '<font color="#9FB0C9" size="9.5">A complete Excel system for products, stock, '
        'purchases, sales, customers, suppliers, expenses and reporting — built with standard '
        'formulas, no macros and no external dependencies.</font>',
        ParagraphStyle("cv3", parent=BODY, leading=15)))
    S.append(Spacer(1, 55 * mm))
    S.append(Paragraph(
        '<font color="#9FB0C9" size="8">Pouria Business · Excel Automation<br/>'
        'pouriabusines1@gmail.com · instagram.com/pouria_busines · t.me/pouria_busines</font>',
        ParagraphStyle("cv4", parent=BODY, leading=13)))
    S.append(NextPageTemplate("body"))
    S.append(PageBreak())

    # ---------------- contents ----------------
    S.append(Paragraph("What is in this guide", H1))
    S.append(Paragraph(
        "This guide takes you from a fresh copy of the workbook to a working system with your own "
        "products and your first invoice. It takes about fifteen minutes to read and about the same "
        "to set up for a small catalogue.", SUB))

    S.append(table([
        ["Section", "What it covers"],
        ["1. Before you start", "Excel requirements, file handling, what the colours mean"],
        ["2. The ten sheets", "What each sheet is for and who uses it"],
        ["3. First-time setup", "Business details, categories, your products"],
        ["4. Daily use", "Recording a purchase, an invoice, an expense"],
        ["5. Reading the dashboard", "What every KPI means and when to act on it"],
        ["6. Reports", "Monthly and annual performance, printing"],
        ["7. Protecting your data", "Backups, sheet protection, what not to edit"],
        ["8. Troubleshooting", "The six things that actually go wrong, and the fix"],
        ["9. Starting clean", "Removing the demo records before going live"],
    ], [40 * mm, 134 * mm]))
    S.append(PageBreak())

    # ---------------- 1 ----------------
    S.append(Paragraph("1. Before you start", H1))

    S.append(Paragraph("Requirements", H2))
    S.append(Paragraph(
        "Microsoft Excel 2016 or newer on Windows or macOS, or Microsoft 365. Excel for the web "
        "works but is slower on large ranges. LibreOffice Calc opens the file and most formulas "
        "calculate, but charts and conditional formatting do not always match Excel exactly, so "
        "Excel is the supported environment.", BODY))

    S.append(Paragraph("What the colours mean", H2))
    S.append(table([
        ["Colour", "Meaning", "Can I type here?"],
        ["White text on dark blue", "An input cell — product names, quantities, prices", "Yes"],
        ["Grey text on navy", "A formula cell — totals, stock levels, statuses", "No (locked)"],
        ["Green", "A good result: in stock, paid, profitable", "—"],
        ["Amber", "Something needs attention: low stock, part paid, balance due", "—"],
        ["Red", "A problem: out of stock, unpaid and overdue", "—"],
    ], [42 * mm, 92 * mm, 40 * mm]))
    S.append(Spacer(1, 4 * mm))
    S.append(callout(
        "No password on protection",
        "Every data sheet is protected so a formula cannot be overwritten by accident, but there is "
        "no password. To edit structure, go to <b>Review &gt; Unprotect Sheet</b>."))

    S.append(Paragraph("Files in this product", H2))
    S.append(table([
        ["File", "Use it for"],
        ["Pouria_Business_Inventory_Manager.xlsx", "The real product, with a full year of demo data so you can see every feature working"],
        ["Sample_Data.xlsx", "Same workbook, all records empty — start your live business here"],
        ["User_Guide.pdf", "This document"],
    ], [72 * mm, 102 * mm]))

    S.append(PageBreak())

    # ---------------- 2 ----------------
    S.append(Paragraph("2. The ten sheets", H1))
    S.append(Paragraph(
        "The navigation strip at the top of every sheet links to all ten. The three sheets at the end "
        "(SalesData, PurchaseData, Lists) are hidden on purpose and are explained in section 7.", BODY))
    S.append(table([
        ["Sheet", "What it does", "Who uses it"],
        ["Dashboard", "Twelve KPIs, a monthly sales chart, top products, recent invoices and a reorder list", "Owner, manager"],
        ["Products", "Your catalogue: cost, selling price, minimum stock, live stock status", "Owner, buying"],
        ["Sales", "One row per invoice: amounts, tax, profit and payment status calculate themselves", "Sales, admin"],
        ["Purchases", "One row per delivery from a supplier; raises stock automatically", "Buying, warehouse"],
        ["Inventory", "Live stock position with reorder quantities and out-of-stock flags", "Warehouse"],
        ["Customers", "Customer database plus lifetime value and outstanding balance", "Sales"],
        ["Suppliers", "Supplier database plus order count and total spend", "Buying"],
        ["Expenses", "Operating costs by category and date", "Owner, accounts"],
        ["Reports", "Month-by-month sales, profit and expenses; annual summary", "Owner, accountant"],
        ["Settings", "Business name, currency, tax rate, and every dropdown list", "Owner"],
    ], [30 * mm, 104 * mm, 40 * mm]))

    S.append(Paragraph("How the sheets fit together", H2))
    S.append(Paragraph(
        "You only ever type on five sheets: Products, Sales, Purchases, Expenses and Customers/"
        "Suppliers. Everything else is calculated. A sale recorded on the Sales sheet immediately "
        "reduces stock on Products, changes the Inventory status, appears in the Dashboard KPIs and "
        "lands in the monthly Reports table. You never update the same figure twice.", BODY))

    S.append(PageBreak())

    # ---------------- 3 ----------------
    S.append(Paragraph("3. First-time setup", H1))

    S.append(Paragraph("Step 1 — business details", H2))
    S.append(Paragraph(
        "Open <b>Settings</b> and fill in the business profile block: business name, currency code and "
        "symbol, tax rate, fiscal year start and low-stock default. The tax rate is a percentage "
        "(9% is entered as <b>0.09</b>) and is used by every invoice, purchase order and expense.", BODY))

    S.append(Paragraph("Step 2 — categories", H2))
    S.append(Paragraph(
        "The category list in Settings feeds the dropdown on the Products sheet and the "
        "“Sales by category” table in Reports. Add or rename categories there, never by typing a new "
        "category directly into the Products sheet — a typo creates a second, separate category in "
        "your reports.", BODY))

    S.append(Paragraph("Step 3 — your products", H2))
    S.append(Paragraph(
        "On <b>Products</b>, each row is one product. The first nine columns are yours to fill:", BODY))
    S.append(table([
        ["Column", "What to enter", "Example"],
        ["Product ID", "A short unique code — never reuse one", "PRD-001"],
        ["Product Name", "What you call it on an invoice", "A5 Dotted Notebook — Charcoal"],
        ["Category", "Pick from the dropdown built from Settings", "Notebooks"],
        ["SKU", "Your own stock-keeping code, if you have one", "NB-A5-CHR"],
        ["Supplier", "Pick the supplier ID from the dropdown", "SUP-002 — Baltic Print & Pack"],
        ["Cost Price", "What you pay per unit", "4.20"],
        ["Selling Price", "What you charge per unit, before discount", "7.80"],
        ["Min Stock", "Reorder point — the level that triggers an alert", "120"],
        ["Opening Stock", "How many you hold on day one", "400"],
    ], [30 * mm, 88 * mm, 56 * mm]))
    S.append(Spacer(1, 2 * mm))
    S.append(Paragraph(
        "The remaining five columns — Purchased, Sold, Current Stock, Stock Value and Stock Status — "
        "are formulas. Do not type in them.", SMALL))

    S.append(PageBreak())

    # ---------------- 4 ----------------
    S.append(Paragraph("4. Daily use", H1))

    S.append(Paragraph("Recording a purchase (a delivery arrives)", H2))
    S.append(Paragraph(
        "Go to <b>Purchases</b>. Enter the PO number, the date and the supplier ID. The sheet adds up "
        "everything that has that PO number in the purchase lines. To add the individual products, "
        "use the hidden PurchaseData sheet (Unprotect Sheet first, add one row per product: date, "
        "product ID, supplier, PO number, quantity, unit cost). Stock on Products rises immediately.", BODY))

    S.append(Paragraph("Recording a sale (an invoice is issued)", H2))
    S.append(Paragraph(
        "Go to <b>Sales</b>. Enter the invoice number, date and customer ID. The visible sheet then "
        "calculates items, subtotal, tax, invoice total, amount paid, balance, payment status, due "
        "date, days overdue, profit and margin. The sale lines themselves live on the hidden "
        "SalesData sheet, one row per product sold.", BODY))
    S.append(callout(
        "Why there are hidden data sheets",
        "An invoice with four products is one row on the Sales sheet but four rows of quantities. "
        "Keeping the quantities on a separate line sheet is how real accounting systems work: the "
        "invoice stays readable while the detail stays complete. The visible amounts are SUMIFs over "
        "those lines, so the two can never disagree."))

    S.append(Paragraph("Recording an expense", H2))
    S.append(Paragraph(
        "Use <b>Expenses</b>: date, category (dropdown), description, who you paid, and the amount "
        "before tax. Tax and total calculate automatically. Expenses reduce net profit but never "
        "touch stock.", BODY))

    S.append(Paragraph("Adding a customer or supplier", H2))
    S.append(Paragraph(
        "Add them on Customers or Suppliers <b>first</b>, then pick the ID from the dropdown on "
        "Sales or Purchases. The dropdowns read the ID column, so a new customer appears in the list "
        "as soon as the row is filled in.", BODY))

    S.append(PageBreak())

    # ---------------- 5 ----------------
    S.append(Paragraph("5. Reading the dashboard", H1))
    S.append(Paragraph(
        "Twelve KPI cards in three bands, then a monthly sales chart, your five best products, the "
        "eight most recent invoices and a live reorder list. Every figure recalculates when you open "
        "the file.", BODY))
    S.append(table([
        ["KPI", "What it tells you", "Act when"],
        ["Total sales", "Value of all invoices, excluding tax", "—"],
        ["Gross profit", "Sales minus the cost of what you sold", "Margin falls below ~30%"],
        ["Net profit", "Gross profit minus operating expenses", "It goes negative"],
        ["Purchases", "Total spend with suppliers", "It outruns sales for 2+ months"],
        ["Expenses", "All operating costs recorded", "A category creeps up"],
        ["Inventory value", "Stock on hand at cost price", "It balloons — cash is sitting on shelves"],
        ["Products", "Active SKUs in the catalogue", "—"],
        ["Low stock", "Products at or below minimum level", "Every day — reorder these"],
        ["Out of stock", "Products with nothing left to sell", "Today, or you lose the sale"],
        ["Receivables", "Invoiced but not yet paid", "It exceeds one month of sales"],
        ["Invoices", "Number of sales documents issued", "—"],
        ["Average invoice", "Mean value per invoice", "It drifts down — check discounting"],
    ], [32 * mm, 84 * mm, 58 * mm]))
    S.append(Spacer(1, 3 * mm))
    S.append(Paragraph(
        "The <b>Reorder now</b> list is the one column to check before you order anything: it ranks "
        "products by how far below twice their minimum level they are, and shows the quantity that "
        "would bring them back up.", BODY))

    S.append(PageBreak())

    # ---------------- 6 / 7 ----------------
    S.append(Paragraph("6. Reports", H1))
    S.append(Paragraph(
        "The Reports sheet has no inputs. It builds three things: a month-by-month table (invoices, "
        "sales, cost of goods, gross profit, expenses), a chart comparing sales and gross profit "
        "across the year, and an annual summary with the figures your accountant will ask for. "
        "Everything is print-ready: File &gt; Print, landscape, fitted to one page wide.", BODY))

    S.append(Paragraph("Month boundaries", H2))
    S.append(Paragraph(
        "Months are read from the date column, so an invoice dated 31 August belongs to August "
        "regardless of when you typed it. If a month shows zero sales, check the date column on the "
        "line sheet — a date stored as text is the usual cause.", BODY))

    S.append(Paragraph("7. Protecting your data", H1))

    S.append(Paragraph("Backups", H2))
    S.append(Paragraph(
        "Keep the workbook in OneDrive or a folder your backup tool covers, and take a copy at "
        "month end named with the period (for example <b>Inventory_2026-08.xlsx</b>). If something "
        "goes badly wrong, restoring last month's copy costs you a month of typing; not having one "
        "costs you the history.", BODY))

    S.append(Paragraph("What not to edit", H2))
    S.append(Paragraph(
        "Do not delete rows on the hidden SalesData or PurchaseData sheets without deleting the "
        "matching invoice — the visible totals are SUMIFs over those rows, so an orphan line will "
        "show up as revenue that belongs to no invoice. Do not rename sheets: the formulas reference "
        "them by name. Do not insert columns in the middle of a data sheet; add to the right-hand end.", BODY))

    S.append(Paragraph("Changing a price", H2))
    S.append(Paragraph(
        "Editing a selling price on Products does not rewrite history. Existing sale lines keep the "
        "price they were sold at, so last year's profit stays accurate and this year's uses the new "
        "price. That is deliberate.", BODY))

    S.append(PageBreak())

    # ---------------- 8 / 9 ----------------
    S.append(Paragraph("8. Troubleshooting", H1))
    S.append(table([
        ["Symptom", "Cause and fix"],
        ["A new product shows zero stock", "No opening stock and no purchase lines yet. Enter Opening Stock, or record the delivery on Purchases."],
        ["Sales total is lower than expected",
         "Invoice lines are missing for that invoice number. Check the invoice number on SalesData matches exactly."],
        ["Every figure shows #NAME?",
         "Usually a renamed sheet or a pasted-over named range (TaxRate). Restore from your last backup."],
        ["Stock is negative",
         "A sale was recorded for more units than you hold. The system caps sales during data entry but a manual line entry can still oversell — correct the quantity."],
        ["A month shows no sales",
         "The date is stored as text, not a real date. Re-enter it, or use Data &gt; Text to Columns with Date format."],
        ["Margin looks wrong on one invoice",
         "The line's unit cost was changed after the sale. Unit Cost on SalesData should hold the cost at the time of sale."],
        ["Dropdown is empty",
         "The list it reads from is on Settings (or the Customers/Suppliers ID column) and has been cleared."],
    ], [52 * mm, 122 * mm]))

    S.append(Paragraph("9. Starting clean", H1))
    S.append(Paragraph(
        "Open <b>Sample_Data.xlsx</b> rather than the demo workbook. It has the same ten sheets, the "
        "same formulas, the same dropdowns and the same dashboard wiring, but no records: no "
        "products, customers, suppliers, invoices or expenses. Fill in Settings, then Products, then "
        "your first purchase, and the dashboard starts working.", BODY))
    S.append(Paragraph(
        "If you have already started in the demo file and want to keep your own records, delete the "
        "demo rows instead: filter Products by the PRD- prefix and delete those rows, then clear "
        "Sales rows 5 onwards and the SalesData/PurchaseData line sheets. Leave row 4 (the header) "
        "in place.", BODY))
    S.append(Spacer(1, 4 * mm))
    S.append(callout(
        "A note on the sample data",
        "Every name, product, price and invoice in the demo workbook is invented for demonstration. "
        "There are no real customers, no real sales and no testimonials. Replace it with your own "
        "data before showing the workbook to anyone."))

    S.append(Spacer(1, 8 * mm))
    S.append(Paragraph("Support", H2))
    S.append(Paragraph(
        "Questions about setup, or a change that is not covered here: "
        "pouriabusines1@gmail.com · Instagram @pouria_busines · Telegram @pouria_busines.", BODY))
    S.append(Spacer(1, 2 * mm))
    S.append(Paragraph(
        f"Pouria Business — Smart Inventory &amp; Sales Manager, version 1.0. "
        f"Guide generated {dt.date(2026, 9, 1).strftime('%d %B %Y')}.", SMALL))

    doc.build(S)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"wrote {os.path.relpath(path, ROOT)}  ({os.path.getsize(path)/1024:.0f} KB)")
