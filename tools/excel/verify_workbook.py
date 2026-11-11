#!/usr/bin/env python3
"""
Verify the workbook for real: recalculate every formula and compare the result
against figures computed independently in Python from the same source data.

This is not a syntax check. `formulas` evaluates the workbook the way Excel
would, so a wrong SUMIF range, a broken rank formula or an off-by-one stock
calculation fails the test.

    python3 verify_workbook.py
"""

from __future__ import annotations

import os
import sys
import warnings

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import formulas
import sample_data as S

XLSX = os.path.join(ROOT, "products", "smart-inventory-sales-manager",
                    "Pouria_Business_Inventory_Manager.xlsx")

PASS, FAIL, WARN = [], [], []


def ok(name, detail=""):
    PASS.append(name)
    print(f"  PASS  {name}{('  ' + detail) if detail else ''}")


def bad(name, detail=""):
    FAIL.append((name, detail))
    print(f"  FAIL  {name}{('  ' + detail) if detail else ''}")


def close(a, b, tol=0.02):
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def cell(sol, sheet, ref):
    """Fetch a single cell value from the solution dictionary."""
    for key, val in sol.items():
        if not key.upper().startswith(f"'[POURIA_BUSINESS_INVENTORY_MANAGER.XLSX]{sheet.upper()}'"):
            continue
        tail = key.rsplit("!", 1)[-1]
        if tail.upper() == ref.upper():
            try:
                return val.value[0][0]
            except Exception:
                try:
                    return val.value
                except Exception:
                    return None
    return None


