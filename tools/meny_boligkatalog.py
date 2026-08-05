#!/usr/bin/env python3
"""Legger «Boligkatalog» inn i alle menyene (før Kontakt-punktet). Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKOR = "ib-meny-boligkatalog"


def main() -> None:
    n = 0
    for fil in ROOT.rglob("*.html"):
        rel = fil.relative_to(ROOT)
        if rel.parts[0] in ("wp-content", "tools", "prosjekt-assets"):
            continue
        html = fil.read_text(encoding="utf-8")
        if MARKOR in html or "<nav" not in html:
            continue
        prefix = "../" * (len(rel.parts) - 1)
        nytt_li = (f'<li class="menu-item menu-item-type-post_type menu-item-object-page {MARKOR}">'
                   f'<a href="{prefix}boligkatalog/" class="menu-link">Boligkatalog</a></li>')
        # sett inn før hvert Kontakt-menypunkt
        mønster = re.compile(r'(<li[^>]*class="menu-item[^"]*"[^>]*>\s*<a[^>]*href="[^"]*kontakt/[^"]*"[^>]*>\s*Kontakt)')
        ny, antall = mønster.subn(nytt_li + r"\1", html)
        if antall:
            fil.write_text(ny, encoding="utf-8")
            n += 1
    print(f"Menypunkt lagt til på {n} sider")


if __name__ == "__main__":
    main()
