En app som viser ritt for TVK-ungdom.

## Treningsdagbok

`trening.html` viser en personlig dag- og ukeplan for U15, U17 og U19. Utøveren
velger tilgjengelige dager og maksimal treningstid. Profil og fullført-status
lagres bare i nettleserens `localStorage`; det finnes ingen konto eller
synkronisering mellom enheter.

Planinnholdet vedlikeholdes i Markdown-filene under `planer/`. Etter en endring
genereres nettdata og testes slik:

```bash
python3 planer/build_training_data.py
node --test planer/trening-core.test.js
```

Arkitekturen er delt i tre lag:

- `data/trening.js` er genererte, strukturerte planer for nettleseren.
- `planer/trening-core.js` inneholder dato-, tilpasnings- og lagringsregler uten DOM.
- `planer/trening.js` renderer grensesnittet og håndterer nettleserlagring.

Tilpasningen er konservativ: den øker ikke treningsmengden, flytter ikke ritt
eller fellestreninger og legger ikke harde økter på nabodager. Økter som ikke kan
plasseres innenfor utøverens tilgjengelighet vises som konflikter.

## Rittplaner

Rittspesifikke planer ligger i `rittplan/`, med én HTML-fil per ritt. Praktisk
tekst, tider, steder, etapper og kartpunkter redigeres direkte i den aktuelle
HTML-filen. Felles funksjoner for MET-vær og Google Maps-lenker ligger i
`rittplan/rittplan.js`.

TVK-påmeldte oppdateres fra EQ Timing med én felles kommando:

```bash
python3 planer/update_ritt_tvk_status.py all --dry-run
python3 planer/update_ritt_tvk_status.py all
```

Bytt `all` med `halden` eller `lillehammer` for å oppdatere bare én side.
Nye ritt konfigureres i `RACES` i oppdateringsscriptet og får egne
`tvk-...`-markører i HTML-filen.

En ny rittplan kobles til terminlisten med `prepUrl` i `data/ritt.js`:

```js
prepUrl: "rittplan/mitt-ritt.html"
```

## Nye ritt

Legg til nye ritt i `data/ritt.js` med dette formatet:

```js
{ name: "XC 12-13 Karl XII rittet",         catKey: "ncterr",     start: "19.09.2026", end: "20.09.2026", location: "Halden",                    club: "Halden CK",       lat: 59.1227, lng: 11.3875 },
```