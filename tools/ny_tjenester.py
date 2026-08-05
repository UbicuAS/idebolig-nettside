#!/usr/bin/env python3
"""Nytt design på tjenester-siden: vekslende tjeneste-rader i sidens stil.

Tekster og bilder hentes uendret fra originalsiden (arkiveres i
tools/original-main/tjenester.html første gang). Kjøres fra repo-roten.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARKIV = Path(__file__).resolve().parent / "original-main"

BILDER = {
    "BYGGTEKNISK RÅDGIVNING": "wp-content/uploads/2025/04/Byggteknisk-radgivning-1024x572.webp",
    "BYGGESØKNADER": "wp-content/uploads/2025/04/Byggesoknader-1024x572.webp",
    "BYGGTEGNINGER": "wp-content/uploads/2025/04/Byggtegninger-1024x572.webp",
    "UTFØRELSE OG MONTASJE": "wp-content/uploads/2025/04/Montasje-og-utforelse-1024x572.webp",
    "BRANN": "wp-content/uploads/2025/04/Brann-1024x572.webp",
}
PEN_TITTEL = {
    "BYGGTEKNISK RÅDGIVNING": "Byggteknisk rådgivning",
    "BYGGESØKNADER": "Byggesøknader",
    "BYGGTEGNINGER": "Byggtegninger",
    "UTFØRELSE OG MONTASJE": "Utførelse og montasje",
    "BRANN": "Brannteknikk",
}


def hent_original() -> str:
    arkiv = ARKIV / "tjenester.html"
    if arkiv.exists():
        return arkiv.read_text(encoding="utf-8")
    html = (ROOT / "tjenester" / "index.html").read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", html)
    main = html[start.end(): html.find("</main>")]
    arkiv.write_text(main, encoding="utf-8")
    return main


def tjenester_fra_original(main: str):
    """(tittel, tekst)-par i dokumentrekkefølge: hver h2 følges av sitt avsnitt."""
    biter = re.split(r"<h2[^>]*>(.*?)</h2>", main, flags=re.S)
    par = []
    for k in range(1, len(biter), 2):
        tittel = re.sub(r"<[^>]+>", "", biter[k]).strip()
        avsnitt = ""
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", biter[k + 1], re.S):
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            txt = re.sub(r"\s+", " ", txt).strip()
            if len(txt) > 40:
                avsnitt = txt
                break
        if tittel in BILDER:
            par.append((tittel, avsnitt))
    return par


def bygg() -> None:
    main = hent_original()
    par = tjenester_fra_original(main)

    rader = []
    for tittel, tekst in par:
        rader.append(f"""
<article class="tj-rad">
  <div class="tj-media"><img src="../{BILDER[tittel]}" alt="{PEN_TITTEL[tittel]}" loading="lazy"></div>
  <div class="tj-innhold">
    <span class="tj-nr"></span>
    <h2>{PEN_TITTEL[tittel]}</h2>
    <p>{tekst}</p>
    <a class="tj-lenke" href="../kontakt/">Snakk med oss om dette →</a>
  </div>
</article>""")

    nytt = f"""
<style>
#tjn{{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:88px 20px 100px}}
:where(#tjn *){{box-sizing:border-box;margin:0}}
.tjn-indre{{max-width:1200px;margin:0 auto}}
.tjn-topp{{max-width:640px;margin-bottom:56px}}
.tjn-kicker{{display:flex;align-items:center;gap:14px;font:600 12px/1 Inter,sans-serif;
  letter-spacing:.24em;text-transform:uppercase;color:var(--gull);margin-bottom:22px}}
.tjn-kicker::after{{content:"";flex:0 0 46px;height:1px;background:var(--gull);opacity:.55}}
#tjn h1{{font-size:clamp(34px,4.5vw,52px);font-weight:700;line-height:1.14;
  letter-spacing:-.015em;margin-bottom:20px}}
.tjn-intro{{color:var(--grå);font-size:16px;line-height:1.75}}
.tj-rad{{display:grid;grid-template-columns:6fr 6fr;gap:44px;align-items:center;
  background:#fff;border-radius:20px;overflow:hidden;margin-bottom:34px;
  box-shadow:0 2px 16px rgba(51,48,44,.08);counter-increment:tj;
  opacity:0;translate:0 26px;transition:opacity .6s ease,translate .6s ease}}
