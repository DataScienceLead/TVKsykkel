# Mal For Værdata På Rittside

Bruk denne som sjekkliste når du skal legge inn værdata på en rittside.

## Grunnvalg

- Ritt:
- Side:
- Skal vær vises per helg, per dag eller per etappe:
- API eller Yr-widget:
- Skal værlenker til Yr være med: ja / nei
- Skal værdata knyttes til arena, start, mål eller overnatting:

## Værpunkt 1

- Etikett:
- Dato:
- Klokkeslett:
- Sted:
- Rolle: arena / start / mål / overnatting
- Koordinater eller bekreftet sted:
- Gjelder for klasser / ryttere:
- Kommentar om hvorfor dette punktet er valgt:

## Værpunkt 2

- Etikett:
- Dato:
- Klokkeslett:
- Sted:
- Rolle: arena / start / mål / overnatting
- Koordinater eller bekreftet sted:
- Gjelder for klasser / ryttere:
- Kommentar om hvorfor dette punktet er valgt:

## Presentasjon

- Hvilke felter skal vises:
  - temperatur
  - værbeskrivelse
  - vind
  - nedbør
  - skydekke
  - faktisk prognosetid
- Skal nærmeste prognosepunkt vises eksplisitt: ja / nei
- Skal værkortene være korte eller detaljerte:
- Skal eventuelle usikre klokkeslett merkes som ca.:

## Kilder Og Attribusjon

- Yr-lenke for hovedsted:
- Andre Yr-lenker:
- Krediteringslinje lagt inn: ja / nei
- Lenke til CC BY 4.0 lagt inn: ja / nei
- Ingen uoffisiell Yr-logo brukt: ja / nei

## Før Publisering

- Er hvert værkort knyttet til en konkret dag eller etappe?
- Er hvert værkort knyttet til riktig praktisk sted?
- Er koordinatene normalisert til maks 4 desimaler hvis API brukes?
- Er fallback-tekst på plass hvis API-kallet feiler?
- Er løsningen kontrollert i nettleser etter at scriptet har kjørt?
- Er værseksjonen nyttig for faktiske beslutninger før start?

## Eksempelutfylling: Lillehammer

- Skal vær vises per helg, per dag eller per etappe: per etappe
- API eller Yr-widget: API
- Skal værdata knyttes til arena, start, mål eller overnatting: start og arena

### Eksempel Værpunkt 1

- Etikett: Fredag 11. september
- Dato: 2026-09-11
- Klokkeslett: ca. 18:00
- Sted: Lysgaardsbakkene
- Rolle: arena / start
- Koordinater eller bekreftet sted: 61.1234, 10.4870
- Gjelder for klasser / ryttere: M15-16
- Kommentar om hvorfor dette punktet er valgt: M15-16 starter fra arenaområdet

### Eksempel Værpunkt 2

- Etikett: Fredag 11. september
- Dato: 2026-09-11
- Klokkeslett: ca. 18:00
- Sted: Nedre Skrefsrud
- Rolle: start
- Koordinater eller bekreftet sted: 61.1228, 10.4960
- Gjelder for klasser / ryttere: M11-12
- Kommentar om hvorfor dette punktet er valgt: M11-12 har eget startpunkt og trenger eget værkort