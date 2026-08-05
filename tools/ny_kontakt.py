#!/usr/bin/env python3
"""Nytt design på kontaktsiden med klargjort skjema.

Skjemaet har honeypot + validering og er klart for Web3Forms/Turnstile:
sett ENDPOINT og ACCESS_KEY når mottaksadresse er avklart (IB1.11).
Inntil da viser innsending en vennlig melding med direkte kontaktinfo.
Kjøres fra repo-roten. Original main arkiveres i tools/original-main/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EMNER = ["Byggteknisk rådgivning", "Byggesøknad", "Arkitekttjenester",
         "Prosjektering", "Utførelse og montasje", "Boligkatalog"]

IKON = {
    "tlf": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a12 12 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
    "post": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m3 7 9 6 9-6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
    "sted": '<svg viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10" r="2.6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>',
}

MAIN = f"""
<style>
#ibk2{{--gull:#C99C55;--mork:#33302C;--grå:#6b6257;--krem:#F7F3EC;
  font-family:Poppins,sans-serif;color:var(--mork);background:var(--krem);
  padding:88px 20px 100px}}
:where(#ibk2 *){{box-sizing:border-box;margin:0}}
.ibk2-indre{{max-width:1200px;margin:0 auto}}
.ibk2-topp{{max-width:640px;margin-bottom:52px}}
.ibk2-kicker{{display:flex;align-items:center;gap:14px;font:600 12px/1 Inter,sans-serif;
  letter-spacing:.24em;text-transform:uppercase;color:var(--gull);margin-bottom:22px}}
.ibk2-kicker::after{{content:"";flex:0 0 46px;height:1px;background:var(--gull);opacity:.55}}
#ibk2 h1{{font-size:clamp(34px,4.5vw,52px);font-weight:700;line-height:1.14;
  letter-spacing:-.015em;margin-bottom:20px}}
.ibk2-intro{{color:var(--grå);font-size:16px;line-height:1.75}}
.ibk2-grid{{display:grid;grid-template-columns:7fr 5fr;gap:34px;align-items:start}}
.ibk2-skjema{{background:#fff;border-radius:20px;padding:38px;
  box-shadow:0 2px 16px rgba(51,48,44,.08)}}
