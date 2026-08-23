#!/usr/bin/env bash
set -euo pipefail

race_name=""
query=""
date_from=""
date_to=""
mode="signup"
take="20"
pick="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --race-name)
      race_name="$2"
      shift 2
      ;;
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
    --mode)
      mode="$2"
      shift 2
      ;;
    --take)
      take="$2"
      shift 2
      ;;
    --pick)
      pick="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$race_name" || -z "$query" || -z "$date_from" || -z "$date_to" ]]; then
  echo "Usage: $0 --race-name \"Race name\" --query \"Search text\" --from YYYY-MM-DD --to YYYY-MM-DD [--mode signup|results] [--take 20] [--pick 1]" >&2
  exit 1
fi

root=".github/skills"
finder="$root/eqtiming-link-finder/scripts/find-eqtiming.sh"
updater="$root/eqtiming-regurl-updater/scripts/suggest-regurl-update.py"

candidates="$($finder --query "$query" --from "$date_from" --to "$date_to" --take "$take" --mode "$mode")"

echo "Candidates:"
echo "$candidates"

chosen_line="$(printf '%s\n' "$candidates" | awk -v pick="$pick" 'NR==pick { print; exit }')"
if [[ -z "$chosen_line" ]]; then
  echo "No candidate found at pick index $pick." >&2
  exit 1
fi

event_id="$(printf '%s\n' "$chosen_line" | cut -f1)"
chosen_url="$(printf '%s\n' "$chosen_line" | awk -F '\t' '{ print $NF }')"

echo
echo "Chosen candidate:"
echo "$chosen_line"
echo
echo "Reason: selected candidate #$pick from the filtered EQ Timing result set; verify organizer, city, date, and discipline before applying."
echo
python3 "$updater" --race-name "$race_name" --event-id "$event_id" --mode "$mode"