# Idébolig — nettside (statisk kopi)

Statisk kopi av [idebolig.no](https://idebolig.no) (WordPress + Astra + Elementor),
speilet 5. august 2026. Brukes som forhåndsvisning for kunden og som utgangspunkt
for ny deploy på eget domene.

## Status

- Alle sider er med: forside, om oss, tjenester, prosjekter, kontakt, boligkatalog
  og husmodellene Alva, Edvard, Edvard Prakt, Embla, Nora, Odin, Tiril og Vilde.
- **Foto er byttet ut med grå plassholdere** («BILDE KOMMER» + filnavn + størrelse).
  Ekte bilder legges inn senere — samme filnavn, samme mappe (`wp-content/uploads/`).
- Logoer og partner-logoer er beholdt.
- Google Analytics / Site Kit-sporing er fjernet fra forhåndsvisningen.
- Kontaktskjemaet (WPForms) rendres, men kan ikke sende inn på en statisk side —
  må kobles til en skjematjeneste eller API før produksjonssetting.

## Lokal kjøring

```
python3 -m http.server 8741
```

## Struktur

- `index.html` + undermapper per side — speilet fra WordPress
- `wp-content/` — tema, plugin-assets og bilder (plassholdere)
- `tools/lag_plassholdere.py` — skriptet som genererte plassholderne
- `.github/workflows/deploy.yml` — deploy til GitHub Pages fra `main`

## Backlog og rapporter

Backlog (IB1.1, IB1.2, …) og rapporter vedlikeholdes på claude-delingen:
`Prosjekter/Idebolig/` (RAPPORT-MARIUS.md og RAPPORT-SANGAR.md).
