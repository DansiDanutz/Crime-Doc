# PRODUCTION_PIPELINE — turning prompts into rendered media

This maps the written prompts (STATE 4–6) onto the connected generation MCP so an episode
goes from `shotlist.json` to finished clips with minimal clicks.

> **Cost discipline:** a full episode is dozens of image + video jobs. Always preflight
> with `get_cost: true` and confirm with the user before batch-spending credits. Check the
> balance first (`show_plans_and_credits`).

## Model choices (defaults)
| Job | Tool | Model | Why |
|-----|------|-------|-----|
| Character ref (white void) | `generate_image` | `nano_banana_pro` | top quality, clean isolation |
| Save character for reuse | `show_reference_elements` (action=create) | — | one element per figure, multi-subject safe, works with Seedance 2.0 + Nano Banana Pro |
| Scene keyframe | `generate_image` | `nano_banana_pro` (or `seedream`) | renders the staged still |
| Scene motion | `generate_video` | `seedance_2_0` | reference-driven, strong identity lock, `start_image` keyframe |
| Thumbnail | `generate_image` | `nano_banana_pro` | best in-image text for the tag labels |

> Confirm exact model ids/params with `models_explore` (`action='get'`) before a run —
> ids and accepted `aspect_ratios` / `durations` can change.

## The pipeline (per episode)

### 1. Lock the cast (once)
For each character in `03-characters.md`:
1. `generate_image` → `nano_banana_pro`, the white-void ref prompt, `count: 4`.
2. Pick the best; create a Reference Element from it
   (`show_reference_elements` action=create) → record the returned **element id**.
3. Write that id into `shotlist.json` → `characters[].element_id`.

This is the **CHARACTER LOCK**: every later scene references the element so the figure
looks identical throughout.

### 2. Render scene keyframes
For each scene in `shotlist.json.chapters[].scenes[]` **except scenes with `reuse` set** (they
borrow an earlier clip; see *Reusing an earlier clip* below):
- `generate_image`, `model: nano_banana_pro`, `prompt: scene.image_prompt`,
  `medias: [{role:"reference", value:<element_id>}, …]` for each character in the scene,
  `aspect_ratio: "16:9"`.
- Record the image job id into `scene.image_job_id`.

### 3. Animate each scene
Again skip scenes with `reuse` set.
- `generate_video`, `model: seedance_2_0`,
  `medias: [{role:"start_image", value: scene.image_job_id}]`,
  `prompt: scene.video_prompt`, `duration: scene.duration_s`, `aspect_ratio:"16:9"`.
- Record the video job id into `scene.video_job_id`.

### Preview clips from the command line (optional)
`tools/render-scenes.py <channel> <slug> --scene <id>` renders a scene with the Higgsfield API
(Seedance 2.5 text-to-video, using the git-ignored `.env.local` key). These are **previews**:
the API endpoint takes a text prompt only, so they are not anchored to the cast elements or a
keyframe. They are recorded in `production/renders.json`, never in `image_job_id` /
`video_job_id`. A run of more than one scene needs `--yes`; `--dry-run` shows what would be sent.