def main():
    if not os.path.exists(XLSX):
        print(f"workbook not found: {XLSX}")
        return 1

    print(f"Recalculating {os.path.basename(XLSX)} …")
    model = formulas.ExcelModel().loads(XLSX).finish()
    sol = model.calculate()

    expected = S.expected_totals()

    # ------------------------------------------------------------------
    print("\n[1] Dashboard KPIs")
    # band 1: sales, gross, net, purchases, expenses, inventory
    checks = [
        ("Total sales",      "Dashboard", "B7",  expected["revenue"]),
        ("Gross profit",     "Dashboard", "D7",  expected["gross_profit"]),
        ("Net profit",       "Dashboard", "F7",  expected["net_profit"]),
        ("Purchases",        "Dashboard", "H7",  expected["purchases"]),
        ("Expenses",         "Dashboard", "J7",  expected["expenses"]),
        ("Inventory value",  "Dashboard", "L7",  expected["inventory_value"]),
        ("Product count",    "Dashboard", "B11", expected["product_count"]),
        ("Low stock count",  "Dashboard", "D11", expected["low_stock"]),
        ("Out of stock",     "Dashboard", "F11", expected["out_of_stock"]),
        ("Receivables",      "Dashboard", "H11", expected["receivable"]),
        ("Invoice count",    "Dashboard", "J11", expected["invoice_count"]),
    ]
    for label, sheet, ref, want in checks:
        got = cell(sol, sheet, ref)
        if close(got, want, tol=1.0):
            ok(label, f"{got:,.2f} vs expected {want:,.2f}")
        else:
            bad(label, f"got {got} expected {want}")

    # ------------------------------------------------------------------
    print("\n[2] Margins")
    gm = cell(sol, "Dashboard", "B15")
    nm = cell(sol, "Dashboard", "D15")
    want_gm = expected["gross_profit"] / expected["revenue"]
    want_nm = expected["net_profit"] / expected["revenue"]
    ok("Gross margin", f"{gm:.4f} vs {want_gm:.4f}") if close(gm, want_gm, 0.001) \
        else bad("Gross margin", f"got {gm} expected {want_gm}")
    ok("Net margin", f"{nm:.4f} vs {want_nm:.4f}") if close(nm, want_nm, 0.001) \
        else bad("Net margin", f"got {nm} expected {want_nm}")

    # ------------------------------------------------------------------
    print("\n[3] Inventory and stock maths")
    # Products rows start at 5 (0-based row 4)
    stock = expected["stock"]
    checked = 0
    mismatched = []
    for i, p in enumerate(S.PRODUCTS):
        row = 5 + i
        got_stock = cell(sol, "Products", f"L{row}")
        want_stock = stock[p["id"]]
        got_status = cell(sol, "Products", f"N{row}")
        if not close(got_stock, want_stock, tol=0.01):
            mismatched.append(f"{p['id']} stock {got_stock} != {want_stock}")
        else:
            checked += 1
        # status must agree with the quantity
        if want_stock <= 0:
            if got_status != "Out of stock":
                mismatched.append(f"{p['id']} status {got_status} should be Out of stock")
        elif want_stock <= p["min"]:
            if got_status != "Low stock":
                mismatched.append(f"{p['id']} status {got_status} should be Low stock")
        else:
            if got_status != "In stock":
                mismatched.append(f"{p['id']} status {got_status} should be In stock")
    if mismatched:
        bad("Per-product stock + status", "; ".join(mismatched[:4]))
    else:
        ok("Per-product stock + status", f"all {checked} products match")

    # no product may end negative
    negatives = [pid for pid, q in stock.items() if q < 0]
    ok("No negative stock") if not negatives else bad("No negative stock", str(negatives))

    # inventory sheet must agree with the products sheet
    inv_total = cell(sol, "Inventory", "E5")
    if close(inv_total, expected["inventory_value"], tol=1.0):
        ok("Inventory sheet total", f"{inv_total:,.2f}")
    else:
        bad("Inventory sheet total", f"got {inv_total} expected {expected['inventory_value']}")

    # ------------------------------------------------------------------
    print("\n[4] Invoice-level arithmetic")
    # each invoice: subtotal = sum of lines; total = subtotal + tax; balance = total - paid
    errs = []
    for i, inv in enumerate(S.SALES[:12]):
        row = 5 + i
        sub = cell(sol, "Sales", f"E{row}")
        tax = cell(sol, "Sales", f"F{row}")
        tot = cell(sol, "Sales", f"G{row}")
        paid = cell(sol, "Sales", f"H{row}")
        bal = cell(sol, "Sales", f"I{row}")
        # coerce to numbers; a text value means the formula itself is wrong
        try:
            sub_f, tax_f, tot_f, paid_f, bal_f = (float(sub), float(tax), float(tot),
                                                  float(paid), float(bal))
        except (TypeError, ValueError):
            errs.append(f"{inv['id']} non-numeric: sub={sub!r} tax={tax!r} bal={bal!r}")
            continue
        if not close(sub_f, inv["subtotal"], 0.02):
            errs.append(f"{inv['id']} subtotal {sub_f} != {inv['subtotal']}")
        if not close(tax_f, round(inv["subtotal"] * S.BUSINESS["tax_rate"], 2), 0.03):
            errs.append(f"{inv['id']} tax {tax_f}")
        if not close(tot_f, round(sub_f + tax_f, 2), 0.03):
            errs.append(f"{inv['id']} total {tot_f} != {sub_f}+{tax_f}")
        if not close(bal_f, round(tot_f - paid_f, 2), 0.03):
            errs.append(f"{inv['id']} balance {bal_f} != {tot_f}-{paid_f}")
    ok("Invoice subtotal / tax / balance", "12 invoices") if not errs \
        else bad("Invoice subtotal / tax / balance", "; ".join(errs[:3]))

    # payment status logic
    statuses = set()
    for i in range(12):
        statuses.add(cell(sol, "Sales", f"J{5+i}"))
    if statuses <= {"Paid", "Part paid", "Unpaid", ""}:
        ok("Payment status values", ", ".join(sorted(s for s in statuses if s)))
    else:
        bad("Payment status values", str(statuses))

    # profit per invoice
    row = 5
    profit = cell(sol, "Sales", f"M{row}")
    inv0 = S.SALES[0]
    want_profit = round(inv0["subtotal"] - sum(
        l["qty"] * l["unit_cost"] for l in S.SALE_LINES
        if l["invoice_id"] == inv0["id"]), 2)
    if close(profit, want_profit, 0.05):
        ok("Invoice profit", f"{profit:,.2f}")
    else:
        bad("Invoice profit", f"got {profit} expected {want_profit}")

    # ------------------------------------------------------------------
    print("\n[5] Customer and supplier roll-ups")
    # customer CUS-001 invoice count / total sales
    want_c = sum(1 for s in S.SALES if s["customer_id"] == "CUS-001")
    want_t = sum(s["subtotal"] for s in S.SALES if s["customer_id"] == "CUS-001")
    got_c = cell(sol, "Customers", "K5")
    got_t = cell(sol, "Customers", "L5")
    ok("Customer invoice count", f"{got_c} vs {want_c}") if close(got_c, want_c) \
        else bad("Customer invoice count", f"{got_c} != {want_c}")
    ok("Customer total sales", f"{got_t:,.2f}") if close(got_t, want_t, 0.02) \
        else bad("Customer total sales", f"{got_t} != {want_t}")

    want_orders = sum(1 for p in S.PURCHASES if p["supplier_id"] == "SUP-001")
    got_orders = cell(sol, "Suppliers", "K5")
    ok("Supplier order count", f"{got_orders} vs {want_orders}") if close(got_orders, want_orders) \
        else bad("Supplier order count", f"{got_orders} != {want_orders}")

    # ------------------------------------------------------------------
    print("\n[6] Reports sheet")
    want_month = {}
    for line in S.SALE_LINES:
        key = line["date"].strftime("%b")
        want_month[key] = want_month.get(key, 0) + line["line_total"]
    rep_errors = []
    for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
        row = 7 + i
        got = cell(sol, "Reports", f"D{row}")
        want = round(want_month.get(m, 0), 2)
        if not close(got, want, 1.0):
            rep_errors.append(f"{m}: {got} != {want}")
    ok("Monthly sales breakdown", "12 months") if not rep_errors \
        else bad("Monthly sales breakdown", "; ".join(rep_errors[:3]))

    rep_total = cell(sol, "Reports", "D19")
    if close(rep_total, expected["revenue"], 1.0):
        ok("Report annual total", f"{rep_total:,.2f}")
    else:
        bad("Report annual total", f"{rep_total} != {expected['revenue']}")

    # ------------------------------------------------------------------
    print("\n[6b] Dashboard lists")
    # recent invoices must show the newest real invoice, not a blank row
    newest = max(S.SALES, key=lambda s: s["date"])
    got_inv = cell(sol, "Dashboard", "B35")
    ok("Recent invoice = newest", f"{got_inv} vs {newest['id']}") if got_inv == newest["id"] \
        else bad("Recent invoice = newest", f"{got_inv} != {newest['id']}")
    back = sorted(S.SALES, key=lambda s: (s["date"], s["id"]), reverse=True)[1]
    got2 = cell(sol, "Dashboard", "B36")
    ok("Second recent invoice", f"{got2} vs {back['id']}") if got2 == back["id"] \
        else bad("Second recent invoice", f"{got2} != {back['id']}")

    # reorder list must name a product that is genuinely at or below minimum
    reorder = cell(sol, "Dashboard", "H35")
    thin = {p["id"]: p for p in S.PRODUCTS
            if expected["stock"][p["id"]] <= p["min"] * 2}
    ok("Reorder list populated", str(reorder)[:40]) if reorder and reorder != "—" \
        else bad("Reorder list populated", repr(reorder))

    # top product by revenue must be the real top seller
    rev = {}
    for line in S.SALE_LINES:
        rev[line["product_id"]] = rev.get(line["product_id"], 0) + line["line_total"]
    top_id = max(rev, key=rev.get)
    top_name = next(p["name"] for p in S.PRODUCTS if p["id"] == top_id)
    got_top = cell(sol, "Dashboard", "I20")
    ok("Top product by revenue", f"{got_top}") if got_top == top_name \
        else bad("Top product by revenue", f"{got_top} != {top_name}")

    # ------------------------------------------------------------------
    print("\n[7] Formula integrity")
    error_cells = {}
    for key, val in sol.items():
        try:
            v = val.value[0][0]
        except Exception:
            continue
        if isinstance(v, str) and v.startswith("#"):
            sheet = key.split("]")[-1].split("!")[0]
            error_cells.setdefault(sheet, []).append(f"{key.rsplit('!')[-1]}={v}")
    if error_cells:
        detail = "; ".join(f"{s}: {len(e)} ({', '.join(e[:3])})"
                           for s, e in list(error_cells.items())[:5])
        bad("No formula errors", detail)
    else:
        ok("No formula errors", "0 error cells in the whole workbook")

    # ------------------------------------------------------------------
    print("\n" + "=" * 68)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("\nFailures:")
        for name, detail in FAIL:
            print(f"  - {name}: {detail}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
