# STATE 5 — Visual flow + scenes

**STYLE ANCHOR (constant for the whole video):**
```
Mannequin world — glossy white civilians / matte red protagonist (The Hacker) / matte black
institution (Bundespost + bank), eggshell featureless heads, Mode B sparse 1980s photoreal
(a Hamburg flat, boxy computers, Btx TV terminals) + Mode A white-void diagram inserts, cool
CRT-green/amber screen glow accent, cinematic key from above, shallow DoF, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
ARRI Alexa, 16:9.
```

**CHARACTER LOCK:** The Hacker (red) · The Btx User (white + TV terminal) · The Journalist
(white + microphone) · The Bundespost Official + The Banker (black) · The Postal Investigator
(black + technical). Same render/wardrobe every scene; reference the saved elements in
`production/shotlist.json`.

---

## Chapter map (≈5:00 → 20 chapters × ~15 s)

| Ch | Time | Script beat | Mode | Scenes |
|----|------|-------------|------|--------|
| 01 | 0:00–0:15 | Cold open — the flat, the dial-in, "Wau" | B flat | 5 |
| 02 | 0:15–0:30 | Anchor — 135,000 marks out, and all of it back | B/A | 4 |
| 03 | 0:30–0:45 | Bildschirmtext: the TV as terminal; "Btx is secure" | B/A | 5 |
| 04 | 0:45–1:00 | The Chaos Computer Club and its argument with the state | A | 5 |
| 05 | 1:00–1:15 | The flaw: overfill a page and the system stumbles | A | 4 |
| 06 | 1:15–1:30 | Ghost characters spill onto the screen | B | 5 |
| 07 | 1:30–1:45 | In the spill: the bank's login — password "USD 70000" | B | 4 |
| 08 | 1:45–2:00 | The paid-page mechanism: 9.97 DM a look | A | 5 |
| 09 | 2:00–2:15 | The 31-line program | B | 4 |
| 10 | 2:15–2:30 | They leave it running and go to sleep | B | 4 |
| 11 | 2:30–2:45 | By morning: 13,000+ calls, ~134,000 DM moved | A/B | 5 |
| 12 | 2:45–3:00 | No alarm — nothing "broke" | A | 4 |
| 13 | 3:00–3:15 | The turn — they don't keep it | B | 4 |
| 14 | 3:15–3:30 | 19 November: the press conference, the cameras | B | 5 |
| 15 | 3:30–3:45 | They return every mark, in full | B | 4 |
| 16 | 3:45–4:00 | Overnight, the most famous hackers in the country | B | 5 |
| 17 | 4:00–4:15 | Bundespost: "minor." CCC: "the whole argument." | A/B | 5 |
| 18 | 4:15–4:30 | Btx never recovers; switched off in 2001 | B | 4 |
| 19 | 4:30–4:45 | The argument didn't switch off: "secure," every year since | A | 5 |
| 20 | 4:45–5:05 | Implicating close — overfill the page, watch what spills | B | 4 |

> Chapters 01–03 are fully built below as the worked pattern. Expand 04–20 identically
> (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per 2–4 s scene), then run
> `tools/build-shotlist.py umbra ep03-ghost-characters` to regenerate the shotlist.

---

## CHAPTER 01 — The dial-in  (0:00–0:15)
**Script covered:** "It's the night of the 16th of November, 1984… connects to a network the German state has promised is safe. His name is Herwart Holland. The people around him call him Wau."
**SFX:** modem handshake tones, a single key clack, a wall clock · **Ambient:** quiet night flat, faint street hum · **Music:** low patient synth drone, one cold pulse

### Scene ch01_s1 — 3s — wide, the flat at night
1. **CHARACTERS IN SCENE:** The Hacker (small, at a desk)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a dim 1980s Hamburg flat at night, a single matte red
mannequin (eggshell head, red cardigan) seated at a cluttered desk before a boxy home computer,
the only light the cool glow of the CRT, sparse Mode B, shallow depth of field, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, very slow push-in toward the red mannequin lit by the screen 0–3s. Dust drifts in
the CRT glow. Quiet, ordinary, nocturnal. Hold color code and wardrobe. No new figures.
```

### Scene ch01_s2 — 3s — the telephone handset into the modem
1. **CHARACTERS IN SCENE:** The Hacker (hands only)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of matte red mannequin hands pressing a
1980s telephone handset into the rubber cups of an acoustic modem, a single status LED lit,
cool desk light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the red hands seat the handset 0–2s, the LED blinks to steady 2–3s. Connection
being made. No camera move. Deadpan, slow. Hold palette.
```

### Scene ch01_s3 — 3s — the screen wakes
1. **CHARACTERS IN SCENE:** The Hacker (over-shoulder)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, over-the-shoulder of a matte red mannequin facing a boxy CRT
that wakes to a blocky 1980s videotex login screen in cool green and amber, screen glow on the
red eggshell head, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static over-the-shoulder, blocky videotex characters paint onto the screen line by line 0–3s,
color glow flickering on the red head. No camera move. Hold palette.
```

### Scene ch01_s4 — 3s — he begins to type
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, medium shot of a matte red mannequin (red cardigan, round
red glasses, eggshell head) leaning toward the CRT and typing on a chunky keyboard, calm and
absorbed, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Medium static, the red mannequin's fingers move over the keys 0–3s, head tilted to the screen,
unremarkable. No camera move. Hold palette.
```

