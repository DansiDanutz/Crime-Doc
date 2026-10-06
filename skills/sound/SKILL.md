---
name: sound
description: Generate music and sound effects for any project. Music is made locally and free with ACE-Step 1.5 (10 s to 10 min, instrumental or with lyrics), with ElevenLabs as a fallback; sound effects are made with ElevenLabs. Use whenever a task needs a soundtrack, a music bed, a jingle or sting, a song, background ambience, or sound effects (UI sounds, foley, impacts, ambience) for a video, game, app, podcast or presentation.
---

# sound — music and sound effects

One script does everything: `~/.claude/skills/sound/scripts/sound.py` (Python 3, standard library
only, runs from any project).

| Need | Engine | Length |
|---|---|---|
| Music, instrumental or with lyrics | **ACE-Step 1.5**, local on this Mac (free, MIT licence) | 10–600 s |
| Music when ACE-Step is not installed | ElevenLabs Music API (uses credits) | 10–300 s |
| Sound effects, foley, ambience | ElevenLabs sound effects (uses credits) | 0.5–22 s |

## Commands
```bash
S=~/.claude/skills/sound/scripts/sound.py
python3 $S status                      # is ACE-Step installed/running, is there an ElevenLabs key
python3 $S music --prompt "..." --seconds 60 --out bed.mp3            # instrumental
python3 $S music --prompt "..." --lyrics lyrics.txt --seconds 120 --out song.mp3
python3 $S music --prompt "..." --seconds 30 --out x.mp3 --seed 42  # reproducible
python3 $S sfx --prompt "..." --seconds 2 --out hit.mp3
python3 $S server start | stop         # the ACE-Step API also starts by itself when needed
```
Each command prints one JSON line (`out`, `engine`, and for ACE-Step the seed and model). Errors
come back as a single `error: …` line with exit code 2. Show that line to the user and don't
retry blindly.

## Writing good prompts
- **Music:** give the genre and mood, the instruments, the tempo or energy, and what to avoid. For
  example: *"dark minimal ambient underscore, low analog synth drone, one cold pulse every few
  seconds, slow, no drums, no vocals"*.
  - For an underscore under narration, say **no vocals, no melody** and keep it sparse.
  - For a sting or sign-off, ask for a short swell that settles on one held note.
- **Lyrics** (ACE-Step only): plain text with section tags on their own lines, such as `[verse]`,
  `[chorus]`, `[bridge]` and `[outro]`. Without `--lyrics`, the piece is instrumental.
- **Sound effects:** describe one concrete sound and its space, for example *"heavy rubber stamp
  thud on paper on a wooden desk"* or *"old CRT television switching off with a fading whine"*. Ask
  for one sound per call and keep it short.

## Rules
- **Cost.** ACE-Step is free, so prefer it for music. ElevenLabs costs credits: tell the user before
  a large batch, and check `status` first.
- **Keys.** Never print or log keys. The ElevenLabs key is read from `ELEVENLABS_API_KEY`, a
  `.env.local` in the project, or `~/.config/sound-skill/env`.
- **First run.** The first ACE-Step run downloads its models (several GB) and can take minutes.
  Its log is in `~/.cache/sound-skill/ace-step-api.log`.
- **Mixing.** Put generated files in the project's own (git-ignored) media folder. Mix them with
  ffmpeg: duck music under speech with `sidechaincompress`, and normalise with
  `loudnorm=I=-14:TP=-1.5` for YouTube.

## Install or update (on the Mac)
Run `install.sh` from this skill's source folder (`skills/sound/` in the Crime-Doc repo). It
installs `uv` if it's missing, clones ACE-Step 1.5 into `~/.local/share/ace-step/ACE-Step-1.5`,
runs `uv sync`, and copies this skill to `~/.claude/skills/sound`. Running it again updates
ACE-Step and the skill.
