#!/usr/bin/env python3
"""Bytter ut innholdet i boligkatalog/index.html med nytt kortgalleri-design.

Header/footer fra Elementor beholdes; kun <main>-innholdet erstattes.
Kjøres fra repo-roten. Idempotent — hele main skrives på nytt hver gang.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "våre-boliger" / "index.html"

BOLIGER = [
    dict(slug="alva", navn="Alva", type="Enebolig", stil="Moderne",
         tagline="En moderne familiebolig med rom for livet",
         bra=214, braenhet=False, sov=5, bad=3, garasje=None, utleie=None, bod=3,
         bilde="wp-content/uploads/2025/04/Fasade-4"),
    dict(slug="edvard", navn="Edvard", type="Enebolig", stil="Klassisk",
         tagline="Klassisk eleganse med dobbel garasje og utleiedel",
         bra=315, braenhet=False, sov=5, bad=2, garasje="Dobbel", utleie="47 m²", bod=1,
         bilde="wp-content/uploads/2025/04/3-post-prod"),
    dict(slug="edvard-prakt", navn="Edvard Prakt", type="Enebolig", stil="Klassisk",
         tagline="En oppgradert versjon av tidløs eleganse",
         bra=337, braenhet=False, sov=5, bad=4, garasje="Dobbel", utleie="30 m²", bod=1,
         bilde="wp-content/uploads/2025/03/Fasade-fremside"),
    dict(slug="embla", navn="Embla", type="4-mannsbolig", stil="Klassisk",
         tagline="Klassisk 4-mannsbolig med moderne komfort",
         bra=84, braenhet=True, sov=2, bad=2, garasje=None, utleie=None, bod=1,
         bilde="wp-content/uploads/2025/04/Fasade-bakside"),
    dict(slug="nora", navn="Nora", type="Enebolig", stil="Klassisk",
         tagline="Drømmehjemmet for den moderne familien",
         bra=310, braenhet=False, sov=4, bad=2, garasje=None, utleie=None, bod=1,
         bilde="wp-content/uploads/2024/11/Fasade-Nora"),
    dict(slug="odin", navn="Odin", type="Enebolig", stil="Klassisk",
         tagline="Sjarmerende og kompakt med smart plassutnyttelse",
         bra=222, braenhet=False, sov=4, bad=2, garasje=None, utleie=None, bod=2,
         bilde="wp-content/uploads/2024/11/Fasade-fremside-post-prod"),
    dict(slug="tiril", navn="Tiril", type="Tomannsbolig", stil="Moderne",
         tagline="Romslig og moderne tomannsbolig over to etasjer",
         bra=176, braenhet=True, sov=4, bad=2, garasje="Ja", utleie=None, bod=1,
         bilde="wp-content/uploads/2025/06/Fasade-fremside"),
    dict(slug="vilde", navn="Vilde", type="Enebolig", stil="Funkis",
         tagline="Hypermoderne funkishus — et moderne mesterverk",
         bra=288, braenhet=False, sov=5, bad=2, garasje="Dobbel", utleie=None, bod=1,
         bilde="wp-content/uploads/2025/05/Fasade-Vilde"),
]


def beste_bilde(stem: str) -> str:
    """Foretrekk 1024- eller 768-variant for lastetid, ellers basefila."""
    for suffix in ("-1024x576", "-1024x572", "-768x432", "-768x429", ""):
        for ext in (".webp", ".png", ".jpg"):
            kandidat = ROOT / f"{stem}{suffix}{ext}"
            if kandidat.exists():
                return f"../{stem}{suffix}{ext}"
    raise FileNotFoundError(stem)


IKON = {
    "bra": '<svg viewBox="0 0 24 24"><path d="M3 3h18v18H3zM3 9h18M9 9v12" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
    "sov": '<svg viewBox="0 0 24 24"><path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M3 18h18M6 10V7h12v3" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
    "bad": '<svg viewBox="0 0 24 24"><path d="M4 12h16v2a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5v-2zM7 12V5a2 2 0 0 1 4 0" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
    "gar": '<svg viewBox="0 0 24 24"><path d="M3 20V9l9-5 9 5v11M7 20v-7h10v7M7 16h10" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>',
}


def kort(b: dict) -> str:
    bra_txt = f'{b["bra"]} m²' + (" <small>pr enhet</small>" if b["braenhet"] else "")
    chips = [f'<span class="ibk-spec">{IKON["bra"]}{bra_txt}</span>',
             f'<span class="ibk-spec">{IKON["sov"]}{b["sov"]} sov</span>',
             f'<span class="ibk-spec">{IKON["bad"]}{b["bad"]} bad</span>']
    if b["garasje"]:
        chips.append(f'<span class="ibk-spec">{IKON["gar"]}Garasje</span>')
    badges = [f'<span class="ibk-badge">{b["type"]}</span>']
    if b["utleie"]:
        badges.append(f'<span class="ibk-badge ibk-badge--gull">Utleiedel {b["utleie"]}</span>')
    return f"""
