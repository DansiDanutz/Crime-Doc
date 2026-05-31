# umbra. — AI Documentary Production System

A production environment for making Fern/Hoog-style "armchair documentary" videos:
deadpan true-crime / intelligence / systems-gone-wrong narration over a **mannequin-world**
visual language (glossy-white / matte-red / matte-black figures), rendered and animated
through the connected image/video generation MCP.

This repo is built so a series is **easy to work, easy to generate, easy to edit, and
easy to produce**. The creative rules live in one locked file; everything else is a
template you clone per episode.

---

## How it's organized

```
dna/CHANNEL_DNA.md      ← LOCKED creative source of truth (style, pacing, visual code)
docs/                   ← how-to references (workflow, writing, visuals, prompts, pipeline)
templates/episode/      ← blank episode scaffold — clone this for every new video
channels/<name>/        ← a channel: branding + shared cast + episodes
tools/new-episode.sh    ← scaffolds a new episode from the template
CLAUDE.md               ← operating manual so any AI session can run the workflow
```

The workflow is a **state machine** (STATE 0 → 7). See `docs/WORKFLOW.md`.

| State | Output | Lives in |
|-------|--------|----------|
| 1 Branding | names, descriptions, logo + banner prompts | `channels/<name>/branding/` |
| 2 Idea | chosen documentary concept | `episodes/<ep>/01-idea.md` |
| 3 Script | continuous narration, mandatory cliffhanger | `episodes/<ep>/02-script.md` |
| 4 Characters | white-void character reference prompts | `episodes/<ep>/03-characters.md` |
| 5 Scenes | chapters → scenes (image + video prompts) | `episodes/<ep>/04-scenes.md` |
| 6 Thumbnails | 5 thumbnail variants | `episodes/<ep>/05-thumbnails.md` |
| — Production | machine-readable shot manifest | `episodes/<ep>/production/shotlist.json` |

## Quick start

```bash
# 1. Read the rules
open dna/CHANNEL_DNA.md  docs/WORKFLOW.md

# 2. Scaffold a new episode in the umbra. channel
tools/new-episode.sh umbra "the-laptop-in-bangkok"

# 3. Fill the markdown files state-by-state (script → characters → scenes → thumbnails)
# 4. Mirror scenes into production/shotlist.json
# 5. Produce: feed shotlist.json to the generation MCP (see docs/PRODUCTION_PIPELINE.md)
```

## Reference implementation

`channels/umbra/episodes/ep01-the-man-who-said-no/` is a **complete worked example**
(Stanislav Petrov / Serpukhov-15, 1983) — read it as the gold-standard template for
tone, structure, and prompt formatting.

## The one rule

Everything obeys `dna/CHANNEL_DNA.md`. No clean endings, no clickbait, no sponsor copy,
no breaking the mannequin color code. When in doubt, the DNA wins.
