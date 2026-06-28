#!/usr/bin/env python3
"""Genererer treningsplan-u17.pdf fra treningsplan-u17.md (via reportlab)."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle, ListFlowable, ListItem,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

TVK_BLUE = colors.HexColor("#194794")
TVK_RED  = colors.HexColor("#E2071D")
ROW_ALT  = colors.HexColor("#E8ECF5")

base = getSampleStyleSheet()

title_style = ParagraphStyle("title", parent=base["Title"],
    textColor=TVK_BLUE, fontSize=18, spaceAfter=4, alignment=TA_CENTER)
subtitle_style = ParagraphStyle("subtitle", parent=base["Normal"],
    textColor=TVK_RED, fontSize=11, spaceAfter=10, alignment=TA_CENTER)
h2_style = ParagraphStyle("h2", parent=base["Heading2"],
    textColor=TVK_BLUE, fontSize=13, spaceBefore=14, spaceAfter=4)
h3_style = ParagraphStyle("h3", parent=base["Heading3"],
    textColor=TVK_RED, fontSize=11, spaceBefore=10, spaceAfter=3)
body_style = ParagraphStyle("body", parent=base["Normal"],
    fontSize=9, leading=13, spaceAfter=4)
total_style = ParagraphStyle("total", parent=body_style,
    fontName="Helvetica-Bold", textColor=TVK_BLUE, spaceAfter=6)
note_style = ParagraphStyle("note", parent=body_style,
    fontName="Helvetica-Oblique", textColor=colors.HexColor("#555555"), spaceAfter=8)


def week_table(rows):
    header = [Paragraph("<b>Dag</b>", body_style),
              Paragraph("<b>Økt</b>", body_style),
              Paragraph("<b>Tid</b>", body_style)]
    data = [header] + [
        [Paragraph(d, body_style), Paragraph(o, body_style), Paragraph(t, body_style)]
        for d, o, t in rows
    ]
    tbl = Table(data, colWidths=[3*cm, 10.5*cm, 3*cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  TVK_BLUE),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 5),
        ("TOPPADDING",     (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 3),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl


def simple_week_table(rows):
    """Ukeplan uten kolonneheader – brukt for måneder med bare tekst i originalen."""
    data = [
        [Paragraph(f"<b>{d}</b>", body_style), Paragraph(o, body_style), Paragraph(t, body_style)]
        for d, o, t in rows
    ]
    tbl = Table(data, colWidths=[3*cm, 10.5*cm, 3*cm])
    tbl.setStyle(TableStyle([
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, ROW_ALT]),
        ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 5),
        ("TOPPADDING",     (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 3),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl


def zone_table():
    header = [Paragraph("<b>Sone</b>", body_style),
              Paragraph("<b>Navn</b>", body_style),
              Paragraph("<b>Beskrivelse</b>", body_style)]
    rows = [
        ("1–2", "Rolig",          "Lett pust, kan holde en samtale. Brukes på rolige turer og restitusjon."),
        ("3",   "Terskel lav",    "Kontrollert anstrenging, noe tyngre pust. Lange intervaller."),
        ("4",   "Terskel",        "Tydelig anstrenging, vanskelig å snakke. Klassiske 4-minutters intervaller."),
        ("5",   "Supra-terskel",  "Hardt, holder 3–7 min. Øker VO₂max."),
        ("6",   "Maks",           "Fullgass, 1–2 min. Brukes sparsomt."),
    ]
    data = [header] + [
        [Paragraph(s, body_style), Paragraph(n, body_style), Paragraph(b, body_style)]
        for s, n, b in rows
    ]
    tbl = Table(data, colWidths=[1.5*cm, 3.5*cm, 11.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  TVK_BLUE),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT]),
        ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 5),
        ("TOPPADDING",     (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 3),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
    ]))
    return tbl


def hr():
    return HRFlowable(width="100%", thickness=1, color=TVK_BLUE, spaceAfter=6, spaceBefore=4)


def p(text, style=None):
    return Paragraph(text, style or body_style)


# ── Story ────────────────────────────────────────────────────────────────────
story = []

story.append(Spacer(1, 0.3*cm))
story.append(p("Treningsplan for TVK U17 – sesongen 2026", title_style))
story.append(p("Trondhjems Velocipedklubb (15–16 år)", subtitle_style))
story.append(hr())

story.append(p(
    "Dette er en skisse som dere kan bruke når dere skal legge opp treningen. "
    "Legg opp 4-ukers sykluser – 3 harde uker, der både mengde og intensitet øker "
    "gradvis, og syklusen avsluttes med en rolig uke (med 8–12 timer og kun 1 intervalløkt)."
))
story.append(p(
    "Har dere spørsmål til øktene send meg en e-post (joakim.prestmo@gmail.com). "
    "Når dere lager treningsplan ønsker jeg at den er så konkret og presis som mulig. "
    "Det er også viktig at dere tilpasser treningen til hvor mye dere har trent tidligere "
    "og hvor mye trening dere har tid og krefter til – dere skal jo også følge skolen."
))

# ══════════════════════════════════════════════════════════
# 1. OPPTRENINGSPERIODE
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Opptreningsperiode", h2_style))
story.append(p(
    "Fokus i denne perioden er å bygge en solid base. Dette gjør vi gjennom lange "
    "intervaller på og under terskelen, i tillegg til langkjøring. Alle treningsmetoder "
    "er løping, ski, fotturer i fjellet eller marka, intensiv ballspill eller svømming."
))

story.append(p("November", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Fri eller restitusjonsøkt",             "0–1 t"),
    ("Tirsdag", "Intervaller – sone 4 (6–10 min × 3–5)", "1 t"),
    ("Onsdag",  "Styrke og rolig langkjøring",            "1,5–2 t"),
    ("Torsdag", "Intervaller – sone 3 (10–15 min × 3–4)","1,5 t"),
    ("Fredag",  "Rolig langkjøring",                      "1–1,5 t"),
    ("Lørdag",  "Styrke og langkjøring",                  "1,5–2,5 t"),
    ("Søndag",  "Langkjøring",                            "2–3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 9–12 timer", total_style))

# ══════════════════════════════════════════════════════════
# 2. OPPKJØRINGSPERIODE
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Oppkjøringsperiode", h2_style))
story.append(p(
    "Fokus i denne perioden blir å øke O₂-opptaket og watt på terskel. Derfor reduseres "
    "volumet, og intensiteten økes. Nå bør en større del av øktene foregå på sykkel. "
    "I februar kan fremdeles mange av øktene gjennomføres på ski, men to av intervallene "
    "og en langtur skal være på sykkel (hvis været tillater det). I mars bør skiene legges "
    "bort. Vi trapper ned styrketreningen til beinstyrke én gang i uka, i tillegg kommer "
    "en basisøkt som dere kan ta hjemme i stua."
))

story.append(p("Februar", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Restitusjonsøkt",                                          "0–1,5 t"),
    ("Tirsdag", "Intervaller – sone 4 (6–10 min × 4–8)",                   "1 t"),
    ("Onsdag",  "Styrke (basis) og rolig langkjøring",                      "2–3 t"),
    ("Torsdag", "Intervaller – sone 5 (5–7 min × 4–8)",                    "1 t"),
    ("Fredag",  "Rolig langkjøring (styrketråkkspurter)",                   "0–2 t"),
    ("Lørdag",  "Styrke og intervaller sone 4 høy (15/15: 5–8 min × 5–7)", "1–2 t"),
    ("Søndag",  "Langkjøring",                                              "3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 10–13 timer", total_style))

story.append(p("Mars", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Restitusjonsøkt",                                        "0–1,5 t"),
    ("Tirsdag", "Intervaller – sone 4 (5–7 min × 4–6)",                  "1 t"),
    ("Onsdag",  "Styrke (basis) og rolig langkjøring",                    "2–3 t"),
    ("Torsdag", "Intervaller – sone 5 (3–5 min × 4–8)",                  "1 t"),
    ("Fredag",  "Rolig langkjøring (spurttrening)",                       "0–2 t"),
    ("Lørdag",  "Styrke og intervaller sone 5 (30/30: 4 min × 5–8)",     "1–2 t"),
    ("Søndag",  "Langkjøring",                                            "2–3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 10–14 timer", total_style))

# ══════════════════════════════════════════════════════════
# 3. RITTFORBEREDELSE
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Rittforberedelse", h2_style))
story.append(p(
    "I perioden før sesongen begynner skikkelig er fokus todelt. Det første er å øke "
    "syretoleransen, og i tillegg har det nå endelig blitt mulig å ta frem raceren. "
    "Derfor reduseres antall intervalløkter, men intensiteten øker. Viktig å opprettholde "
    "en styrkeøkt i uka."
))

story.append(p("April", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Restitusjonsøkt",                                      "0–1,5 t"),
    ("Tirsdag", "Intervaller – sone 4 (6–8 min × 4–6)",                "1 t"),
    ("Onsdag",  "Styrke (basis) og rolig langkjøring",                  "2 t"),
    ("Torsdag", "Langkjøring (styrketråkkspurter)",                     "1–2 t"),
    ("Fredag",  "Intervaller – sone 5 (30/30: 4–6 min × 4–6)",         "1 t"),
    ("Lørdag",  "Styrke og langkjøring (kort styrkeøkt + langtur)",     "2–3 t"),
    ("Søndag",  "Langkjøring (spurttrening)",                           "3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 10–13 timer", total_style))

# ══════════════════════════════════════════════════════════
# 4. VÅRSESONG
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Vårsesong", h2_style))
story.append(p(
    "I vårsesongen som strekker seg fra slutten av april til slutten av juni er det viktig "
    "å ikke slippe opp for mye. Det er nødvendig å trene tilstrekkelig mellom rittene. "
    "Det er enklest hvis en prioriterer ritt og bruker noen mindre viktige ritt som trening "
    "(altså at dere ikke legger inn hvile i forkant av rittene). Uker uten ritt trener man "
    "mer og hardere enn uker med ritt (rittukene)."
))

story.append(p("Mai – Juni – rittuke", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                "0–1 t"),
    ("Tirsdag", "Rolig langkjøring",                                        "1–1,5 t"),
    ("Onsdag",  "Sone 4-intervaller (4 × 4–5 min)",                        "1,5–2 t"),
    ("Torsdag", "Rolig langkjøring",                                        "1–1,5 t"),
    ("Fredag",  "Aktiveringsøkt: 3–5 korte spurter, ellers hvile",          "0,5–1 t"),
    ("Lørdag",  "Ritt",                                                     "1,5–3 t"),
    ("Søndag",  "Ritt, eller rolig langkjøring hvis kun ett ritt",          "1,5–3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 8–13 timer", total_style))

story.append(p("Mai – Juni – treningsuke", h3_style))
story.append(simple_week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                        "0–1 t"),
    ("Tirsdag", "Lavterskelintervaller sone 3+: 3 × 12–15 min",                    "1,5–2 t"),
    ("Onsdag",  "Rolig langkjøring sone 1–2",                                       "1,5–3 t"),
    ("Torsdag", "Sone 4-intervaller: 4 × 4–5 min",                                 "1,5–2 t"),
    ("Fredag",  "Rolig tur eller hvile",                                            "0,5–1 t"),
    ("Lørdag",  "Langkjøring, gjerne med noen spurter avslutningsvis",              "1,5–3 t"),
    ("Søndag",  "Langkjøring med sone 4-intervaller: 3 × 6–8 min",                 "1,5–3 t"),
]))
story.append(p("<b>Totalbelastning:</b> 10–15 timer", total_style))

# ══════════════════════════════════════════════════════════
# 5. SOMMER – VOLUMBLOKK
# ══════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(p("Sommer – volumblokk", h2_style))
story.append(p(
    "I denne perioden er det to tre-ukers blokker med fokus på å øke aerob kapasitet og "
    "terskelstyrke. Tre intervalløkter per uke i harde uker (2 × sone 3, 1 × sone 4), "
    "to i rolige uker. Øktene bør gjennomføres på sykkel, men 1–2 økter i uka kan med "
    "fordel være alternativ trening slik som løping eller rulleski."
))
story.append(p("<b>Periode:</b> 29. juni – 8. august"))
story.append(p("<b>Struktur:</b> 2 harde uker + 1 rolig uke × 2 blokker"))

# Blokk 1
story.append(p("Blokk 1", h3_style))

story.append(p("<b>Uke 1 – hard (29. juni – 5. juli)</b>"))
story.append(week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                        "0–1,5 t"),
    ("Tirsdag", "Sone 3-intervaller: 5 × 8 min (pause 2 min) – 40 min",            "1,5–2 t"),
    ("Onsdag",  "Rolig langkjøring sone 1–2",                                       "2,5–3,5 t"),
    ("Torsdag", "Sone 4-intervaller: 4 × 4 min (pause 3 min) – 16 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "2,5–3,5 t"),
    ("Søndag",  "Sone 3-intervaller: 4 × 9 min (pause 2–3 min) – 36 min",          "2–2,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 11–16,5 timer", total_style))

story.append(p("<b>Uke 2 – hard (6. juli – 12. juli)</b>"))
story.append(week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                        "0–1,5 t"),
    ("Tirsdag", "Sone 3-intervaller: 5 × 9 min (pause 2 min) – 45 min",            "1,5–2 t"),
    ("Onsdag",  "Rolig langkjøring sone 1–2",                                       "3–4 t"),
    ("Torsdag", "Sone 4-intervaller: 5 × 5 min (pause 3 min) – 25 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "3–4 t"),
    ("Søndag",  "Sone 3-intervaller: 4 × 10 min (pause 3 min) – 40 min",           "2–2,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 12–17,5 timer", total_style))

story.append(p("<b>Uke 3 – rolig (13. juli – 19. juli)</b>"))
story.append(week_table([
    ("Mandag",  "Fri",                                                               "0 t"),
    ("Tirsdag", "Sone 3-intervaller: 4 × 7 min (pause 2 min) – 28 min",            "1,5–2 t"),
    ("Onsdag",  "Rolig sykkeltur sone 1–2",                                         "1,5–2 t"),
    ("Torsdag", "Sone 4-intervaller: 3 × 5 min (pause 3 min) – 15 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "2–2,5 t"),
    ("Søndag",  "Rolig sykkeltur",                                                  "1–1,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 8,5–12,5 timer", total_style))

# Blokk 2
story.append(p("Blokk 2", h3_style))

story.append(p("<b>Uke 4 – hard (20. juli – 26. juli)</b>"))
story.append(week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                        "0–1,5 t"),
    ("Tirsdag", "Sone 3-intervaller: 5 × 9 min (pause 2 min) – 45 min",            "1,5–2 t"),
    ("Onsdag",  "Rolig langkjøring sone 1–2",                                       "2,5–3,5 t"),
    ("Torsdag", "Sone 4-intervaller: 4 × 5 min (pause 3 min) – 20 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "2,5–3,5 t"),
    ("Søndag",  "Sone 3-intervaller: 4 × 10 min (pause 2–3 min) – 40 min",         "2–2,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 11–16,5 timer", total_style))

story.append(p("<b>Uke 5 – hard (27. juli – 2. august)</b>"))
story.append(week_table([
    ("Mandag",  "Restitusjonsøkt eller fri",                                        "0–1,5 t"),
    ("Tirsdag", "Sone 3-intervaller: 4 × 12 min (pause 3 min) – 48 min",           "2–2,5 t"),
    ("Onsdag",  "Rolig langkjøring sone 1–2",                                       "3–4 t"),
    ("Torsdag", "Sone 4-intervaller: 5 × 6 min (pause 3 min) – 30 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "3–4 t"),
    ("Søndag",  "Sone 3-intervaller: 4 × 10 min (pause 3 min) – 40 min",           "2–2,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 12,5–18 timer", total_style))

story.append(p("<b>Uke 6 – rolig (3. august – 8. august)</b>"))
story.append(week_table([
    ("Mandag",  "Fri",                                                               "0 t"),
    ("Tirsdag", "Sone 3-intervaller: 4 × 7 min (pause 2 min) – 28 min",            "1,5–2 t"),
    ("Onsdag",  "Rolig sykkeltur sone 1–2",                                         "1,5–2 t"),
    ("Torsdag", "Sone 4-intervaller: 3 × 5 min (pause 3 min) – 15 min",            "1,5–2 t"),
    ("Fredag",  "Basisøkt + rolig sykkeltur",                                       "1–1,5 t"),
    ("Lørdag",  "Langkjøring sone 1–2",                                             "2–2,5 t"),
]))
story.append(p("<b>Totalbelastning:</b> 7,5–10 timer", total_style))

# ══════════════════════════════════════════════════════════
# 6. BASISSTYRKE
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Basisstyrke", h2_style))
story.append(p(
    "Dette er øvelser du kan gjøre hjemme i stua etter endt økt. "
    "Forslag til øvelser (her er det bare fantasien som setter grenser):"
))
styrke = [
    "<b>Sit-ups</b> (3 × 15 repetisjoner)",
    "<b>Rygg-hev</b> (3 × 10 rep.) – ligg på mage og hev overkropp og bein",
    "<b>Push-ups</b> (3 × 10–15 rep.) – blir det tungt, start med knærne i gulvet",
    "<b>Spenst-hopp</b> (3 × 10 rep.) – maks innsats, gå dypt",
    "<b>Hang-ups, ett-bens knebøy, ett-bens markløft, sideveis sit-up, glute-bridge</b>",
]
story.append(ListFlowable(
    [ListItem(Paragraph(i, body_style), leftIndent=12, bulletIndent=0) for i in styrke],
    bulletType="bullet", leftIndent=20,
))

# ══════════════════════════════════════════════════════════
# 7. BEVEGELIGHETSTRENING
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Bevegelighetstrening", h2_style))
story.append(p(
    "Det er viktig for å kunne sitte riktig på sykkelen og holde god teknikk selv om man er "
    "sliten, at man har trent styrke i mage/rygg og tøyd godt. En sterk overkropp gjør at det "
    "er lettere å sitte rolig på sykkelen, og ikke minst ved spurter vil man klare å opprettholde "
    "teknikk og kraft. For å sitte fremoverlent trenger man smidig muskulatur."
))
story.append(p("Forslag til øvelser:"))
tøy = ["Bakside lår", "Fremside lår", "Setemuskulatur", "Hofteleddsbøyer",
       "Legger", "Nakke", "Lange ryggsstrekkeren", "Bryst", "Overgang bryst og rygg"]
story.append(ListFlowable(
    [ListItem(Paragraph(i, body_style), leftIndent=12, bulletIndent=0) for i in tøy],
    bulletType="bullet", leftIndent=20,
))

# ══════════════════════════════════════════════════════════
# 8. SONEFORKLARING
# ══════════════════════════════════════════════════════════
story.append(hr())
story.append(p("Soneforklaring", h2_style))
story.append(zone_table())

story.append(Spacer(1, 0.5*cm))
story.append(p("Lykke til med sesongen! 🚴", ParagraphStyle(
    "closing", parent=body_style, alignment=TA_CENTER,
    textColor=TVK_BLUE, fontSize=10, fontName="Helvetica-Bold"
)))

# ── Generer PDF ─────────────────────────────────────────────────────────────────
OUT = "planer/treningsplan-u17.pdf"
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Treningsplan TVK U17 2026",
    author="Trondhjems Velocipedklubb",
)
doc.build(story)
print(f"PDF generert: {OUT}")