### Reusing an earlier clip
A scene can borrow an earlier scene's clip instead of being rendered (a callback, or the same
diagram again). Add a line after its VIDEO PROMPT block in `04-scenes.md`:
`4. **REUSE:** ch02_s3 — why it fits`. `build-shotlist.py` records it as `scene.reuse` (it must
name an earlier scene that is not itself a reuse), `render-scenes.py` never renders that scene,
and the edit places the named clip there, trimmed to the scene's own duration. Rendered clips are
at least 4 s long (the model's minimum), so a reused clip covers any scene of up to 4 s even when
its own planned duration is shorter.

### 4. Thumbnails
- `generate_image`, `model: nano_banana_pro`, each prompt from `05-thumbnails.md`,
  `count: 4`, `aspect_ratio:"16:9"`.

### 5. Voiceover (ElevenLabs, voice Brian)
`tools/voiceover.py <channel> <slug>` reads `02-script.md` with the ElevenLabs voice **Brian**
(`--voice` / `--voice-id` to change it; `eleven_multilingual_v2`), using `ELEVENLABS_API_KEY` from
`.env.local`.
- **Chapter by chapter.** A script whose narration is marked `<!-- chNN -->` is recorded one take
  per chapter, each sent with the lines around it so the delivery stays continuous, and each laid
  0.35 s into its own chapter window. The track (`production/vo/<slug>-vo.mp3`) is exactly as long
  as the cut, and no line drifts off its pictures. A take slightly long for its window is tightened
  (≤8%, pitch kept); a longer one is reported, so its line can be shortened. A script without
  markers is read in one take.
- **Pronunciation.** Names the voice misreads are respelled for the read only in
  `production/pronunciation.json` (EP03: Wau → "Vow", "USD 70000", Btx).
- **Cost control.** Takes live in `production/vo/takes/` with a `vo.json` receipt. A re-run records
  only chapters whose words or neighbours changed; `--force` re-records all of them, and
  `--dry-run` shows the per-chapter plan without a key.

### 5b. Music and sound effects (ElevenLabs)
`production/sound.json` is the episode's soundtrack plan:
- **`music`:** one bed per section of chapters (`from`/`to`). Each bed is written from the "Music" notes in `04-scenes.md`. A chapter can be left without music on purpose; EP03's ch13 is silent ("music drops out").
- **`sfx`:** one-shot effects at a time into a chapter, written from the "SFX" and "Ambient" notes.

`tools/soundtrack.py <channel> <slug>` records every cue with ElevenLabs, using the same `ELEVENLABS_API_KEY`:
- **Music** comes from the Music API. If the account's plan has no Music API, each section falls back to a seamless ambient loop from the sound-effects API, looped to length.
- **Effects** come from the sound-effects API.
- **The outro sting** (`music` in `channels/<name>/outro.json`) is recorded once per channel in `channels/<name>/sound/` and reused, so every ending sounds the same.

Recordings are content-addressed (kind, prompt and length) and kept only after they decode, so a re-run records only what changed. Changing a level or a time rebuilds the stems without spending anything. The output is two stems as long as the cut: `production/sound/<slug>-music.mp3` and `<slug>-sfx.mp3` (git-ignored).

### 6. Cards
`production/cards.json` lists the on-screen cards: date/place stamps, DNA name tags with a pointer,
big figures, the questions put to the viewer, act titles, a "keep in mind" flag, a summary of a
document's findings, and short lists. Each card names its chapter, its time into that chapter and
how long it stays, and only one card is on screen at a time. `tools/cards.py <channel> <slug>`
checks them; `--sheet x.png` draws every card on one contact sheet. The cards are drawn with Pillow
in the umbra. look (white on near-black, one red accent) and faded in over the picture by the
assembler.

### 6a. The channel outro (every episode, the same)
`channels/<name>/outro.json` holds the fixed sign-off that follows every story's last line: the
narrator's text, its length, and the end card (`kind: endcard`). `voiceover.py` records it as one
more take, with a 0.8 s pause after the story and no story context, so the last line still lands
as an ending. `assemble-episode.py` appends the end card after the storyboard. A 5:00 storyboard
plus umbra.'s 12 s outro makes a 5:12 video. Change it in that one file and every episode follows.

### 6b. Assemble
`tools/assemble-episode.py <channel> <slug>` cuts the rendered clips (from `production/renders.json`,
with REUSE scenes taking their source clip) into one cut, each clip trimmed to its scene's duration,
1280x720 at 24 fps: `production/output/<slug>-roughcut.mp4`.
- **Cards.** It lays the cards over the picture (`--no-cards` leaves them out).
- **Sound.** It mixes the step 5b stems under the narration: the music dips whenever the narrator
  speaks (sidechain ducking), and the whole mix is loudness-normalised to YouTube's -14 LUFS
  (`--no-sound` leaves them out; stale stems are refused).
- **Voice.** It lays the step 5 track under it automatically. Alternatives are `--vo <audio>` for any
  other track, `--scratch-vo` on macOS for a free `say` read as a timing guide, and `--no-vo`.
- **Safety.** It refuses to cut while scenes have no clip unless `--allow-gaps` is passed. A clip
  shorter than its scene is held on its last frame, and the finished cut is checked against the
  storyboard length before it is written.

### 7. Finish (outside this repo)
Concatenate the scene videos in chapter order, lay the VO + SFX/ambient/music split
(per-chapter notes in `04-scenes.md`) in an editor. Keep rendered binaries out of git
(see `.gitignore`); the prompts + shotlist are the reproducible source.

## shotlist.json contract
The single machine-readable artifact production reads. Fields with `null` are filled as
jobs complete:
```jsonc
{
  "episode": "...", "channel": "...", "aspect_ratio": "16:9",
  "style_anchor": "the locked render + palette string",
  "models": { "image": "nano_banana_pro", "video": "seedance_2_0" },
  "characters": [ { "id": "...", "label": "red|black|white|uniform",
                    "ref_prompt": "...", "image_job_id": null, "element_id": null } ],
  "chapters": [ { "id": "ch01", "title": "...", "duration_s": 15,
                  "sfx": "...", "ambient": "...", "music": "...",
                  "scenes": [ { "id": "ch01_s1", "duration_s": 3,
                                "characters": ["petrov"],
                                "image_prompt": "...", "video_prompt": "...",
                                "image_job_id": null, "video_job_id": null } ] } ]
}
```
A future helper can loop this file and issue the calls in §1–4 automatically.

## Keeping shotlist.json in sync
`04-scenes.md` is the human-authored storyboard; `shotlist.json` is generated from it so the
two never drift. After editing scenes, regenerate:
```bash
tools/build-shotlist.py <channel> <episode-slug>
```
It re-parses the chapters/scenes and **preserves** the header (episode/channel/style_anchor/
models/characters) and any `image_job_id` / `video_job_id` already filled in.