<a class="ibk-kort" href="../{b['slug']}/" data-navn="{b['navn'].lower()}" data-type="{b['type']}"
   data-stil="{b['stil'].lower()}" data-bra="{b['bra']}" data-sov="{b['sov']}"
   data-garasje="{1 if b['garasje'] else 0}" data-utleie="{1 if b['utleie'] else 0}">
  <div class="ibk-bilde"><img src="{beste_bilde(b['bilde'])}" alt="{b['navn']} — fasade" loading="lazy">
    <div class="ibk-badges">{''.join(badges)}</div></div>
  <div class="ibk-tekst">
    <h3>{b['navn']}</h3>
    <p class="ibk-tagline">{b['tagline']}</p>
    <div class="ibk-specs">{''.join(chips)}</div>
    <span class="ibk-cta">Se boligen <span aria-hidden="true">→</span></span>
  </div>
</a>"""


MAIN = """
<style>
#ibk{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:56px 20px 90px}
#ibk *{box-sizing:border-box;margin:0}
.ibk-indre{max-width:1200px;margin:0 auto}
.ibk-kicker{font:600 12px/1 Inter,sans-serif;letter-spacing:.22em;text-transform:uppercase;
  color:var(--gull);margin-bottom:14px}
#ibk h1{font-size:clamp(30px,4.5vw,46px);font-weight:700;line-height:1.1}
.ibk-intro{color:var(--grå);max-width:560px;margin-top:14px;line-height:1.6}
.ibk-verktoy{display:flex;flex-wrap:wrap;gap:12px;align-items:center;
  margin:36px 0 8px;padding:14px;background:#fff;border-radius:14px;
  box-shadow:0 2px 14px rgba(51,48,44,.07)}
.ibk-sok{flex:1 1 200px;position:relative}
.ibk-sok input{width:100%;padding:11px 14px 11px 38px;border:1px solid #E3DCCF;
  border-radius:9px;font:400 14px Poppins,sans-serif;background:var(--krem);outline:none}
.ibk-sok input:focus{border-color:var(--gull)}
.ibk-sok svg{position:absolute;left:12px;top:50%;translate:0 -50%;width:16px;height:16px;
  stroke:var(--grå);fill:none;stroke-width:2}
.ibk-filtre{display:flex;flex-wrap:wrap;gap:8px}
.ibk-chip{padding:9px 15px;border:1px solid #E3DCCF;border-radius:99px;background:#fff;
  font:500 13px Poppins,sans-serif;color:var(--grå);cursor:pointer;transition:.18s}
