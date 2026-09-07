#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "TVKsykkel/1.0 (TVK participant updater)"
TVK_MATCHES = {
    "trondhjems velocipedklubb",
    "trondhjems velociped klubb",
    "tvk",
}

HALDEN_EVENTS = [
    {
        "key": "xco",
        "label": "XCO lørdag",
        "event_id": 81510,
        "dashboard_url": "https://live.eqtiming.com/81510#dashboard",
        "rows": [
            ("09:15", "M/K 10", ("10",)),
            ("09:30", "M/K 11-12", ("11-12",)),
            ("10:40", "M/K 13-14", ("13-14",)),
            ("11:30", "M15-16", ("15-16",)),
            ("13:00-14:50", "Junior og elite", ("junior", "elite", "senior")),
        ],
    },
    {
        "key": "xcc",
        "label": "XCC søndag",
        "event_id": 81511,
        "dashboard_url": "https://live.eqtiming.com/81511#dashboard",
        "rows": [
            ("09:30", "M/K 10", ("10",)),
            ("10:20", "M/K 11-12", ("11-12",)),
            ("11:00", "M/K 13-14", ("13-14",)),
            ("12:00", "M/K 15-16", ("15-16",)),
            ("13:00-14:00", "Junior og elite", ("junior", "elite", "senior")),
        ],
    },
]

RACES = {
    "halden": {
        "name": "Halden",
        "html_path": ROOT / "rittplan" / "halden-karl-xii.html",
        "events": HALDEN_EVENTS,
        "renderer": "halden",
    },
    "lillehammer": {
        "name": "Lillehammer Sykkelfestival",
        "html_path": ROOT / "rittplan" / "lillehammer-sykkelfestival.html",
        "events": [
            {
                "key": "festival",
                "label": "Lillehammer Sykkelfestival",
                "event_id": 81060,
                "dashboard_url": "https://live.eqtiming.com/81060#dashboard",
            }
        ],
        "renderer": "summary",
    },
}


@dataclass
class Entry:
    name: str
    class_name: str
    club: str
    status: str
    start_time: str


def fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(request) as response:
        return json.load(response)


def normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def is_tvk_entry(item: dict[str, Any]) -> bool:
    athlete = item.get("Utover") or {}
    club = ((athlete.get("Klubb") or {}).get("Navn") or "")
    team = ((athlete.get("Team") or {}).get("Navn") or "")
    candidates = [club, team, item.get("KlubbTeamFormatert") or "", item.get("Klubbnavn") or ""]

    for candidate in candidates:
        normalized_candidate = normalize(candidate)
        if normalized_candidate in TVK_MATCHES or "trondhjems velocipedklubb" in normalized_candidate:
            return True

    return False


def normalize_start_time(value: str) -> str:
    try:
        return datetime.strptime(value, "%H:%M:%S").strftime("%H:%M")
    except ValueError:
        return value


def extract_start_time(item: dict[str, Any]) -> str:
    for stage in (item.get("EtappeDeltaker") or {}).values():
        start_time = stage.get("StarttidFormatert")
        if start_time:
            return normalize_start_time(start_time)

    wave = item.get("Pulje") or {}
    start_time = wave.get("WaveStartTidFormatert")
    if start_time:
        return normalize_start_time(start_time)

    first_start = (item.get("Arrangement") or {}).get("ForsteStart")
    if first_start:
        try:
            return datetime.fromisoformat(first_start).strftime("%H:%M")
        except ValueError:
            return first_start

    return "Ikke publisert"


def fetch_event_entries(event_id: int) -> list[Entry]:
    url = f"https://live.eqtiming.com/api/Startlist/{event_id}/0?startAt=1&query=&filter=&sortcols=&count=500"
    payload = fetch_json(url)
    entries = []

    for item in (payload.get("Items") or {}).values():
        if not is_tvk_entry(item):
            continue

        athlete = item.get("Utover") or {}
        entries.append(
            Entry(
                name=athlete.get("NavnFormatert") or "Ukjent rytter",
                class_name=((item.get("Klasse") or {}).get("Navn") or "Ukjent klasse"),
                club=item.get("KlubbTeamFormatert") or ((athlete.get("Klubb") or {}).get("Navn") or "TVK"),
                status=((item.get("Status") or {}).get("Navn") or "Registrert"),
                start_time=extract_start_time(item),
            )
        )

    entries.sort(key=lambda entry: (entry.start_time, entry.class_name, entry.name))
    return entries


