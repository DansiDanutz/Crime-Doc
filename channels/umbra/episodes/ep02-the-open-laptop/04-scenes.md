# STATE 5 — Visual flow + scenes

**STYLE ANCHOR (constant for the whole video):**
```
Mannequin world — glossy white civilians / matte red main subject (Ross Ulbricht) / matte
black police (FBI), eggshell featureless heads, Mode B sparse photoreal (public library,
server-glow dark web inserts) + Mode A white-void diagram inserts, cinematic key from above,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9.
```

**CHARACTER LOCK:** Ross Ulbricht (red) · The Moderator (white + headset) · Library Patron
(white) · FBI Investigator (black) · The Arrest Team (black + undercover). Same render/wardrobe
in every scene; reference the saved elements (see `production/shotlist.json`).

---

## Chapter map (≈5:00 → 20 chapters × ~15 s)

| Ch | Time | Script beat | Mode | Scenes |
|----|------|-------------|------|--------|
| 01 | 0:00–0:15 | Cold open — Ulbricht opens the laptop and logs in | B library | 5 |
| 02 | 0:15–0:30 | "most wanted man on the internet" + the three-seconds anchor | B/A | 4 |
| 03 | 0:30–0:45 | Silk Road: dark web, Tor, Bitcoin, a billion in sales | A/B | 5 |
| 04 | 0:45–1:00 | Dread Pirate Roberts the ghost; the FBI has nothing | A | 5 |
| 05 | 1:00–1:15 | "Then they find a thread" — the 2011 altoid post | B | 5 |
| 06 | 1:15–1:30 | The slip — rossulbricht@gmail.com | B | 4 |
| 07 | 1:30–1:45 | Name, face, city — but the laptop is encrypted | B/A | 5 |
| 08 | 1:45–2:00 | The problem: lid closes → locked; need it open | A | 4 |
| 09 | 2:00–2:15 | "They plan around three seconds" | A | 4 |
| 10 | 2:15–2:30 | Oct 1 — agents follow him in; he logs in as admin | B | 5 |
| 11 | 2:30–2:45 | The staged quarrel begins behind him | B | 5 |
| 12 | 2:45–3:00 | The grab — laptop lifted, passed, kept awake | B | 6 |
| 13 | 3:00–3:15 | He turns back to an empty table | B | 4 |
| 14 | 3:15–3:30 | On the screen: DPR admin, the confirming line | B | 5 |
| 15 | 3:30–3:45 | The laptop's contents: journal, logbook, Bitcoin | B | 5 |
| 16 | 3:45–4:00 | The murder-for-hire files; scams, no bodies | A/B | 5 |
| 17 | 4:00–4:20 | Trial 2015; two life terms + 40 years, no parole | B | 5 |
| 18 | 4:20–4:35 | A decade in a cell; the textbook example | B | 4 |
| 19 | 4:35–4:50 | January 2025 — the pardon; he walks out free | B | 5 |
| 20 | 4:50–5:05 | Implicating turn — the next DPR has read every word | A | 4 |

> Chapters 01–03 are fully built below as the worked pattern. Expand 04–20 the same way
> (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per 2–4 s scene), then run
> `tools/build-shotlist.py umbra ep02-the-open-laptop` to regenerate the shotlist.

---

## CHAPTER 01 — Cold open: the login  (0:00–0:15)
**Script covered:** "It's the 1st of October, 2013… opens a laptop, and begins to type. His name is Ross Ulbricht. He is 29 years old."
**SFX:** keyboard taps, a page turning, distant library hush · **Ambient:** quiet library room tone, fluorescent hum · **Music:** low patient drone, one soft electronic pulse

### Scene ch01_s1 — 3s — wide establishing, the library
1. **CHARACTERS IN SCENE:** Ross Ulbricht (small, by the window), Library Patron (background)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the sunlit science-fiction corner of a public library, a
single matte red mannequin (eggshell head, casual red hoodie) seated alone at a wooden table
by a tall window, a glossy white mannequin patron browsing a shelf in the background, sparse
Mode B environment, soft daylight from the window, shallow depth of field, volumetric light,
dust particles in air, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide lock-off, very slow push-in toward the red mannequin at the table. Dust drifts in
the window light; the white patron shifts a book. 0–1s settle, 1–3s push begins. Hold color
code and wardrobe. No new figures.
```

### Scene ch01_s2 — 3s — the laptop opens (insert)
1. **CHARACTERS IN SCENE:** Ross Ulbricht (hands only, close)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a matte red mannequin's hands opening
a laptop lid on a library table, the screen waking to a faint blue glow, daylight, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro. The red hands raise the laptop lid 0–2s, the screen glow rises on the red
fingers 2–3s. Shallow focus on the hinge. No camera move. Deadpan, slow.
```

### Scene ch01_s3 — 3s — the login screen
1. **CHARACTERS IN SCENE:** Ross Ulbricht (over-shoulder)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, over-the-shoulder of a matte red mannequin facing a laptop
showing a plain login prompt with a blinking cursor, blue screen light on the red eggshell
head, library table, Mode B, shallow depth of field, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static over-the-shoulder, the cursor blinks and a password fills the field dot by dot 0–3s,
screen light flickering on the red head. No camera move. Hold palette.
```

### Scene ch01_s4 — 3s — he begins to type
1. **CHARACTERS IN SCENE:** Ross Ulbricht
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of a matte red mannequin (red hoodie, eggshell
head) leaning toward a laptop and typing, calm and absorbed, library window light behind, Mode
B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Medium static. The red mannequin's fingers move over the keys 0–3s, head tilted to the screen,
utterly unremarkable. No camera move. Hold palette.
```