.ibk2-felt{{margin-bottom:20px}}
.ibk2-to{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.ibk2-felt label{{display:block;font:600 12.5px Inter,sans-serif;margin-bottom:7px}}
.ibk2-felt label small{{color:var(--gull)}}
.ibk2-felt input,.ibk2-felt select,.ibk2-felt textarea{{width:100%;padding:13px 15px;
  border:1.5px solid #E3DCCF;border-radius:10px;background:var(--krem);
  font:400 14.5px Poppins,sans-serif;color:var(--mork);outline:none;
  transition:border-color .2s,box-shadow .2s}}
.ibk2-felt input:focus,.ibk2-felt select:focus,.ibk2-felt textarea:focus{{
  border-color:var(--gull);box-shadow:0 0 0 3px rgba(201,156,85,.18);background:#fff}}
.ibk2-felt textarea{{min-height:140px;resize:vertical}}
.ibk2-felt .ugyldig{{border-color:#C0492F}}
.ibk2-feil{{display:none;font:500 12px Inter,sans-serif;color:#C0492F;margin-top:6px}}
.ibk2-hp{{position:absolute;left:-6000px;top:auto;height:1px;overflow:hidden}}
.ibk2-send{{display:inline-flex;align-items:center;gap:10px;background:var(--gull);
  color:#fff;font:600 15px Poppins,sans-serif;padding:14px 26px;border:0;
  border-radius:10px;cursor:pointer;transition:filter .2s}}
.ibk2-send:hover{{filter:brightness(1.07)}}
.ibk2-send[disabled]{{opacity:.6;cursor:wait}}
.ibk2-status{{display:none;margin-top:18px;padding:15px 17px;border-radius:10px;
  font:500 13.5px Inter,sans-serif;line-height:1.6}}
.ibk2-status.ok{{display:block;background:#EDF5EC;color:#2E5E2A}}
.ibk2-status.info{{display:block;background:#F7EFE2;color:#7A5A22}}
.ibk2-status a{{color:inherit}}
.ibk2-info{{display:flex;flex-direction:column;gap:16px}}
.ibk2-kort{{display:flex;gap:16px;align-items:flex-start;background:#fff;
  border-radius:16px;padding:22px;box-shadow:0 2px 14px rgba(51,48,44,.07);
  text-decoration:none;color:inherit;transition:transform .25s,box-shadow .25s}}
a.ibk2-kort:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(51,48,44,.13)}}
.ibk2-ikon{{flex:0 0 44px;height:44px;border-radius:12px;background:var(--krem);
  display:flex;align-items:center;justify-content:center;color:var(--gull)}}
.ibk2-ikon svg{{width:21px;height:21px}}
.ibk2-kort b{{display:block;font-size:15.5px;margin-bottom:3px}}
.ibk2-kort span{{color:var(--grå);font-size:13.5px;line-height:1.55}}
.ibk2-svar{{background:var(--mork);color:#D9D2C5;border-radius:16px;padding:24px}}
.ibk2-svar b{{color:#fff;display:block;margin-bottom:6px;font-size:15.5px}}
.ibk2-svar span{{font-size:13.5px;line-height:1.6}}
@media(max-width:900px){{.ibk2-grid{{grid-template-columns:1fr}}
 .ibk2-to{{grid-template-columns:1fr}}.ibk2-skjema{{padding:26px}}}}
</style>
<section id="ibk2">
 <div class="ibk2-indre">
  <div class="ibk2-topp">
    <p class="ibk2-kicker">Kontakt</p>
    <h1>La oss gjøre ideen til virkelighet</h1>
    <p class="ibk2-intro">Fortell oss kort om planene dine — så tar vi kontakt for en
      uforpliktende prat om hvordan vi kan hjelpe deg videre.</p>
  </div>
  <div class="ibk2-grid">
   <form class="ibk2-skjema" id="ibk2-form" novalidate>
    <div class="ibk2-to">
      <div class="ibk2-felt"><label for="f-navn">Navn <small>*</small></label>
        <input id="f-navn" name="navn" type="text" autocomplete="name" required>
        <p class="ibk2-feil">Skriv inn navnet ditt.</p></div>
      <div class="ibk2-felt"><label for="f-epost">E-post <small>*</small></label>
        <input id="f-epost" name="epost" type="email" autocomplete="email" required>
        <p class="ibk2-feil">Skriv inn en gyldig e-postadresse.</p></div>
    </div>
    <div class="ibk2-to">
      <div class="ibk2-felt"><label for="f-tlf">Telefon</label>
        <input id="f-tlf" name="telefon" type="tel" autocomplete="tel"></div>
      <div class="ibk2-felt"><label for="f-emne">Henvendelsen gjelder</label>
        <select id="f-emne" name="emne">{"".join(f"<option>{e}</option>" for e in EMNER)}</select></div>
    </div>
    <div class="ibk2-felt"><label for="f-melding">Melding <small>*</small></label>
      <textarea id="f-melding" name="melding" required
        placeholder="Fortell oss kort om prosjektet ditt …"></textarea>
      <p class="ibk2-feil">Skriv en kort melding (minst 10 tegn).</p></div>
    <div class="ibk2-hp" aria-hidden="true">
      <label for="f-firma">Firma</label>
      <input id="f-firma" name="firma" type="text" tabindex="-1" autocomplete="off"></div>
    <button class="ibk2-send" type="submit">Send melding <span aria-hidden="true">→</span></button>
    <p class="ibk2-status" id="ibk2-status" role="status"></p>
   </form>
   <div class="ibk2-info">
    <a class="ibk2-kort" href="tel:+4791926666">
      <span class="ibk2-ikon">{IKON["tlf"]}</span>
      <span><b>Ring oss</b><span>+47 91 92 66 66</span></span></a>
    <a class="ibk2-kort" href="mailto:post@idebolig.no">
      <span class="ibk2-ikon">{IKON["post"]}</span>
      <span><b>Send e-post</b><span>post@idebolig.no</span></span></a>
    <div class="ibk2-kort">
      <span class="ibk2-ikon">{IKON["sted"]}</span>
      <span><b>Besøk oss</b><span>Jølstadbakken 14<br>2318 Hamar</span></span></div>
    <div class="ibk2-svar"><b>Rask tilbakemelding</b>
      <span>Vi svarer normalt innen én virkedag. Gjelder det noe som haster,
      er det raskest å ringe.</span></div>
   </div>
  </div>
 </div>
</section>
<script>
(function(){{
 // IB1.11: sett ENDPOINT + ACCESS_KEY (Web3Forms e.l.) + Turnstile ved aktivering.
 var ENDPOINT='';
 var form=document.getElementById('ibk2-form'),status=document.getElementById('ibk2-status');
 function valider(){{
  var ok=true;
  [['f-navn',function(v){{return v.trim().length>1;}}],
   ['f-epost',function(v){{return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]{{2,}}$/.test(v);}}],
   ['f-melding',function(v){{return v.trim().length>=10;}}]].forEach(function(par){{
    var el=document.getElementById(par[0]),feil=el.parentElement.querySelector('.ibk2-feil'),
        god=par[1](el.value);
    el.classList.toggle('ugyldig',!god);
    if(feil)feil.style.display=god?'none':'block';
    if(!god)ok=false;}});
  return ok;}}
 form.addEventListener('submit',function(e){{
  e.preventDefault();
  status.className='ibk2-status';
  if(document.getElementById('f-firma').value)return; // honeypot: stille avvisning
  if(!valider())return;
  if(!ENDPOINT){{
   status.className='ibk2-status info';
   status.innerHTML='Takk, '+document.getElementById('f-navn').value.split(' ')[0]
    +'! Skjemaet aktiveres når nettsiden lanseres. Frem til da når du oss på '
    +'<a href="mailto:post@idebolig.no">post@idebolig.no</a> eller telefon '
    +'<a href="tel:+4791926666">91 92 66 66</a>.';
   return;}}
  var knapp=form.querySelector('.ibk2-send');knapp.disabled=true;
  fetch(ENDPOINT,{{method:'POST',headers:{{'Content-Type':'application/json'}},
   body:JSON.stringify({{navn:document.getElementById('f-navn').value,
    epost:document.getElementById('f-epost').value,
    telefon:document.getElementById('f-tlf').value,
    emne:document.getElementById('f-emne').value,
    melding:document.getElementById('f-melding').value}})}})
   .then(function(r){{if(!r.ok)throw 0;
    status.className='ibk2-status ok';
    status.textContent='Takk for henvendelsen! Vi svarer normalt innen én virkedag.';
    form.reset();}})
   .catch(function(){{status.className='ibk2-status info';
    status.innerHTML='Noe gikk galt — prøv igjen, eller send e-post til '
     +'<a href="mailto:post@idebolig.no">post@idebolig.no</a>.';}})
   .finally(function(){{knapp.disabled=false;}});
 }});
 ['f-navn','f-epost','f-melding'].forEach(function(id){{
  document.getElementById(id).addEventListener('input',function(){{
   if(this.classList.contains('ugyldig'))valider();}});}});
}})();
</script>
"""


def main() -> None:
    fil = ROOT / "kontakt" / "index.html"
    html = fil.read_text(encoding="utf-8")
    arkiv = Path(__file__).resolve().parent / "original-main" / "kontakt.html"
    start = re.search(r"<main[^>]*>", html)
    end = html.find("</main>")
    if not arkiv.exists():
        arkiv.write_text(html[start.end():end], encoding="utf-8")
    fil.write_text(html[: start.end()] + MAIN + html[end:], encoding="utf-8")
    print("Skrev ny kontaktside")


if __name__ == "__main__":
    main()
