---
name: eqtiming-regurl-workflow
description: 'Find the correct EQ Timing event and generate the exact regUrl update for data/ritt.js in one workflow. Use when a race is missing regUrl, when you want both candidate links and a patch suggestion, or when you need a safe end-to-end EQ Timing lookup for this repository.'
argument-hint: 'Race name and date window'
user-invocable: true
---

# EQ Timing regUrl Workflow

Use this skill when you want the whole EQ Timing workflow in one place:

1. search EQ Timing for candidate events
2. choose signup or results URL
3. generate the exact `data/ritt.js` update

This skill combines [eqtiming-link-finder](./../eqtiming-link-finder/SKILL.md) and [eqtiming-regurl-updater](./../eqtiming-regurl-updater/SKILL.md).

## When to Use

- A race in `data/ritt.js` is missing `regUrl`
- You need to replace an outdated EQ Timing ID
- You want both candidate matches and a ready patch
- You want one repeatable command instead of two separate steps

## Procedure

1. Read the race row in [data/ritt.js](./../../data/ritt.js) and collect the exact race name plus a narrow date window.
2. Run [scripts/eqtiming-regurl-workflow.sh](./scripts/eqtiming-regurl-workflow.sh) with `--race-name`, `--query`, `--from`, and `--to`.
3. Inspect the returned candidate rows from EQ Timing.
4. Confirm the chosen candidate by year, date overlap, organizer, city, and discipline.
5. Review the suggested updated line and patch.
6. Apply the patch only if the row match is exact and the selected event is clearly the right one.

## Recommended Command

```bash
.github/skills/eqtiming-regurl-workflow/scripts/eqtiming-regurl-workflow.sh \
  --race-name "Sørlandet Petit Prix" \
  --query "Sørlandet Petit Prix" \
  --from 2026-08-07 \
  --to 2026-08-10
```

For results links:

```bash
.github/skills/eqtiming-regurl-workflow/scripts/eqtiming-regurl-workflow.sh \
  --race-name "Sørlandet Petit Prix" \
  --query "Sørlandet Petit Prix" \
  --from 2026-08-07 \
  --to 2026-08-10 \
  --mode results
```

## Rules

- Do not guess if no 2026 candidate fits
- Prefer the earliest relevant event for split weekend registrations unless there is a dedicated umbrella signup page
- Leave `regUrl` unset if the API only returns old editions or unrelated events
- Update only `data/ritt.js`

## Output Format

The workflow should produce:

- candidate EQ Timing rows
- chosen event ID and URL
- reason for the selection
- matched `data/ritt.js` line number
- updated line
- ready-to-apply `apply_patch` block
