#!/usr/bin/env python3
"""Bygger prosjekter-siden: klargjør bilder/video fra delingen og genererer design.

Bruk:  python tools/nytt_prosjekter.py assets   # komprimer/kopier media (én gang)
       python tools/nytt_prosjekter.py side     # generer prosjekter/index.html
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KILDE = Path("/Volumes/claude/Prosjekter/Idebolig/bilder/Prosjekter")
UT = ROOT / "prosjekt-assets"

PROSJEKTER = [
    dict(slug="edvard-griegs-vei", tittel="Edvard Griegs vei 15",
         sted="Fjellhamar, Lørenskog", kategori="Nybygg",
         mapper=["Edvard_Griegs_vei_15_Fjellhamar_Lørenskog_kommune_nr1",
                 "VS__Edvard_Griegs_vei_15_Fjellhamar_Lørenskog_kommune_nr2"],
         tekst="Boligprosjekt i Edvard Griegs vei 15 på Fjellhamar i Lørenskog "
               "kommune. Vi har fulgt prosjektet gjennom hele byggeprosessen — "
               "se bilder og video fra arbeidet."),
    dict(slug="hagejordet-lillehammer", tittel="Hagejordet leilighetsbygg",
         sted="Lillehammer", kategori="Nybygg",
         mapper=["Hagejordet Lillehamer leilighetsbygg A,B,C og D_"],
         tekst="Oppføring av leilighetsbyggene A, B, C og D på Hagejordet i "
               "Lillehammer — et større boligprosjekt med flere byggetrinn."),
    dict(slug="parkgata-gjovik", tittel="Kontorbygg Parkgata BT2 og BT3",
         sted="Gjøvik", kategori="Næringsbygg",
         mapper=["Montasje, komplettering kontorbygg Parkgata BT2 og BT3 - Gjøvik.-"],
         tekst="Montasje og komplettering av kontorbygg i Parkgata på Gjøvik, "
               "byggetrinn 2 og 3."),
    dict(slug="nadderudskogen-garasjeanlegg", tittel="Nadderudskogen garasjeanlegg",
         sted="Hosle, Bærum", kategori="Nybygg",
         mapper=["Nadderudskogen garasjeanlegg i Bankveien og Wilh. Wilhelmsens vei 6, 1362 Hosle Bærum kommune"],
         tekst="Nytt garasjeanlegg i Bankveien og Wilh. Wilhelmsens vei 6 på Hosle "
               "i Bærum kommune — fra tegninger til ferdig anlegg."),
    dict(slug="smebyvegen-hamar", tittel="Smebyvegen 17A — totalrenovering",
         sted="Hamar", kategori="Renovering",
         mapper=["Smebyvegen 17a, hamar Total renovering"],
         tekst="Totalrenovering av bolig i Smebyvegen 17A på Hamar. Boligen ble "
               "fullstendig oppgradert innvendig og utvendig."),
    dict(slug="stromsveien-lillestrom", tittel="Strømsveien 6 — tilbygg",
         sted="Lillestrøm", kategori="Tilbygg",
         mapper=["Strømsveien 6 Lillestrøm Oppføring av tilbygg i 2 etasjer med loft"],
         tekst="Oppføring av tilbygg over to etasjer med loft i Strømsveien 6 i "
               "Lillestrøm — en betydelig utvidelse av eksisterende bolig."),
    dict(slug="ostregate-hamar", tittel="Østregate 23 — fasade og vinduer",
         sted="Hamar", kategori="Renovering",
         mapper=["Østregate 23 Hamar , riving innvendig samt bytting av alle vinduer og fasadearbeid"],
         tekst="Innvendig riving, utskifting av samtlige vinduer og fasadearbeid "
               "i Østregate 23 på Hamar."),
]

BILDE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}


def lag_assets() -> None:
    from PIL import Image, ImageOps
    for p in PROSJEKTER:
        ut = UT / p["slug"]
        ut.mkdir(parents=True, exist_ok=True)
        n_bilde = n_video = 0
        for mappe in p["mapper"]:
            for fil in sorted((KILDE / mappe).iterdir()):
                ext = fil.suffix.lower()
                if ext in BILDE_EXT:
                    n_bilde += 1
                    mål = ut / f"bilde-{n_bilde:02d}.webp"
                    if mål.exists():
                        continue
                    with Image.open(fil) as im:
                        im = ImageOps.exif_transpose(im)
                        if im.width > 1600:
                            im = im.resize((1600, round(im.height * 1600 / im.width)),
                                           Image.LANCZOS)
                        im.convert("RGB").save(mål, "WEBP", quality=80)
                elif ext in VIDEO_EXT:
                    n_video += 1
                    mål = ut / f"video-{n_video:02d}.mp4"
                    if not mål.exists():
                        shutil.copyfile(fil, mål)
        print(f"{p['slug']}: {n_bilde} bilder, {n_video} videoer")


CSS = """
<style>
#ibp{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:88px 20px 100px}
:where(#ibp *){box-sizing:border-box;margin:0}
.ibp-indre{max-width:1200px;margin:0 auto}
.ibp-topp{max-width:640px;margin-bottom:46px}
.ibp-kicker{display:flex;align-items:center;gap:14px;font:600 12px/1 Inter,sans-serif;
  letter-spacing:.24em;text-transform:uppercase;color:var(--gull);margin-bottom:22px}
.ibp-kicker::after{content:"";flex:0 0 46px;height:1px;background:var(--gull);opacity:.55}
#ibp h1{font-size:clamp(34px,4.5vw,52px);font-weight:700;line-height:1.14;
  letter-spacing:-.015em;margin-bottom:20px}