### Scene ch01_s5 — 3s — the ordinary room around him (handoff)
1. **CHARACTERS IN SCENE:** The Hacker (small)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a calm wide of the quiet flat, the lone matte red mannequin
at his glowing desk among bookshelves and coffee cups, an ordinary night, Mode B, shallow depth
of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow pull-back from the red figure revealing the calm ordinary room 0–3s. Nothing seems to be
happening. Hold palette. No new figures.
```

**Chapter handoff →** hold on the unremarkable room; cut to the anchor line of Chapter 02.

---

## CHAPTER 02 — A hundred and thirty-five thousand marks  (0:15–0:30)
**Script covered:** "This is the story of how two men moved a hundred and thirty-five thousand marks out of a bank in a single night, and gave every last one of them back."
**SFX:** a deep impact hit on the anchor line, coins settling, then silence · **Ambient:** thinning room tone · **Music:** drone lifts a step, a single struck note

### Scene ch02_s1 — 4s — STYLE ANCHOR / title beat
1. **CHARACTERS IN SCENE:** The Hacker (tiny, centered)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte red mannequin seated very small and centered
at a desk in a vast dark space, immense negative space, one shaft of cool screen light, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static symmetrical wide, almost still. Imperceptible push-in 0–4s; dust drifts in the light. The
lone red figure motionless. Title-card emptiness. Hold palette. No new figures.
```

### Scene ch02_s2 — 4s — money leaves (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of stylized matte
currency notes flowing along a single line from a black bank vault icon toward a small red folder
icon, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the notes slide from the black vault to the red folder 0–4s. Money moving the
wrong way. No figures. Hold palette.
```

### Scene ch02_s3 — 4s — and all of it back (the line reverses)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, the same diagram now reversed —
the stylized currency notes flowing back from the red folder icon into the black bank vault icon,
cold clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the notes reverse and flow back into the vault 0–4s. A robbery that undoes
itself. No figures. Hold palette.
```

### Scene ch02_s4 — 3s — the red figure, unreadable (handoff)
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a close, near-symmetrical shot of the matte red mannequin's
eggshell head lit by cool screen glow in the dark, utterly still, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static close, the red head motionless as screen light shifts across it 0–3s. Motive withheld.
No camera move. Hold palette.
```

**Chapter handoff →** push into the CRT; the screen becomes the promise of Bildschirmtext.

---

## CHAPTER 03 — Bildschirmtext  (0:30–0:45)
**Script covered:** "The network is called Bildschirmtext… a nationwide system, run by the Deutsche Bundespost, that turns an ordinary television into a terminal… The Post Office tells the public one thing above all else. Btx is secure."
**SFX:** cheerful 1980s ad jingle fragment, a TV click, a stamp thud · **Ambient:** living-room room tone · **Music:** bright period synth turning cold underneath

### Scene ch03_s1 — 3s — the living-room terminal
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glossy white mannequin seated in a tidy 1980s living room
before a boxy television showing a blocky colorful Btx menu, a small numeric keypad in its hand,
warm domestic light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the white mannequin thumbs the keypad and the Btx menu changes on the TV 0–3s.
The future, at home. Hold palette. No new figures.
```

### Scene ch03_s2 — 3s — a nation of terminals (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of many small
television icons across a stylized map of West Germany, each linked by thin lines to one central
node, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the links light up one by one from the central node to the TVs 0–3s. A whole
country wired to one system. No figures. Hold palette.
```

### Scene ch03_s3 — 3s — the Bundespost stamps it secure
1. **CHARACTERS IN SCENE:** The Bundespost Official (black)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform and peaked cap (small posthorn emblem), pressing a rubber stamp down onto a document on a
counter, infinite white void, soft contact shadow, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black official brings the stamp down and holds it 0–3s. The state's guarantee,
pressed onto paper. Hold the color code. No new figures.
```

### Scene ch03_s4 — 3s — "SECURE" (the word)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a freshly stamped document in white void,
a single blocky official seal reading as a bold mark, cold clinical light, soft contact shadow,
cinematic key from above, shallow depth of field, volumetric light, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the wet seal settles on the page 0–3s, edges sharpening. One word, guaranteed. No
figures. Hold palette.
```

### Scene ch03_s5 — 3s — the red figure watches the promise (handoff)
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the matte red mannequin at his CRT, the blocky Btx promise
screen reflected across its red eggshell head, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the red figure as the promise screen plays across its head 0–3s. The man who
doesn't believe it. Hold palette. No new figures.
```

**Chapter handoff →** the reflected promise narrows to a single overfilled page; Chapter 04
introduces the Chaos Computer Club and the argument.

---

> **Chapters 04–20:** expand identically (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per scene),
> keeping The Hacker red, Bundespost/Bank black, the public/press white. Then run
> `tools/build-shotlist.py umbra ep03-ghost-characters`.

Type "next" for thumbnail prompts.
