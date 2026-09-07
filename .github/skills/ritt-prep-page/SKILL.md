---
name: ritt-prep-page
description: 'Lag eller oppdater en forberedende nettside for et ritt, etapperitt eller tempohelg. Use when you need race prep info such as overnatting, startsted, starttid, flere etapper, reisevei fra overnatting til start, avreisetid, oppvarmingstid, EQ Timing startlister, tempo, bakketempo, eller en samlet helgeplan.'
argument-hint: 'Rittnavn og kjente detaljer om overnatting, etapper eller starttider'
user-invocable: true
---

# Ritt Prep Page

Bruk denne ferdigheten når du skal lage eller oppdatere en rittspesifikk nettside med alt utøverne og de foresatte trenger for en helg: overnatting, etapper, startsteder, oppmøtetider, oppvarming og lenker til oppdatert EQ Timing-informasjon.

Målet er en praktisk side som svarer på tre spørsmål:

1. Hvor skal vi bo, og når må vi reise?
2. Hvor og når starter hver etappe eller klasse?
3. Når må rytterne være klare til oppvarming og start?

## Når Ferdigheten Skal Brukes

- Du vil lage en ny forberedende nettside for ett bestemt ritt
- Du vil oppdatere en eksisterende rittside når arrangøren publiserer nye starttider
- Rittet går over flere dager eller flere etapper
- Tempo eller bakketempo får startlister sent, og siden må tydelig vise hva som er bekreftet og hva som fortsatt venter
- Du trenger et oppsett som kombinerer praktisk logistikk og sportslig tidsplan i samme side

## Kilder Og Referanser

- Bruk [data/ritt.js](./../../../data/ritt.js) som første kilde for rittnavn, dato og sted
- Bruk [terminliste.html](./../../../terminliste.html) som referanse for hvordan ritt presenteres i oversikten
- Bruk [ritt-guide.html](./../../../ritt-guide.html) og [planer/ritt-guide.md](./../../../planer/ritt-guide.md) som referanse for tone, TVK-kontekst og oppvarmingsprinsipper
- Hvis EQ Timing-lenke mangler eller er usikker, bruk [eqtiming-regurl-workflow](./../eqtiming-regurl-workflow/SKILL.md)
- Bruk [assets/ritt-prep-template.md](./assets/ritt-prep-template.md) som minimumsstruktur for innholdet

## Nødvendige Inndata

Samle inn eller avklar dette før siden ferdigstilles:

- rittnavn
- datoer for hele rittet
- om dette er en ny side eller en oppdatering av en eksisterende rittside
- ønsket filnavn eller slug hvis siden er ny
- hvor siden skal kunne finnes:
   - kun via terminliste
   - også andre steder hvis brukeren uttrykkelig ber om det
- overnatting: navn, adresse, innsjekk, utsjekt, eller tydelig beskjed om at bosted ikke er avklart ennå
- transportmåte: bil, minibuss eller annet
- om siden skal ha kart:
   - ingen kart
   - ett samlet helgekart
   - ett kart per dag eller etappe
- om rå koordinater skal vises i teksten eller bare brukes internt i kart og lenker
- én eller flere etapper med:
  - dato
  - disiplin, for eksempel fellesstart, tempo, bakketempo eller rundbane
   - hvilke klasser eller ryttere etappen gjelder for
   - arena, startsted og målsted hvis disse er forskjellige
   - adresse eller koordinater for hvert kjent punkt
   - om klassene skal vises i faktisk startrekkefølge den dagen
  - starttid for aktuell klasse eller tydelig markering om at starttid ikke er publisert ennå
  - ønsket oppmøtetid
   - ønsket oppvarmingsvindu, eller beskjed om at Rittguide-standard skal brukes
- om Google Maps-lenker skal være med, og i så fall om de skal bruke:
   - brukerens posisjon
   - et fast startpunkt som hotell eller klubbhus
- om det skal beregnes referansetid med bil fra et fast punkt til stadion, arena eller start
- relevante lenker til EQ Timing, arrangørside eller teknisk guide

Hvis brukeren ikke har all informasjon klar, skal du ikke gjette. Merk heller feltet som avventer bekreftelse.

## Prosedyre

1. Finn målflaten.
   Velg først om du skal oppdatere en eksisterende rittside eller lage en ny. Standard i dette repoet er en egen HTML-side per ritt. Hvis repoet ikke allerede har en egen side for rittet, opprett en ny statisk HTML-side som følger prosjektets eksisterende uttrykk.