.ibp-intro{color:var(--grå);font-size:16px;line-height:1.75}
.ibp-filtre{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:44px}
.ibp-chip{padding:9px 15px;border:1px solid #E3DCCF;border-radius:99px;background:#fff;
  font:500 13px Poppins,sans-serif;color:var(--grå);cursor:pointer;transition:.18s}
.ibp-chip:hover{border-color:var(--gull);color:var(--mork)}
.ibp-chip.aktiv{background:var(--mork);border-color:var(--mork);color:#fff}
.ibp-rad{display:grid;grid-template-columns:7fr 5fr;gap:44px;align-items:center;
  background:#fff;border-radius:20px;overflow:hidden;margin-bottom:34px;
  box-shadow:0 2px 16px rgba(51,48,44,.08);
  opacity:0;translate:0 26px;transition:opacity .6s ease,translate .6s ease}
.ibp-rad.vis{opacity:1;translate:0 0}
.ibp-rad.skjult{display:none}
.ibp-rad:nth-child(even){grid-template-columns:5fr 7fr}
.ibp-rad:nth-child(even) .ibp-media{order:2}
.ibp-media{position:relative;cursor:zoom-in;align-self:stretch;min-height:340px}
.ibp-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transition:transform .6s ease}
.ibp-rad:hover .ibp-media img{transform:scale(1.045)}
.ibp-merker{position:absolute;left:14px;bottom:14px;display:flex;gap:7px}
.ibp-merke{font:600 11.5px Inter,sans-serif;background:rgba(24,22,19,.72);color:#fff;
  backdrop-filter:blur(3px);padding:8px 12px;border-radius:99px}
.ibp-innhold{padding:40px 44px 40px 0}
.ibp-rad:nth-child(even) .ibp-innhold{padding:40px 0 40px 44px}
.ibp-kat{font:600 11px Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gull);margin-bottom:10px;display:block}
.ibp-innhold h2{font-size:clamp(21px,2.4vw,27px);font-weight:700;line-height:1.25;
  margin-bottom:6px}
.ibp-sted{font:500 13.5px Inter,sans-serif;color:var(--grå);margin-bottom:14px;
  display:flex;align-items:center;gap:6px}
