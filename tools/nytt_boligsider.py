#!/usr/bin/env python3
"""Nytt design på alle boligmodell-sidene, i stil med katalogen.

Henter tekst og bilder fra eksisterende sider, beholder header/footer og
erstatter <main>. Spesifikasjoner gjenbrukes fra nytt_boligkatalog.BOLIGER.
Kjøres fra repo-roten. Idempotent på ORIGINAL-kopier: første kjøring lagrer
main-innholdet i tools/original-main/<slug>.html og leser derfra siden.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nytt_boligkatalog import BOLIGER, beste_bilde  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARKIV = Path(__file__).resolve().parent / "original-main"
ARKIV.mkdir(exist_ok=True)

SPECLABELS = {"bra", "bra pr enhet", "utleiedel", "bad", "soverom", "garasje", "bod"}
LOGO = re.compile(r"(logo|totalkontroll|download|bvnlogo|cropped|favicon|icon)", re.I)
VARIANT = re.compile(r"-\d+x\d+$")


def hent_original_main(slug: str) -> str:
    arkivfil = ARKIV / f"{slug}.html"
    if arkivfil.exists():
        return arkivfil.read_text(encoding="utf-8")
    html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", html)
    main = html[start.end(): html.find("</main>")]
    arkivfil.write_text(main, encoding="utf-8")
    return main


def tekst_og_bilder(main: str):
    """Avsnitt (uten spec-labels/verdier) og bildestier i dokumentrekkefølge."""
    avsnitt = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", main, re.S):
        txt = re.sub(r"<[^>]+>", " ", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) > 60:
            avsnitt.append(txt)
    bilder, sett = [], set()
    for m in re.finditer(r'(?:src="|url\((?:&quot;|")?)\.\./(wp-content/uploads[^)"&]+\.(?:webp|png|jpg))', main):
        sti = m.group(1)
        if LOGO.search(sti):
            continue
        stem = VARIANT.sub("", sti.rsplit(".", 1)[0])
        if stem in sett:
            continue
        sett.add(stem)
        bilder.append(stem)
    return avsnitt, bilder


CSS = """
<style>
#ibs{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding-bottom:100px}
:where(#ibs *){box-sizing:border-box;margin:0}
.ibs-hero{position:relative;min-height:62vh;display:flex;align-items:flex-end;overflow:hidden}
.ibs-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ibs-hero::after{content:"";position:absolute;inset:0;
  background:linear-gradient(to top,rgba(24,22,19,.78) 0%,rgba(24,22,19,.25) 45%,rgba(24,22,19,.15) 100%)}
.ibs-heroinnhold{position:relative;z-index:1;width:100%;max-width:1200px;
  margin:0 auto;padding:70px 20px 46px;color:#fff}
.ibs-smuler{font:500 13px Inter,sans-serif;margin-bottom:16px}
.ibs-smuler a{color:#fff;opacity:.75;text-decoration:none}
.ibs-smuler a:hover{opacity:1}
.ibs-smuler span{opacity:.55;margin:0 8px}
.ibs-badges{display:flex;gap:8px;margin-bottom:14px}
.ibs-badge{font:600 11px/1 Inter,sans-serif;letter-spacing:.05em;
  background:rgba(255,255,255,.16);backdrop-filter:blur(4px);
  border:1px solid rgba(255,255,255,.35);padding:8px 13px;border-radius:99px}
.ibs-badge--gull{background:var(--gull);border-color:var(--gull)}
#ibs h1{font-size:clamp(38px,5.5vw,60px);font-weight:700;line-height:1.08;letter-spacing:-.015em;color:#fff}
.ibs-tagline{margin-top:12px;font-size:17px;opacity:.92;max-width:600px;line-height:1.6}
.ibs-indre{max-width:1200px;margin:0 auto;padding:0 20px}
.ibs-specband{position:relative;z-index:2;margin-top:-34px;display:flex;flex-wrap:wrap;
  gap:1px;background:#E9E2D4;border-radius:16px;overflow:hidden;
  box-shadow:0 10px 32px rgba(51,48,44,.12)}
.ibs-spec{flex:1 1 130px;background:#fff;padding:20px 16px;text-align:center}
.ibs-spec b{display:block;font:700 21px Poppins,sans-serif}
.ibs-spec b small{font-size:12px;font-weight:500;color:var(--grå)}
.ibs-spec span{font:600 10.5px Inter,sans-serif;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gull)}
.ibs-seksjon{margin-top:72px}
.ibs-kicker{display:flex;align-items:center;gap:14px;font:600 12px/1 Inter,sans-serif;
  letter-spacing:.24em;text-transform:uppercase;color:var(--gull);margin-bottom:18px}
.ibs-kicker::after{content:"";flex:0 0 46px;height:1px;background:var(--gull);opacity:.55}
#ibs h2{font-size:clamp(24px,3vw,32px);font-weight:700;letter-spacing:-.01em;margin-bottom:22px}
.ibs-prosa{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:48px;align-items:start}
.ibs-prosa p{color:var(--grå);line-height:1.85;font-size:15.5px}
.ibs-prosa p+p{margin-top:18px}
.ibs-prosa p:first-of-type::first-letter{font-size:44px;font-weight:700;float:left;
  line-height:.9;margin:4px 10px 0 0;color:var(--mork)}
.ibs-kort{position:sticky;top:24px;background:#fff;border-radius:16px;padding:26px;
  box-shadow:0 2px 14px rgba(51,48,44,.08)}
.ibs-kort h3{font-size:18px;font-weight:700;margin-bottom:6px}
.ibs-kort p{font-size:13.5px;color:var(--grå);line-height:1.6;margin-bottom:18px}
.ibs-knapp{display:block;text-align:center;background:var(--gull);color:#fff;
  font:600 15px Poppins,sans-serif;padding:14px;border-radius:10px;text-decoration:none;
  transition:filter .2s}
.ibs-knapp:hover{filter:brightness(1.07)}
.ibs-knapp--sek{background:transparent;color:var(--mork);border:1.5px solid #E3DCCF;margin-top:10px}
.ibs-galleri{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.ibs-galleri button{border:0;padding:0;cursor:zoom-in;border-radius:14px;overflow:hidden;
  aspect-ratio:4/3;background:#E9E2D4}
.ibs-galleri img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.ibs-galleri button:hover img{transform:scale(1.05)}
.ibs-plan .ibs-galleri button{aspect-ratio:16/9}
.ibs-navig{margin-top:80px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.ibs-navkort{display:flex;align-items:center;gap:16px;background:#fff;border-radius:14px;
  padding:16px 20px;text-decoration:none;color:inherit;box-shadow:0 2px 14px rgba(51,48,44,.07);
  transition:transform .25s,box-shadow .25s}
.ibs-navkort:hover{transform:translateY(-4px);box-shadow:0 10px 26px rgba(51,48,44,.14)}
.ibs-navkort img{width:74px;height:56px;object-fit:cover;border-radius:9px}
.ibs-navkort.neste{flex-direction:row-reverse;text-align:right}
.ibs-navkort small{font:600 10.5px Inter,sans-serif;letter-spacing:.14em;
  text-transform:uppercase;color:var(--gull)}
.ibs-navkort b{display:block;font-size:16.5px}
.ibs-lys{position:fixed;inset:0;z-index:9999;background:rgba(20,18,16,.93);display:none;
  align-items:center;justify-content:center;padding:34px}
.ibs-lys.vis{display:flex}
.ibs-lys img{max-width:92vw;max-height:86vh;border-radius:8px;object-fit:contain}
.ibs-lys button{position:absolute;background:rgba(255,255,255,.12);border:0;color:#fff;
  width:46px;height:46px;border-radius:50%;font-size:21px;cursor:pointer;transition:background .2s}
.ibs-lys button:hover{background:rgba(255,255,255,.28)}
.ibs-lukk{top:22px;right:22px}
.ibs-forrige{left:22px;top:50%;translate:0 -50%}
.ibs-neste{right:22px;top:50%;translate:0 -50%}
.ibs-teller{position:absolute;bottom:22px;left:50%;translate:-50% 0;color:#fff;
  font:500 13px Inter,sans-serif;opacity:.8}
.ibs-avslor{opacity:0;translate:0 24px;transition:opacity .55s ease,translate .55s ease}
.ibs-avslor.vis{opacity:1;translate:0 0}
@media(max-width:900px){.ibs-prosa{grid-template-columns:1fr}.ibs-kort{position:static}}
@media(max-width:640px){.ibs-navig{grid-template-columns:1fr}.ibs-hero{min-height:48vh}}
</style>
"""

JS = """
<script>
(function(){
 var bilder=[].slice.call(document.querySelectorAll('.ibs-galleri button')),
     lys=document.getElementById('ibs-lys'),bilde=lys.querySelector('img'),
     teller=lys.querySelector('.ibs-teller'),i=0;
 function visLys(n){i=(n+bilder.length)%bilder.length;
  bilde.src=bilder[i].dataset.full;teller.textContent=(i+1)+' / '+bilder.length;
  lys.classList.add('vis');document.body.style.overflow='hidden';}
 function lukk(){lys.classList.remove('vis');document.body.style.overflow='';}
 bilder.forEach(function(b,n){b.addEventListener('click',function(){visLys(n);});});
 lys.querySelector('.ibs-lukk').addEventListener('click',lukk);
 lys.querySelector('.ibs-forrige').addEventListener('click',function(e){e.stopPropagation();visLys(i-1);});
 lys.querySelector('.ibs-neste').addEventListener('click',function(e){e.stopPropagation();visLys(i+1);});
 lys.addEventListener('click',function(e){if(e.target===lys)lukk();});
 document.addEventListener('keydown',function(e){
  if(!lys.classList.contains('vis'))return;
  if(e.key==='Escape')lukk();
  if(e.key==='ArrowLeft'||e.key==='Left')visLys(i-1);
  if(e.key==='ArrowRight'||e.key==='Right')visLys(i+1);});
 var avslor=[].slice.call(document.querySelectorAll('.ibs-avslor'));
 if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
   if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target);}});},{threshold:.1});
  avslor.forEach(function(el){io.observe(el);});
 }else avslor.forEach(function(el){el.classList.add('vis');});
})();
</script>
"""


def full_sti(stem: str) -> str:
    for ext in (".webp", ".png", ".jpg"):
        if (ROOT / f"{stem}{ext}").exists():
            return f"../{stem}{ext}"
    return beste_bilde(stem)


def galleri_html(stems: list, alt_prefix: str) -> str:
    knapper = []
    for s in stems:
        knapper.append(
            f'<button class="ibs-avslor" data-full="{full_sti(s)}">'
            f'<img src="{beste_bilde(s)}" alt="{alt_prefix}" loading="lazy"></button>')
    return "".join(knapper)


def spec_html(b: dict) -> str:
    bra = f'{b["bra"]} m²' + (' <small>pr enhet</small>' if b["braenhet"] else "")
    specs = [("BRA", bra), ("Soverom", str(b["sov"])), ("Bad", str(b["bad"])),
             ("Garasje", b["garasje"] or "Nei"),
             ("Utleiedel", b["utleie"] or "Nei"), ("Bod", str(b["bod"]))]
    return "".join(f'<div class="ibs-spec"><b>{v}</b><span>{k}</span></div>' for k, v in specs)


def bygg_side(idx: int) -> None:
    b = BOLIGER[idx]
    slug = b["slug"]
    main = hent_original_main(slug)
    avsnitt, bilder = tekst_og_bilder(main)
    planer = [s for s in bilder if re.search(r"plan|etg", s, re.I)]
    foto = [s for s in bilder if s not in planer]
    forrige, neste = BOLIGER[idx - 1], BOLIGER[(idx + 1) % len(BOLIGER)]

    badges = [f'<span class="ibs-badge">{b["type"]}</span>']
    if b["utleie"]:
        badges.append(f'<span class="ibs-badge ibs-badge--gull">Utleiedel {b["utleie"]}</span>')

    plan_seksjon = ""
    if planer:
        plan_seksjon = f"""
  <section class="ibs-seksjon ibs-plan">
    <p class="ibs-kicker">Planløsning</p>
    <h2>Plantegninger</h2>
    <div class="ibs-galleri">{galleri_html(planer, b['navn'] + ' — plantegning')}</div>
  </section>"""

    tekst = "".join(f"<p>{a}</p>" for a in avsnitt)
    nytt = f"""{CSS}
