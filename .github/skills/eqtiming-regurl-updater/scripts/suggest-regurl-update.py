#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys


def build_url(event_id: str | None, url: str | None, mode: str) -> str:
    if url:
      return url
    base = f"https://live.eqtiming.com/{event_id}"
    return base if mode == "results" else f"{base}#dashboard"


def update_line(line: str, url: str) -> str:
    if 'regUrl: "' in line:
        return re.sub(r'regUrl: "[^"]+"', f'regUrl: "{url}"', line)
    return re.sub(r'\s*\},\s*$', f', regUrl: "{url}" }},', line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--race-name', required=True)
    parser.add_argument('--event-id')
    parser.add_argument('--url')
    parser.add_argument('--mode', choices=['signup', 'results'], default='signup')
    parser.add_argument('--file', default='data/ritt.js')
    args = parser.parse_args()

    if not args.event_id and not args.url:
        print('Provide either --event-id or --url.', file=sys.stderr)
        return 1

    target_url = build_url(args.event_id, args.url, args.mode)
    path = pathlib.Path(args.file)
    lines = path.read_text(encoding='utf-8').splitlines()
    needle = f'{{ name: "{args.race_name}",' 

    matches = [(index + 1, line) for index, line in enumerate(lines) if needle in line]

    if not matches:
        print(f'No exact race match found for {args.race_name!r} in {args.file}.', file=sys.stderr)
        return 1

    if len(matches) > 1:
        print(f'Multiple exact race matches found for {args.race_name!r} in {args.file}.', file=sys.stderr)
        for line_number, line in matches:
            print(f'{line_number}: {line}', file=sys.stderr)
        return 1

    line_number, original_line = matches[0]
    updated_line = update_line(original_line, target_url)

    print(f'Matched line: {line_number}')
    print('Original:')
    print(original_line)
    print('Updated:')
    print(updated_line)
    print()
    print('Patch:')
    print('*** Begin Patch')
    print(f'*** Update File: {path.resolve()}')
    print(original_line)
    print(f'-{original_line}')
    print(f'+{updated_line}')
    print('*** End Patch')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())