.tj-rad.vis{{opacity:1;translate:0 0}}
.tj-rad:nth-child(even){{direction:rtl}}
.tj-rad:nth-child(even) .tj-innhold{{direction:ltr}}
.tj-rad:nth-child(even) .tj-media{{direction:ltr}}
.tj-media{{align-self:stretch;min-height:300px;position:relative}}
.tj-media img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transition:transform .6s ease}}
.tj-rad:hover .tj-media img{{transform:scale(1.045)}}
.tj-innhold{{padding:44px 46px 44px 2px}}
.tj-rad:nth-child(even) .tj-innhold{{padding:44px 2px 44px 46px}}
.tj-nr::before{{content:counter(tj,decimal-leading-zero)}}
.tj-nr{{font:700 15px Inter,sans-serif;color:var(--gull);display:inline-block;
  margin-bottom:10px;letter-spacing:.1em}}
.tj-innhold h2{{font-size:clamp(21px,2.6vw,28px);font-weight:700;letter-spacing:-.01em;
  margin-bottom:12px}}
.tj-innhold p{{color:var(--grå);font-size:14.5px;line-height:1.8;margin-bottom:20px}}
.tj-lenke{{font:600 14px Poppins,sans-serif;color:var(--gull);text-decoration:none;
  display:inline-flex;gap:8px;transition:gap .2s}}
.tj-lenke:hover{{gap:13px}}
#tjn{{counter-reset:tj}}
.tj-cta{{margin-top:60px;background:linear-gradient(150deg,#3A362F,#26231F);
  border-radius:20px;padding:52px 40px;text-align:center;color:#D9D2C5}}
.tj-cta h2{{color:#fff;font-size:clamp(22px,3vw,30px);font-weight:700;margin-bottom:10px}}
.tj-cta p{{font-size:15px;line-height:1.7;max-width:520px;margin:0 auto 24px}}
.tj-cta a{{display:inline-block;background:var(--gull);color:#fff;
  font:600 15px Poppins,sans-serif;padding:14px 28px;border-radius:10px;
  text-decoration:none;transition:filter .2s,transform .2s}}
.tj-cta a:hover{{filter:brightness(1.07);transform:translateY(-2px)}}
@media(max-width:880px){{
 .tj-rad,.tj-rad:nth-child(even){{grid-template-columns:1fr;direction:ltr;gap:0}}
 .tj-media{{min-height:220px}}
 .tj-innhold,.tj-rad:nth-child(even) .tj-innhold{{padding:26px 26px 30px}}}}
</style>
<section id="tjn">
 <div class="tjn-indre">
  <div class="tjn-topp">
    <p class="tjn-kicker">Tjenester</p>
    <h1>Dette hjelper vi deg med</h1>
    <p class="tjn-intro">Fra første skisse til ferdig bygg — vi dekker hele løpet,
      enten du bygger nytt, bygger om eller trenger dokumentasjonen i orden.</p>
  </div>
  {''.join(rader)}
  <div class="tj-cta">
    <h2>Usikker på hvor du skal begynne?</h2>
    <p>Ta kontakt for en uforpliktende prat — så finner vi ut sammen hva
      prosjektet ditt trenger.</p>
    <a href="../kontakt/">Kontakt oss</a>
  </div>
 </div>
</section>
<script>
(function(){{
 var rader=[].slice.call(document.querySelectorAll('.tj-rad'));
 if('IntersectionObserver' in window){{
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{
   if(e.isIntersecting){{e.target.classList.add('vis');io.unobserve(e.target);}}}});}},
   {{threshold:.1}});
  rader.forEach(function(r){{io.observe(r);}});
 }}else rader.forEach(function(r){{r.classList.add('vis');}});
}})();
</script>
"""

    fil = ROOT / "tjenester" / "index.html"
    html = fil.read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", html)
    end = html.find("</main>")
    fil.write_text(html[: start.end()] + nytt + html[end:], encoding="utf-8")
    print(f"Skrev ny tjenesteside med {len(par)} tjenester")


if __name__ == "__main__":
    bygg()
