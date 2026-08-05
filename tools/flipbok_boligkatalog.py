#!/usr/bin/env python3
"""Bygger bla-katalogen (flipbok) på /boligkatalog/ — inspirert av caddieboka i
CourseCraft (rotateY-hengsel rundt bokryggen, solo-forside med kamera-skyv,
hjørnebrett som inviterer til blading).

Sideskall (header/footer) hentes fra våre-boliger/index.html.
Kjøres fra repo-roten etter meny_boligkatalog.py. Idempotent.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nytt_boligkatalog import BOLIGER, beste_bilde  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARKIV = Path(__file__).resolve().parent / "original-main"


def kort_tekst(slug: str, maks: int = 250) -> str:
    """Første avsnitt fra boligsidens originaltekst, kuttet på ordgrense."""
    kilde = (ARKIV / f"{slug}.html").read_text(encoding="utf-8")
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", kilde, re.S):
        txt = re.sub(r"<[^>]+>", " ", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) > 60:
            if len(txt) <= maks:
                return txt
            kutt = txt[:maks].rsplit(" ", 1)[0]
            return kutt.rstrip(",.;:") + " …"
    return ""


def spread_html(b: dict) -> tuple[str, str]:
    bra = f'{b["bra"]} m²' + (" pr enhet" if b["braenhet"] else "")
    specs = [("BRA", bra), ("Soverom", str(b["sov"])), ("Bad", str(b["bad"]))]
    if b["garasje"]:
        specs.append(("Garasje", b["garasje"]))
    if b["utleie"]:
        specs.append(("Utleiedel", b["utleie"]))
    spec_html = "".join(f'<div class="fb-spec"><span>{k}</span><b>{v}</b></div>'
                        for k, v in specs)
    venstre = (f'<div class="fb-foto"><img src="{beste_bilde(b["bilde"])}" alt="{b["navn"]}">'
               f'<p>{b["navn"]}</p></div>')
    høyre = f"""<div class="fb-info">
      <p class="fb-kicker">{b['type']} · {b['stil']}</p>
      <h3>{b['navn']}</h3>
      <p class="fb-tagline">{b['tagline']}</p>
      <div class="fb-specs">{spec_html}</div>
      <p class="fb-tekst">{kort_tekst(b['slug'])}</p>
      <a class="fb-lenke" href="../{b['slug']}/">Se boligen på nettsiden →</a>
    </div>"""
    return venstre, høyre


def bygg() -> None:
    forside = """<div class="fb-perm">
      <img src="../wp-content/uploads/2024/11/Hvit-logo-sidestilt.png" alt="Idébolig AS">
      <div class="fb-permlinje"></div>
      <h2>Boligkatalog</h2>
      <p>Åtte boliger — fra klassisk til funkis</p>
      <span class="fb-permhint">Klikk eller bruk piltastene for å bla</span>
    </div>"""
    bakside = """<div class="fb-perm fb-perm--bak">
      <img src="../wp-content/uploads/2024/11/Hvit-logo-sidestilt.png" alt="Idébolig AS">
      <div class="fb-permlinje"></div>
      <p>Idébolig AS · Jølstadbakken 14, 2318 Hamar</p>
      <p>91 92 66 66 · post@idebolig.no</p>
      <a class="fb-permlenke" href="../kontakt/">Ta kontakt →</a>
    </div>"""

    sider = [None, forside]  # spread 0: solo forside
    for b in BOLIGER:
        v, h = spread_html(b)
        sider += [v, h]
    sider += [bakside, None]  # siste spread: solo bakside

    spreads = [[sider[i], sider[i + 1]] for i in range(0, len(sider), 2)]
    spread_divs = "".join(
        f'<template id="fb-s{i}l">{v or ""}</template>'
        f'<template id="fb-s{i}r">{h or ""}</template>'
        for i, (v, h) in enumerate(spreads))
    solo = [i for i, (v, h) in enumerate(spreads) if v is None or h is None]

    main = f"""
