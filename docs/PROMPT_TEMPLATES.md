# PROMPT_TEMPLATES — fill-in-the-blank prompts

Copy these, replace the `[BRACKETS]`, keep the trailing render language. All conform to
DNA §7/§8. Default aspect ratio: video `16:9`, thumbnail `16:9`, character ref `2:3` or `1:1`.

---

## A. Character reference (STATE 4) — white void, one figure
```
Cinematic photorealistic 3D render, a single [RED / BLACK / glossy white] featureless
mannequin with a smooth eggshell head (no eyes, nose, mouth, ears, or hair), realistic
human proportions, polished matte [red / black] surface, [wearing detailed [UNIFORM] with
[badges/epaulettes/duty belt/tie] | no clothing], [POSE — standing / seated / mid-stride],
isolated on a pure white seamless void background, soft contact shadow beneath, cinematic
key light from above, shallow depth of field, volumetric light, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 2:3
```
Rules: ONE figure, white void only, no environment, no facial features.

---

## B. Scene keyframe (STATE 5 image prompt) — Mode A or Mode B
```
Cinematic photorealistic 3D render, [N] mannequin figures —
[a matte RED mannequin (protagonist) | N matte BLACK mannequins (institution) | glossy
white mannequins (civilians)] with smooth eggshell heads (no facial features),
[wearing [UNIFORM] with [details] where it matters], [ACTION / POSE / staging — who faces
whom], in [Mode A: an infinite white void with soft contact shadows | Mode B: a [SPARSE
ENVIRONMENT] with [specific props]], [LIGHTING — key from above, accent [red] glow],
shallow depth of field, volumetric light, dust particles in air, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```

---

## C. Scene motion (STATE 5 video prompt) — animates keyframe B
```
[CAMERA: slow push-in / static lock-off / lateral dolly / slow crane-down] on [SUBJECT].
[SUBJECT MOTION: the red mannequin turns its head / raises a hand / steps forward].
[ENVIRONMENT MOTION: dust drifts through the volumetric beam / screens flicker red].
Beat timing across [N] seconds: [0–1s … 1–2s … 2–3s …]. Hold the color code and wardrobe
exactly as the keyframe. No new figures. Cinematic, deadpan, slow.
```
Feed as `seedance_2_0` with `start_image` = the keyframe job id.

---

## D. Thumbnail (STATE 6) — high contrast, label tags
```
Cinematic photorealistic 3D render thumbnail, a single matte RED featureless mannequin
([SUBJECT ROLE]) centered/right, [N] matte BLACK mannequins ([INSTITUTION]) flanking and
[aiming at / closing in on] it, glossy white mannequins blurred in the background, smooth
eggshell heads no facial features, [SPARSE ENVIRONMENT], stark high-contrast lighting, key
from above, deep shadows, bold red / pure white / deep black palette, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9.
Overlaid graphic tags: a RED rectangular tag reading "[SUBJECT LABEL]" with a small
triangular pointer at the red figure's head; a BLACK rectangular tag reading
"[INSTITUTION LABEL]" with a triangular pointer at a black figure's head. Bold ALL-CAPS
sans-serif, 1–3 words per tag, white or red text.
```
Use `nano_banana_pro` (best in-image text). Generate 4 counts, pick the cleanest tags.

---

## E. Logo / banner (STATE 1)
**Logo:**
```
Minimalist monochrome channel logo, a single [LETTER]-form with a dot inside a clean
circle, flat white on near-black geometric background, subtle [green/red] accent glow, no
gradient, high negative space, vector-clean, modern broadcast mark.
```
**Banner:**
```
YouTube banner, minimalist monochrome, lowercase wordmark "[name.]" in clean white sans on
a dark near-black field, generous headroom and negative space, one subtle [green/red]
accent line, geometric, no photography, no gradient, 2560×1440 safe-area centered.
```