2. Bekreft grunninformasjon.
   Sammenlign brukerens opplysninger med eksisterende rittdata og eventuelle EQ Timing-lenker. Pass på at rittnavn, dato og sted er konsistente.

3. Avklar sideatferd tidlig.
   Bekreft før videre arbeid om siden skal være skjult fra hovedmenyen, om den bare skal lenkes fra terminlisten, og om koordinater skal holdes ute av synlig tekst hvis de primært er tekniske.

4. Del opp rittet i etapper eller dager.
   Lag én egen blokk per konkurransedag eller etappe. For hvert punkt skal siden gjøre det tydelig hva som skjer den dagen og hva rytteren må forholde seg til.

5. Sorter klasseinformasjonen i praktisk dagsrekkefølge.
   Innen hver dag skal klasser og ryttere vises i den rekkefølgen de faktisk starter. Knytt oppvarming og eventuelle avreisetider direkte til hver klasse, slik at siden kan leses kronologisk gjennom dagen.

6. Bygg tidslinjen baklengs fra start.
   For hver etappe:
   - registrer offisiell starttid hvis den finnes
   - trekk fra ønsket oppvarmingstid for å finne når oppvarmingen må starte
   - trekk fra reise- eller kjøretid fra overnatting for å finne anbefalt avreise
   - legg inn en liten sikkerhetsmargin hvis brukeren har oppgitt behov for parkering, registrering eller kø

7. Bruk standard oppvarming hvis brukeren ikke har gitt et eget opplegg.
   Følg Rittguide som standard:
   - klasse 11-12 aar: bruk 25 min oppvarming uansett distanse
   - fra 13 aar og oppover: bruk 40 min for tempo, gateritt og andre intensive ritt
   - fra 13 aar og oppover: bruk 10-15 min for fellesstart hvis ikke brukeren ber om noe annet

8. Hent sen startinformasjon fra EQ Timing når relevant.
   Dette er spesielt viktig for tempo og bakketempo. Slike starttider publiseres ofte sent. Hvis detaljene finnes på EQ Timing eller arrangørens side, oppdater siden. Hvis de ikke finnes ennå, skriv eksplisitt at starttidene avventer publisering og lenk til kilden som skal sjekkes.

9. Skill mellom bekreftet og foreløpig informasjon.
   Bruk tydelige etiketter som "Bekreftet", "Foreløpig" eller "Avventer EQ Timing" når ikke alle detaljer er klare.

10. Legg inn kart og kjørelenker bare når de faktisk hjelper.
   Hvis brukeren ønsker kart, bruk ett samlet helgekart når det gir best oversikt, eller flere små kart når punktene ellers blir uleselige. Hvis siden også trenger Google Maps-lenker eller reisetider, bruk [google-maps-race-logistics](./../google-maps-race-logistics/SKILL.md).

11. Skriv siden for praktisk bruk.
   Presentasjonen skal være lett å skanne på mobil før avreise. Prioriter konkrete klokkeslett, adresser, avreisetider og korte forklaringer fremfor lange avsnitt. Ikke legg inn unødig metatekst som forklarer hvor informasjonen er hentet fra, med mindre brukeren eksplisitt ber om det.

12. Koble siden til terminlisten når brukeren ønsker det.
   Ikke legg rittsiden i hovednavigasjonen. Hvis siden skal være tilgjengelig fra terminlisteflaten, foretrekk en løsning der lenken styres fra delt rittdata i [data/ritt.js](./../../../data/ritt.js) og rendres i [terminliste.html](./../../../terminliste.html), i stedet for å hardkode lenken bare ett sted.

13. Kvalitetssikre før levering.
   Kontroller at hver dag eller etappe svarer på:
   - hvor vi bor
   - hvor start er
   - hvor arena eller mål er hvis det er et annet punkt enn start
   - når vi må reise
   - når oppvarming starter
   - når rittet starter
   - hvor oppdatert informasjon finnes hvis noe mangler

## Beslutningspunkter

### Enkeltstart Eller Etapperitt

- Hvis rittet bare har én konkurransedag, hold siden kort og konsentrert rundt én plan
- Hvis rittet har flere etapper, lag en tydelig seksjon per dag eller etappe og en samlet helgeoversikt øverst

### Starttid Finnes Ikke Enda