<style>
#fbk{{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;--papir:#FDFBF7;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:80px 20px 100px;overflow:hidden}}
:where(#fbk *){{box-sizing:border-box;margin:0}}
.fbk-indre{{max-width:1160px;margin:0 auto}}
.fbk-topp{{max-width:640px;margin:0 auto 44px;text-align:center}}
.fbk-kicker{{display:flex;align-items:center;justify-content:center;gap:14px;
  font:600 12px/1 Inter,sans-serif;letter-spacing:.24em;text-transform:uppercase;
  color:var(--gull);margin-bottom:20px}}
.fbk-kicker::before,.fbk-kicker::after{{content:"";flex:0 0 46px;height:1px;
  background:var(--gull);opacity:.55}}
#fbk h1{{font-size:clamp(32px,4.5vw,48px);font-weight:700;letter-spacing:-.015em;
  margin-bottom:16px}}
.fbk-intro{{color:var(--grå);font-size:15.5px;line-height:1.7}}
.fb-scene{{perspective:2600px;max-width:1020px;margin:0 auto}}
.fb-stack{{position:relative;width:100%;aspect-ratio:3/2;
  transition:translate 1.15s cubic-bezier(.36,.04,.22,1);will-change:translate}}
.fb-halv{{position:absolute;top:0;bottom:0;width:50%;background:var(--papir);
  overflow:hidden;box-shadow:0 18px 50px rgba(51,48,44,.22)}}
.fb-halv--v{{left:0;border-radius:10px 2px 2px 10px}}
.fb-halv--h{{right:0;border-radius:2px 10px 10px 2px}}
.fb-halv--v::after{{content:"";position:absolute;inset:0 0 0 auto;width:34px;
  background:linear-gradient(to left,rgba(0,0,0,.09),transparent)}}
.fb-halv--h::after{{content:"";position:absolute;inset:0 auto 0 0;width:34px;
  background:linear-gradient(to right,rgba(0,0,0,.09),transparent)}}
.fb-halv.fb-blank{{visibility:hidden}}
.fb-leaf{{position:absolute;top:0;bottom:0;left:50%;width:50%;
  transform-style:preserve-3d;transform-origin:left center;z-index:5;
  will-change:transform;--fb-ms:1150ms}}
.fb-leaf-f,.fb-leaf-b{{position:absolute;inset:0;backface-visibility:hidden;
  background:var(--papir);overflow:hidden;border-radius:2px 10px 10px 2px;
  transform:translateZ(0)}}
.fb-leaf-b{{transform:rotateY(180deg) translateZ(0);border-radius:10px 2px 2px 10px}}
.fb-leaf-f::after,.fb-leaf-b::after{{content:"";position:absolute;inset:0;
  pointer-events:none;opacity:0;
  background:linear-gradient(to right,rgba(24,22,19,.30),rgba(24,22,19,.06) 55%,transparent);
  animation:fbSkygge var(--fb-ms) ease-in-out forwards}}
@keyframes fbSkygge{{0%{{opacity:0}}45%{{opacity:1}}100%{{opacity:0}}}}
@keyframes fbNeste{{0%{{transform:rotateY(0) rotateX(0)}}
  30%{{transform:rotateY(-54deg) rotateX(1.6deg)}}
  50%{{transform:rotateY(-90deg) rotateX(2deg)}}
  70%{{transform:rotateY(-126deg) rotateX(1.6deg)}}
  100%{{transform:rotateY(-180deg) rotateX(0)}}}}
@keyframes fbForrige{{0%{{transform:rotateY(-180deg) rotateX(0)}}
  30%{{transform:rotateY(-126deg) rotateX(1.6deg)}}
  50%{{transform:rotateY(-90deg) rotateX(2deg)}}
  70%{{transform:rotateY(-54deg) rotateX(1.6deg)}}
  100%{{transform:rotateY(0) rotateX(0)}}}}
.fb-hjorne{{position:absolute;top:0;width:74px;height:74px;pointer-events:none;
  opacity:0;transition:opacity .3s;z-index:6}}
