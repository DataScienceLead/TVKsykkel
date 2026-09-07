---
name: race-weather-data
description: 'Lag eller oppdater værdata for rittsider med MET Norway / Yr-data. Use when you need weather forecasts for race stages, arena, startsted, målområde, Yr-lenker, attribution, or stage-specific weather cards on a static HTML page.'
argument-hint: 'Rittnavn, datoer, etapper eller startpunkter, og om vær skal vises per dag, per etappe eller per sted'
user-invocable: true
---

# Race Weather Data

Bruk denne ferdigheten når du skal legge til eller oppdatere værinformasjon på en rittside i dette repoet.

Målet er å vise vær der det faktisk hjelper deltakerne:

1. For riktig dag og omtrent riktig klokkeslett
2. For riktig arena, startsted eller målområde
3. Med korrekt attribusjon til MET Norway / Yr

## Når Ferdigheten Skal Brukes

- Du vil legge til værinfo på en eksisterende rittside
- Du vil vise vær for én eller flere etapper i stedet for bare ett generelt stedsvarsel
- Du trenger værkort for start, arena eller mål på bestemte dager
- Du vil bruke MET Norway API direkte i en statisk HTML-side
- Du må avklare om Yr-widget eller API er riktig løsning
- Du vil legge til lenker til Yr for full detaljvisning
- Du vil sikre at attribusjon og lisenskrav blir fulgt

## Kilder Og Referanser

- Bruk [assets/weather-template.md](./assets/weather-template.md) som sjekkliste for input og presentasjon
- Hvis vær legges inn i en rittside, kombiner med [ritt-prep-page](./../ritt-prep-page/SKILL.md)
- Hvis siden også trenger stedspunkter eller kjørelenker, kombiner med [google-maps-race-logistics](./../google-maps-race-logistics/SKILL.md)
- Bruk [data/ritt.js](./../../data/ritt.js) som første kilde for rittnavn, dato og stedskontekst
- Følg MET/Yr sine vilkår for attribusjon og rimelig bruk

## Nødvendige Inndata

Samle inn eller avklar dette før implementasjon:

- rittnavn
- hvilken HTML-side værdata skal inn på
- om vær skal vises:
  - for hele helgen samlet
  - per dag
  - per etappe
  - per klasse eller startsted hvis disse skiller seg praktisk
- dato for hver etappe eller dag
- ønsket klokkeslett for prognosen:
  - starttid
  - oppmøtetid
  - oppvarmingsstart
  - et annet eksplisitt tidspunkt
- hvilket sted vær skal knyttes til for hvert kort:
  - arena
  - startsted
  - mål
  - overnattingssted hvis brukeren uttrykkelig ønsker det
- koordinater i desimalformat eller et bekreftet stedsnavn som kan kobles til koordinater
- om værinformasjonen skal være kortfattet eller mer detaljert
- om siden også skal ha lenker til Yr for manuell kontroll
- om værseksjonen skal bruke:
  - API-drevne kort
  - offisiell Yr-widget
- om løsningen skal være et rent klientkall i nettleseren eller senere kunne flyttes bak en proxy hvis trafikken blir høyere

Hvis tidspunkt eller sted er uklart, ikke gjett. Merk heller at værkortet er knyttet til nærmeste kjente arena eller at klokkeslettet er omtrentlig.

## Når API Bør Foretrekkes

Bruk MET Norway `locationforecast/2.0/compact` når:

- vær skal knyttes til konkrete etapper eller flere ulike steder
- start og arena er forskjellige og begge er relevante
- siden trenger egne kort med temperatur, vind, nedbør og skydekke
- du vil styre utvalg av prognosepunkt nær et bestemt klokkeslett

API-format:

```text
https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=LAT&lon=LON
```

Bruk maksimalt 4 desimaler i koordinatene.

## Når Widget Kan Være Nok

Bruk en offisiell Yr-widget bare når brukeren ønsker et enkelt, generelt varsel for ett sted, og det ikke er viktig å knytte vær til spesifikke etapper eller klokkeslett.

Ikke bruk en uoffisiell eller egenlaget Yr-logo.

## Konkret Eksempel: Lillehammer

På Lillehammer-siden var widget ikke tilstrekkelig, fordi været måtte knyttes til flere praktiske punkter og tider:

- fredag bakketempo for M15-16 ved Lysgaardsbakkene rundt kl. 18:00
- fredag bakketempo for M11-12 ved Nedre Skrefsrud rundt kl. 18:00
- lørdag gateritt ved Birkebeineren skistadion rundt kl. 09:00
- lørdag tempo ved Birkebeineren skistadion rundt kl. 15:00
- søndag fellesstart for M15-16 i Øyer rundt kl. 08:00
- søndag fellesstart for M11-12 på Tretten kl. 08:32

Dette er et mønster for lignende ritthelger:

- bruk ett værkort per praktiske beslutningspunkt, ikke bare ett kort per helg
- hvis arena og start er ulike og betyr noe for oppmøte eller oppvarming, behold dem separate
- vis hvilket prognosepunkt som faktisk ble brukt hvis API-tiden ikke treffer eksakt starttid
- behold Yr som manuell kontrollflate via lenker, men bruk MET API til selve etappekortene

## Prosedyre

1. Finn kontrollpunktet for været.
   Gå til stedet deltakerne faktisk trenger vær for: start, arena eller mål. Hvis én side har flere praktiske punkter, behold dem som egne værpunkter.

2. Knyt hvert værkort til en konkret etappe.
   Lag en liten struktur per dag eller etappe med:
   - etikett
   - sted
   - klokkeslett
   - koordinater
   - eventuell note om hvorfor akkurat dette punktet er valgt

