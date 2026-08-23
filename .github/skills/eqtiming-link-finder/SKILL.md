---
name: eqtiming-link-finder
description: 'Find the correct EQ Timing signup or results link for cycling races in this repository. Use when adding or fixing regUrl in data/ritt.js, looking up EQ Timing event IDs, matching races by name/date/organizer/city, or deciding whether to use #dashboard for signup or the base live URL for results.'
argument-hint: 'Race name or month/date window'
user-invocable: true
---

# EQ Timing Link Finder

Use this skill when you need the correct EQ Timing link for a race in this project.

This repository keeps race registration links in [data/ritt.js](./../../data/ritt.js). The correct source of truth for EQ Timing discovery is the public events API on `events.eqtiming.com`, not a manual site search.

## Use Cases

- Add a missing `regUrl` to a race in `data/ritt.js`
- Replace an outdated EQ Timing ID with the correct 2026 event
- Choose between signup and results URLs
- Resolve multi-day weekends where EQ Timing has one ID per day or discipline

## Project Rules

- Edit only `data/ritt.js` for race links
- Skip `trening` entries unless the race explicitly uses EQ Timing
- Use `regUrl: "spond"` only for Spond-based local events
- If no verified EQ Timing event exists yet, leave `regUrl` unset rather than guessing

## Procedure

1. Find the target race in `data/ritt.js` and note `name`, `start`, `end`, `location`, `club`, and `catKey`.
2. Query the EQ Timing API with the race name and a tight date window around the event.
3. Filter matches by year, organizer, city, and discipline.
4. If EQ Timing splits a weekend into several event IDs, prefer the first day or the clearest umbrella signup page.
5. Build the URL:
   - Signup: `https://live.eqtiming.com/<ID>#dashboard`
   - Results: `https://live.eqtiming.com/<ID>`
6. Update only the matching row in `data/ritt.js`.

## Recommended Command

Run [scripts/find-eqtiming.sh](./scripts/find-eqtiming.sh) with race name and date window:

```bash
.github/skills/eqtiming-link-finder/scripts/find-eqtiming.sh \
  --query "Sørlandet Petit Prix" \
  --from 2026-08-07 \
  --to 2026-08-10
```

## Match Heuristics

- Prefer exact-year matches in the requested date window
- Prefer organizer and city that match the row in `data/ritt.js`
- For `ncterr`, prefer MTB/XC names like `XCO`, `XCC`, `Rundbane`, `Kortbane`
- For `ncfranking` and `bioracer`, landeverihelger often appear as separate `tempo`, `gateritt`, or `fellesstart` events
- When several IDs are valid for the same weekend, use the earliest relevant event unless a dedicated combined signup page is returned
- For past races, remove `#dashboard` and use the base live URL when the goal is results

## Verification

- Confirm the returned year is correct
- Confirm the event date overlaps the race row
- Confirm organizer or city is consistent with the race row
- Do not add a link if the API returns only old editions or unrelated sports

## Output Format

When using this skill, report:

- chosen event ID
- chosen URL
- why that match was selected
- whether it is a signup link or a results link

After the URL is verified, use the companion skill `eqtiming-regurl-updater` to generate the exact `data/ritt.js` line update, or use `eqtiming-regurl-workflow` to do both steps in one pass.