.ibp-sted svg{width:14px;height:14px;stroke:var(--gull);fill:none;stroke-width:1.8}
.ibp-innhold p{color:var(--grå);font-size:14.5px;line-height:1.75;margin-bottom:20px}
.ibp-knapp{display:inline-flex;align-items:center;gap:9px;background:var(--gull);
  color:#fff;font:600 14px Poppins,sans-serif;padding:12px 20px;border:0;
  border-radius:10px;cursor:pointer;transition:filter .2s}
.ibp-knapp:hover{filter:brightness(1.07)}
.ibp-lys{position:fixed;inset:0;z-index:9999;background:rgba(20,18,16,.94);display:none;
  align-items:center;justify-content:center;padding:34px;flex-direction:column;gap:14px}
.ibp-lys.vis{display:flex}
.ibp-lys img,.ibp-lys video{max-width:92vw;max-height:80vh;border-radius:8px;object-fit:contain}
.ibp-lys button{position:absolute;background:rgba(255,255,255,.12);border:0;color:#fff;
  width:46px;height:46px;border-radius:50%;font-size:21px;cursor:pointer;transition:background .2s}
.ibp-lys button:hover{background:rgba(255,255,255,.28)}
.ibp-lukk{top:22px;right:22px}
.ibp-forrige{left:22px;top:50%;translate:0 -50%}
.ibp-neste{right:22px;top:50%;translate:0 -50%}
.ibp-tekstlinje{color:#fff;font:500 13px Inter,sans-serif;opacity:.85;text-align:center}
@media(max-width:900px){
 .ibp-rad,.ibp-rad:nth-child(even){grid-template-columns:1fr}
 .ibp-rad:nth-child(even) .ibp-media{order:0}
 .ibp-media{min-height:250px}
 .ibp-innhold,.ibp-rad:nth-child(even) .ibp-innhold{padding:6px 26px 30px}}
</style>
"""

JS = """
<script>
(function(){
 var rader=[].slice.call(document.querySelectorAll('.ibp-rad')),
     filtre=document.getElementById('ibp-filtre'),
     lys=document.getElementById('ibp-lys'),ramme=document.getElementById('ibp-ramme'),
     linje=lys.querySelector('.ibp-tekstlinje'),liste=[],i=0,tittel='';
 filtre.addEventListener('click',function(e){
  var b=e.target.closest('.ibp-chip');if(!b)return;
  filtre.querySelectorAll('.ibp-chip').forEach(function(c){c.classList.remove('aktiv');});
  b.classList.add('aktiv');
  rader.forEach(function(r){
   r.classList.toggle('skjult',b.dataset.f!=='alle'&&r.dataset.kat!==b.dataset.f);});
 });
 function visMedia(){
  var m=liste[i],el;
  ramme.innerHTML='';
  if(/\\.mp4$/.test(m)){el=document.createElement('video');el.src=m;el.controls=true;
   el.autoplay=true;el.playsInline=true;}
  else{el=document.createElement('img');el.src=m;el.alt=tittel;}
  ramme.appendChild(el);
  linje.textContent=tittel+' — '+(i+1)+' / '+liste.length+(/\\.mp4$/.test(m)?' (video)':'');
 }
 function aapne(r){liste=r.dataset.media.split('|');tittel=r.dataset.tittel;i=0;
  lys.classList.add('vis');document.body.style.overflow='hidden';visMedia();}
 function lukk(){lys.classList.remove('vis');document.body.style.overflow='';ramme.innerHTML='';}
 rader.forEach(function(r){
  r.querySelector('.ibp-media').addEventListener('click',function(){aapne(r);});
  r.querySelector('.ibp-knapp').addEventListener('click',function(){aapne(r);});});
 lys.querySelector('.ibp-lukk').addEventListener('click',lukk);
 lys.querySelector('.ibp-forrige').addEventListener('click',function(){i=(i-1+liste.length)%liste.length;visMedia();});
 lys.querySelector('.ibp-neste').addEventListener('click',function(){i=(i+1)%liste.length;visMedia();});
 lys.addEventListener('click',function(e){if(e.target===lys)lukk();});
 document.addEventListener('keydown',function(e){
  if(!lys.classList.contains('vis'))return;
  if(e.key==='Escape')lukk();
  if(e.key==='ArrowLeft'||e.key==='Left'){i=(i-1+liste.length)%liste.length;visMedia();}
  if(e.key==='ArrowRight'||e.key==='Right'){i=(i+1)%liste.length;visMedia();}});
 if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
   if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target);}});},{threshold:.08});
  rader.forEach(function(r){io.observe(r);});
 }else rader.forEach(function(r){r.classList.add('vis');});
})();
</script>
"""

STED_IKON = ('<svg viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 '
             '5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>')


def bygg_side() -> None:
    kategorier = sorted({p["kategori"] for p in PROSJEKTER})
    chips = ['<button class="ibp-chip aktiv" data-f="alle">Alle</button>'] + [
        f'<button class="ibp-chip" data-f="{k}">{k}</button>' for k in kategorier]

    rader = []
    for p in PROSJEKTER:
        mappe = UT / p["slug"]
        bilder = sorted(x.name for x in mappe.glob("bilde-*.webp"))
        videoer = sorted(x.name for x in mappe.glob("video-*.mp4"))
        media = "|".join(f"../prosjekt-assets/{p['slug']}/{n}" for n in bilder + videoer)
        merker = [f'<span class="ibp-merke">{len(bilder)} bilder</span>']
        if videoer:
            merker.append(f'<span class="ibp-merke">▶ {len(videoer)} video'
                          + ("er" if len(videoer) > 1 else "") + '</span>')
        rader.append(f"""