3. Velg løsningstype.
   - Bruk API hvis været skal være etappevis eller stedsspesifikt
   - Bruk widget bare hvis ett generelt sted er tilstrekkelig

4. Normaliser koordinater.
   Konverter eventuelle grader-minutter-sekunder til desimalformat, og trunker til maks 4 desimaler før API-kall.

5. Hent prognosen.
   Les `timeseries` fra MET-endepunktet og finn nærmeste prognosepunkt til ønsket klokkeslett. Hvis nærmeste punkt er for langt unna, skriv dette tydelig i stedet for å late som om tiden er eksakt.

5a. Sjekk værvinduet før du lover detaljer.
   MET-prognosen dekker bare et begrenset antall dager fram i tid. Hvis rittdatoen ligger utenfor siste `timeseries`-punkt, skal siden vise en tydelig fallback som sier at kortene fylles når datoen kommer innenfor varselvinduet, og peke til Yr-lenker i mellomtiden.

6. Presenter bare det som er nyttig.
   Foretrekk kompakte kort med:
   - temperatur
   - kort værbeskrivelse
   - vind
   - nedbør
   - skydekke
   - tidspunktet prognosen faktisk gjelder for

7. Skill mellom sted og prognosetid.
   Skriv tydelig hvilket sted kortet gjelder for, og hvilket prognosepunkt som ble valgt. Det er spesielt viktig hvis nærmeste API-tid er én eller to timer unna start.

8. Legg inn fallback-lenker.
   Legg ved én eller flere Yr-lenker for full manuell visning når brukeren vil kontrollere siste oppdatering selv.

9. Legg inn korrekt attribusjon.
   Vis en kort krediteringslinje på siden, for eksempel:
   - Data fra MET Norway
   - lenke til Yr eller MET Norway
   - lenke til CC BY 4.0-lisensen

10. Unngå unødvendig pynt.
   Ikke legg inn uoffisielle Yr-logoer eller dekor som kan forveksles med offisiell merkevarebruk. Bruk ren tekstattribusjon med lenker.

11. Ta hensyn til trafikk og caching.
   For små statiske sider kan enkel klientsidehenting være akseptabelt. Hvis løsningen senere brukes bredt eller ofte, bør data caches eller flyttes bak en proxy.

12. Valider i nettleser.
   Kontroller at seksjonen faktisk rendres, at feiltilfeller håndteres ryddig, og at bruker ser både status og eventuelle værkort.

## Beslutningspunkter

### Ett Sted Eller Flere

- Hvis hele helgen foregår på samme arena, kan ett sted være nok
- Hvis start, arena eller mål er ulike og praktisk viktige, lag egne værkort

### Eksakt Starttid Finnes Ikke

- Bruk et kjent omtrentlig klokkeslett, som "ca. kl. 15:00"
- Skriv gjerne hvilket prognosepunkt som faktisk ble brukt
- Ikke presenter været som mer presist enn datagrunnlaget tillater

### Brukeren Ber Om Yr

- Yr kan brukes som synlig referanse og lenkemål
- Hvis bruker egentlig trenger etappevis vær, foretrekk fortsatt MET API framfor widget
- Widget er bare riktig når ett enkelt stedssammendrag er nok

### Klientside Eller Backend

- For denne typen statiske HTML-sider er klientsidehenting normalt enklest
- Ved høyere trafikk, behov for caching eller strengere kontroll, planlegg for proxy/backend senere

### Flere Nærliggende Punkter

- Hvis to punkter ligger svært nær hverandre, kan ett værpunkt dekke begge
- Hvis de representerer ulike praktiske beslutninger, behold dem separate likevel

### Ingen Sikker Lokasjon Enda

- Ikke finn på koordinater
- Bruk heller en Yr-lenke til området og merk stedet som foreløpig
- Oppdater til API-kort når nøyaktig sted er bekreftet

## Kvalitetskriterier

Ferdigheten er ferdig når:

- værseksjonen er knyttet til riktige dager eller etapper
- hvert værkort er knyttet til et riktig sted
- koordinatene er normalisert og ikke mer presise enn nødvendig
- siden viser værdata som faktisk hjelper brukeren å planlegge
- det er tydelig hvilket klokkeslett prognosen er hentet nærmest
- feiltilfeller gir forståelig fallback-tekst
- eventuelle Yr-lenker peker til relevante steder
- attribusjon til MET Norway og lisenslenke er med
- siden ikke bruker uoffisiell Yr-logo eller misvisende merkevare
- løsningen er validert i nettleseren, ikke bare i kildekoden

## Forventet Leveranse

Resultatet bør være ett eller flere av disse:

- en oppdatert værseksjon på en rittside
- API-drevne værkort per dag, etappe eller startsted
- relevante Yr-lenker for manuell kontroll
- en kort oppsummering av hvilke steder og klokkeslett værdataene gjelder for

## Eksempel På Arbeidsoppdrag

- "Legg til værdata på rittsiden for Tour te Fjells og vis ett kort per etappe."
- "Bruk Yr-data for startområdet på lørdag og målområdet på søndag."
- "Bytt ut en generell widget med API-drevne værkort for hver etappe."
- "Legg inn værseksjon på Lillehammer-siden og knytt den til startstedene for M11-12 og M15-16."
- "Lag værkort for Lillehammer der fredag deles i ett kort for Lysgaardsbakkene og ett for Nedre Skrefsrud, mens søndag deles mellom Øyer og Tretten." 