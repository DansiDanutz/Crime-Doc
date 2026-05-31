# STATE 5 — Visual flow + scenes

**STYLE ANCHOR (constant for the whole video):**
```
Mannequin world — glossy white civilians / matte red protagonist (Petrov) / matte black
institution (Duty Officers, The General), eggshell featureless heads, Mode B sparse
photoreal bunker interior + Mode A white-void inserts, cinematic key from above, red panel
glow as the only accent, shallow DoF, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9.
```

**CHARACTER LOCK:** Petrov (red) · Duty Officer (black) · The General (black + photoreal
uniform) · Civilian (white). Same render/wardrobe in every scene. Reference the saved
elements (see `production/shotlist.json`).

---

## Chapter map (≈5:00 → 20 chapters × ~15 s)

| Ch | Time | Script beat | Mode | Scenes |
|----|------|-------------|------|--------|
| 01 | 0:00–0:15 | Cold open — Petrov pours tea, sits at screens | B bunker | 5 |
| 02 | 0:15–0:30 | "decided whether the world would end" + Serpukhov-15 reveal | B/A | 4 |
| 03 | 0:30–0:45 | Oko satellites watch the US; "trust the system" | A/space | 5 |
| 04 | 0:45–1:00 | Cold War at its lowest; KAL 007; fingers near the button | B/A | 5 |
| 05 | 1:00–1:15 | "the system moves" — LAUNCH fills the panel, siren | B | 5 |
| 06 | 1:15–1:30 | One ICBM reported, climbing toward USSR | A/space | 4 |
| 07 | 1:30–1:45 | The protocol — phone, chain of command | B | 5 |
| 08 | 1:45–2:00 | Launch on warning explained | A | 4 |
| 09 | 2:00–2:15 | "But Petrov hesitates" — one missile makes no sense | B | 5 |
| 10 | 2:15–2:30 | Seconds to decide; ~20 min to impact | B | 4 |
| 11 | 2:30–2:45 | He reports a malfunction | B | 4 |
| 12 | 2:45–3:00 | Second, third, fourth, fifth missile | B | 6 |
| 13 | 3:00–3:15 | He holds; reports malfunction again | B | 4 |
| 14 | 3:15–3:35 | He waits, watches the clock | B | 5 |
| 15 | 3:35–3:50 | Nothing happens; empty sky on ground radar | A/B | 5 |
| 16 | 3:50–4:05 | "Petrov was right" + the sunlight-on-clouds cause | A/space | 5 |
| 17 | 4:05–4:20 | No medal; reprimand; reassigned | B | 5 |
| 18 | 4:20–4:35 | Ten years unknown; dies 2017, forgotten | B/A | 4 |
| 19 | 4:35–4:50 | The system is still there, in every nuclear state | A | 5 |
| 20 | 4:50–5:05 | Implicating turn — "may decide to believe it" | A | 4 |

> Chapters 01–03 are fully built below as the worked pattern. Chapters 04–20 follow the
> identical structure (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per 2–4 s scene); expand
> them the same way and mirror into `production/shotlist.json`. The first chapter is also
> encoded in the shotlist as the canonical machine-readable example.

---

## CHAPTER 01 — Cold open: the thermos  (0:00–0:15)
**Script covered:** "It's just after midnight, the 26th of September 1983… facing a wall of screens. He isn't supposed to be here tonight. Someone else called in sick."
**SFX:** thermos pour, chair creak, single distant relay click · **Ambient:** low bunker hum, fluorescent buzz · **Music:** sub-bass drone, one slow piano note

### Scene ch01_s1 — 3s — wide establishing
1. **CHARACTERS IN SCENE:** Petrov (seated, distant)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red featureless mannequin (a Soviet
officer, eggshell head, no facial features) seated alone at a long Soviet-era command
console in a dim underground bunker, walls of dark monitoring screens faintly glowing, vast
empty room around him, sparse Mode B environment, cinematic key light from above, faint red
panel glow as the only accent, shallow depth of field, volumetric light, dust particles in
air, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide lock-off, very slow almost-imperceptible push-in on the seated red mannequin.
Dust drifts through the volumetric beam; the screens flicker faintly. The figure is still.
0–1s settle, 1–3s the room hum builds. Hold color code and wardrobe exactly. No new figures.
```

### Scene ch01_s2 — 3s — the pour (insert)
1. **CHARACTERS IN SCENE:** Petrov (hands only, close)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a matte red mannequin's hands
pouring tea from a battered steel thermos into a small metal cup, steam rising, against the
dark bunker console with faint red glow, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro shot. Tea streams from the thermos for 0–2s, steam curls upward 2–3s. Tiny
red-hand tremor. Shallow focus on the cup. No camera move. Deadpan, slow.
```

### Scene ch01_s3 — 3s — sits down
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red featureless mannequin (Soviet officer,
eggshell head) lowering itself into a worn chair before a wall of monitoring screens in a
dim bunker, mid-motion, Mode B, cinematic key from above, faint red panel glow, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Medium shot, static. The red mannequin settles into the chair 0–2s, then goes still facing
the screens 2–3s. Faint screen flicker reflects on the matte red surface. No camera move.
```

### Scene ch01_s4 — 3s — the empty room behind him
1. **CHARACTERS IN SCENE:** Petrov (back of figure), empty stations
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, over-the-shoulder from behind a lone matte red mannequin
seated at a console, rows of empty unmanned duty stations stretching away into the dark
bunker, one chair conspicuously vacant, Mode B, cinematic key from above, faint red glow,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow lateral dolly left behind the red mannequin, revealing the empty stations and the one
vacant chair. 0–3s continuous drift. Emphasize isolation. Hold the color code. No new figures.
```

