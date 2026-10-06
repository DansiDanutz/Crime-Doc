#!/usr/bin/env bash
# install.sh — install (or update) ACE-Step 1.5 and the `sound` Claude Code skill for this user.
#
#   ACE-Step 1.5  -> ~/.local/share/ace-step/ACE-Step-1.5   (override with ACE_STEP_HOME)
#   the skill     -> ~/.claude/skills/sound                 (available in every project)
#
# Supply chain: ACE-Step is checked out at a pinned, reviewed commit (ACE_STEP_COMMIT) and the
# checkout is verified to be exactly that commit before anything in it runs; its dependencies are
# installed only from its own lockfile (`uv sync --frozen`). uv itself must come from a package
# manager (Homebrew) — this script never pipes a downloaded installer into a shell. To move to a
# newer ACE-Step, review it and change ACE_STEP_COMMIT here (or pass it in the environment).
# Nothing here needs sudo. The model weights download the first time ACE-Step starts.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACE_HOME="${ACE_STEP_HOME:-$HOME/.local/share/ace-step/ACE-Step-1.5}"
ACE_REPO="https://github.com/ace-step/ACE-Step-1.5.git"
ACE_STEP_COMMIT="${ACE_STEP_COMMIT:-ca1e85fe9430179831e6bc6be790c332190a3866}"  # main, 2026-10-06
SKILL_DIR="$HOME/.claude/skills/sound"

say() { printf '\033[1m%s\033[0m\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 2; }

[[ "$ACE_STEP_COMMIT" =~ ^[0-9a-f]{40}$ ]] || die "ACE_STEP_COMMIT must be a full 40-character commit hash"
command -v git >/dev/null || die "git is required (xcode-select --install)"
command -v uv >/dev/null || die "uv is required: install it with Homebrew (brew install uv), then run this again"

if [ -d "$ACE_HOME/.git" ] && [ -n "$(git -C "$ACE_HOME" status --porcelain --untracked-files=no)" ]; then
  die "$ACE_HOME has local changes; commit or stash them first (nothing was changed)"
fi
if [ ! -d "$ACE_HOME/.git" ]; then
  say "cloning ACE-Step 1.5 into $ACE_HOME…"
  mkdir -p "$(dirname "$ACE_HOME")"
  git clone --quiet "$ACE_REPO" "$ACE_HOME"   # writes files only; nothing in it runs before the pin is verified
fi
say "checking out the pinned ACE-Step commit ${ACE_STEP_COMMIT:0:12}…"
git -C "$ACE_HOME" fetch --quiet origin "$ACE_STEP_COMMIT" 2>/dev/null || git -C "$ACE_HOME" fetch --quiet origin
git -C "$ACE_HOME" -c advice.detachedHead=false checkout --quiet "$ACE_STEP_COMMIT"
[ "$(git -C "$ACE_HOME" rev-parse HEAD)" = "$ACE_STEP_COMMIT" ] || die "the ACE-Step checkout is not the pinned commit"
[ -z "$(git -C "$ACE_HOME" status --porcelain --untracked-files=no)" ] || die "the ACE-Step checkout has local changes"
[ -f "$ACE_HOME/uv.lock" ] || die "the pinned ACE-Step commit has no uv.lock"

say "installing ACE-Step's locked dependencies (uv sync --frozen)…"
(cd "$ACE_HOME" && uv sync --frozen)

say "installing the sound skill into $SKILL_DIR…"
mkdir -p "$SKILL_DIR/scripts"
cp "$SRC/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SRC/scripts/sound.py" "$SKILL_DIR/scripts/sound.py"
chmod +x "$SKILL_DIR/scripts/sound.py"

say "done."
echo "  ACE-Step commit: $ACE_STEP_COMMIT (pinned)"
echo "  check:  python3 $SKILL_DIR/scripts/sound.py status"
echo "  first music run starts the ACE-Step server and downloads its models (several GB)."