- Hvis offisiell starttid mangler, ikke estimer et konkret klokkeslett uten grunnlag
- Skriv at tidspunktet ikke er publisert ennå
- Lenke til EQ Timing eller arrangørside skal være med
- Dersom brukeren vet naar startlisten normalt publiseres, skriv dette konkret, for eksempel "Sjekk EQ Timing 10. september eller samme dag"

### Oppvarming Skal Standardiseres

- Hvis brukeren ikke har gitt eget oppvarmingsopplegg, bruk Rittguide som standard
- Klasse 11-12 aar: 25 min oppvarming uansett distanse
- Fra 13 aar og oppover: 40 min for tempo, gateritt og andre intensive ritt
- Fra 13 aar og oppover: 10-15 min for fellesstart

### Reisevei Er Uklar

- Hvis brukeren oppgir kjent kjøretid eller reisetid, bruk den
- Hvis kun adresse er kjent og du ikke kan verifisere rute pålitelig, be om estimert kjøretid i stedet for å finne på et tall
- Hvis reisetiden varierer per etappe, vis den separat per dag

### Overnatting Er Ikke Avklart

- Lag siden likevel hvis resten av rittgrunnlaget finnes
- Marker avreise, kjøretid og praktisk logistikk som avventer
- Oppdater senere når hotell eller annen base er kjent

### Kart, Koordinater Og Lenker

- Spør eksplisitt om koordinater skal vises i den synlige teksten eller bare brukes i kart og lenker
- Hvis arena, start og mål er forskjellige, ikke slå dem sammen til ett punkt uten grunnlag
- Hvis brukeren vil ha kjørelenker eller reisetider, bruk [google-maps-race-logistics](./../google-maps-race-logistics/SKILL.md)

### Flere Ryttere Eller Klasser

- Hvis siden gjelder hele laget, vis tydelig hvilken klasse eller hvilke ryttere hvert klokkeslett gjelder for
- Hvis ulike ryttere har ulike starttider, bruk tabell eller punktliste per rytter eller klasse
- Sorter innen hver dag i den rekkefølgen klassene faktisk starter, slik at oppvarming og start kan leses ovenfra og ned

### Rittside Skal Kun Vises Fra Terminlisten

- Ikke legg inn lenke i hovedmenyen
- Hvis rittsiden skal lenkes opp, gjør det fra terminliste-oversikten eller relevant rittvisning
- Hold koblingen så datadrevet som mulig, helst via et felt på rittobjektet i [data/ritt.js](./../../../data/ritt.js)

## Kvalitetskriterier

Ferdigheten er ferdig når siden:

- har korrekt rittnavn, dato og sted
- viser overnatting og praktisk reiseinformasjon
- dekker alle kjente etapper eller konkurransedager
- skiller tydelig mellom arena, start og mål når dette er egne punkter
- tydelig skiller mellom bekreftet og manglende startinformasjon
- gjør avreisetid og oppvarmingsstart eksplisitt
- bruker Rittguide-standard for oppvarming hvis ikke annet er avtalt
- bruker kart og koordinater på en måte som passer brukerens ønske om detaljnivå
- bare eksponerer rittsiden der brukeren ønsker det, uten å legge den i hovedmenyen
- inneholder lenker til EQ Timing eller arrangørside der brukeren senere må sjekke oppdateringer
- unngaar unodig metatekst om kilder i den synlige siden
- er lett å lese på mobil og følger eksisterende TVK-stil

## Forventet Leveranse

Når du bruker ferdigheten, bør resultatet være:

- en oppdatert eller ny rittspesifikk HTML-side
- eventuell kobling fra terminlisteflaten, men ikke fra hovednavigasjonen
- eventuelt en tilhørende tekst- eller markdown-kilde hvis det passer arbeidsflyten
- en kort oppsummering til brukeren av hva som er bekreftet, hva som avventer, og hvilke kilder som må sjekkes igjen senere

## Eksempel På Arbeidsoppdrag

- "Lag en forberedende side for Tour te Fjells. Vi bor på Scandic Oppdal fra fredag til søndag, og det er både tempo og fellesstart."
- "Oppdater Jentebirken-siden med nye starttider fra EQ Timing og regn ut når vi må reise fra hytta."
- "Lag en mobilvennlig rittside for etapperittet på Lillehammer med en seksjon per dag og tydelig markering av at tempo-starttidene ikke er publisert ennå."