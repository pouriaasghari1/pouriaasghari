#!/usr/bin/env python3
"""
Fast pre-flight: parse every formula in the workbook before the (slow) full
recalculation. Catches unbalanced parentheses, stray quotes and malformed
operators in seconds.
"""
import glob, os, re, sys, tempfile, zipfile, warnings
warnings.filterwarnings("ignore")
from formulas import Parser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
XLSX = os.path.join(ROOT, "products", "smart-inventory-sales-manager",
                    "Pouria_Business_Inventory_Manager.xlsx")


def main():
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(XLSX) as z:
        z.extractall(tmp)
    total = 0
    bad = []
    for f in sorted(glob.glob(os.path.join(tmp, "xl/worksheets/sheet*.xml"))):
        s = open(f, encoding="utf-8").read()
        for m in re.finditer(r'<c r="([A-Z]+\d+)"[^>]*><f>([^<]*)</f>', s):
            ref, fml = m.group(1), m.group(2)
            fml = fml.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            total += 1
            try:
                Parser().ast("=" + fml)
            except Exception as e:
                bad.append((os.path.basename(f), ref, fml, type(e).__name__))
    print(f"{total} formulas parsed, {len(bad)} invalid")
    for b in bad[:15]:
        print(f"  {b[0]} {b[1]}: {b[2][:140]}  [{b[3]}]")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
