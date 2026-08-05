#!/usr/bin/env python3
"""Global mobilfiks: hindrer horisontal scroll og klemmer Elementor-nedtrekksmenyen
innenfor skjermen. Injiseres i <head> på alle sider. Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = """<style id="ib-mobilfiks">
html,body{overflow-x:hidden}
.elementor-nav-menu--dropdown.elementor-nav-menu__container{max-width:calc(100vw - 34px)}
/* statisk kopi: Elementor-JS-en viser aldri mobilmenyen - gjor det med CSS */
.elementor-menu-toggle.elementor-active + .elementor-nav-menu--dropdown{display:block;
  background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.14);border-radius:0 0 12px 12px}
</style>
"""


def main() -> None:
    n = 0
    for fil in ROOT.rglob("*.html"):
        rel = fil.relative_to(ROOT)
        if rel.parts[0] in ("wp-content", "tools", "prosjekt-assets"):
            continue
        html = fil.read_text(encoding="utf-8")
        if "</head>" not in html:
            continue
        html = re.sub(r'<style id="ib-mobilfiks">.*?</style>\n', "", html, flags=re.S)
        fil.write_text(html.replace("</head>", CSS + "</head>", 1), encoding="utf-8")
        n += 1
    print(f"Mobilfiks lagt inn på {n} sider")


if __name__ == "__main__":
    main()
