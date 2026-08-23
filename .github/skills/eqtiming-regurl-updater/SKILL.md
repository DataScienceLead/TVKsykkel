---
name: eqtiming-regurl-updater
description: 'Generate a safe, exact update for regUrl in data/ritt.js after an EQ Timing link has been verified. Use when you already know the correct event ID or URL and want the matching race row updated without editing the wrong entry.'
argument-hint: 'Race name plus event ID or URL'
user-invocable: true
---

# EQ Timing regUrl Updater

Use this skill after an EQ Timing link has already been verified.

This skill does not search EQ Timing. Its job is to find the correct race row in [data/ritt.js](./../../data/ritt.js) and generate the exact replacement line or patch needed to set `regUrl` safely.

## Use Cases

- Add `regUrl` to a race that is missing it
- Replace an outdated `regUrl` with a new 2026 event ID
- Convert a verified event ID into the exact `data/ritt.js` edit
- Avoid updating the wrong race when similar race names exist

## Procedure

1. Start with a verified EQ Timing URL or event ID.
2. Identify the exact race name in `data/ritt.js`.
3. Run [scripts/suggest-regurl-update.py](./scripts/suggest-regurl-update.py) with either `--url` or `--event-id`.
4. Review the original and updated line.
5. Apply the suggested patch only if the race name matches exactly.

## Recommended Commands

From a verified URL:

```bash
python3 .github/skills/eqtiming-regurl-updater/scripts/suggest-regurl-update.py \
  --race-name "Sørlandet Petit Prix" \
  --url "https://live.eqtiming.com/83129#dashboard"
```

From an event ID:

```bash
python3 .github/skills/eqtiming-regurl-updater/scripts/suggest-regurl-update.py \
  --race-name "Sørlandet Petit Prix" \
  --event-id 83129
```

For a results URL instead of signup:

```bash
python3 .github/skills/eqtiming-regurl-updater/scripts/suggest-regurl-update.py \
  --race-name "Sørlandet Petit Prix" \
  --event-id 83129 \
  --mode results
```

## Rules

- Update only one race row at a time
- Match the `name` field exactly
- If the race is not found exactly once, stop and inspect manually
- Prefer `#dashboard` for signup links
- Use the base live URL without `#dashboard` only when the goal is results

## Output Format

The script should be used to produce:

- matched line number
- original line
- updated line
- ready-to-apply `apply_patch` block

If you still need to identify the correct EQ Timing candidate first, use `eqtiming-regurl-workflow` instead.

