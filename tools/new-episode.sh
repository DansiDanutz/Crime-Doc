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

dest="$chan_dir/episodes/$slug"
if [[ -e "$dest" ]]; then
  echo "error: $dest already exists" >&2
  exit 1
fi

cp -r "$TEMPLATE" "$dest"
today="$(date +%Y-%m-%d)"

# fill obvious placeholders in the copied files. slug/channel are already validated
# above; the title is arbitrary user text, so escape it for the sed replacement side
# (backslash, the '/' delimiter, and '&') before use.
for f in "$dest/episode.yaml" "$dest/production/shotlist.json"; do
  [[ -f "$f" ]] || continue
  tmp="$(mktemp)"
  sed -e "s/EPISODE_SLUG/$slug/g" -e "s/CHANNEL_NAME/$channel/g" "$f" > "$tmp" && mv "$tmp" "$f"
done
if [[ -n "$title" && -f "$dest/episode.yaml" ]]; then
  esc_title="$(printf '%s' "$title" | sed -e 's/[\\/&]/\\&/g')"
  tmp="$(mktemp)"
  sed -e "s/^title: .*/title: \"$esc_title\"/" -e "s/^created: .*/created: \"$today\"/" \
      "$dest/episode.yaml" > "$tmp" && mv "$tmp" "$dest/episode.yaml"
fi

echo "created $dest"
echo "next: fill 01-idea.md -> 02-script.md -> 03-characters.md -> 04-scenes.md -> 05-thumbnails.md"
echo "rules: dna/CHANNEL_DNA.md   pipeline: docs/PRODUCTION_PIPELINE.md"
