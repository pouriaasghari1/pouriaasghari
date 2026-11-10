#!/usr/bin/env python3
"""One command: rebuilds every page of the site."""
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_home, build_parts, build_pages  # noqa: F401  (they write on import)

ROOT = "/home/user/pouriaasghari"

def normalise(path):
    s = open(path, encoding="utf-8").read()
    def fix(m):
        inner = m.group(1)
        inner = inner.replace("{{", "{").replace("}}", "}")
        return "<style>" + inner + "</style>"
    s2 = re.sub(r"<style>(.*?)</style>", fix, s, flags=re.S)
    if s2 != s:
        open(path, "w", encoding="utf-8").write(s2)
        return True
    return False

print("all pages rebuilt")
