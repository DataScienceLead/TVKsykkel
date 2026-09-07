---
name: google-maps-race-logistics
description: 'Lag eller oppdater Google Maps-kartreferanser, lenker til kjoreinstruksjoner og beregninger av reisevei, distanse og tid til stadion, arena eller startsted. Use when you need Google Maps links, map references, driving directions, travel time, route distance, coordinates, current-location directions, or race logistics to a venue.'
argument-hint: 'Destinasjon, koordinater eller adresse, og om lenken skal bruke brukerens posisjon eller fast startpunkt'
user-invocable: true
---

# Google Maps Race Logistics

Bruk denne ferdigheten når du trenger en liten, presis arbeidsflyt for kartreferanser og kjorelogistikk til rittarena, stadion, startsted eller overnatting.

Denne ferdigheten dekker tre ting:

1. Lage riktig Google Maps-lenke for navigasjon
2. Knytte en kjent adresse eller koordinat til et kartpunkt på en side
3. Beregne og skrive inn reisetid og distanse for bil til et relevant sted

## Når Ferdigheten Skal Brukes

- Du trenger en Google Maps-lenke til stadion, arena, start eller hotell
- Du vil at lenken skal bruke brukerens naavaerende posisjon
- Du vil beregne reisetid med bil fra et fast punkt, som hotell eller klubbhus
- Du vil legge inn kartreferanser i en rittside, popup, kort eller praktisk info-blokk
- Du har koordinater, men mangler riktig Google Maps-format eller lesbar destinasjon
- Du vil hente faktisk kjoretid og distanse fra Google Maps i stedet for aa gjette

## Kilder Og Referanser

- Bruk [assets/destinations-template.md](./assets/destinations-template.md) som sjekkliste for destinasjoner og lenketyper
- Hvis dette brukes som del av en rittside, kombiner med [ritt-prep-page](./../ritt-prep-page/SKILL.md)
- Hvis rittet finnes i delt rittdata, bruk [data/ritt.js](./../../data/ritt.js) for navn, dato og stedskontekst

## Nødvendige Inndata

Samle inn dette for hvert sted du skal lage logistikk for:

- navn paa destinasjonen, for eksempel stadion, arena eller startsted
- om destinasjonen faktisk er stadion, arena, start eller maal
- enten koordinater i desimalformat eller en bekreftet adresse
- om lenken skal bruke:
  - brukerens naavaerende posisjon
  - et fast startpunkt, som hotell eller klubbhus
- transporttype hvis annet enn bil er oensket
- om du bare skal lage lenke, eller ogsaa skrive inn estimert reisetid og distanse
- om lenken skal brukes i:
   - synlig tekst
   - knapp eller kort
   - kartpopup
   - JavaScript-kartdata
- om koordinatene skal vises til brukeren eller bare brukes teknisk bak lenken eller kartet

Hvis adresse eller koordinater er uklare, ikke gjett. Behold stedet som uavklart eller bruk bare den mest presise informasjonen som er verifisert.

## URL-Moenstre

### Kjoereinstruksjoner fra brukerens posisjon

Bruk dette naar lenken skal aapne Google Maps fra der brukeren er:

```text
https://www.google.com/maps/dir/?api=1&destination=LAT,LNG&travelmode=driving
```

### Kjoereinstruksjoner fra et fast startpunkt

Bruk dette naar du trenger en fast referanserute, for eksempel for aa beregne tid fra hotell til stadion:

```text
https://www.google.com/maps/dir/?api=1&origin=LAT1,LNG1&destination=LAT2,LNG2&travelmode=driving
```

### Soekelenke uten koordinater

Hvis du bare har et stedsnavn eller en adresse:

```text
https://www.google.com/maps/search/?api=1&query=URL_ENCODET_STED
```

## Prosedyre

1. Finn ett konkret destinasjonspunkt.
   Start med stadion, arena eller startstedet som faktisk skal brukes. Hvis en side bare nevner et stort omraade, gaatt ett hakk naermere til stedet deltakerne faktisk maa navigere til.

2. Normaliser destinasjonen.
   Foretrekk desimalkoordinater hvis de finnes. Hvis brukeren oppgir grader, minutter og sekunder, konverter til desimalformat foer du lager lenker eller kartdata.

3. Velg riktig lenketype.
   - Bruk `destination` alene naar brukeren skal navigere fra sin egen posisjon.
   - Bruk `origin + destination` naar du trenger en fast referanserute for planlegging.
   - Bruk `search` bare naar presise koordinater ikke finnes.

4. Lag kartreferansen.
   Hvis stedet skal vises i en HTML-side eller et kartbibliotek, lagre koordinatene i et format som passer flaten, for eksempel `[lat, lng]` i JavaScript.