<article class="ibp-rad" data-kat="{p['kategori']}" data-tittel="{p['tittel']}" data-media="{media}">
  <div class="ibp-media">
    <img src="../prosjekt-assets/{p['slug']}/{bilder[0]}" alt="{p['tittel']}" loading="lazy">
    <div class="ibp-merker">{''.join(merker)}</div>
  </div>
  <div class="ibp-innhold">
    <span class="ibp-kat">{p['kategori']}</span>
    <h2>{p['tittel']}</h2>
    <p class="ibp-sted">{STED_IKON}{p['sted']}</p>
    <p>{p['tekst']}</p>
    <button class="ibp-knapp">Se prosjektet <span aria-hidden="true">→</span></button>
  </div>
</article>""")

    nytt = f"""{CSS}
<section id="ibp">
 <div class="ibp-indre">
  <div class="ibp-topp">
    <p class="ibp-kicker">Referanser</p>
    <h1>Prosjekter</h1>
    <p class="ibp-intro">Et utvalg av prosjektene vi har gjennomført — fra
      totalrenoveringer og tilbygg til leilighetsbygg og næringsbygg.</p>
  </div>
  <div class="ibp-filtre" id="ibp-filtre">{''.join(chips)}</div>
  {''.join(rader)}
 </div>
 <div class="ibp-lys" id="ibp-lys" role="dialog" aria-label="Prosjektvisning">
   <div id="ibp-ramme"></div>
   <p class="ibp-tekstlinje"></p>
   <button class="ibp-lukk" aria-label="Lukk">✕</button>
   <button class="ibp-forrige" aria-label="Forrige">‹</button>
   <button class="ibp-neste" aria-label="Neste">›</button>
 </div>
</section>
{JS}"""

    fil = ROOT / "prosjekter" / "index.html"
    html = fil.read_text(encoding="utf-8")
    arkiv = Path(__file__).resolve().parent / "original-main" / "prosjekter.html"
    start = re.search(r"<main[^>]*>", html)
    end = html.find("</main>")
    if not arkiv.exists():
        arkiv.write_text(html[start.end():end], encoding="utf-8")
    fil.write_text(html[: start.end()] + nytt + html[end:], encoding="utf-8")
    print(f"Skrev prosjekter/index.html med {len(PROSJEKTER)} prosjekter")


if __name__ == "__main__":
    if sys.argv[1:] == ["assets"]:
        lag_assets()
    else:
        bygg_side()
