#!/usr/bin/env bash
# new-episode.sh — scaffold a new episode from the template.
# Usage: tools/new-episode.sh <channel> <slug> ["Working Title"]
# Example: tools/new-episode.sh umbra the-laptop-in-bangkok "The Laptop in Bangkok"
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT/templates/episode"

channel="${1:-}"; slug="${2:-}"; title="${3:-}"
if [[ -z "$channel" || -z "$slug" ]]; then
  echo "usage: tools/new-episode.sh <channel> <slug> [\"Working Title\"]" >&2
  exit 1
fi

if [[ ! "$channel" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "error: channel must use lowercase kebab-case" >&2
  exit 1
fi

chan_dir="$ROOT/channels/$channel"
if [[ ! -d "$chan_dir" ]]; then
  echo "error: channel '$channel' not found at $chan_dir" >&2
  echo "create it first: channels/$channel/{branding,cast,episodes} + SERIES_BIBLE.md" >&2
  exit 1
fi

# auto-number the episode prefix (ep01, ep02, ...) if slug isn't already prefixed
if [[ "$slug" != ep[0-9]* ]]; then
  count=$(find "$chan_dir/episodes" -mindepth 1 -maxdepth 1 -type d -name 'ep[0-9]*' 2>/dev/null | wc -l | tr -d ' ')
  printf -v num 'ep%02d' "$((count + 1))"
  slug="${num}-${slug}"
fi

# reject anything that isn't a bounded epNN-kebab-case slug — prevents a stray
# '/', '..', or copy-pasted path from writing the template outside episodes/
if [[ ! "$slug" =~ ^ep[0-9]{2,}-[a-z0-9][a-z0-9-]*$ ]]; then
  echo "error: slug must be epNN-kebab-case (lowercase letters, digits, hyphens); got '$slug'" >&2
  exit 1
fi

python3 - "$title" <<'PY'
import sys

title = sys.argv[1]
if len(title) > 200:
    raise SystemExit("error: title must be 200 characters or fewer")
if title and title.splitlines() != [title]:
    raise SystemExit("error: title must be a single line")
PY

dest="$chan_dir/episodes/$slug"
if [[ -e "$dest" ]]; then
  echo "error: $dest already exists" >&2
  exit 1
fi

cp -r "$TEMPLATE" "$dest"
today="$(date +%Y-%m-%d)"

# Fill validated path placeholders first.
for f in "$dest/episode.yaml" "$dest/production/shotlist.json"; do
  [[ -f "$f" ]] || continue
  tmp="$(mktemp)"
  sed -e "s/EPISODE_SLUG/$slug/g" -e "s/CHANNEL_NAME/$channel/g" "$f" > "$tmp" && mv "$tmp" "$f"
done
if [[ -n "$title" && -f "$dest/episode.yaml" ]]; then
  python3 - "$dest/episode.yaml" "$title" "$today" <<'PY'
import json
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
content = path.read_text()
encoded_title = json.dumps(sys.argv[2], ensure_ascii=False)
encoded_created = json.dumps(sys.argv[3])
content = re.sub(r"^title:.*$", lambda _: f"title: {encoded_title}", content, flags=re.MULTILINE)
content = re.sub(r"^created:.*$", lambda _: f"created: {encoded_created}", content, flags=re.MULTILINE)
path.write_text(content)
PY
fi

echo "created $dest"
echo "next: fill 01-idea.md -> 02-script.md -> 03-characters.md -> 04-scenes.md -> 05-thumbnails.md"
echo "rules: dna/CHANNEL_DNA.md   pipeline: docs/PRODUCTION_PIPELINE.md"
