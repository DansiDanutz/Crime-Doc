# CLAUDE.md — Operating manual for this repo

You are running the **umbra. documentary production workflow**. The full creative
DNA is already captured in `dna/CHANNEL_DNA.md` — treat it as absorbed and locked.
Do **not** ask the user to upload PDFs, transcripts, or screenshots. Do not summarize
the DNA back at them.

## What this repo is
A factory for Fern/Hoog-style AI crime/intelligence documentaries. Scripts use a
deadpan clinical register; visuals use the mannequin-world color code
(white=civilian, red=protagonist, black=institution). Production runs through the
connected generation MCP.

## The workflow (state machine)
Follow `docs/WORKFLOW.md`. States: 0 DNA → 1 Branding → 2 Idea → 3 Script →
4 Characters → 5 Scenes → 6 Thumbnails → 7 Export. One state at a time; don't skip.

When invoked fresh and conversationally, STATE 0's only message is exactly:
> DNA absorbed. Ready when you are — type "go" to start with channel branding.

When the user instead asks you to *build/scaffold/plan* (as a developer), produce the
artifacts as files under `channels/<name>/…` using the templates, and keep them
conformant to the DNA.

## Hard rules (from DNA)
- **Never** write: "In this video…", "Today we're going to…", "Have you ever wondered…",
  clickbait, emotional editorializing, sponsor copy, or clean resolved endings.
- Cold open = exact date + location + one physical action, then ONE anchor line.
- Pacing = 2.5 words/sec → `words = minutes × 150`.
- Endings must be unresolved/unsettling; last line ≤12 words landing on a noun/name/date.
- Mannequin color code is inviolable. No facial features. No gore. No horror lighting.

## Production engine (generation MCP)
See `docs/PRODUCTION_PIPELINE.md` for exact tool calls. Summary:
- **Character refs** → `generate_image` (`nano_banana_pro`), white void → save each as a
  Reference Element (`show_reference_elements` action=create) for consistency.
- **Scene keyframe** → `generate_image` referencing the character elements.
- **Scene motion** → `generate_video` (`seedance_2_0`, `start_image` = keyframe job id).
- **Thumbnails** → `generate_image` (`nano_banana_pro`, best text rendering).
- Always preflight cost with `get_cost: true` before large batches; confirm with the user
  before spending credits on a full episode.

## Editing / changing
- Change the channel's look/voice → edit `channels/<name>/SERIES_BIBLE.md` (it overrides
  nothing in the DNA, only specializes it).
- Add an episode → `tools/new-episode.sh <channel> <slug>`.
- The single machine-readable artifact production reads is `production/shotlist.json`.

## Git
- Develop on branch `claude/beautiful-heisenberg-FV9ho`. Commit with clear messages.
- Push with `git push -u origin <branch>`; open a **draft** PR after pushing.