<section id="ibs">
 <div class="ibs-hero">
  <img src="{full_sti(foto[0]) if foto else beste_bilde(b['bilde'])}" alt="{b['navn']} — fasade">
  <div class="ibs-heroinnhold">
    <p class="ibs-smuler"><a href="../v%C3%A5re-boliger/">Våre boliger</a><span>/</span>{b['navn']}</p>
    <div class="ibs-badges">{''.join(badges)}</div>
    <h1>{b['navn']}</h1>
    <p class="ibs-tagline">{b['tagline']}</p>
  </div>
 </div>
 <div class="ibs-indre">
  <div class="ibs-specband">{spec_html(b)}</div>
  <section class="ibs-seksjon">
    <p class="ibs-kicker">Om boligen</p>
    <h2>{b['tagline']}</h2>
    <div class="ibs-prosa">
      <div>{tekst}</div>
      <aside class="ibs-kort">
        <h3>Interessert i {b['navn']}?</h3>
        <p>Ta kontakt for prisoverslag, tilpasninger og tomtevurdering — helt uforpliktende.</p>
        <a class="ibs-knapp" href="../kontakt/">Kontakt oss</a>
        <a class="ibs-knapp ibs-knapp--sek" href="../v%C3%A5re-boliger/">Se alle boliger</a>
      </aside>
    </div>
  </section>
  <section class="ibs-seksjon">
    <p class="ibs-kicker">Galleri</p>
    <h2>Se {b['navn']} innvendig og utvendig</h2>
    <div class="ibs-galleri">{galleri_html(foto, b['navn'])}</div>
  </section>{plan_seksjon}
  <nav class="ibs-navig">
    <a class="ibs-navkort" href="../{forrige['slug']}/">
      <img src="{beste_bilde(forrige['bilde'])}" alt="{forrige['navn']}" loading="lazy">
      <div><small>← Forrige bolig</small><b>{forrige['navn']}</b></div></a>
    <a class="ibs-navkort neste" href="../{neste['slug']}/">
      <img src="{beste_bilde(neste['bilde'])}" alt="{neste['navn']}" loading="lazy">
      <div><small>Neste bolig →</small><b>{neste['navn']}</b></div></a>
  </nav>
 </div>
 <div class="ibs-lys" id="ibs-lys" role="dialog" aria-label="Bildevisning">
   <img src="" alt=""><button class="ibs-lukk" aria-label="Lukk">✕</button>
   <button class="ibs-forrige" aria-label="Forrige">‹</button>
   <button class="ibs-neste" aria-label="Neste">›</button>
   <p class="ibs-teller"></p>
 </div>
</section>
{JS}"""

    fil = ROOT / slug / "index.html"
    html = fil.read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", html)
    end = html.find("</main>")
    fil.write_text(html[: start.end()] + nytt + html[end:], encoding="utf-8")
    print(f"OK {slug}: {len(avsnitt)} avsnitt, {len(foto)} foto, {len(planer)} planer")


if __name__ == "__main__":
    for idx in range(len(BOLIGER)):
        bygg_side(idx)
