#!/usr/bin/env bash
# archive-to-drive.sh — archive this project to Google Drive, following the Mac Studio Recovery
# Archive plan ("START HERE — Mac Studio Archive Index"), then (only after verification) free space.
#
#   tools/archive-to-drive.sh            archive + verify (nothing local is deleted)
#   tools/archive-to-drive.sh --free     delete the local generated media, ONLY if the archive of
#                                        the current state was verified by a previous run
#
# What goes to Drive, under "01 — Project Archives/<YYYY-MM-DD>__Crime-Doc__<commit>/":
#   source.tar.gz     tracked files of HEAD (git archive)
#   history.bundle    the whole git history, every local branch and fetched remote branch
#   media.tar.gz      what git does not hold: rendered clips, the render ledger, the final video,
#                     voiceover and soundtrack takes, the channel outro sting (never .env.local,
#                     .venv or other credentials)
#   MANIFEST.txt      paths, sizes, SHA-256s, included/excluded, restore steps
# and a copy of the manifest goes to "Manifests and Restore Instructions" as <name>.manifest.txt.
#
# Verification (all must pass before --free will delete anything):
#   rclone check (sizes + MD5) of the upload; a fresh download of every file; SHA-256 match;
#   test extraction of both tarballs into empty folders with file counts matching; the git bundle
#   verifies and clones to the same HEAD.
#
# Needs rclone with a Google Drive remote (auto-detected; or set RCLONE_REMOTE=name:).
set -euo pipefail

PROJECT_ARCHIVES_ID="1-R3TgMpVOTjpxL73h1uzi0zl4JeSZ9mX"   # 01 — Project Archives
MANIFESTS_ID="17ef8MgIcxCJegXDrm8ZeIw4NvxwrZ2AB"          # Manifests and Restore Instructions
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="${ARCHIVE_WORK:-$HOME/.cache/crime-doc-archive}"
say() { printf '\033[1m%s\033[0m\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 2; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

# The generated media that git does not hold (relative to the repo).
media_paths() {
  (cd "$REPO" && for p in channels/*/episodes/*/production/renders.json \
                          channels/*/episodes/*/production/clips \
                          channels/*/episodes/*/production/output \
                          channels/*/episodes/*/production/vo \
                          channels/*/episodes/*/production/sound \
                          channels/*/sound; do
     [ -e "$p" ] && printf '%s\n' "$p"
   done) || true
}

state_key() {  # what the verified archive covers: commit + the media file list and sizes
  { git -C "$REPO" rev-parse HEAD
    (cd "$REPO" && media_paths | while read -r p; do find "$p" -type f ! -name '*.lock' ! -name '.*' -print0 \
       | xargs -0 ls -ln 2>/dev/null | awk '{print $5, $9}'; done | sort)
  } | shasum -a 256 | awk '{print $1}'
}

if [ "${1:-}" = "--free" ]; then
  marker="$WORK/VERIFIED"
  [ -f "$marker" ] || die "no verified archive yet; run tools/archive-to-drive.sh first"
  [ "$(sed -n 's/^state=//p' "$marker")" = "$(state_key)" ] \
    || die "the project changed since the verified archive; run tools/archive-to-drive.sh again"
  say "the archive $(sed -n 's/^name=//p' "$marker") was verified; freeing space…"
  before=$(du -sk "$REPO" | awk '{print $1}')
  (cd "$REPO" && media_paths | while read -r p; do
     case "$p" in */renders.json) continue ;; esac   # the tiny ledger stays, so the tools still know the clips
     echo "  removing $p"; rm -rf -- "$p"; done)
  [ -d "$REPO/.venv" ] && { echo "  removing .venv (recreate: python3 -m venv .venv && pip install -r requirements.txt)"; rm -rf -- "$REPO/.venv"; }
  rm -rf -- "$WORK/stage" "$WORK/verify"
  after=$(du -sk "$REPO" | awk '{print $1}')
  say "freed $(( (before - after) / 1024 )) MB in $REPO (source, git history and .env.local kept)."
  exit 0
fi

command -v rclone >/dev/null || die "rclone is not installed (brew install rclone)"
REMOTE="${RCLONE_REMOTE:-$(rclone listremotes --long | awk '$2=="drive"{print $1; exit}')}"
[ -n "$REMOTE" ] || die "no Google Drive remote in rclone; set RCLONE_REMOTE=name:"
case "$REMOTE" in *:) ;; *) REMOTE="$REMOTE:" ;; esac

