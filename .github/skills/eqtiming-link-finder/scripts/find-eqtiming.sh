#!/usr/bin/env bash
set -euo pipefail

query=""
date_from=""
date_to=""
take="20"
mode="signup"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)
      query="$2"
      shift 2
      ;;
    --from)
      date_from="$2"
      shift 2
      ;;
    --to)
      date_to="$2"
      shift 2
      ;;
    --take)
      take="$2"
      shift 2
      ;;
    --mode)
      mode="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$query" || -z "$date_from" || -z "$date_to" ]]; then
  echo "Usage: $0 --query \"Race name\" --from YYYY-MM-DD --to YYYY-MM-DD [--take 20] [--mode signup|results]" >&2
  exit 1
fi

curl -L --silent --get 'https://events.eqtiming.com/api/Events' \
  --data-urlencode "query=$query" \
  --data "dateFrom=${date_from}T00:00:00" \
  --data "dateTo=${date_to}T23:59:59" \
  --data "take=$take" \
  --data 'dateSort=true' \
  --data 'desc=false' \
  --data 'onlyValidated=true' | python3 -c '
import json
import sys

mode = sys.argv[1]
data = json.load(sys.stdin)

def build_url(event_id: int) -> str:
    base = f"https://live.eqtiming.com/{event_id}"
    return base if mode == "results" else f"{base}#dashboard"

if not data:
    print("No EQ Timing matches found in the requested date window.")
    raise SystemExit(0)

for event in data:
    event_id = event.get("Id")
    name = event.get("Name", "")
    date = event.get("Date", "")[:10]
    organizer = ((event.get("Organizer") or {}).get("Name")) or ""
    city = ((event.get("City") or {}).get("Name")) or ""
    level = ((event.get("Sportlevel") or {}).get("Name")) or ""
    discipline = ((event.get("Dicipline") or {}).get("Name")) or ""
    print(f"{event_id}\t{date}\t{name}\t{organizer}\t{city}\t{level}\t{discipline}\t{build_url(event_id)}")
' "$mode"