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
For each scene in `shotlist.json.chapters[].scenes[]`:
- `generate_image`, `model: nano_banana_pro`, `prompt: scene.image_prompt`,
  `medias: [{role:"reference", value:<element_id>}, …]` for each character in the scene,
  `aspect_ratio: "16:9"`.
- Record the image job id into `scene.image_job_id`.

### 3. Animate each scene
- `generate_video`, `model: seedance_2_0`,
  `medias: [{role:"start_image", value: scene.image_job_id}]`,
  `prompt: scene.video_prompt`, `duration: scene.duration_s`, `aspect_ratio:"16:9"`.
- Record the video job id into `scene.video_job_id`.

### 4. Thumbnails
- `generate_image`, `model: nano_banana_pro`, each prompt from `05-thumbnails.md`,
  `count: 4`, `aspect_ratio:"16:9"`.

### 5. Assemble (outside this repo)
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
