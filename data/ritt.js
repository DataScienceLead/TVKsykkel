// Felles ritt-data for TVKsykkel.
// Denne filen er eneste kilde til sannhet – rediger kun her.
//
// Felt:
//   name     – Visningsnavn
//   catKey   – Kategori (ncterr, bioracer, turritt, ncfranking, lokale, trening)
//   start    – Startdato "DD.MM.ÅÅÅÅ"
//   end      – Sluttdato "DD.MM.ÅÅÅÅ"
//   location – Sted (tekst)
//   club     – Arrangør
//   lat/lng  – Koordinater for kart (ikke påkrevd for ritt uten kart-pin)
//   regUrl   – Påmeldingslenke (valgfri):
//                "https://live.eqtiming.com/XXXXX#dashboard"  – eqtiming-ritt
//                "spond"                                       – Spond-påmelding
//                (utelatt)                                     – ingen knapp

const rittData = [
    { name: "XC NC1-2",                         catKey: "ncterr",     start: "18.04.2026", end: "19.04.2026", location: "Son",                          club: "Soon CK",             lat: 59.5283,   lng: 10.6872,  regUrl: "https://live.eqtiming.com/82148#dashboard" },
    { name: "XC NC3-5",                         catKey: "ncterr",     start: "01.05.2026", end: "03.05.2026", location: "Oslo",                         club: "Rye",                 lat: 59.96985,  lng: 10.7927,  regUrl: "https://live.eqtiming.com/81388#dashboard" },
    { name: "Rogaland 3Ds",                     catKey: "ncfranking", start: "01.05.2026", end: "03.05.2026", location: "Rogaland",                     club: "Stavanger SK",        lat: 58.8963,   lng: 5.6676,   regUrl: "https://live.eqtiming.com/80945#dashboard" },
    { name: "Bioracer-cup #1",                  catKey: "bioracer",   start: "06.05.2026", end: "06.05.2026", location: "Prestmoen",                    club: "Stjørdals-Blink",     lat: 63.451815, lng: 10.991306, regUrl: "https://live.eqtiming.com/80359#dashboard" },
    { name: "Bioracer-cup #2",                  catKey: "bioracer",   start: "20.05.2026", end: "20.05.2026", location: "Lånkebanen",                   club: "Stjørdals-Blink",     lat: 63.406884, lng: 10.913933, regUrl: "https://live.eqtiming.com/80360#dashboard" },
    { name: "Treningsritt TVK&Gauldal #1",      catKey: "lokale",     start: "28.05.2026", end: "28.05.2026", location: "Trehjørningen arena",          club: "Gauldal Sykkelklubb", lat: 63.204291, lng: 10.249985, regUrl: "spond" },
    { name: "XC NM",                            catKey: "ncterr",     start: "30.05.2026", end: "31.05.2026", location: "Sande",                        club: "Sande SK",            lat: 59.5887,   lng: 10.2416,  regUrl: "https://live.eqtiming.com/82514#dashboard" },
    { name: "XC NC6-7 Terrengsykkelfestivalen", catKey: "ncterr",     start: "06.06.2026", end: "07.06.2026", location: "Oslo",                         club: "Frøy",                lat: 59.9200,   lng: 10.7400,  regUrl: "https://live.eqtiming.com/82147#dashboard" },
    { name: "Bioracer-cup #3",                  catKey: "bioracer",   start: "10.06.2026", end: "10.06.2026", location: "Lånkebanen",                   club: "Stjørdals-Blink",     lat: 63.406884, lng: 10.913933, regUrl: "https://live.eqtiming.com/83134#dashboard" },
    { name: "Follo 2D",                         catKey: "ncfranking", start: "13.06.2026", end: "14.06.2026", location: "Follo",                        club: "Follo",               lat: 59.7196,   lng: 10.8485 },
    { name: "L'etape Trondheim",                catKey: "turritt",    start: "13.06.2026", end: "13.06.2026", location: "Trondheim",                    club: "TVK",                 lat: 63.4305,   lng: 10.3951,  regUrl: "https://live.eqtiming.com/80549#dashboard" },
    { name: "Treningsritt TVK&Gauldal #2",      catKey: "lokale",     start: "15.06.2026", end: "15.06.2026", location: "Nilsbyen Terrengsykkelpark",   club: "TVK",                 lat: 63.4080,   lng: 10.3500,  regUrl: "spond" },
    { name: "Vestfold 3Ds",                     catKey: "ncfranking", start: "19.06.2026", end: "21.06.2026", location: "Vestfold",                     club: "Tønsberg",            lat: 59.2672,   lng: 10.4075,  regUrl: "https://live.eqtiming.com/81567#dashboard" },
    { name: "Nerskogrittet",                    catKey: "turritt",    start: "20.06.2026", end: "20.06.2026", location: "Nerskogen",                    club: "Rennebu IL",          lat: 62.799549, lng: 9.650608, regUrl: "https://live.eqtiming.com/78773#dashboard" },
    { name: "XC NC8-9",                         catKey: "ncterr",     start: "27.06.2026", end: "28.06.2026", location: "Elverum",                      club: "CK Elverum",          lat: 60.8818,   lng: 11.5613,  regUrl: "https://live.eqtiming.com/82676#dashboard" },
    { name: "Ferie",                            catKey: "trening",    start: "29.06.2026", end: "02.08.2026" },
    { name: "Sørlandet Petit Prix",             catKey: "ncfranking", start: "08.08.2026", end: "09.08.2026", location: "Kristiansand",                 club: "Kristiansand CK",     lat: 58.146,    lng: 7.995 },
    { name: "Treningssamling UM",               catKey: "trening",    start: "07.08.2026", end: "08.08.2026", location: "Trondheim",                    club: "TVK",                 lat: 63.4250,   lng: 10.4000 },
    { name: "IF Frøys Jokerfestival",           catKey: "ncfranking", start: "21.08.2026", end: "23.08.2026", location: "Ås",                           club: "Frøy SK",             lat: 59.6655,   lng: 10.7891 },
    { name: "Stjørdalsdagene GP",               catKey: "ncfranking", start: "14.08.2026", end: "16.08.2026", location: "Stjørdal",                     club: "Stjørdals-Blink",     lat: 63.4698,   lng: 10.9119 },
    { name: "Jokermesterskapet UM",             catKey: "ncfranking", start: "15.08.2026", end: "16.08.2026", location: "Skien",                        club: "Grenland SK",         lat: 59.2098,   lng: 9.6089 },
    { name: "UngdomsBirken",                    catKey: "turritt",    start: "29.08.2026", end: "29.08.2026", location: "Lillehammer",                  club: "Lillehammer CK",      lat: 61.1153,   lng: 10.4662 },
    { name: "XC NC10-11 Nilsbyen",              catKey: "ncterr",     start: "05.09.2026", end: "06.09.2026", location: "Nilsbyen Terrengsykkelpark",   club: "TVK",                 lat: 63.4080,   lng: 10.3500 },
    { name: "Lillehammer Sykkelfestival",       catKey: "ncfranking", start: "11.09.2026", end: "13.09.2026", location: "Lillehammer",                  club: "Lillehammer CK",      lat: 61.1200,   lng: 10.4700 },
    { name: "XC 12-13 Karl XII rittet",         catKey: "ncterr",     start: "19.09.2026", end: "20.09.2026", location: "Halden",                       club: "Halden CK",           lat: 59.1227,   lng: 11.3875 },
];
