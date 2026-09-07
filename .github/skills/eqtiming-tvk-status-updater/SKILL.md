---
name: eqtiming-tvk-status-updater
description: 'Oppdater TVK-påmeldte på en statisk rittside fra EQ Timing via et lokalt script. Use when a prep page needs current TVK entrants, live participant status from EQ Timing, a local HTML rewrite step, or when browser fetch is blocked by CORS.'
argument-hint: 'HTML-side, EQ Timing event-IDer, hvilke TVK-seksjoner som skal oppdateres, og om det trengs dry-run eller faktisk oppdatering'
user-invocable: true
---

# EQ Timing TVK Status Updater

Bruk denne ferdigheten når en statisk rittside skal vise oppdatert TVK-status fra EQ Timing, men dataene ikke kan hentes direkte i nettleseren.

Dette er riktig løsning når:

1. Brukeren vil ha oppdatert TVK-deltakerstatus på en HTML-side
2. EQ Timing-data er offentlige, men klient-`fetch()` stoppes av CORS
3. En enkel lokal oppdatering med ett kommando-kall er bedre enn manuell redigering

## Når Ferdigheten Skal Brukes

- Du har en statisk rittside som skal vise TVK-påmeldte
- Brukeren ber om automatisk eller halvautomatisk oppdatering fra EQ Timing
- Nettleserforsøk mot `https://live.eqtiming.com/...` feiler med CORS
- Siden skal oppdateres lokalt før publisering, ikke rendres dynamisk fra backend
- Du trenger en `--dry-run` for å se deltakerstatus før du skriver til HTML

## Kilder Og Referanser

- Bruk EQ Timing API når det finnes, ikke HTML-skraping, som førstevalg
- Typisk endepunkt for startliste: `https://live.eqtiming.com/api/Startlist/{eventId}/0?startAt=1&query=&filter=&sortcols=&count=500`
- Bruk den aktuelle rittsiden som målflate, for eksempel `rittplan/halden-karl-xii.html`
- Hvis siden inngår i en rittplan, kombiner med [ritt-prep-page](./../ritt-prep-page/SKILL.md)

## Viktige Begrensninger

- Direkte `fetch()` fra en statisk HTML-side til EQ Timing vil normalt feile på grunn av manglende `Access-Control-Allow-Origin`
- Ikke bygg en skjør klientløsning først og oppdag CORS sent i oppdraget. Test dette tidlig.
- Hvis EQ Timing har et API-endepunkt i nettverkstrafikken, bruk det. Ikke parse hele HTML-dokumentet hvis JSON finnes.

## Prosedyre

1. Bekreft at TVK-status faktisk skal være oppdatert fra EQ Timing.
   Ikke bygg lokal oppdaterer hvis brukeren bare vil ha statiske lenker eller manuell status.

2. Test CORS tidlig.
   Prøv én browser-`fetch()` eller inspiser responsheaderne. Hvis forespørselen blokkeres, gå direkte til lokal oppdaterer.

3. Finn riktig EQ Timing-endepunkt.
   Se etter nettverkskall som `api/Startlist/{eventId}` eller `api/Contestants/{eventId}`. Foretrekk endepunktet som faktisk inneholder navn, klubb, klasse og starttid.

4. Velg en liten, lokal oppdaterer.
   I dette repoet er et lite Python-script passende. Scriptet bør:
   - hente JSON fra ett eller flere event-ID-er
   - filtrere på TVK-klubbnavn
   - gruppere ryttere per dag, klasse eller tabellrad etter behov
   - skrive resultatet tilbake til tydelig markerte seksjoner i HTML

5. Bruk markører i HTML-en.
   Sett eksplisitte start/slutt-markører rundt delene som scriptet skal eie, slik at senere designendringer ikke krever full parser av hele siden.

6. Bygg inn `--dry-run`.
   Det skal være mulig å hente og oppsummere TVK-status uten å skrive filen.

7. Skriv siste oppdateringstid inn i siden.
   Brukeren må kunne se når TVK-statusen sist ble hentet fra EQ Timing.

8. Valider ved å kjøre scriptet med ekte data.
   Kjør først `--dry-run`, deretter vanlig oppdatering, og les tilbake de oppdaterte HTML-seksjonene eller rendret side.

## Repo-spesifikk Referanse

- `planer/update_ritt_tvk_status.py` er den generelle implementasjonen i dette repoet
- Den oppdaterer både `rittplan/halden-karl-xii.html` og `rittplan/lillehammer-sykkelfestival.html`
- Nye ritt legges til i `RACES` og bruker eksplisitte `tvk-...`-markører i HTML-filen
- Kjør med:

```bash
/usr/bin/python3 planer/update_ritt_tvk_status.py all --dry-run
/usr/bin/python3 planer/update_ritt_tvk_status.py all
/usr/bin/python3 planer/update_ritt_tvk_status.py lillehammer --dry-run
```

## Kvalitetskriterier

Ferdigheten er ferdig når:

- deltakerdata hentes fra et stabilt EQ Timing-API-endepunkt
- CORS-begrensningen er avklart tidlig og ikke ignorert
- HTML-en oppdateres via tydelige markører i stedet for skjørt søk/erstatt på tilfeldig tekst
- scriptet støtter både dry-run og faktisk oppdatering
- siden viser siste oppdateringstid
- den oppdaterte siden er verifisert enten i browser eller ved målrettet lesing av HTML

## Forventet Leveranse

Resultatet bør være ett eller flere av disse:

- et lokalt script som oppdaterer TVK-status på en rittside
- markerte HTML-seksjoner som scriptet kan eie trygt
- dokumentert kommando for oppdatering og dry-run
- en kort oppsummering av hvilke event-ID-er og sideflater som er koblet sammen