def format_now() -> str:
    now = datetime.now().astimezone()
    months = {
        1: "januar",
        2: "februar",
        3: "mars",
        4: "april",
        5: "mai",
        6: "juni",
        7: "juli",
        8: "august",
        9: "september",
        10: "oktober",
        11: "november",
        12: "desember",
    }
    return f"{now.day}. {months[now.month]} {now.year} kl. {now.strftime('%H:%M')}"


def replace_between_markers(html: str, marker: str, replacement: str) -> str:
    start_token = f"<!-- {marker}:start -->"
    end_token = f"<!-- {marker}:end -->"
    start_index = html.find(start_token)
    end_index = html.find(end_token)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise ValueError(f"Fant ikke ett gyldig markørpar for {marker}")
    if html.count(start_token) != 1 or html.count(end_token) != 1:
        raise ValueError(f"Forventet nøyaktig ett markørpar for {marker}")

    content_start = start_index + len(start_token)
    return html[:content_start] + "\n" + replacement + "\n    " + html[end_index:]


def build_detail_html(
    race_name: str,
    events: list[dict[str, Any]],
    entries_by_event: dict[str, list[Entry]],
    timestamp_text: str,
) -> str:
    total_entries = sum(len(entries) for entries in entries_by_event.values())
    suffix = "er" if total_entries != 1 else ""
    parts = [
        '                    <div class="status-item">',
        '                        <strong>TVK-påmeldte</strong>',
        f'                        <p>Oppdatert automatisk fra EQ Timing {escape(timestamp_text)}. Fant {total_entries} TVK-påmelding{suffix} for {escape(race_name)}.</p>',
    ]

    for event in events:
        entries = entries_by_event[event["key"]]
        if entries:
            lines = "<br>".join(
                escape(f"{entry.start_time} - {entry.name} ({entry.class_name}, {entry.status})")
                for entry in entries
            )
            paragraph = f'<p><strong>{escape(event["label"])}:</strong><br>{lines}</p>'
        else:
            paragraph = (
                f'<p><strong>{escape(event["label"])}:</strong> Ingen TVK-ryttere synlige i deltakerlista. '
                f'<a href="{escape(event["dashboard_url"])}" target="_blank" rel="noopener">Åpne EQ Timing</a>.</p>'
            )
        parts.append(f"                        {paragraph}")

    parts.append("                    </div>")
    return "\n".join(parts)


def group_event_rows(event: dict[str, Any], entries: list[Entry]) -> dict[str, list[Entry]]:
    grouped = {label: [] for _, label, _ in event["rows"]}
    for entry in entries:
        normalized_class = normalize(entry.class_name)
        for _, label, needles in event["rows"]:
            if any(needle in normalized_class for needle in needles):
                grouped[label].append(entry)
                break
    return grouped


def build_table_rows(event: dict[str, Any], entries: list[Entry]) -> str:
    grouped = group_event_rows(event, entries)
    rows = []
    for time_text, label, _ in event["rows"]:
        event_entries = grouped[label]
        status_html = "<br>".join(
            escape(f"{entry.name} ({entry.class_name})") for entry in event_entries
        ) or "Ingen TVK-navn publisert"
        rows.append(
            "                                    <tr>\n"
            f"                                        <td>{escape(time_text)}</td>\n"
            f"                                        <td>{escape(label)}</td>\n"
            f"                                        <td>{status_html}</td>\n"
            "                                    </tr>"
        )
    return "                                <tbody>\n" + "\n".join(rows) + "\n                                </tbody>"