### Scene ch01_s5 — 3s — the ordinary room around him (handoff)
1. **CHARACTERS IN SCENE:** Ross Ulbricht (small), Library Patron
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a calm wide of the quiet library, the lone matte red
mannequin at his table among empty chairs and one distant glossy white patron, ordinary
afternoon, Mode B, soft daylight, shallow depth of field, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow pull-back from the red figure revealing the calm ordinary room 0–3s. Nothing seems to be
happening. Hold palette. No new figures.
```

**Chapter handoff →** hold on the unremarkable room; cut to the anchor line of Chapter 02.

---

## CHAPTER 02 — The most wanted man  (0:15–0:30)
**Script covered:** "This is the story of how the FBI caught the most wanted man on the internet, and the three seconds that made it possible."
**SFX:** a deep impact hit on the anchor line, a single clock tick · **Ambient:** library hush thinning · **Music:** drone steps up, a ticking enters

### Scene ch02_s1 — 4s — STYLE ANCHOR / title beat
1. **CHARACTERS IN SCENE:** Ross Ulbricht (tiny, centered)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red mannequin seated very small and centered
at a table in a vast dim library, immense negative space around it, one shaft of daylight from
a high window, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static symmetrical wide, almost still. Imperceptible push-in 0–4s; dust drifts in the light
shaft. The lone red figure motionless. Title-card emptiness. Hold palette. No new figures.
```

### Scene ch02_s2 — 4s — a stopwatch / three seconds
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of an old analog stopwatch on a dark
surface, the second hand frozen near three seconds, cold light, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the stopwatch second hand ticks toward three and stops 0–4s. The hinge the whole
story turns on. No camera move. Hold palette.
```

### Scene ch02_s3 — 4s — the FBI watching (black, white void)
1. **CHARACTERS IN SCENE:** FBI Investigator (black)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin (plain suit, FBI windbreaker
silhouette, badge lanyard) standing in an infinite white void, arms folded, watching, soft
contact shadow, cinematic key from above, shallow depth of field, volumetric light, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the black FBI mannequin standing still 0–4s, impassive. The hunter introduced.
Hold the color code. No new figures.
```

### Scene ch02_s4 — 3s — back to Ulbricht, unaware (handoff)
1. **CHARACTERS IN SCENE:** Ross Ulbricht
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of the matte red mannequin typing at the
library table, oblivious, soft daylight, Mode B, shallow depth of field, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium on the red figure typing 0–3s, calm and unaware. The gap between him and the
watcher. No camera move. Hold palette.
```

**Chapter handoff →** push into the laptop screen; the screen becomes the dark web of Chapter 03.

---

## CHAPTER 03 — Silk Road  (0:30–0:45)
**Script covered:** "For two years, a website called Silk Road has sold almost anything illegal you can imagine… It runs on the dark web, reachable only through Tor… Payment is in Bitcoin… more than a billion dollars in sales."
**SFX:** server-room hum, soft data chimes, coins clicking · **Ambient:** electronic undertone · **Music:** cold pulsing synth motif

### Scene ch03_s1 — 3s — the marketplace screen
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a dark laptop screen filled with a clean anonymous
marketplace grid of unlabeled product tiles, cold blue glow, no text legible, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked on the screen, the marketplace grid scrolls slowly upward 0–3s, tiles loading. Vast and
anonymous. No camera move. Hold palette.
```

### Scene ch03_s2 — 3s — Tor: the bouncing route (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a single
connection line bouncing between many simplified globe nodes around the world, the endpoints
hidden, cold and geometric, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the connection line hops node to node around the globe ring 0–3s, never
settling. Anonymity made visible. No figures. Hold palette.
```

### Scene ch03_s3 — 3s — Bitcoin, untraceable
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of stylized matte coins moving along a faint chain
of glowing blocks on a dark surface, no logos legible, cold blue light, Mode B, shallow depth
of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the coins slide along the block chain and dissolve into it 0–3s. Money that
leaves no trail. No camera move. Hold palette.
```

### Scene ch03_s4 — 3s — "a billion dollars" scale
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, an enormous towering stack of
plain matte currency blocks receding upward out of frame, cold clinical scale, soft contact
shadows, cinematic key from above, shallow depth of field, volumetric light, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane-up the towering stack of currency blocks 0–3s, never reaching the top. The scale of
it. No figures. Hold palette.
```

### Scene ch03_s5 — 3s — Ulbricht at the center of it (handoff)
1. **CHARACTERS IN SCENE:** Ross Ulbricht
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the matte red mannequin small at the library table, the
cold blue marketplace glow now reflected across its red eggshell head, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the red figure as the blue marketplace glow plays across its head 0–3s. The man
behind the billion. Hold palette. No new figures.
```

**Chapter handoff →** the glow narrows to a single forum window; Chapter 04 names the ghost.

---

> **Chapters 04–20:** expand identically (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per scene),
> keeping Ulbricht red, FBI black, the arrest team black + undercover, civilians white. Then
> run `tools/build-shotlist.py umbra ep02-the-open-laptop`.

Type "next" for thumbnail prompts.