.fb-hjorne--h{{right:0;clip-path:polygon(100% 0,0 0,100% 100%);
  background:radial-gradient(circle at 100% 0,#fff 0%,#EDE6D8 55%,#D9CFBB 100%);
  filter:drop-shadow(-3px 3px 4px rgba(0,0,0,.18))}}
.fb-hjorne--v{{left:0;clip-path:polygon(0 0,100% 0,0 100%);
  background:radial-gradient(circle at 0 0,#fff 0%,#EDE6D8 55%,#D9CFBB 100%);
  filter:drop-shadow(3px 3px 4px rgba(0,0,0,.18))}}
.fb-scene:hover .fb-hjorne.fb-kan{{opacity:.9}}
.fb-side-innhold{{position:absolute;inset:0}}
.fb-foto{{position:absolute;inset:0}}
.fb-foto img{{width:100%;height:100%;object-fit:cover}}
.fb-foto p{{position:absolute;left:0;right:0;bottom:0;padding:26px 28px 18px;
  color:#fff;font:700 24px Poppins,sans-serif;
  background:linear-gradient(to top,rgba(24,22,19,.72),transparent)}}
.fb-info{{position:absolute;inset:0;padding:8% 9%;display:flex;flex-direction:column}}
.fb-kicker{{font:600 10.5px Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;
  color:var(--gull);margin-bottom:10px}}
.fb-info h3{{font-size:clamp(20px,2.6vw,30px);font-weight:700;margin-bottom:6px}}
.fb-tagline{{color:var(--grå);font-size:clamp(11px,1.3vw,14px);line-height:1.55;margin-bottom:14px}}
.fb-specs{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:14px}}
.fb-spec{{background:var(--krem);border-radius:8px;padding:8px 11px}}
.fb-spec span{{display:block;font:600 9px Inter,sans-serif;letter-spacing:.12em;
  text-transform:uppercase;color:var(--gull)}}
.fb-spec b{{font-size:clamp(11px,1.4vw,14.5px)}}
.fb-tekst{{color:var(--grå);font-size:clamp(10.5px,1.25vw,13.5px);line-height:1.65;flex:1;overflow:hidden}}
.fb-lenke{{font:600 clamp(11px,1.3vw,14px) Poppins,sans-serif;color:var(--gull);text-decoration:none}}
.fb-perm{{position:absolute;inset:0;background:linear-gradient(150deg,#3A362F,#26231F);
  color:#D9D2C5;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;padding:10%}}
.fb-perm img{{width:46%;max-width:230px;margin-bottom:22px}}
.fb-permlinje{{width:52px;height:2px;background:var(--gull);margin-bottom:22px}}
.fb-perm h2{{font-size:clamp(24px,3.4vw,38px);font-weight:700;color:#fff;
  letter-spacing:.04em;margin-bottom:10px}}
.fb-perm p{{font-size:clamp(11px,1.4vw,15px);line-height:1.7}}
.fb-permhint{{margin-top:26px;font:500 clamp(10px,1.2vw,12.5px) Inter,sans-serif;opacity:.65}}
.fb-permlenke{{margin-top:18px;font:600 clamp(12px,1.4vw,15px) Poppins,sans-serif;
  color:var(--gull);text-decoration:none}}
.fbk-kontroll{{display:flex;align-items:center;justify-content:center;gap:20px;margin-top:34px}}
.fbk-kontroll button{{width:46px;height:46px;border-radius:50%;border:1.5px solid #E3DCCF;
  background:#fff;color:var(--mork);font-size:19px;cursor:pointer;transition:.2s}}
.fbk-kontroll button:hover:not([disabled]){{background:var(--gull);border-color:var(--gull);color:#fff}}
.fbk-kontroll button[disabled]{{opacity:.35;cursor:default}}
.fbk-teller{{font:500 13.5px Inter,sans-serif;color:var(--grå);min-width:110px;text-align:center}}
.fbk-kontroll button{{flex:0 0 46px;padding:0;line-height:1;min-width:0}}
@media(hover:none){{.fb-hjorne{{display:none}}}}
@media(max-width:700px){{
 #fbk{{padding:56px 0 70px}}
 .fbk-topp{{padding:0 16px}}
 .fb-scene{{overflow:hidden;perspective:1400px}}
 .fb-stack{{width:200%;transition:translate .8s cubic-bezier(.36,.04,.22,1)}}
 .fb-halv--v{{border-radius:10px}}
 .fb-halv--h{{border-radius:10px}}
 .fb-specs{{gap:5px}}
 .fb-foto p{{font-size:19px}}
 .fb-info{{padding:7% 8%}}
}}
</style>
<section id="fbk">
 <div class="fbk-indre">
  <div class="fbk-topp">
    <p class="fbk-kicker">Bla i katalogen</p>
    <h1>Boligkatalog</h1>
    <p class="fbk-intro">Bla deg gjennom boligene våre som i en ekte katalog —
      klikk på sidene, bruk pilene eller sveip.</p>
  </div>
  <div class="fb-scene" id="fb-scene">
    <div class="fb-stack" id="fb-stack">
      <div class="fb-halv fb-halv--v" id="fb-venstre"></div>
      <div class="fb-halv fb-halv--h" id="fb-hoyre"></div>
      <div class="fb-hjorne fb-hjorne--v" id="fb-hj-v"></div>
      <div class="fb-hjorne fb-hjorne--h" id="fb-hj-h"></div>
    </div>
  </div>
  <div class="fbk-kontroll">
    <button id="fb-forrige" aria-label="Forrige side">‹</button>
    <span class="fbk-teller" id="fb-teller"></span>
    <button id="fb-neste" aria-label="Neste side">›</button>
  </div>
  {spread_divs}
 </div>
</section>
<script>
(function(){{
 var ANTALL={len(spreads)},SOLO={solo},i=0,side='r',laast=false,MS=1150;
 var v=document.getElementById('fb-venstre'),h=document.getElementById('fb-hoyre'),
     stack=document.getElementById('fb-stack'),teller=document.getElementById('fb-teller'),
     knappF=document.getElementById('fb-forrige'),knappN=document.getElementById('fb-neste'),
     hjV=document.getElementById('fb-hj-v'),hjH=document.getElementById('fb-hj-h'),
     smal=window.matchMedia('(max-width:700px)');
 function harInnhold(s,kant){{var tpl=document.getElementById('fb-s'+s+kant);
  return !!(tpl&&tpl.content.firstElementChild);}}
 // flat sideliste til telleren på mobil
 var SIDER=[];
 for(var s=0;s<ANTALL;s++){{['l','r'].forEach(function(kant){{
  if(harInnhold(s,kant))SIDER.push(s+kant);}});}}
 function inn(el,id){{var tpl=document.getElementById(id);el.innerHTML='';
  if(tpl&&tpl.content.firstElementChild){{el.appendChild(tpl.content.firstElementChild.cloneNode(true));
   el.classList.remove('fb-blank');}}else el.classList.add('fb-blank');}}
 function mobil(){{return smal.matches;}}
 function fiksSide(){{
  if(!harInnhold(i,'l'))side='r';
  else if(!harInnhold(i,'r'))side='l';
 }}
 function vis(){{
  inn(v,'fb-s'+i+'l');inn(h,'fb-s'+i+'r');
  if(mobil()){{
   fiksSide();
   stack.style.translate=(side==='r')?'-50%':'0';
   teller.textContent='Side '+(SIDER.indexOf(i+side)+1)+' av '+SIDER.length;
   knappF.disabled=(i===0&&side==='r'&&!harInnhold(0,'l'))||(i===0&&side==='l');
   knappN.disabled=(i===ANTALL-1&&side==='l'&&!harInnhold(ANTALL-1,'r'))||(i===ANTALL-1&&side==='r');
   if(i===0)knappF.disabled=true;
   if(i===ANTALL-1)knappN.disabled=(side==='l'&&!harInnhold(ANTALL-1,'r'))||side==='r'||!harInnhold(ANTALL-1,'r');
  }}else{{
   stack.style.translate=(SOLO.indexOf(i)>-1)?(v.classList.contains('fb-blank')?'-25%':'25%'):'0';
   teller.textContent=i===0?'Forside':(i===ANTALL-1?'Bakside':'Oppslag '+i+' av '+(ANTALL-2));
   knappF.disabled=i===0;knappN.disabled=i===ANTALL-1;
  }}
  hjH.classList.toggle('fb-kan',i<ANTALL-1);hjV.classList.toggle('fb-kan',i>0);
 }}
 function vend(retning,etterSide){{
  var ny=i+retning;
  if(laast||ny<0||ny>=ANTALL)return;
  laast=true;
  var leaf=document.createElement('div');leaf.className='fb-leaf';
  var ff=document.createElement('div');ff.className='fb-leaf-f';
  var fb=document.createElement('div');fb.className='fb-leaf-b';
  leaf.appendChild(ff);leaf.appendChild(fb);
  var anim;
  if(retning>0){{inn(ff,'fb-s'+i+'r');inn(fb,'fb-s'+ny+'l');inn(h,'fb-s'+ny+'r');
   anim='fbNeste';}}
  else{{leaf.style.transform='rotateY(-180deg)';
   inn(ff,'fb-s'+ny+'r');inn(fb,'fb-s'+i+'l');inn(v,'fb-s'+ny+'l');
   anim='fbForrige';}}
  stack.appendChild(leaf);
  var maalTranslate;
  if(mobil()){{
   side=etterSide;
   if(!harInnhold(ny,side==='l'?'l':'r'))side=(side==='l')?'r':'l';
   maalTranslate=(side==='r')?'-50%':'0';
  }}else{{
   maalTranslate=(SOLO.indexOf(ny)>-1)?(ny===0?'25%':'-25%'):'0';
  }}
  var ferdig=false;
  function avslutt(){{if(ferdig)return;ferdig=true;i=ny;vis();leaf.remove();laast=false;}}
  leaf.addEventListener('animationend',avslutt);
  setTimeout(avslutt,MS+250); // sikkerhetsnett
  // la DOM-byttet males ferdig foer animasjonen starter (unngaar hakking)
  void leaf.offsetWidth;
  requestAnimationFrame(function(){{requestAnimationFrame(function(){{
   leaf.style.animation=anim+' '+MS+'ms cubic-bezier(.36,.04,.22,1) forwards';
   stack.style.translate=maalTranslate;
  }});}});
 }}
 function bla(retning){{
  if(laast)return;
  if(mobil()){{
   if(retning>0){{
    if(side==='l'&&harInnhold(i,'r')){{side='r';vis();}}
    else vend(1,'l');
   }}else{{
    if(side==='r'&&harInnhold(i,'l')){{side='l';vis();}}
    else vend(-1,'r');
   }}
  }}else vend(retning,retning>0?'l':'r');
 }}
 smal.addEventListener('change',function(){{fiksSide();vis();}});
 knappN.addEventListener('click',function(){{bla(1);}});
 knappF.addEventListener('click',function(){{bla(-1);}});
 h.addEventListener('click',function(e){{if(!e.target.closest('a'))bla(1);}});
 v.addEventListener('click',function(e){{if(!e.target.closest('a'))bla(-1);}});
 document.addEventListener('keydown',function(e){{
  if(e.key==='ArrowRight'||e.key==='Right')bla(1);
  if(e.key==='ArrowLeft'||e.key==='Left')bla(-1);}});
 var sx=null;
 stack.addEventListener('touchstart',function(e){{sx=e.touches[0].clientX;}},{{passive:true}});
 stack.addEventListener('touchend',function(e){{if(sx===null)return;
  var dx=e.changedTouches[0].clientX-sx;sx=null;
  if(dx<-40)bla(1);if(dx>40)bla(-1);}},{{passive:true}});
 vis();
 // forhaandsdekod alle katalogbilder i ledig tid - ingen dekoding midt i bladingen
 function forhaandslast(){{
  var sett={{}};
  [].slice.call(document.querySelectorAll('#fbk template')).forEach(function(tpl){{
   [].slice.call(tpl.content.querySelectorAll('img')).forEach(function(im){{
    var s=im.getAttribute('src');if(s&&!sett[s]){{sett[s]=1;
     var b=new Image();b.src=s;if(b.decode)b.decode().catch(function(){{}});}}}});}});
 }}
 if('requestIdleCallback' in window)requestIdleCallback(forhaandslast,{{timeout:2500}});
 else setTimeout(forhaandslast,1200);
}})();
</script>
"""

    skall = (ROOT / "våre-boliger" / "index.html").read_text(encoding="utf-8")
    start = re.search(r"<main[^>]*>", skall)
    end = skall.find("</main>")
    side = skall[: start.end()] + main + skall[end:]
    side = side.replace("<title>Boligkatalog – Idébolig AS</title>",
                        "<title>Boligkatalog – Idébolig AS</title>")
    (ROOT / "boligkatalog").mkdir(exist_ok=True)
    (ROOT / "boligkatalog" / "index.html").write_text(side, encoding="utf-8")
    print(f"Skrev flipbok med {len(spreads)} oppslag til boligkatalog/index.html")


if __name__ == "__main__":
    bygg()
