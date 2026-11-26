---
name: treningsplan-og-pdf
description: Lag, sammenlign, oppdater eller formater TVKs sesongplaner for sykkeltrening, og lag eller kontroller PDF fra en eksisterende Markdown-plan.
argument-hint: Aldersgruppe, sesong, eksisterende plan, ønskede endringer og eventuelt PDF
user-invocable: true
---

# Treningsplan og PDF

Bruk denne ferdigheten for sesong- og ukeplaner i `planer/`, inkludert aldersgruppetilpasning, gjennomgang av øktendringer og konvertering til PDF. Dette er noe annet enn en rittspesifikk forberedelsesside.

## Finn grunnlaget

1. Les den aktuelle Markdown-filen og relevant referanseplan. Kontroller arbeidskopien før redigering, og bevar endringer brukeren allerede har gjort.
2. Avklar aldersgruppe, sesong og hvilke perioder som skal endres. Bruk eksisterende økter som utgangspunkt, ikke som en antakelse om hva alle utøvere skal tåle.
3. Kartlegg faste fellesøkter, tilgjengelige dager, alternative idretter, trenings- og rittuker, samt eventuelle ønsker om hvile og valgfrie økter. Kontroller den aktuelle planen og spør dersom opplysninger som påvirker oppsettet mangler.
4. Bruk riktige årstall og ukedager. Et sesongår i tittelen beviser ikke at datoene inni planen tilhører det året. Kontroller ritt mot gjeldende terminliste før de presenteres som bekreftet; avklar med brukeren om relative uker eller uavklarte ritt skal brukes når terminlisten mangler.

## Foreslå og oppdatere

- Vis en konkret sammenligning av gamle og nye økter, dager, intensitet og varighet når brukeren ønsker å vurdere endringene. Når brukeren bare ber om et forslag eller uttrykkelig ønsker gjennomgang før redigering, ikke endre filer før det er avklart.
- Følg brukerens beslutning om når planen skal oppdateres. Behold uendrede perioder og individuelle tilpasninger.
- Ikke kopier belastning direkte fra en eldre aldersgruppe. Tilpass forslag til alder, erfaring og overskudd, og gjør det tydelig at unge utøvere bør avklare samlet belastning med trener og foresatte.
- Ta hensyn til resten mellom harde økter. Hvis en valgfri intervalløkt ligger tett på en annen, gjør valgfriheten og behovet for tilpasning tydelig.
- Vis avtalte faste økter på riktig dag og i riktig intensitet. Eksempel fra U15-planen for 2027 er felles styrke mandag og felles sone 3 på rulle onsdag fra november til februar; les den aktuelle planen og kontroller at oppsettet fortsatt gjelder før det gjenbrukes.
- Vis konkrete øktendringer mot forrige plan i svaret, også når enkelte økter utgår, er valgfrie eller er nye. Skill nye forslag fra bekreftede ritt og treningsavtaler.

## Kontroller mengde og formatering

- Summer minimum og maksimum for hver uke fra alle dagene, også valgfrie økter med null som mulig varighet. Oppgi hva summen inkluderer. Hvis en varighet er ukjent, angi summen for de kjente øktene separat og forklar at den ukjente kommer i tillegg.
- Kontroller at intervallenes antall, varighet og oppgitte effektive minutter stemmer overens, og at beskrivelsene av antall intervalløkter samsvarer med tabellene.
- Når oppgaven bare er formatering eller PDF, ikke endre treningsinnhold eller tall i det stille. Varsle om uoverensstemmelser og be om avklaring før innhold endres.
- Gjør Markdown lesbar med tydelige overskrifter, konsekvente tabeller og god luft. Kontroller at formatering ikke endrer det rendrerte innholdet.

## Lag PDF

1. Bruk den oppdaterte Markdown-filen som innholdskilde. Ikke anta at `planer/gen_u15_pdf.py`, `planer/gen_u17_pdf.py` eller andre eksisterende generatorer faktisk leser Markdown: undersøk dem først. Hardkodede økter kan gi en utdatert PDF selv om skriptets beskrivelse sier noe annet.
2. Bruk tilgjengelige lokale verktøy til å rendere Markdown, inkludert tabeller, til en lesbar PDF. Ikke send treningsplanen til en ekstern konverteringstjeneste.
3. Bruk tydelige overskrifter, lesbar tekst og kolonnebredder, og hold tabeller og tilhørende ukeoverskrifter samlet på siden der det er mulig. Bruk gjerne eksisterende TVK-farger og sidetall.
4. Åpne eller gjengi representative sider og kontroller sideskift, tabeller, tegn og lesbarhet. Trekk ut PDF-tekst og sammenlign med Markdown-kilden, inkludert siste del og oppdaterte økter. Kontroller også at PDF-en er lagret på forventet sti og at relevante lenker fortsatt peker dit.
5. Hvis kilden inneholder ukjente eller feilaktige verdier, ikke skjul dette i PDF-en eller endre dem uten avklaring. Opplys brukeren om avvikene.

## Leveranse

- Lenke til oppdatert plan og eventuelt PDF.
- Kort oversikt over de faktiske forskjellene mot tidligere plan når økter er endret.
- Resultat av kontrollene og eventuelle uavklarte datoer, varigheter eller summer.
