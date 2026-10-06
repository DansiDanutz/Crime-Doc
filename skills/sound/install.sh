#!/usr/bin/env bash
# install.sh — install (or update) ACE-Step 1.5 and the `sound` Claude Code skill for this user.
#
#   ACE-Step 1.5  -> ~/.local/share/ace-step/ACE-Step-1.5   (override with ACE_STEP_HOME)
#   the skill     -> ~/.claude/skills/sound                 (available in every project)
#
# Re-running updates both. Nothing here needs sudo. The model weights (several GB) download the
# first time ACE-Step starts, not here.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACE_HOME="${ACE_STEP_HOME:-$HOME/.local/share/ace-step/ACE-Step-1.5}"
ACE_REPO="https://github.com/ace-step/ACE-Step-1.5.git"
SKILL_DIR="$HOME/.claude/skills/sound"

say() { printf '\033[1m%s\033[0m\n' "$*"; }

command -v git >/dev/null || { echo "error: git is required (xcode-select --install)"; exit 2; }
if ! command -v uv >/dev/null; then
  say "installing uv (Python package manager from astral.sh)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$ACE_HOME/.git" ]; then
  say "updating ACE-Step 1.5 in $ACE_HOME…"
  git -C "$ACE_HOME" pull --ff-only
else
  say "cloning ACE-Step 1.5 into $ACE_HOME…"
  mkdir -p "$(dirname "$ACE_HOME")"
  git clone --depth 1 "$ACE_REPO" "$ACE_HOME"
fi
say "installing ACE-Step's dependencies (uv sync)…"
(cd "$ACE_HOME" && uv sync)

say "installing the sound skill into $SKILL_DIR…"
mkdir -p "$SKILL_DIR/scripts"
cp "$SRC/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SRC/scripts/sound.py" "$SKILL_DIR/scripts/sound.py"
chmod +x "$SKILL_DIR/scripts/sound.py"

say "done."
echo "  ACE-Step commit: $(git -C "$ACE_HOME" rev-parse --short HEAD)"
echo "  check:  python3 $SKILL_DIR/scripts/sound.py status"
echo "  first music run starts the ACE-Step server and downloads its models (several GB)."
