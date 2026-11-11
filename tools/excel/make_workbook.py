#!/usr/bin/env python3
"""
Build the deliverable .xlsx files.

    python3 make_workbook.py            # builds all three workbooks
    python3 make_workbook.py --main     # only the main workbook

Outputs (into the product folder):
    Pouria_Business_Inventory_Manager.xlsx   the commercial product
    Sample_Data.xlsx                          a clean starting file, no demo records
"""

from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "products", "smart-inventory-sales-manager")

sys.path.insert(0, HERE)

from build_workbook import Workbook, DATA_ROWS, LAST_DATA_ROW, PRODUCT_ROWS
import sheets_master as M
import sheets_transactions as T
import sheets_inventory as I
import sheets_dashboard as D
import sample_data as S

MAIN_NAME = "Pouria_Business_Inventory_Manager.xlsx"
SAMPLE_NAME = "Sample_Data.xlsx"


def build(path: str, *, demo: bool = True):
    """demo=False produces the empty starter file (same structure, no records)."""
    import sample_data as _sd
    if not demo:
        _empty_the_data(_sd)
    wb = Workbook(path)

    # master data
    M.build_products(wb)
    M.build_customers(wb)
    M.build_suppliers(wb)
    M.build_settings(wb)

    # transactions + hidden line data
    T.build_sales_data(wb)
    T.build_purchase_data(wb)
    T.build_sales(wb)
    T.build_purchases(wb)
    T.build_expenses(wb)

    # derived
    I.build_inventory(wb)
    D.build_dashboard(wb)
    D.build_reports(wb)

    # workbook-level settings
    wb.wb.set_properties({
        "title": "Pouria Business — Smart Inventory & Sales Manager",
        "subject": "Inventory, sales and business reporting for small business",
        "author": "Pouria Asghari",
        "company": "Pouria Business",
        "category": "Business / Inventory management",
        "keywords": "inventory, sales, purchases, expenses, dashboard, Excel",
        "comments": "Built with standard Excel formulas and tables. No macros, no external links.",
        "status": "Released",
        "created": __import__("datetime").datetime(2026, 9, 1),
    })
    wb.wb.set_calc_mode("auto")

    # protect the formula-bearing sheets (no password: Review > Unprotect Sheet)
    for name in ("Products", "Customers", "Suppliers", "Inventory",
                 "Dashboard", "Reports", "Settings"):
        ws = wb.ws[name]
        ws.protect("", {
            "select_locked_cells": True,
            "select_unlocked_cells": True,
            "format_columns": True,
            "format_rows": True,
            "sort": True,
            "autofilter": True,
            "pivot_tables": True,
        })

    wb.wb.close()
    return path


def _empty_the_data(sd):
    """Strip the demo records but keep one example row so the layout reads."""
    sd.PRODUCTS = []
    sd.PRODUCT_BY_ID = {}
    sd.CUSTOMERS = []
    sd.CUSTOMER_BY_ID = {}
    sd.SUPPLIERS = []
    sd.SALES = []
    sd.SALE_LINES = []
    sd.PURCHASES = []
    sd.PURCHASE_LINES = []
    sd.EXPENSE_ROWS = []
    sd.OPENING_STOCK = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    built = []
    if args.main or not (args.main or args.sample):
        p = build(os.path.join(OUT, MAIN_NAME), demo=True)
        built.append(p)
    if args.sample or not (args.main or args.sample):
        p = build(os.path.join(OUT, SAMPLE_NAME), demo=False)
        built.append(p)
    for p in built:
        size = os.path.getsize(p)
        print(f"wrote {os.path.relpath(p, ROOT)}  ({size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
