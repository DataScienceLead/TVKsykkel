#!/usr/bin/env python3
"""Build data/trening.js from the three Markdown training plans."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "trening.js"
GROUPS = {
    "u15": ("U15", "13–14 år", "treningsplan-u15.md"),
    "u17": ("U17", "15–16 år", "treningsplan-u17.md"),
    "u19": ("Junior / U19", "17–18 år", "treningsplan-u19.md"),
}
DAY_NAMES = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
MONTHS = {
    "januar": 1, "februar": 2, "mars": 3, "april": 4, "mai": 5,
    "juni": 6, "juli": 7, "august": 8, "september": 9,
    "oktober": 10, "november": 11, "desember": 12,
}
PHASE_NAMES = {
    "Opptreningsperiode", "Oppkjøringsperiode", "Rittforberedelse",
    "Vårsesong", "Sommer – volumblokk", "Sensommer – VO₂ og rittperiode",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("--", "–").replace("\\", "")).strip()


def duration_values(text: str) -> tuple[float, float]:
    numbers = [float(value.replace(",", ".")) for value in re.findall(r"\d+(?:[,.]\d+)?", text)]
    if not numbers:
        return 0.0, 0.0
    return numbers[0], numbers[-1]


def workout_metadata(title: str) -> dict[str, object]:
    value = title.casefold()
    if "fri" in value or "hvile" in value:
        category, intensity, priority = "rest", "rest", 0
    elif "ritt" in value:
        category, intensity, priority = "race", "max", 3
    elif "styrke" in value or "basisøkt" in value:
        category, intensity, priority = "strength", "medium", 2
    elif "intervall" in value or "sone 4" in value or "sone 5" in value or "sone 6" in value:
        category, intensity, priority = "interval", "high", 3
    elif "langkjøring" in value or "langtur" in value:
        category, intensity, priority = "endurance", "low", 2
    else:
        category, intensity, priority = "easy", "low", 1
    if "sone 6" in value or "maks" in value:
        intensity = "max"
    elif "sone 3" in value and intensity == "high":
        intensity = "medium"
    return {
        "category": category,
        "intensity": intensity,
        "priority": priority,
        "movable": "ritt" not in value and "fellestrening" not in value,
        "recoveryDays": 1 if intensity in {"high", "max"} else 0,
    }


def make_day(day: str, title: str, duration: str, index: int) -> dict[str, object]:
    minimum, maximum = duration_values(duration)
    return {
        "dayIndex": index,
        "day": day,
        "title": clean(title),
        "duration": clean(duration),
        "minHours": minimum,
        "maxHours": maximum,
        **workout_metadata(title),
    }


def table_row(line: str) -> tuple[str, str, str] | None:
    if not line.startswith("|"):
        return None
    cells = [clean(cell) for cell in line.strip().strip("|").split("|")]
    if len(cells) < 3 or cells[0] in {"Dag", "----------"} or set(cells[0]) <= {"-", ":"}:
        return None
    if cells[0] not in DAY_NAMES:
        return None
    return cells[0], cells[1], cells[2]


def parse_date_range(title: str) -> tuple[str, str] | None:
    match = re.search(
        r"\((\d{1,2})\.?(?:\s+([a-zæøå]+))?\s*[–-]\s*(\d{1,2})\.\s+([a-zæøå]+)\)",
        title.casefold(),
    )
    if not match:
        return None
    start_day, start_month_name, end_day, end_month_name = match.groups()
    end_month = MONTHS[end_month_name]
    start_month = MONTHS[start_month_name] if start_month_name else end_month
    return (
        date(2026, start_month, int(start_day)).isoformat(),
        date(2026, end_month, int(end_day)).isoformat(),
    )


def template_months(title: str) -> list[int]:
    lowered = title.casefold()
    return [month for name, month in MONTHS.items() if re.search(rf"\b{name}\b", lowered)]


def parse_plan(group_key: str, label: str, age: str, source: Path) -> dict[str, object]:
    lines = source.read_text(encoding="utf-8").splitlines()
    templates: list[dict[str, object]] = []
    weeks: list[dict[str, object]] = []
    phase = ""
    current: dict[str, object] | None = None
    pending_day: tuple[str, str] | None = None

    def finish_current() -> None:
        nonlocal current
        if not current:
            return
        days = current.get("days", [])
        if len(days) == 7:
            target = weeks if current.get("start") else templates
            position = len(target) + 1
            current["id"] = f"{group_key}-{'week' if target is weeks else 'template'}-{position}"
            for day in days:
                day["id"] = f"{current['id']}-d{day['dayIndex']}"
            target.append(current)
        current = None

    for raw_line in lines:
        line = raw_line.strip()
        if pending_day and line and not line.startswith(("**", "#", "|", "---")):
            day, value = pending_day
            pending_day = (day, clean(f"{value} {line}"))
            continue
        if pending_day:
            day, value = pending_day
            duration_match = re.search(r"(\d+(?:[,.]\d+)?(?:\s*[–-]\s*\d+(?:[,.]\d+)?)?\s*t)\s*$", value)
            if current and duration_match:
                title = value[:duration_match.start()].strip()
                current["days"].append(make_day(day, title, duration_match.group(1), DAY_NAMES.index(day)))
            pending_day = None

        heading = clean(re.sub(r"^#{2,3}\s+", "", line)) if re.match(r"^#{2,3}\s+", line) else ""
        bold_heading = clean(line.strip("*")) if line.startswith("**") and line.endswith("**") else ""
        candidate = heading or bold_heading

        if candidate in PHASE_NAMES:
            finish_current()
            phase = candidate
            continue

        is_week = candidate.startswith("Uke ") and parse_date_range(candidate)
        months = template_months(candidate) if candidate else []
        is_template = bool(months) and not is_week and not candidate.startswith(("Periode:", "Totalbelastning:"))
        if is_week or is_template:
            finish_current()
            current = {"title": candidate, "phase": phase, "total": "", "days": []}
            if is_week:
                current["start"], current["end"] = parse_date_range(candidate) or ("", "")
            else:
                current["months"] = months
                lowered = candidate.casefold()
                current["variant"] = "race" if "rittuke" in lowered else "training" if "treningsuke" in lowered else "default"
            continue

        row = table_row(line)
        if row and current:
            day, title, duration = row
            current["days"].append(make_day(day, title, duration, DAY_NAMES.index(day)))
            continue

        day_match = re.match(r"^\*\*(Mandag|Tirsdag|Onsdag|Torsdag|Fredag|Lørdag|Søndag):\*\*\s*(.+)$", line)
        if day_match and current:
            pending_day = (day_match.group(1), clean(day_match.group(2)))
            continue

        total_match = re.match(r"^\*\*(?:Totalbelastning:\*\*\s*)?([\d,.]+\s*[–-]\s*[\d,.]+\s*timer)\*?\*?$", line)
        if total_match and current:
            current["total"] = clean(total_match.group(1))

    if pending_day and current:
        day, value = pending_day
        duration_match = re.search(r"(\d+(?:[,.]\d+)?(?:\s*[–-]\s*\d+(?:[,.]\d+)?)?\s*t)\s*$", value)
        if duration_match:
            current["days"].append(make_day(day, value[:duration_match.start()], duration_match.group(1), DAY_NAMES.index(day)))
    finish_current()
    return {
        "id": group_key,
        "label": label,
        "age": age,
        "source": f"planer/{source.name}",
        "templates": templates,
        "weeks": weeks,
    }


def main() -> None:
    groups = {
        key: parse_plan(key, label, age, ROOT / "planer" / filename)
        for key, (label, age, filename) in GROUPS.items()
    }
    payload = {
        "version": 1,
        "season": {"label": "2026", "start": "2025-11-01", "end": "2026-11-01"},
        "groups": groups,
    }
    javascript = "globalThis.TRAINING_PLANS = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    OUTPUT.write_text(javascript, encoding="utf-8")
    for key, group in groups.items():
        print(f"{key}: {len(group['templates'])} maler, {len(group['weeks'])} daterte uker")


if __name__ == "__main__":
    main()