5. Avklar forskjellen mellom dynamisk navigasjon og faste referansetider.
   Hvis brukeren vil ha lenker fra sin egen posisjon, bruk `destination`-lenker uten fast `origin`. Hvis brukeren samtidig vil ha reisetid eller distanse i teksten, ma disse beregnes fra et fast referansepunkt som hotell eller klubbhus.

6. Hent faktisk kjoretid og distanse naar brukeren ber om beregning.
   Aapne Google Maps med fast `origin` og riktig `destination`, og les ut:
   - raskeste kjoretid
   - distanse
   - gjerne ogsaa hovedrute, for eksempel `via E6`

7. Skriv inn reiseinformasjonen tydelig.
   Hold estimerte tider atskilt fra navigasjonslenker:
   - navigasjonslenker kan bruke brukerens posisjon
   - referansetider kan vaere beregnet fra hotell eller annet fast punkt

8. Merk hva som er dynamisk og hva som er referanse.
   Hvis siden inneholder baade lenker fra brukerens posisjon og referansetider fra et hotell, skal teksten si dette eksplisitt.

9. Tilpass detaljnivaaet i UI-et.
   Hvis brukeren ikke vil se koordinater i selve teksten, behold dem i kode, kartdata eller lenker, men skriv menneskelige stedsnavn i synlig innhold. Unngaa ogsaa unodig metatekst om hvor opplysningene ble hentet fra, med mindre brukeren ber om det.

## Beslutningspunkter

### Brukeren Vil Ha En Klikkbar Lenke

- Lag en `destination`-basert Google Maps-lenke
- Ikke hardkod `origin` hvis brukeren vil navigere fra sin egen posisjon

### Brukeren Vil Ha Et Tidsestimat

- Bruk en fast `origin` som hotell eller klubbhus
- Les ut faktisk kjoretid og distanse fra Google Maps
- Ikke presenter tiden som universell hvis den bare gjelder ett bestemt startpunkt

### Flere Naerliggende Punkter Paa Samme Arena

- Skill mellom arena, start og maal hvis de er praktisk forskjellige
- Hvis flere punkter overlapper i kartet, vurder ett tydelig arena-punkt i tillegg til egne tekstlenker

### Brukeren Vil Ikke Se Koordinater I Teksten

- Behold koordinatene i lenker eller kartdata hvis de trengs teknisk
- Vis stedsnavn i stedet for ra koordinater i kort, tabeller og oppsummeringer
- La popup eller knappetekst vaere kort og lesbar

### Repoet Trenger Innebygget Kart

- Hvis du legger inn kart i dette repoet, bruk eksisterende Leaflet-oppsett og CARTO-baselag som allerede brukes i nettstedet
- Ikke lag en separat kartstil hvis samme flate kan gjenbruke prosjektets etablerte mønster

### Bare Koordinater Er Oppgitt

- Bruk koordinatene direkte i `destination`
- Hvis Google Maps resolver til et overraskende navn, behold gjerne koordinatbasert lenke men bruk et menneskelig label-navn i UI-et

### Kartpopup Eller Tooltip

- Legg lenken direkte i popup-HTML-en
- Hold etiketten kort, for eksempel `Google Maps`
- Pass paa at `target="_blank"` og `rel="noopener"` er med i HTML-lenker

## Kvalitetskriterier

Ferdigheten er ferdig naar:

- hver destinasjon har riktig adresse eller koordinat
- riktig Google Maps-lenketype er valgt for bruksbehovet
- kjoreinstruksjonslenker faktisk peker til riktig sted
- reisetid og distanse bare oppgis naar de er verifisert mot Google Maps
- teksten skiller mellom dynamisk navigasjon og faste referanseestimater
- koordinater vises bare hvis brukeren faktisk vil ha dem i synlig innhold
- kartreferanser og popup-lenker er korte, tydelige og mobilvennlige

## Forventet Leveranse

Resultatet boer vaere ett eller flere av disse:

- en eller flere Google Maps-lenker til navigasjon
- koordinater eller kartreferanser klare til bruk i HTML eller JavaScript
- oppdatert sideinnhold med reisetid og distanse
- en kort oppsummering av hvilke steder som er bekreftet og hvilket startpunkt tidsestimatene er basert paa

## Eksempel Paa Arbeidsoppdrag

- "Lag en Google Maps-lenke til Birkebeineren skistadion fra brukerens posisjon."
- "Beregn kjoretid fra Scandic Lillehammer til start paa Tretten og skriv det inn paa rittsiden."
- "Legg Google Maps-lenker inn i kartpopupene og bruk dagens posisjon som startpunkt."
- "Vi har bare koordinater til stadion. Lag baade kartreferanse og navigasjonslenke."