cd "$REPO"
git fetch -q origin 2>/dev/null || echo "  (offline: archiving the branches already fetched)"
COMMIT=$(git rev-parse --short=12 HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
NAME="$(date +%Y-%m-%d)__Crime-Doc__${COMMIT}"
STAGE="$WORK/stage/$NAME"
VERIFY="$WORK/verify/$NAME"
rm -rf -- "$STAGE" "$VERIFY"; mkdir -p "$STAGE" "$VERIFY"
DIRTY=$(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')

say "1/5 packing $NAME…"
git archive --format=tar.gz -o "$STAGE/source.tar.gz" HEAD
git bundle create -q "$STAGE/history.bundle" --all
MEDIA=$(media_paths)
if [ -n "$MEDIA" ]; then
  # shellcheck disable=SC2086
  (cd "$REPO" && tar -czf "$STAGE/media.tar.gz" --exclude='*.lock' --exclude='.*.part' --exclude='.env*' $MEDIA)
fi
SOURCE_FILES=$(git ls-files | wc -l | tr -d ' ')
MEDIA_FILES=0
[ -f "$STAGE/media.tar.gz" ] && MEDIA_FILES=$(tar -tzf "$STAGE/media.tar.gz" | grep -cv '/$' || true)

{
  echo "# Manifest: $NAME"
  echo "Project: Crime-Doc (umbra. documentary factory; EP03 'Ghost Characters' final cut 5:12) — ON HOLD"
  echo "Original: $REPO"
  echo "Archived: $(date -u +%Y-%m-%dT%H:%M:%SZ) from $(hostname -s)"
  echo "Git remote: $(git remote get-url origin 2>/dev/null || echo none)"
  echo "HEAD: $(git rev-parse HEAD) on branch $BRANCH ($DIRTY uncommitted tracked change(s) NOT in source.tar.gz)"
  echo "Branches in history.bundle:"; git for-each-ref --format='  %(refname:short) %(objectname:short)' refs/heads refs/remotes
  echo
  echo "## Files"
  for f in source.tar.gz history.bundle media.tar.gz; do
    [ -f "$STAGE/$f" ] && echo "$f  $(wc -c < "$STAGE/$f" | tr -d ' ') bytes  sha256 $(sha "$STAGE/$f")"
  done
  echo
  echo "source.tar.gz: $SOURCE_FILES tracked files of HEAD (git archive; modes kept, not timestamps)."
  echo "history.bundle: full git history, all local branches and fetched remote branches."
  echo "media.tar.gz: $MEDIA_FILES files — generated media git does not hold:"
  printf '%s\n' "$MEDIA" | sed 's/^/  /'
  echo "Excluded: .env.local and all credentials, .venv, *.lock, temp/.part files, git-ignored caches."
  echo "The EP03 thumbnail is Higgsfield job 4084030d-de68-4db0-911a-3931b57f3e2d (re-download from Higgsfield)."
  echo
  echo "## Restore"
  echo "1. Download this folder; verify: shasum -a 256 *.tar.gz *.bundle (compare with the list above)."
  echo "2. Code + history: git clone history.bundle Crime-Doc && cd Crime-Doc && git remote set-url origin https://github.com/DansiDanutz/Crime-Doc.git"
  echo "   (or simply clone from GitHub; the bundle is the offline copy)."
  echo "3. Media: tar -xzf media.tar.gz -C Crime-Doc   (puts clips, video, takes back in place)."
  echo "4. Recreate the environment: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt;"
  echo "   re-add .env.local (HF_KEY, ELEVENLABS_API_KEY) from your own key store."
} > "$STAGE/MANIFEST.txt"

say "2/5 uploading to Drive (01 — Project Archives/$NAME)…"
rclone copy "$STAGE" "${REMOTE}${NAME}" --drive-root-folder-id "$PROJECT_ARCHIVES_ID"

say "3/5 checking the upload (sizes + MD5)…"
rclone check "$STAGE" "${REMOTE}${NAME}" --drive-root-folder-id "$PROJECT_ARCHIVES_ID" --one-way

say "4/5 downloading it again and testing it…"
rclone copy "${REMOTE}${NAME}" "$VERIFY" --drive-root-folder-id "$PROJECT_ARCHIVES_ID"
for f in "$STAGE"/*; do
  b=$(basename "$f")
  [ "$(sha "$f")" = "$(sha "$VERIFY/$b")" ] || die "$b: the downloaded copy does not match (SHA-256)"
done
mkdir -p "$VERIFY/x-source" "$VERIFY/x-media"
tar -xzf "$VERIFY/source.tar.gz" -C "$VERIFY/x-source"
[ "$(find "$VERIFY/x-source" -type f | wc -l | tr -d ' ')" = "$SOURCE_FILES" ] || die "source.tar.gz extracts to a different file count"
if [ -f "$VERIFY/media.tar.gz" ]; then
  tar -xzf "$VERIFY/media.tar.gz" -C "$VERIFY/x-media"
  [ "$(find "$VERIFY/x-media" -type f | wc -l | tr -d ' ')" = "$MEDIA_FILES" ] || die "media.tar.gz extracts to a different file count"
fi
git bundle verify -q "$VERIFY/history.bundle" >/dev/null 2>&1 || die "history.bundle does not verify"
git clone -q "$VERIFY/history.bundle" "$VERIFY/x-clone" 2>/dev/null || true
[ "$(git -C "$VERIFY/x-clone" rev-parse "$(git rev-parse HEAD)^{commit}" 2>/dev/null)" = "$(git rev-parse HEAD)" ] \
  || die "the bundle does not contain HEAD"

say "5/5 filing the manifest in Manifests and Restore Instructions…"
cp "$STAGE/MANIFEST.txt" "$WORK/$NAME.manifest.txt"
rclone copy "$WORK/$NAME.manifest.txt" "$REMOTE" --drive-root-folder-id "$MANIFESTS_ID"

{ echo "name=$NAME"; echo "state=$(state_key)"; echo "verified=$(date -u +%Y-%m-%dT%H:%M:%SZ)"; } > "$WORK/VERIFIED"
rm -rf -- "$VERIFY"
say "archived and verified: $NAME"
sed -n '/^## Files/,/^$/p' "$STAGE/MANIFEST.txt"
echo "Free the local media now with:  tools/archive-to-drive.sh --free"
