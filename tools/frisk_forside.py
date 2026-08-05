#!/usr/bin/env python3
"""Forsiktig oppfriskning av forsiden: hero-inntreden, kort-stil på
tjenesteboksene, gullaksenter og scroll-avsløring. Kun index.html, idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIL = ROOT / "index.html"

CSS = """<style id="ib-forside-frisk">
/* — hero: myk inntreden + gull-aksent — */
@keyframes ibFadeUp{from{opacity:0;translate:0 26px}to{opacity:1;translate:0 0}}
.elementor-element-3805cf9 .elementor-widget{opacity:0;animation:ibFadeUp .9s ease forwards}
.elementor-element-3805cf9 .elementor-widget:nth-child(1){animation-delay:.15s}
.elementor-element-3805cf9 .elementor-widget:nth-child(2){animation-delay:.3s}
.elementor-element-3805cf9 .elementor-widget:nth-child(3){animation-delay:.5s}
.elementor-element-3805cf9 h1{letter-spacing:.02em;
  text-shadow:0 2px 18px rgba(0,0,0,.35)}
/* — knapper: rundere, løft på hover — */
.elementor-button{border-radius:10px!important;
  transition:transform .22s ease,box-shadow .22s ease,filter .22s ease!important}
.elementor-button:hover{transform:translateY(-3px);filter:brightness(1.06);
  box-shadow:0 10px 24px rgba(201,156,85,.4)}
/* — tjenestebokser som kort — */
.elementor-widget-icon-box>.elementor-widget-container{background:#fff;
  border-radius:16px;padding:30px 22px 26px;height:100%;
  box-shadow:0 2px 14px rgba(51,48,44,.07);
  transition:transform .28s ease,box-shadow .28s ease}
.elementor-widget-icon-box:hover>.elementor-widget-container{transform:translateY(-6px);
  box-shadow:0 14px 32px rgba(51,48,44,.15)}
.elementor-widget-icon-box .elementor-icon{color:#C99C55!important;fill:#C99C55!important;
  transition:transform .28s ease}
.elementor-widget-icon-box .elementor-icon svg{fill:#C99C55!important}
.elementor-widget-icon-box:hover .elementor-icon{transform:scale(1.12)}
.elementor-widget-icon-box .elementor-icon-box-title{letter-spacing:-.01em}
/* — overskrifter med diskret gull-strek under seksjonstitlene — */
.elementor-widget-heading h2.elementor-heading-title{letter-spacing:-.012em}
/* — scroll-avsløring — */
.ib-avslor{opacity:0;translate:0 22px;
  transition:opacity .6s ease,translate .6s ease}
.ib-avslor.ib-vis{opacity:1;translate:0 0}
@media(prefers-reduced-motion:reduce){
 .elementor-element-3805cf9 .elementor-widget{animation:none;opacity:1}
 .ib-avslor{opacity:1;translate:0 0;transition:none}}
</style>
"""

JS = """<script id="ib-forside-frisk-js">
(function(){
 if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
 var mål=[].slice.call(document.querySelectorAll(
  '.elementor-widget-icon-box,.elementor-widget-heading:not(.elementor-element-c7345d2):not(.elementor-element-3805cf9 *)'));
 mål=mål.filter(function(el){return !el.closest('.elementor-element-3805cf9')});
 if(!('IntersectionObserver' in window)){return;}
 var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('ib-vis');io.unobserve(e.target);}});},
  {threshold:.15});
 mål.forEach(function(el,i){el.classList.add('ib-avslor');
  el.style.transitionDelay=(i%5*70)+'ms';io.observe(el);});
})();
</script>
"""


def main() -> None:
    html = FIL.read_text(encoding="utf-8")
    html = re.sub(r'<style id="ib-forside-frisk">.*?</style>\n', "", html, flags=re.S)
    html = re.sub(r'<script id="ib-forside-frisk-js">.*?</script>\n', "", html, flags=re.S)
    html = html.replace("</head>", CSS + "</head>", 1)
    html = html.replace("</body>", JS + "</body>", 1)
    FIL.write_text(html, encoding="utf-8")
    print("Forsiden frisket opp")


if __name__ == "__main__":
    main()