def update_halden_html(
    html: str,
    config: dict[str, Any],
    entries_by_event: dict[str, list[Entry]],
    timestamp_text: str,
) -> tuple[str, str]:
    total_entries = sum(len(entries) for entries in entries_by_event.values())
    xco_count = len(entries_by_event["xco"])
    xcc_count = len(entries_by_event["xcc"])
    suffix = "er" if total_entries != 1 else ""

    if total_entries == 0:
        hero_status = f'                    <div class="hero-item-value">Ingen ryttere fra TVK ligger i deltakerlistene for verken XCO eller XCC per {escape(timestamp_text)}.</div>'
        summary_status = '                        <div class="summary-item-value">Ingen TVK-navn er synlige i dagens deltakerlister. Denne siden fungerer derfor foreløpig som praktisk helgeside og oppdateres når eventuelle etteranmeldinger kommer.</div>'
    else:
        hero_status = (
            '                    <div class="hero-item-value">'
            f'{total_entries} TVK-påmelding{suffix} funnet per {escape(timestamp_text)} '
            f'({xco_count} i XCO, {xcc_count} i XCC).</div>'
        )
        summary_status = (
            '                        <div class="summary-item-value">'
            f'{total_entries} TVK-ryttere er nå synlige i deltakerlistene. Bruk TVK-statusen under for navn, klasser og starttider fra siste oppdatering {escape(timestamp_text)}.</div>'
        )

    notice_html = (
        '    <div class="notice">\n'
        f'        Starttider og deltakerstatus er hentet fra EQ Timing {escape(timestamp_text)}. '
        'Overnatting, avreise og eventuell TVK-lagbase er markert som foreløpig inntil mer praktisk info er avklart.\n'
        '    </div>'
    )
    replacements = {
        "tvk-hero-status": hero_status,
        "tvk-notice": notice_html,
        "tvk-summary-status": summary_status,
        "tvk-xco-rows": build_table_rows(config["events"][0], entries_by_event["xco"]),
        "tvk-xcc-rows": build_table_rows(config["events"][1], entries_by_event["xcc"]),
        "tvk-detail-status": build_detail_html(config["name"], config["events"], entries_by_event, timestamp_text),
    }
    for marker, replacement in replacements.items():
        html = replace_between_markers(html, marker, replacement)

    summary = f"XCO: {xco_count}, XCC: {xcc_count}, totalt: {total_entries}"
    return html, summary


def update_summary_html(
    html: str,
    config: dict[str, Any],
    entries_by_event: dict[str, list[Entry]],
    timestamp_text: str,
) -> tuple[str, str]:
    entries = [entry for event_entries in entries_by_event.values() for entry in event_entries]
    total_entries = len(entries)
    suffix = "er" if total_entries != 1 else ""
    names = ", ".join(entry.name for entry in entries)

    if entries:
        hero_text = (
            f"{total_entries} TVK-påmelding{suffix} funnet per {escape(timestamp_text)}: "
            f"{escape(names)}. Sjekk detaljene under for publiserte starttider."
        )
    else:
        hero_text = f"Ingen TVK-ryttere er synlige i deltakerlista per {escape(timestamp_text)}."

    hero_status = f'                    <div class="hero-item-value">{hero_text}</div>'
    detail_status = build_detail_html(config["name"], config["events"], entries_by_event, timestamp_text)
    html = replace_between_markers(html, "tvk-hero-status", hero_status)
    html = replace_between_markers(html, "tvk-detail-status", detail_status)
    return html, f"totalt: {total_entries}"


def fetch_race_entries(config: dict[str, Any]) -> dict[str, list[Entry]]:
    return {
        event["key"]: fetch_event_entries(event["event_id"])
        for event in config["events"]
    }


def update_race(race_key: str, html_override: str | None, dry_run: bool) -> None:
    config = RACES[race_key]
    entries_by_event = fetch_race_entries(config)
    timestamp_text = format_now()

    if dry_run:
        print(f"TVK-status for {config['name']} hentet {timestamp_text}")
        for event in config["events"]:
            entries = entries_by_event[event["key"]]
            print(f"- {event['label']}: {len(entries)} TVK-ryttere")
            for entry in entries:
                print(f"  {entry.start_time} {entry.name} | {entry.class_name} | {entry.status}")
        return

    html_path = Path(html_override).resolve() if html_override else config["html_path"]
    html = html_path.read_text(encoding="utf-8")
    if config["renderer"] == "halden":
        html, summary = update_halden_html(html, config, entries_by_event, timestamp_text)
    else:
        html, summary = update_summary_html(html, config, entries_by_event, timestamp_text)
    html_path.write_text(html, encoding="utf-8")
    print(f"Oppdaterte {config['name']} {timestamp_text}. {summary}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Oppdater TVK-deltakerstatus på rittplaner fra EQ Timing.")
    parser.add_argument("race", nargs="?", default="all", choices=["all", *RACES], help="Ritt som skal oppdateres")
    parser.add_argument("--html", help="Alternativ HTML-fil; kan bare brukes for ett ritt")
    parser.add_argument("--dry-run", action="store_true", help="Hent og oppsummer uten å skrive til HTML-filene")
    args = parser.parse_args()

    if args.race == "all" and args.html:
        parser.error("--html kan ikke brukes sammen med 'all'")

    race_keys = RACES if args.race == "all" else [args.race]
    for race_key in race_keys:
        update_race(race_key, args.html, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())