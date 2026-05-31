# WORKFLOW — the state machine

Linear, one state at a time, no skipping. Each state writes one file in the episode
folder (except STATE 1, which writes the channel branding once).

```
STATE 0  DNA init        (already loaded — never re-ingest)
STATE 1  Branding        → channels/<name>/branding/
STATE 2  Idea            → episodes/<ep>/01-idea.md
STATE 3  Script          → episodes/<ep>/02-script.md
STATE 4  Characters      → episodes/<ep>/03-characters.md
STATE 5  Scenes          → episodes/<ep>/04-scenes.md  (+ production/shotlist.json)
STATE 6  Thumbnails      → episodes/<ep>/05-thumbnails.md
STATE 7  Export          → optional Word/PDF bundle
```

---

### STATE 0 — DNA init
DNA is loaded from `dna/CHANNEL_DNA.md`. In a conversational run, the only message is:
> DNA absorbed. Ready when you are — type "go" to start with channel branding.

### STATE 1 — Branding
On "go", produce **10 channel names**, **2 descriptions**, **1 logo prompt**,
**1 banner prompt** (DNA §1–3). Save to `channels/<name>/branding/branding.md`.
End with: *Type "next" when ready for video ideas.*

### STATE 2 — Ideas
**10 documentary ideas** in the DNA topic territory (DNA §10). The chosen one is
copied into the episode's `01-idea.md`.
End with: *Pick a number, or describe a different topic.*

### STATE 3 — Script
Ask: *"How long should the script be? Anywhere from 1 to 10 minutes."*
Then write **continuous narration only** — no chapter labels, no camera directions, no
production notes, no sponsor copy. Mandatory cliffhanger ending (DNA §4).
`word_count = minutes × 150`. Save to `02-script.md`.
End with: *Type "next" for character creation.*

### STATE 4 — Characters
**MANDATORY ensemble — every episode casts all four role categories** (see
`channels/<name>/cast/CAST.md`): a MAIN SUBJECT (matte red, exactly one), one or more
SECONDARY SUBJECTS (white + one photoreal signifier), POLICE (matte black), and SPECIAL
POLICE / the solvers (black + photoreal tactical gear). One reference prompt per figure.
**Pure white-void background only.** No environments, no facial features. Save to
`03-characters.md`. End with the locked STATE-4 closing line (see template).

### STATE 5 — Visual flow + scenes
On "next", **immediately** (do not ask permission):
1. **Chapter the script** — 14–15 s chapters, mixed anchor + cutaway rhythm, STYLE
   ANCHOR per chapter, chapter handoffs. Never exceed 15 s/chapter.
2. **Split each chapter into scenes** (2–4 s each → ~4–7 scenes/chapter). For each scene
   output, in order:
   1. **CHARACTERS IN SCENE** — by exact STATE-4 names, or "Civilians / crowd only".
   2. **IMAGE PROMPT** — still keyframe, DNA §7/§8 template, ends with aspect ratio.
   3. **VIDEO PROMPT** — how the keyframe animates (camera, subject motion, beat timing).
   Keep CHARACTER LOCK + STYLE ANCHOR consistent across all scenes. Per chapter, keep an
   SFX / Ambient / Music split.
Save prose to `04-scenes.md`; mirror into `production/shotlist.json`.
End with: *Type "next" for thumbnail prompts.*

### STATE 6 — Thumbnails
**5 variants** (DNA §6). Each = concept, text overlay, emotion trigger, composition note,
full image prompt. Save to `05-thumbnails.md`.
End with the locked STATE-6 closing line (see template).

### STATE 7 — Export
Optional: bundle all states into a clean document. Run:
```bash
tools/export-episode.py <channel> <episode-slug>
```
It writes `export/<slug>.md` and a standalone printable `export/<slug>.html` (cover sheet from
`episode.yaml` + production summary from `shotlist.json`, then states 01–05). Open the HTML in a
browser and Print → Save as PDF for a Word/PDF-style bundle.