### Scene ch01_s5 — 3s — the wall of screens
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a towering wall of dark Soviet-era monitoring screens
and a large map board of the northern hemisphere, faintly backlit, silent, in a dim bunker,
Mode B, cinematic key from above, faint red standby glow, shallow depth of field, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane-up across the screen wall, screens in quiet standby. 0–3s upward drift, a single
indicator blinks once at 2s. Calm, clinical. No figures. Hold palette.
```

**Chapter handoff →** end on the silent screen wall; cut to the same room widening into the
title beat of Chapter 02.

---

## CHAPTER 02 — "Serpukhov-15"  (0:15–0:30)
**Script covered:** "This is the story of how one man, in twenty-three minutes, decided whether the world would end. The bunker is called Serpukhov-15."
**SFX:** deep impact hit on the anchor line, low relay clicks · **Ambient:** bunker hum · **Music:** drone swells one step

### Scene ch02_s1 — 4s — STYLE ANCHOR / title beat
1. **CHARACTERS IN SCENE:** Petrov (tiny, centered)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red featureless mannequin seated very
small and centered in a vast dark bunker, immense negative space and shadow around it, one
shaft of cinematic key light from above, faint red panel glow, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static symmetrical wide, almost still. Imperceptible push-in 0–4s; dust drifts in the light
shaft. The lone red figure motionless. Title-card emptiness. Hold palette. No new figures.
```

### Scene ch02_s2 — 4s — exterior bunker (Mode B)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a concrete Soviet command bunker entrance set into a
dark pine forest at night, antennas and a perimeter fence, cold blue moonlight, one small
red-lit doorway, no people, sparse Mode B, shallow depth of field, volumetric fog, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow aerial descent toward the bunker entrance, fog rolling 0–4s, the red doorway the only
warm point. Cold and clinical. No figures. Hold palette.
```

### Scene ch02_s3 — 4s — the Oko console nameplate
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a Soviet console with a stenciled Cyrillic
label and a single large indicator panel reading standby, faint red glow, dim bunker, Mode
B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, slow rack focus from the stenciled label to the standby indicator 0–4s.
A relay clicks at 2s. No camera move. Clinical.
```

### Scene ch02_s4 — 3s — Petrov small at the console (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide low-angle of a lone matte red mannequin at a Soviet
command console beneath the towering screen wall, dwarfed by the machine, Mode B, faint red
glow, cinematic key from above, shallow depth of field, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in low-angle toward the small red figure under the screen wall 0–3s. Screens hold
standby. The figure still. Builds scale of the system. Hold palette. No new figures.
```

**Chapter handoff →** push past Petrov into the screens; the screens become the satellite
POV opening Chapter 03.

---

## CHAPTER 03 — Oko, the eye  (0:30–0:45)
**Script covered:** "It is the brain of a system called Oko — Russian for 'eye.' Oko is a network of satellites that stare down at the United States… Watch the screens. Trust the system. Report what it tells him."
**SFX:** soft satellite telemetry beeps, vacuum tone · **Ambient:** space silence under bunker hum · **Music:** cold sustained pad

### Scene ch03_s1 — 3s — satellites over Earth (Mode A/space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a Soviet early-warning satellite in orbit above a dark
curve of Earth at night, sensor aperture aimed downward at the continents, stark sunlight on
one panel, deep black space, clinical and cold, shallow depth of field, volumetric light
rim, dust-free vacuum, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow orbital drift past the satellite 0–3s, Earth turning slowly below, the sensor aperture
glinting. Cold, silent, clinical. No figures.
```

### Scene ch03_s2 — 3s — the watched continent
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, top-down satellite view of the dark northern United
States at night seen through a faint targeting reticle overlay, scattered city lights, cold
clinical surveillance aesthetic, deep black, shallow depth of field, volumetric haze,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow downward zoom through the reticle toward the dark continent 0–3s, reticle subtly
realigns. Surveillance calm. No figures.
```

### Scene ch03_s3 — 3s — screens reflect on Petrov
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close profile of a matte red mannequin's eggshell head
and shoulder, the glow of monitoring screens reflected across its smooth red surface, dim
bunker, Mode B, cinematic key from above, faint red accent, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static tight profile. Screen-light reflections crawl across the red eggshell head 0–3s. The
figure perfectly still, watching. No camera move. Hold palette.
```

### Scene ch03_s4 — 3s — "trust the system" (the protocol card)
1. **CHARACTERS IN SCENE:** Petrov (hand), console
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin hand resting beside a red telephone
handset and a printed protocol checklist on a Soviet console, faint red glow, dim bunker,
Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked insert, slow rack focus from the red mannequin hand to the red telephone handset
0–3s. Nothing moves but the focus. Foreboding calm. No new figures.
```

### Scene ch03_s5 — 3s — wide, the eye and the man (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide shot of a lone matte red mannequin facing a vast
illuminated hemispheric map board of the world, the figure small against the glowing map,
dim bunker, Mode B, faint red accent, cinematic key from above, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Very slow push-in toward the small red figure before the glowing map 0–3s. The map holds
steady. Calm before the alarm. Hold palette. No new figures.
```

**Chapter handoff →** hold on the calm map board; in Chapter 05 this same board erupts in red
with the LAUNCH alert.

---

> **Chapters 04–20:** build identically. Keep Petrov red, the staff/General black, civilians
> white; keep the bunker + space + white-void modes; reuse the saved character elements.
> Mirror every scene into `production/shotlist.json` as you go.

Type "next" for thumbnail prompts.
