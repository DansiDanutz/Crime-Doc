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
1. **CHARACTERS IN SCENE:** Petrov (back of figure)
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
1. **CHARACTERS IN SCENE:** Petrov (hand)
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

## CHAPTER 04 — The lowest point  (0:45–1:00)
**Script covered:** "The Cold War is at its lowest point in twenty years. Three weeks earlier, a Soviet fighter shot down a Korean passenger jet, killing 269 people… everyone is waiting for the other side to move first."
**SFX:** distant jet rumble, a single cold tone on "269" · **Ambient:** wind, low static · **Music:** drone, a dissonant string enters

### Scene ch04_s1 — 4s — the downed airliner (implied, never graphic)
1. **CHARACTERS IN SCENE:** Civilians (glossy white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the silhouette of a passenger airliner banking against a
cold night sky over dark ocean, a single matte black fighter mannequin-pilot shape trailing
behind it, no impact shown, glossy white mannequin passenger shapes faintly visible in the
windows, Mode B, stark moonlight, cold blue grade, shallow DoF, volumetric haze, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow lateral track as the airliner banks away 0–3s, the black fighter shape holding behind,
then both slip into cloud 3–4s. Violence implied, never shown. Cold, clinical. Hold palette.
```

### Scene ch04_s2 — 3s — 269 white figures
1. **CHARACTERS IN SCENE:** Civilians (glossy white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a vast grid of identical glossy white featureless
mannequins standing in cold rows in an infinite white void (Mode A), receding to the
horizon, soft contact shadows, clinical, cinematic key from above, shallow DoF, volumetric
light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane-up over the grid of white figures 0–3s, revealing the scale of the rows. Nothing
moves. The number made physical. Hold palette. No new figures.
```

### Scene ch04_s3 — 3s — military exercises near the border
1. **CHARACTERS IN SCENE:** Duty Officer / System (black, several)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a row of matte black featureless mannequins in military
uniform silhouettes standing along a stark border line drawn across a cold grey plain, facing
outward, Mode B, overcast flat light, shallow DoF, volumetric haze, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow lateral dolly along the line of black figures 0–3s, all motionless, facing out. Tension
of a standoff. Hold the color code. No new figures.
```

### Scene ch04_s4 — 3s — fingers near the button
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of two anonymous matte black mannequin
hands hovering over identical red launch keys on opposing consoles, mirrored composition,
dark, faint red glow, Mode B, shallow DoF, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked symmetrical macro, the two black hands hovering, neither touching the keys 0–3s. A
faint tremor. Mirror tension. No camera move. Hold palette.
```

### Scene ch04_s5 — 3s — back to Petrov, waiting (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a lone matte red mannequin seated still at the bunker
console, the screen wall calm in standby behind, dim, faint red glow, Mode B, cinematic key
from above, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium on the red figure 0–2s, then the standby screens behind begin to pulse faintly
2–3s — the calm about to break. No camera move. Hold palette.
```

**Chapter handoff →** the faint pulse becomes the full red alert opening Chapter 05.

---

## CHAPTER 05 — LAUNCH  (1:00–1:15)
**Script covered:** "At fourteen minutes past midnight, the system moves. A single word fills the main panel in red letters: LAUNCH. A siren begins to wail."
**SFX:** alarm klaxon, hard relay slam, klaxon loop · **Ambient:** bunker hum spikes · **Music:** drone breaks into a pulsing alarm motif

### Scene ch05_s1 — 3s — the clock 00:14
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a Soviet console clock reading
00:14, faint green numerals, the moment before alarm, dim bunker, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the clock 0–2s, the numerals tick to 00:14, then a sudden red glow washes
over the frame 2–3s. No camera move. Snap of dread.
```

### Scene ch05_s2 — 3s — LAUNCH fills the wall
1. **CHARACTERS IN SCENE:** Petrov (silhouette, foreground)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the towering bunker screen wall erupting in a single
enormous word "LAUNCH" in red, a small matte red mannequin silhouetted in the foreground
dwarfed by it, blazing red light flooding the room, Mode B, high contrast, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide. The word LAUNCH snaps on at 0s, red light floods the room and the red mannequin
0–1s, then a fast push-in toward the figure 1–3s as the klaxon hits. Hold palette. No new figures.
```

### Scene ch05_s3 — 3s — the siren / rotating beacon
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a red rotating alarm beacon mounted on a concrete bunker
ceiling, throwing sweeping red light through dust and haze, Mode B, dark, shallow DoF,
volumetric light, heavy dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static low angle, the beacon sweeps red light across the frame in rotation 0–3s, haze lit in
pulses. Relentless rhythm. No camera move. Hold palette.
```

### Scene ch05_s4 — 3s — Petrov recoils
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin (Soviet officer, eggshell head)
sitting upright sharply in its chair, head turned to the blazing red screen wall, lit hard
red, dim bunker, Mode B, high contrast, shallow DoF, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Medium static. The red figure snaps upright and turns its head to the wall 0–2s, then freezes
2–3s, red alarm light pulsing across the eggshell head. No camera move. Hold palette.
```

### Scene ch05_s5 — 3s — empty stations, alarm everywhere (handoff)
1. **CHARACTERS IN SCENE:** Petrov (small)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide shot of the bunker bathed in pulsing red alarm light,
the lone red mannequin small at its console, every other station empty, Mode B, high contrast,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow pull-back from the red figure revealing the empty alarmed room 0–3s, red light pulsing.
He is alone with it. Hold palette. No new figures.
```

**Chapter handoff →** push into the red screen; the screen content becomes the single-missile track of Chapter 06.

---

## CHAPTER 06 — One missile  (1:15–1:30)
**Script covered:** "The computer reports one intercontinental ballistic missile, fired from a base in the United States, climbing now, aimed at the Soviet Union."
**SFX:** telemetry ping, rising track tone · **Ambient:** klaxon now muffled under · **Music:** single ascending pulse

### Scene ch06_s1 — 4s — the track on the map
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glowing hemispheric map board showing a single red
missile arc rising from North America toward the USSR, lone trajectory line, dark bunker,
Mode B, red glow, shallow DoF, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the map board, the single red arc draws itself upward across the map 0–4s, a small
icon climbing along it. Cold and precise. No camera move. Hold palette.
```

### Scene ch06_s2 — 3s — the missile climbs (space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single ICBM rising through the upper atmosphere seen
from orbit, thin exhaust trail, dark curve of Earth below, deep black space, clinical, cold
grade, shallow DoF, volumetric light rim, dust-free vacuum, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow track following the lone missile climbing 0–3s, Earth turning beneath, thin trail
behind. Silent, cold. No figures. Hold the cold space grade.
```

### Scene ch06_s3 — 4s — "one" on the readout
1. **CHARACTERS IN SCENE:** Petrov (hand/profile)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close on a Soviet console readout displaying a single
red numeral "1" beside a missile glyph, a matte red mannequin hand resting near it, dim
bunker, red glow, Mode B, shallow DoF, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the readout 0–2s, the numeral "1" pulses, the red hand stays still 2–4s. The
strangeness of a single missile lingers. No camera move. Hold palette.
```

### Scene ch06_s4 — 3s — Petrov staring at the wall (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin seen from behind, head tilted
slightly, facing the red missile track on the screen wall, dim bunker, Mode B, red glow,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static from behind the red figure 0–3s, only the red track on the wall moving, the figure
motionless and tilted in thought. No camera move. Hold palette.
```

**Chapter handoff →** the red phone beside him glints; Chapter 07 opens on the protocol.

---

## CHAPTER 07 — The protocol  (1:30–1:45)
**Script covered:** "Petrov has a protocol. He is to pick up the phone, call his superiors, and report a confirmed attack. From that call the chain runs upward in minutes — to the General Staff…"
**SFX:** phone handset tone, paper rustle, distant chain of clicks · **Ambient:** muffled klaxon · **Music:** low ticking motif begins

### Scene ch07_s1 — 3s — the red phone
1. **CHARACTERS IN SCENE:** Petrov (hand)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a red Soviet field telephone on the console,
a matte red mannequin hand hovering just above the handset, faint red alarm glow, dim bunker,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the red hand hovers over the handset 0–3s, fingers flexing, not lifting it.
Hesitation made physical. No camera move. Hold palette.
```

### Scene ch07_s2 — 3s — the protocol checklist
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a printed Soviet duty protocol card clamped
to the console, dense rows of text and one highlighted line, faint red glow, dim bunker,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked insert, slow rack focus down the checklist to the highlighted line 0–3s. Bureaucratic
inevitability. No camera move. Hold palette.
```

### Scene ch07_s3 — 3s — the chain of command (white-void diagram)
1. **CHARACTERS IN SCENE:** Petrov (red, bottom), Duty Officers + The General (black, ascending)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void (Mode A), a single matte red
mannequin at the bottom of an ascending line of matte black mannequins that grows in rank
toward a black mannequin in a photoreal Soviet general's dress uniform at the top, a clear
upward chain, soft contact shadows, cinematic key from above, shallow DoF, volumetric light,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane-up along the chain from the red figure at the base to the uniformed general at the
top 0–3s. The system rising above the man. Hold the color code. No new figures.
```

### Scene ch07_s4 — 3s — the General waiting
1. **CHARACTERS IN SCENE:** The General (black + photoreal uniform)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte black mannequin in a photoreal Soviet general's
dress uniform (olive tunic, gold shoulder boards, medals) standing in an infinite white void,
hands clasped, waiting, soft contact shadow, cinematic key from above, shallow DoF,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the uniformed general standing still 0–3s, the eggshell head impassive.
Authority that waits for one phone call. Hold palette. No new figures.
```

### Scene ch07_s5 — 3s — Petrov and the phone (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of a matte red mannequin seated at the
console, the red phone in frame, the figure leaning toward it but stopped, dim bunker, red
glow, Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure leans toward the phone 0–2s then holds, frozen between act and
restraint 2–3s. No camera move. Hold palette.
```

**Chapter handoff →** cut from the frozen reach to the doctrine that drives it — Chapter 08.

---

## CHAPTER 08 — Launch on warning  (1:45–2:00)
**Script covered:** "The doctrine is called launch on warning. You do not wait for the first bomb to land. You fire while the enemy's missiles are still in the air."
**SFX:** two opposing low booms, mirrored · **Ambient:** thin high tone · **Music:** ticking motif intensifies

### Scene ch08_s1 — 4s — two arcs crossing (white void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, two opposing red and black
missile arcs crossing midair between two simplified globes, mirrored mutual launch, clean
diagrammatic, soft contact shadows, cinematic key from above, shallow DoF, volumetric light,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static symmetrical, the two arcs draw toward each other and cross at center 0–4s. The logic of
mutual destruction, clean and cold. No figures. Hold palette.
```

### Scene ch08_s2 — 4s — the counterstrike massed (black)
1. **CHARACTERS IN SCENE:** Duty Officers / System (black, many)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a vast field of identical matte black missile silos
opening in unison across a dark plain, faint red launch glow rising from each, Mode B, cold,
shallow DoF, volumetric haze, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane-up over the field of opening silos 0–4s, red glow building. A thousand warheads
implied, never shown. Cold and clinical. Hold palette.
```

### Scene ch08_s3 — 3s — the clock against the doctrine
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a console countdown ticking down beside the
red missile track, urgency, dim bunker, red glow, Mode B, shallow DoF, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the countdown ticking 0–3s, each second heavy. No camera move. Hold palette.
```

### Scene ch08_s4 — 3s — Petrov alone with the doctrine (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin sitting very still at the console,
the crossing-arcs logic reflected faintly on the screen wall behind, dim bunker, red glow,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium on the still red figure 0–3s, the doctrine glowing behind him. The whole system
resting on one chair. No camera move. Hold palette.
```

**Chapter handoff →** tight on the red eggshell head as the doubt forms — Chapter 09.

---

## CHAPTER 09 — Hesitation  (2:00–2:15)
**Script covered:** "But Petrov hesitates. Something about the picture is wrong. One missile. The Americans have thousands… Nobody starts a nuclear war with a single shot. It makes no sense."
**SFX:** the klaxon drops to near-silence, a heartbeat · **Ambient:** ringing quiet · **Music:** ticking thins to a single pulse

### Scene ch09_s1 — 3s — the single arc, again
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the map board showing just one lonely red missile arc on
a vast empty map, conspicuous emptiness around it, dim bunker, red glow, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the single arc amid empty map 0–3s. The wrongness of one. No camera move.
Hold palette.
```

### Scene ch09_s2 — 4s — what a real strike looks like (white void)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a dense wall of hundreds of red
arcs launching all at once between two globes — contrasted against a single thin arc beside
it, diagrammatic comparison, soft contact shadows, cinematic key from above, shallow DoF,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static comparison, the dense wall of arcs surges up 0–2s, then the lone thin arc fades in
beside it 2–4s. The mismatch is the argument. No figures. Hold palette.
```

### Scene ch09_s3 — 3s — Petrov's head tilts (the doubt)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, tight close-up of a matte red mannequin's eggshell head
tilting slowly, screen glow crawling across the smooth surface, dim bunker, red accent, Mode
B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static tight, the red head tilts a few degrees 0–3s as if calculating, reflections shifting.
Thought without a face. No camera move. Hold palette.
```

### Scene ch09_s4 — 3s — the empty radar (the missing confirmation)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a circular ground-radar scope sweeping, completely empty,
green trace finding nothing, dim bunker, faint red glow at the edges, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the radar sweep rotates twice 0–3s, finding nothing. The silence speaks. No
camera move. Hold palette.
```

### Scene ch09_s5 — 3s — Petrov decides to doubt (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of a matte red mannequin sitting back from the
console, posture settling into resolve, dim bunker, red glow, Mode B, shallow DoF, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure leans back slowly 0–3s, settling — a decision forming. No camera
move. Hold palette.
```

**Chapter handoff →** the calm breaks against the clock — Chapter 10.

---

## CHAPTER 10 — Seconds  (2:15–2:30)
**Script covered:** "He has seconds. If the missile is real, it lands in about twenty minutes."
**SFX:** loud ticking, a single breath · **Ambient:** klaxon swells back · **Music:** pulse accelerates

### Scene ch10_s1 — 4s — the clock vs. impact
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, split composition of a console clock and a glowing "~20
MIN TO IMPACT" readout in red, urgent, dim bunker, red glow, Mode B, shallow DoF, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the seconds tick on the clock while the impact readout pulses 0–4s. Time as
pressure. No camera move. Hold palette.
```

### Scene ch10_s2 — 3s — the missile mid-arc (space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the single ICBM at the top of its arc above the dark Earth,
poised, deep black space, cold grade, shallow DoF, volumetric light rim, dust-free vacuum,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow drift past the missile at apogee 0–3s, Earth below. The threat suspended. No figures.
Hold the cold space grade.
```

### Scene ch10_s3 — 4s — Petrov's stillness under pressure
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin gripping the edge of the console,
absolutely still amid the red alarm light, dim bunker, Mode B, high contrast, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the red figure gripping the console 0–4s, red light pulsing, the figure
refusing to move. Pressure held. Hold palette. No new figures.
```

### Scene ch10_s4 — 3s — the hand near the phone again (handoff)
1. **CHARACTERS IN SCENE:** Petrov (hand)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of the matte red mannequin hand settling onto
the red telephone handset, decision imminent, red glow, dim bunker, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the red hand lowers onto the handset 0–3s and grips it. The call is about to be
made — but not the one expected. No camera move. Hold palette.
```

**Chapter handoff →** he lifts the phone; Chapter 11 is what he says.

---

## CHAPTER 11 — Malfunction  (2:30–2:45)
**Script covered:** "He picks up the phone and reports a system malfunction. A false alarm. He has no way to know if he is right."
**SFX:** handset lift, a single spoken-cadence beat, line static · **Ambient:** klaxon muffled by the call · **Music:** the pulse holds its breath

### Scene ch11_s1 — 4s — lifting the phone
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin raising the red telephone handset
to the side of its eggshell head, deliberate, dim bunker, red glow, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure raises the handset to its head 0–3s and holds 3–4s. The
decisive act, deadpan. No camera move. Hold palette.
```

### Scene ch11_s2 — 4s — the word travels (white void)
1. **CHARACTERS IN SCENE:** The General (black + uniform, listening)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, the matte black uniformed
general mannequin holding a phone to its eggshell head, listening, a thin red line connecting
off-frame, soft contact shadow, cinematic key from above, shallow DoF, volumetric light,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the uniformed general listening on the phone 0–4s, impassive. The word
"malfunction" lands on the system. Hold palette. No new figures.
```

### Scene ch11_s3 — 3s — "false alarm" on the readout
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a console readout where Petrov has logged a status, the
red LAUNCH word still blazing above it unchanged, contradiction visible, dim bunker, red glow,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, focus pulls from the logged status up to the still-blazing LAUNCH word 0–3s.
His word against the machine's. No camera move. Hold palette.
```

### Scene ch11_s4 — 3s — Petrov sets down the phone (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin lowering the handset back to its
cradle, alone in the red-lit bunker, Mode B, shallow DoF, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure lowers the handset 0–2s and sits back into stillness 2–3s. The
deed done, uncertain. No camera move. Hold palette.
```

**Chapter handoff →** the screen flickers; a second numeral appears — Chapter 12.

---

## CHAPTER 12 — Two, three, four, five  (2:45–3:00)
**Script covered:** "Then the system reports a second missile. Then a third. A fourth. A fifth. The screen now reads five inbound warheads. The siren does not stop."
**SFX:** four escalating alarm stabs, klaxon redoubles · **Ambient:** chaos of tones · **Music:** the motif breaks into five hammering beats

### Scene ch12_s1 — 3s — the second missile appears
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the map board as a second red missile arc snaps into being
beside the first, two trajectories now, dim bunker, intensifying red glow, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the map, a second red arc snaps in at 1s and climbs 1–3s. The picture worsening. No
camera move. Hold palette.
```

### Scene ch12_s2 — 3s — three, four
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the map board with a third and fourth red missile arc
snapping into being in rapid succession, four trajectories climbing, harsh red glow, dim
bunker, Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the map, a third arc snaps in at 0.5s, a fourth at 2s, both climbing. Escalation.
No camera move. Hold palette.
```

### Scene ch12_s3 — 3s — FIVE on the readout
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of the console readout flipping to a red
numeral "5" beside a missile glyph, blazing alarm light, dim bunker, Mode B, high contrast,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the numeral flips 1→…→5 in hard steps 0–2s, then holds blazing 2–3s. The worst
number. No camera move. Hold palette.
```

### Scene ch12_s4 — 3s — the room screams red
1. **CHARACTERS IN SCENE:** Petrov (silhouette)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide shot of the bunker drowning in red alarm light with
five missile tracks blazing on the screen wall, the matte red mannequin a small silhouette
before it, Mode B, extreme contrast, shallow DoF, volumetric light, heavy dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in toward the small red silhouette against five blazing tracks 0–3s, light pulsing
violently. The system at full cry. Hold palette. No new figures.
```

### Scene ch12_s5 — 3s — every machine says "real"
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a bank of Soviet indicators all flipped to red CONFIRM
states in unison, rows of red lights, dim bunker, Mode B, high contrast, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the indicator bank flips red one after another left to right 0–3s. Unanimous machine
verdict. No camera move. Hold palette.
```

### Scene ch12_s6 — 3s — Petrov, unmoved (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, tight on the matte red mannequin's eggshell head and
shoulders, perfectly still amid violent red alarm light, dim bunker, Mode B, high contrast,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static tight, red light hammering across the still red head 0–3s, no movement at all. Stillness
against chaos. No camera move. Hold palette.
```

**Chapter handoff →** against five missiles, he makes the same call again — Chapter 13.

---

## CHAPTER 13 — He holds  (3:00–3:15)
**Script covered:** "Petrov holds. He reports it again as a malfunction."
**SFX:** handset lift again, line static, klaxon under · **Ambient:** klaxon muffled by the call · **Music:** a single sustained low note

### Scene ch13_s1 — 4s — the second call
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin again raising the red handset to its
eggshell head, five missile tracks blazing on the wall behind, dim bunker, Mode B, high
contrast, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure raises the handset against the blazing wall 0–3s and holds 3–4s.
Repeating the refusal, now with five. No camera move. Hold palette.
```

### Scene ch13_s2 — 4s — the general receives it again (white void)
1. **CHARACTERS IN SCENE:** The General (black + uniform)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, the matte black uniformed
general mannequin on the phone, head tilting in disbelief, soft contact shadow, cinematic key
from above, shallow DoF, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the general, head tilting slowly as the impossible report lands 0–4s. The system
hesitating with him. Hold palette. No new figures.
```

### Scene ch13_s3 — 3s — his word logged against five
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the console status reading a logged malfunction beside the
blazing "5 INBOUND" readout, stark contradiction, dim bunker, red glow, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, focus shifts between the logged malfunction and the "5 INBOUND" reading 0–3s.
One man versus five confirmations. No camera move. Hold palette.
```

### Scene ch13_s4 — 3s — phone down, the wait begins (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin lowering the handset and sitting
back, facing the five blazing tracks, alone, dim bunker, Mode B, high contrast, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure lowers the handset and settles to wait 0–3s, the tracks blazing
on. Nothing left to do but wait. No camera move. Hold palette.
```

**Chapter handoff →** time itself becomes the subject — Chapter 14.

---

## CHAPTER 14 — The wait  (3:15–3:35)
**Script covered:** "And then he sits, and he waits, and he watches the clock, knowing that if he is wrong, the first detonations will arrive in minutes, and he will have spent the last quiet moments of the world being stubborn."
**SFX:** a slow loud clock tick, distant city ambience layered under · **Ambient:** klaxon fades to a low throb · **Music:** sparse single piano notes, wide space

### Scene ch14_s1 — 4s — the clock, ticking
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of the console clock's second hand
advancing, every tick heavy, faint red glow, dim bunker, Mode B, shallow DoF, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the second hand advancing 0–4s, each tick deliberate. Time stretched. No
camera move. Hold palette.
```

### Scene ch14_s2 — 4s — Petrov motionless, wide
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide shot of a lone matte red mannequin sitting perfectly
still in the dim alarmed bunker, five tracks faint on the wall, vast stillness, Mode B,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red figure utterly still 0–4s, only dust drifting in the light. Endurance as
action. No camera move. Hold palette.
```

### Scene ch14_s3 — 4s — the sleeping city (the stakes, white)
1. **CHARACTERS IN SCENE:** Civilians (glossy white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, glossy white featureless mannequins asleep in a quiet city
apartment at night — a figure in a bed, a smaller figure nearby — unaware, soft moonlight,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the sleeping white figures 0–4s, curtains stirring faintly. The world that
doesn't know. Hold palette. No new figures.
```

### Scene ch14_s4 — 4s — the city skyline, unaware
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a quiet 1980s city skyline at night, scattered warm
windows, utterly calm, no people visible, Mode B, cool night grade, shallow DoF, volumetric
haze, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Very slow aerial drift over the calm skyline 0–4s, a window light blinking off. Fragile
normalcy. No figures. Hold palette.
```

### Scene ch14_s5 — 4s — back to the still red figure (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of the matte red mannequin watching the clock,
head fixed, the bunker quiet around it, dim, Mode B, shallow DoF, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium on the watching red figure 0–4s, total stillness, the clock implied off-frame.
The longest minutes. No camera move. Hold palette.
```

**Chapter handoff →** the minutes run out; Chapter 15 is what arrives.

---

## CHAPTER 15 — Nothing  (3:35–3:50)
**Script covered:** "The minutes pass. Nothing happens. No flash. No call. The missiles that were never there never arrive. Ground radar… shows an empty sky."
**SFX:** the klaxon cuts out abruptly, ringing silence, one exhaled breath · **Ambient:** pure quiet · **Music:** a single resolving low note, held

### Scene ch15_s1 — 3s — the impact clock hits zero
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the console impact countdown reaching 00:00, and nothing
happening, the readout simply blank, dim bunker, the red glow beginning to fade, Mode B,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the countdown reaches 00:00 at 1s and just holds, empty 1–3s. The absence of
catastrophe. No camera move. Hold palette.
```

### Scene ch15_s2 — 3s — the empty sky (space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a calm dark night sky over Earth from orbit, completely
empty, no missiles, no trails, deep black space with faint stars, cold grade, shallow DoF,
volumetric light rim, dust-free vacuum, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow drift across the empty night sky over Earth 0–3s. Nothing there. Relief made of absence.
No figures. Hold the cold space grade.
```

### Scene ch15_s3 — 3s — the radar, still empty
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the circular ground-radar scope sweeping a clean empty
field, green trace finding nothing across the horizon line, dim bunker, the red glow gone,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the radar completes three clean sweeps 0–3s, empty. Confirmation by silence. No
camera move. Hold palette.
```

### Scene ch15_s4 — 3s — the alarm dies, lights normalize
1. **CHARACTERS IN SCENE:** Petrov (silhouette)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide shot of the bunker as the red alarm light fades to
ordinary dim light, the lone matte red mannequin still seated, the screen wall going dark,
Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5,
octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red alarm light drains from the room 0–3s, the screens going dark, the red
figure unmoved. The storm passing. No camera move. Hold palette.
```

### Scene ch15_s5 — 3s — Petrov, finally moves (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close on the matte red mannequin's shoulders lowering, a
held tension releasing, dim ordinary bunker light, Mode B, shallow DoF, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static tight, the red figure's shoulders lower slowly 0–3s as the tension leaves. Survival,
deadpan. No camera move. Hold palette.
```

**Chapter handoff →** flat declarative beat — Chapter 16 names what happened.

---

## CHAPTER 16 — He was right  (3:50–4:05)
**Script covered:** "Petrov was right. Later, the engineers find the cause. The Oko satellites had caught sunlight glinting off high clouds over the northern United States and read the reflection as the heat of a launch."
**SFX:** quiet daylight room tone, a soft sun-flare swell · **Ambient:** calm · **Music:** a cold, clarifying chord

### Scene ch16_s1 — 3s — flat title beat "He was right"
1. **CHARACTERS IN SCENE:** Petrov (small, centered)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red mannequin seated small and centered in
the quiet dim bunker, ordinary light restored, immense calm negative space, Mode B, shallow
DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static symmetrical wide, the lone red figure still 0–3s, dust drifting. A flat, declarative
beat. No camera move. Hold palette.
```

### Scene ch16_s2 — 4s — the sunlight glint (the cause, space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, sunlight glinting brilliantly off high-altitude clouds
over the dark northern United States, seen from orbit, a bright false bloom of light, the Oko
satellite aperture catching it, deep black space, clinical, shallow DoF, volumetric light rim,
dust-free vacuum, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow track as the sun-glint flares off the clouds into the satellite aperture 0–4s. The lie
the machine believed. No figures. Hold the cold space grade.
```

### Scene ch16_s3 — 3s — the alignment (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of the sun, a
satellite, and a cloud layer aligning along one bright ray to a globe, geometric and cold,
soft contact shadows, cinematic key from above, shallow DoF, volumetric light, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the three elements drift into alignment along the ray 0–3s. A rare, stupid
geometry. No figures. Hold palette.
```

### Scene ch16_s4 — 3s — "the system did what it was built to do"
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the Oko satellite in orbit functioning perfectly, sensor
steady, indifferent, dark Earth below, deep black space, clinical, shallow DoF, volumetric
light rim, dust-free vacuum, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow drift past the satellite working flawlessly 0–3s, utterly indifferent. It saw the wrong
thing, perfectly. No figures. Hold the cold space grade.
```

### Scene ch16_s5 — 3s — Petrov against the working machine (handoff)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin standing and facing the now-quiet
screen wall, small against it, dim bunker, ordinary light, Mode B, shallow DoF, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the red figure facing the dark screen wall 0–3s. Man and machine, both still.
Hold palette. No new figures.
```

**Chapter handoff →** the institution's response — Chapter 17.

---

## CHAPTER 17 — No medal  (4:05–4:20)
**Script covered:** "Petrov is not given a medal… He is quietly reprimanded for a gap in his logbook during the incident… He is reassigned. He takes early retirement."
**SFX:** a stamp on paper, a closing door, footsteps in a corridor · **Ambient:** sterile office tone · **Music:** dry, deflating motif

### Scene ch17_s1 — 4s — the institution turns away (white void)
1. **CHARACTERS IN SCENE:** Petrov (red), Duty Officers (black, several), The General (black + uniform)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a single matte red mannequin
facing a row of matte black mannequins and a uniformed general mannequin who stand turned
slightly away from it, refusing acknowledgment, soft contact shadows, cinematic key from
above, shallow DoF, volumetric light, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow pull-back as the black figures hold their turned-away posture toward the lone red figure
0–4s. Recognition withheld. Hold the color code. No new figures.
```

### Scene ch17_s2 — 3s — the empty medal box
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of an open empty medal presentation box on a
bare desk, velvet interior, no medal inside, sterile office light, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the empty velvet box 0–3s, a slow rack focus to its emptiness. The reward that
wasn't. No camera move. Hold palette.
```

### Scene ch17_s3 — 3s — the reprimand: the logbook
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of an open Soviet duty logbook with a conspicuous
blank gap in the handwritten entries, a red official stamp pressing down beside it, sterile
office light, Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the red stamp presses down beside the blank gap in the logbook 0–3s. Punished
for the gap, not thanked for the world. No camera move. Hold palette.
```

### Scene ch17_s4 — 3s — reassigned, the corridor
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a lone matte red mannequin walking away down a long bare
concrete corridor, small, institutional light, Mode B, shallow DoF, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red figure walks away down the corridor growing smaller 0–3s. Quiet exit. No
camera move. Hold palette.
```

### Scene ch17_s5 — 3s — the door closes (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a plain institutional door at the end of a corridor easing
shut, a thin seam of light narrowing, cold light, Mode B, shallow DoF, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the door eases shut and the seam of light narrows to nothing 0–3s. A career closing.
No camera move. Hold palette.
```

**Chapter handoff →** years pass behind that door — Chapter 18.

---

## CHAPTER 18 — Forgotten  (4:20–4:35)
**Script covered:** "For ten years, no one outside that bunker knows his name. He dies in 2017, in a small apartment outside Moscow, largely forgotten."
**SFX:** a clock ticking down years, faint TV murmur, silence · **Ambient:** small-apartment quiet · **Music:** sparse, fading piano

### Scene ch18_s1 — 4s — ten years pass (white void)
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red mannequin standing alone in an infinite
white void as faint year-markers drift past it like dust, the figure unmoving, soft contact
shadow, cinematic key from above, shallow DoF, volumetric light, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the still red figure as faint year-numbers drift past and fade 0–4s. Time eroding
recognition. Hold palette. No new figures.
```

### Scene ch18_s2 — 4s — the small apartment
1. **CHARACTERS IN SCENE:** Petrov
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin seated alone in a small, plain
apartment, modest furniture, a single window with grey daylight, ordinary and quiet, Mode B,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Very slow push-in on the red figure alone in the apartment 0–4s, grey light, total quiet.
Anonymity. Hold palette. No new figures.
```

### Scene ch18_s3 — 3s — the empty chair (2017)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the same small apartment now with an empty chair where the
red figure sat, grey daylight, stillness, "2017" implied by a calendar on the wall, Mode B,
shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the empty chair 0–3s, dust drifting in the grey light, the calendar faint on the
wall. Absence. No camera move. Hold palette.
```

### Scene ch18_s4 — 3s — the unread story (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single small newspaper notice on a table, headline too
small to read, partly in shadow, no one around, grey light, Mode B, shallow DoF, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro on the small unread notice 0–3s, a slow drift of dust across it. The story almost
no one read. No camera move. Hold palette.
```

**Chapter handoff →** the man is gone; the machine is not — Chapter 19.

---

## CHAPTER 19 — The system is still there  (4:35–4:50)
**Script covered:** "But the system is still there. Some version of it sits in every nuclear state on Earth, scanning the sky, deciding in seconds what takes the rest of us a lifetime to understand. It is faster than us now. It is trusted more than us."
**SFX:** a cold rising server hum, layered global telemetry · **Ambient:** electronic quiet · **Music:** the alarm motif returns, cold and distant

### Scene ch19_s1 — 3s — satellites everywhere (space)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, many early-warning satellites in orbit around the whole
Earth at night, sensors all aimed downward, a web of watching machines, deep black space,
clinical, shallow DoF, volumetric light rim, dust-free vacuum, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow orbital pull-back revealing the full ring of satellites watching Earth 0–3s. The system,
multiplied. No figures. Hold the cold space grade.
```

### Scene ch19_s2 — 4s — identical empty chairs (white void)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a long receding row of
identical empty command chairs before dark consoles, each waiting for someone, soft contact
shadows, cinematic key from above, shallow DoF, volumetric light, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow dolly along the row of empty chairs 0–4s, each identical. The post that always exists. No
figures. Hold palette.
```

### Scene ch19_s3 — 3s — "faster than us" (the machine decides)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a sleek modern threat-assessment screen processing data at
blinding speed, cold blue and red readouts cascading, no human present, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static on the screen as data cascades far faster than a human could read 0–3s. Speed as
authority. No figures. Hold palette.
```

### Scene ch19_s4 — 3s — the world below, unaware (white)
1. **CHARACTERS IN SCENE:** Civilians (glossy white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a wide field of glossy white featureless mannequins going
about ordinary life in a plaza, unaware, watched from above, Mode B, even daylight, shallow
DoF, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow high crane-down over the white crowd in the plaza 0–3s, all oblivious. The watched and
the watcher. Hold palette. No new figures.
```

### Scene ch19_s5 — 3s — one empty chair, waiting (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single empty command chair before a dark console and a
quiet screen wall in standby, faint red glow, waiting, Mode B, shallow DoF, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in toward the empty chair 0–3s, the screen wall in faint red standby. Someone will
sit here. Hold palette. No figures.
```

**Chapter handoff →** the final turn lands in that empty chair — Chapter 20.

---

## CHAPTER 20 — The man in the chair  (4:50–5:05)
**Script covered:** "And the next time it sees something that isn't there, the man in the chair may decide to believe it."
**SFX:** a single distant alarm tone fading, then silence · **Ambient:** dead quiet · **Music:** the motif resolves to one unresolved held note

### Scene ch20_s1 — 4s — a new figure sits down
1. **CHARACTERS IN SCENE:** Civilian (glossy white) — an anonymous new operator
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, an anonymous glossy white featureless mannequin lowering
itself into the command chair before a dark modern console, faint red standby glow, replacing
the one who came before, Mode B, shallow DoF, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the white figure settles into the chair 0–3s and goes still facing the console
3–4s. A new, unknown hand on the decision. Hold palette. No new figures.
```

### Scene ch20_s2 — 4s — the screen flickers a false bloom
1. **CHARACTERS IN SCENE:** Civilian (glossy white, from behind)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, over-the-shoulder of the glossy white operator as a single
red alert begins to bloom on the dark screen wall, the start of another warning, Mode B, red
glow rising, shallow DoF, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static over-the-shoulder, a red alert blooms on the screen wall 0–4s, light rising on the
still white figure. History about to repeat. Hold palette. No new figures.
```

### Scene ch20_s3 — 4s — the hand over the phone (will they believe it?)
1. **CHARACTERS IN SCENE:** Civilian (glossy white, hand)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a glossy white mannequin hand hovering over a
red telephone handset, the choice unmade, red alert glow, dark console, Mode B, shallow DoF,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the white hand hovers over the red handset 0–4s and does not decide. The
question left open. No camera move. Hold palette.
```

### Scene ch20_s4 — 3s — final image: the lit screen, the still figure (end card)
1. **CHARACTERS IN SCENE:** Civilian (glossy white, silhouette)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, wide final shot of a small glossy white figure silhouetted
before a screen wall glowing with a single red alert, vast dark room, immense negative space,
unresolved, Mode B, shallow DoF, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Very slow push-in toward the small silhouetted figure before the red-lit screen wall 0–3s,
then hold and cut to black. End on the unresolved image. Hold palette. No new figures.
```

**Final handoff →** cut to black on the held note. The umbra. wordmark resolves last. No
"thanks for watching", no resolution.

---

Type "next" for thumbnail prompts.
