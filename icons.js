/**
 * TVK ikonbibliotek
 *
 * Injiserer et SVG-sprite med alle ikoner øverst i <body>.
 * Legg til <script src="icons.js"></script> øverst i <body> på alle sider.
 * Bruk ikoner med: <svg><use href="#icon-navn"/></svg>
 *
 * Tilgjengelige ikoner:
 *   Navigasjon:   icon-home, icon-map, icon-cyclist
 *   Treningssiden: icon-calendar, icon-bolt, icon-sprint, icon-clipboard,
 *                  icon-phone, icon-sprout, icon-pdf
 *   Ritt-guide:   icon-clock, icon-tag, icon-flame, icon-radio, icon-shirt,
 *                  icon-coffee, icon-bike, icon-users, icon-check-square
 *   Terminliste:  icon-trophy
 */
(function () {
    var sprite = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    sprite.setAttribute('style', 'display:none');
    sprite.setAttribute('aria-hidden', 'true');
    sprite.innerHTML = '\
<symbol id="icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M3 9.5L12 3l9 6.5V20a1.5 1.5 0 01-1.5 1.5h-15A1.5 1.5 0 013 20z"/>\
    <polyline points="9 22 9 12 15 12 15 22"/>\
</symbol>\
<symbol id="icon-map" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>\
    <line x1="8" y1="2" x2="8" y2="18"/>\
    <line x1="16" y1="6" x2="16" y2="22"/>\
</symbol>\
<symbol id="icon-cyclist" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <polyline points="2 12 6 12 8 5 11 19 14 9 16 12 22 12"/>\
</symbol>\
<symbol id="icon-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>\
    <line x1="16" y1="2" x2="16" y2="6"/>\
    <line x1="8" y1="2" x2="8" y2="6"/>\
    <line x1="3" y1="10" x2="21" y2="10"/>\
    <line x1="9" y1="10" x2="9" y2="22"/>\
    <line x1="15" y1="10" x2="15" y2="22"/>\
    <line x1="3" y1="15" x2="21" y2="15"/>\
</symbol>\
<symbol id="icon-bolt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>\
</symbol>\
<symbol id="icon-sprint" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <circle cx="17" cy="4" r="2"/>\
    <path d="M15 7l-4 4 2.5 2.5L11 18"/>\
    <path d="M19 7l-1.5 5-4-3"/>\
    <line x1="2" y1="10" x2="6" y2="10"/>\
    <line x1="3" y1="13" x2="7" y2="13"/>\
    <line x1="2" y1="16" x2="5" y2="16"/>\
</symbol>\
<symbol id="icon-clipboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/>\
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>\
    <line x1="8" y1="12" x2="16" y2="12"/>\
    <line x1="8" y1="16" x2="12" y2="16"/>\
</symbol>\
<symbol id="icon-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/>\
</symbol>\
<symbol id="icon-sprout" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M12 22V10"/>\
    <path d="M6 14c0-3.5 2.5-6 6-6"/>\
    <path d="M18 10c0-4-3-7-6-7"/>\
    <path d="M12 3c3 0 6 3 6 7"/>\
    <path d="M12 10c-3.5 0-6 2.5-6 6"/>\
</symbol>\
<symbol id="icon-bike" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <circle cx="5.5" cy="17.5" r="3.5"/>\
    <circle cx="18.5" cy="17.5" r="3.5"/>\
    <polyline points="5.5 17.5 9 10 12 17.5"/>\
    <line x1="9" y1="10" x2="15.5" y2="7"/>\
    <polyline points="12 17.5 15.5 7 18.5 17.5"/>\
    <line x1="15.5" y1="7" x2="18" y2="6"/>\
</symbol>\
<symbol id="icon-flame" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M12 22c-4 0-7-3-7-7.5 0-3 1.5-5.5 3.5-8C10 4.5 12 2 12 2s2 2.5 3.5 4.5c2 2.5 3.5 5 3.5 8 0 4.5-3 7.5-7 7.5z"/>\
    <path d="M12 22c-1.5 0-3-1.5-3-3.5 0-1.5.7-2.5 1.5-3.5.5-.5 1.5-1.5 1.5-1.5s1 1 1.5 1.5c.8 1 1.5 2 1.5 3.5 0 2-1.5 3.5-3 3.5z"/>\
</symbol>\
<symbol id="icon-trophy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M6 9V4h12v5c0 3.3-2.7 6-6 6s-6-2.7-6-6z"/>\
    <path d="M6 5H3v2c0 1.7 1.3 3 3 3"/>\
    <path d="M18 5h3v2c0 1.7-1.3 3-3 3"/>\
    <line x1="12" y1="15" x2="12" y2="19"/>\
    <rect x="8" y="19" width="8" height="2" rx="1"/>\
</symbol>\
<symbol id="icon-users" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>\
    <circle cx="9" cy="7" r="4"/>\
    <path d="M23 21v-2a4 4 0 00-3-3.87"/>\
    <path d="M16 3.13a4 4 0 010 7.75"/>\
</symbol>\
<symbol id="icon-pdf" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>\
    <polyline points="14 2 14 8 20 8"/>\
    <line x1="12" y1="18" x2="12" y2="12"/>\
    <polyline points="9 15 12 18 15 15"/>\
</symbol>\
<symbol id="icon-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <circle cx="12" cy="12" r="10"/>\
    <polyline points="12 6 12 12 16 14"/>\
</symbol>\
<symbol id="icon-tag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z"/>\
    <line x1="7" y1="7" x2="7.01" y2="7"/>\
</symbol>\
<symbol id="icon-radio" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <circle cx="12" cy="12" r="2"/>\
    <path d="M16.24 7.76a6 6 0 010 8.49m-8.48-.01a6 6 0 010-8.49m11.31-2.82a10 10 0 010 14.14m-14.14 0a10 10 0 010-14.14"/>\
</symbol>\
<symbol id="icon-shirt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M20.38 3.46L16 2a4 4 0 01-8 0L3.62 3.46a2 2 0 00-1.34 2.23l.58 3.57a1 1 0 00.99.86H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.86l.58-3.57a2 2 0 00-1.34-2.23z"/>\
</symbol>\
<symbol id="icon-coffee" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <path d="M18 8h1a4 4 0 010 8h-1"/>\
    <path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/>\
    <line x1="6" y1="1" x2="6" y2="4"/>\
    <line x1="10" y1="1" x2="10" y2="4"/>\
    <line x1="14" y1="1" x2="14" y2="4"/>\
</symbol>\
<symbol id="icon-check-square" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\
    <polyline points="9 11 12 14 22 4"/>\
    <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>\
</symbol>';
    document.body.insertBefore(sprite, document.body.firstChild);
})();