.ibk-chip:hover{border-color:var(--gull);color:var(--mork)}
.ibk-chip.aktiv{background:var(--mork);border-color:var(--mork);color:#fff}
.ibk-verktoy select{padding:10px 12px;border:1px solid #E3DCCF;border-radius:9px;
  font:500 13px Poppins,sans-serif;color:var(--mork);background:#fff;cursor:pointer}
.ibk-antall{font:500 13px Inter,sans-serif;color:var(--grå);margin:14px 2px 18px}
.ibk-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:26px}
.ibk-kort{display:flex;flex-direction:column;background:#fff;border-radius:16px;overflow:hidden;
  text-decoration:none;color:inherit;box-shadow:0 2px 14px rgba(51,48,44,.08);
  transition:transform .28s ease,box-shadow .28s ease;opacity:0;translate:0 22px}
.ibk-kort.vis{opacity:1;translate:0 0;transition:transform .28s ease,box-shadow .28s ease,
  opacity .5s ease,translate .5s ease}
.ibk-kort:hover{transform:translateY(-6px);box-shadow:0 14px 34px rgba(51,48,44,.16)}
.ibk-kort.skjult{display:none}
.ibk-bilde{position:relative;aspect-ratio:16/10;overflow:hidden;background:#E9E2D4}
.ibk-bilde img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.ibk-kort:hover .ibk-bilde img{transform:scale(1.06)}
.ibk-badges{position:absolute;left:12px;top:12px;display:flex;gap:6px;flex-wrap:wrap}
.ibk-badge{font:600 11px/1 Inter,sans-serif;letter-spacing:.04em;color:var(--mork);
  background:rgba(255,255,255,.92);padding:7px 11px;border-radius:99px}
.ibk-badge--gull{background:var(--gull);color:#fff}
.ibk-tekst{display:flex;flex-direction:column;gap:9px;padding:20px 22px 22px;flex:1}
.ibk-tekst h3{font-size:21px;font-weight:700}
.ibk-tagline{font-size:13.5px;color:var(--grå);line-height:1.5;flex:1}
.ibk-specs{display:flex;flex-wrap:wrap;gap:7px;margin-top:2px}
.ibk-spec{display:inline-flex;align-items:center;gap:6px;font:500 12px Inter,sans-serif;
  color:var(--mork);background:var(--krem);padding:7px 10px;border-radius:8px}
.ibk-spec svg{width:15px;height:15px;color:var(--gull)}
.ibk-spec small{font-weight:400;color:var(--grå)}
.ibk-cta{margin-top:12px;font:600 14px Poppins,sans-serif;color:var(--gull);
  display:inline-flex;gap:7px;align-items:center;transition:gap .2s}
.ibk-kort:hover .ibk-cta{gap:12px}
.ibk-tom{display:none;text-align:center;padding:70px 0;color:var(--grå)}
.ibk-tom.vis{display:block}
.ibk-tom button{margin-top:14px;padding:11px 22px;border:0;border-radius:9px;cursor:pointer;
  background:var(--gull);color:#fff;font:600 14px Poppins,sans-serif}
@media(max-width:640px){.ibk-verktoy{padding:12px}.ibk-grid{gap:18px}}
</style>
<section id="ibk">
 <div class="ibk-indre">
  <p class="ibk-kicker">Boligkatalog</p>
  <h1>Våre boliger</h1>
  <p class="ibk-intro">Åtte gjennomtenkte boligmodeller — fra kompakte klassikere til
    moderne funkis. Filtrer og sorter for å finne boligen som passer deg.</p>
  <div class="ibk-verktoy">
    <div class="ibk-sok"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>
      <input id="ibk-sok" type="search" placeholder="Søk etter modellnavn …" aria-label="Søk"></div>
    <div class="ibk-filtre" id="ibk-filtre">
      <button class="ibk-chip aktiv" data-f="alle">Alle</button>
      <button class="ibk-chip" data-f="type:Enebolig">Enebolig</button>
      <button class="ibk-chip" data-f="type:Tomannsbolig">Tomannsbolig</button>
      <button class="ibk-chip" data-f="type:4-mannsbolig">4-mannsbolig</button>
      <button class="ibk-chip" data-f="garasje">Med garasje</button>
      <button class="ibk-chip" data-f="utleie">Med utleiedel</button>
    </div>
    <select id="ibk-sort" aria-label="Sortering">
      <option value="navn">Navn A–Å</option>
      <option value="bra-ned">Størst først</option>
      <option value="bra-opp">Minst først</option>
      <option value="sov-ned">Flest soverom</option>
    </select>
  </div>
  <p class="ibk-antall" id="ibk-antall"></p>
  <div class="ibk-grid" id="ibk-grid">__KORT__</div>
  <div class="ibk-tom" id="ibk-tom"><p>Ingen boliger matcher valgene dine.</p>
    <button id="ibk-nullstill">Nullstill filter</button></div>
 </div>
</section>
<script>
(function(){
 var grid=document.getElementById('ibk-grid'),kort=[].slice.call(grid.children),
     sok=document.getElementById('ibk-sok'),sort=document.getElementById('ibk-sort'),
     antall=document.getElementById('ibk-antall'),tom=document.getElementById('ibk-tom'),
     filtre=document.getElementById('ibk-filtre'),aktiv='alle';
 function oppdater(){
  var q=sok.value.trim().toLowerCase(),n=0;
  kort.forEach(function(k){
   var ok=(!q||k.dataset.navn.indexOf(q)>-1);
   if(aktiv!=='alle'){
    if(aktiv.indexOf('type:')===0) ok=ok&&k.dataset.type===aktiv.slice(5);
    else ok=ok&&k.dataset[aktiv]==='1';
   }
   k.classList.toggle('skjult',!ok); if(ok)n++;
  });
  antall.textContent=n===kort.length?'Viser alle '+n+' boligmodeller':'Viser '+n+' av '+kort.length+' boligmodeller';
  tom.classList.toggle('vis',n===0);
  var s=sort.value;
  kort.slice().sort(function(a,b){
   if(s==='bra-ned')return b.dataset.bra-a.dataset.bra;
   if(s==='bra-opp')return a.dataset.bra-b.dataset.bra;
   if(s==='sov-ned')return b.dataset.sov-a.dataset.sov||b.dataset.bra-a.dataset.bra;
   return a.dataset.navn<b.dataset.navn?-1:1;
  }).forEach(function(k){grid.appendChild(k);});
 }
 filtre.addEventListener('click',function(e){
  var b=e.target.closest('.ibk-chip');if(!b)return;
  filtre.querySelectorAll('.ibk-chip').forEach(function(c){c.classList.remove('aktiv');});
  b.classList.add('aktiv');aktiv=b.dataset.f;oppdater();
 });
 document.getElementById('ibk-nullstill').addEventListener('click',function(){
  sok.value='';aktiv='alle';
  filtre.querySelectorAll('.ibk-chip').forEach(function(c){c.classList.toggle('aktiv',c.dataset.f==='alle');});
  oppdater();
 });
 sok.addEventListener('input',oppdater);sort.addEventListener('change',oppdater);
 oppdater();
 if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
   if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target);}});},{threshold:.12});
  kort.forEach(function(k,i){k.style.transitionDelay=(i%3*70)+'ms';io.observe(k);});
 }else kort.forEach(function(k){k.classList.add('vis');});
})();
</script>
"""


def main() -> None:
    html = PAGE.read_text(encoding="utf-8")
    start = re.search(r'<main[^>]*>', html)
    end = html.find("</main>")
    kortene = "".join(kort(b) for b in BOLIGER)
    nytt = MAIN.replace("__KORT__", kortene)
    PAGE.write_text(html[: start.end()] + nytt + html[end:], encoding="utf-8")
    print(f"Skrev nytt katalogdesign ({len(nytt)} tegn) inn i {PAGE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
