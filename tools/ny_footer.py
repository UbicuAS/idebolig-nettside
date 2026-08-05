#!/usr/bin/env python3
"""Bytter ut footeren på alle sider med nytt design i sidens stil.

Innholdet er hentet fra den gamle footeren: logo, slagord, kontaktinfo,
sosiale medier og de fire samarbeidslogoene. Kjøres fra repo-roten, idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PARTNERE = [
    ("Totalkontroll", "wp-content/uploads/2024/11/Totalkontroll-300x115.png"),
    ("Holte", "wp-content/uploads/2024/11/Holte-logo_hor_C-Copy-300x136.png"),
    ("Internsikring AS", "wp-content/uploads/2024/11/download-300x136.png"),
    ("Byggevarenord", "wp-content/uploads/2024/11/bvnlogo-211x300.jpg"),
]

FB = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.1c0-.9.3-1.5 1.6-1.5h1.3V4.9c-.2 0-1-.1-1.9-.1-1.9 0-3.2 1.2-3.2 3.3V11H9v3h2.3v7h2.2z"/></svg>'
YT = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8c1.6.4 7.8.4 7.8.4s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15.2V8.8L15.6 12 10 15.2z"/></svg>'


def footer_html(prefix: str) -> str:
    partnere = "".join(
        f'<div class="ibf-partner"><img src="{prefix}{sti}" alt="{navn}" loading="lazy"></div>'
        for navn, sti in PARTNERE)
    return f"""<footer class="ibf" itemscope itemtype="https://schema.org/LocalBusiness">
<style>
.ibf{{--gull:#C99C55;--mork:#26231F;background:var(--mork);color:#D9D2C5;
  font-family:Poppins,sans-serif;font-size:14px;line-height:1.7}}
:where(.ibf *){{box-sizing:border-box;margin:0}}
.ibf-indre{{max-width:1200px;margin:0 auto;padding:64px 20px 0}}
.ibf-kolonner{{display:grid;grid-template-columns:1.4fr 1fr 1.2fr;gap:48px;padding-bottom:52px}}
.ibf-logo img{{width:190px;height:auto;margin-bottom:18px}}
.ibf-slagord{{color:#B5AC9C;max-width:300px;margin-bottom:22px}}
.ibf-some{{display:flex;gap:10px}}
.ibf-some a{{display:flex;align-items:center;justify-content:center;width:40px;height:40px;
  border-radius:50%;background:rgba(255,255,255,.08);color:#fff;transition:.2s}}
.ibf-some a:hover{{background:var(--gull)}}
.ibf-some svg{{width:19px;height:19px}}
.ibf h4{{font:600 12px Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gull);margin-bottom:18px}}
.ibf-lenker{{list-style:none;padding:0}}
.ibf-lenker li{{margin-bottom:10px}}
.ibf-lenker a{{color:#D9D2C5;text-decoration:none;transition:color .2s}}
.ibf-lenker a:hover{{color:#fff}}
.ibf-kontakt p{{margin-bottom:8px;color:#B5AC9C}}
.ibf-kontakt a{{color:#D9D2C5;text-decoration:none}}
.ibf-kontakt a:hover{{color:#fff}}
.ibf-partnerfelt{{border-top:1px solid rgba(255,255,255,.09);padding:34px 0}}
.ibf-partnerfelt h4{{text-align:center;margin-bottom:22px}}
.ibf-partnerrad{{display:flex;flex-wrap:wrap;justify-content:center;gap:16px}}
.ibf-partner{{background:#fff;border-radius:12px;padding:12px 22px;display:flex;
  align-items:center;justify-content:center;height:64px;transition:transform .25s}}
.ibf-partner:hover{{transform:translateY(-3px)}}
.ibf-partner img{{max-height:40px;max-width:130px;width:auto;height:auto;object-fit:contain}}
.ibf-bunn{{border-top:1px solid rgba(255,255,255,.09);padding:20px;display:flex;
  flex-wrap:wrap;gap:8px;justify-content:center;text-align:center;
  font:400 12.5px Inter,sans-serif;color:#8F877A}}
@media(max-width:820px){{.ibf-kolonner{{grid-template-columns:1fr;gap:34px}}}}
</style>
<div class="ibf-indre">
 <div class="ibf-kolonner">
  <div class="ibf-logo">
    <img src="{prefix}wp-content/uploads/2024/11/Hvit-logo-sidestilt.png" alt="Idébolig AS">
    <p class="ibf-slagord">Vi gjør ideen til virkelighet.</p>
    <div class="ibf-some">
      <a href="https://www.facebook.com/idebolig" aria-label="Facebook" rel="noopener">{FB}</a>
      <a href="https://www.youtube.com/@Idebolig" aria-label="Youtube" rel="noopener">{YT}</a>
    </div>
  </div>
  <nav aria-label="Bunnmeny">
    <h4>Snarveier</h4>
    <ul class="ibf-lenker">
      <li><a href="{prefix}tjenester/">Tjenester</a></li>
      <li><a href="{prefix}prosjekter/">Prosjekter</a></li>
      <li><a href="{prefix}v%C3%A5re-boliger/">Våre boliger</a></li>
      <li><a href="{prefix}kontakt/">Kontakt</a></li>
    </ul>
  </nav>
  <div class="ibf-kontakt">
    <h4>Kontakt</h4>
    <p itemprop="name"><strong>Idébolig AS</strong></p>
    <p itemprop="address">Jølstadbakken 14, 2318 Hamar</p>
    <p>Telefon: <a href="tel:+4791926666" itemprop="telephone">91 92 66 66</a></p>
    <p>E-post: <a href="mailto:post@idebolig.no" itemprop="email">post@idebolig.no</a></p>
    <p>Org.nr.: 924 487 259</p>
  </div>
 </div>
 <div class="ibf-partnerfelt">
   <div class="ibf-partnerrad">{partnere}</div>
 </div>
</div>
<div class="ibf-bunn">© 2026 Idébolig AS — Vi gjør ideen til virkelighet</div>
</footer>"""


def main() -> None:
    n = 0
    for fil in ROOT.rglob("*.html"):
        rel = fil.relative_to(ROOT)
        if rel.parts[0] in ("wp-content", "tools", "prosjekt-assets", "boligkatalog"):
            continue
        html = fil.read_text(encoding="utf-8")
        if "<footer" not in html:
            continue
        dybde = len(rel.parts) - 1
        prefix = "../" * dybde
        nytt = re.sub(r"<footer.*?</footer>", lambda _: footer_html(prefix),
                      html, count=1, flags=re.S)
        if nytt != html:
            fil.write_text(nytt, encoding="utf-8")
            n += 1
    print(f"Ny footer på {n} sider")


if __name__ == "__main__":
    main()
