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

## Chapter map (5:00 = 20 chapters × 15 s, derived from the narration)

Windows come from the script's actual word timeline, **not** one paragraph per chapter: narration
runs 2.5 words/s, so every 15 s chapter carries ≤37 words of VO (720 words ≈ 4:48 in total; the
~12 s of slack is absorbed as breathing room). Dense paragraphs therefore span two chapters.

| Ch | Time | Script beat (VO in this window) | Mode | Scenes |
|----|------|---------------------------------|------|--------|
| 01 | 0:00–0:15 | Cold open — the flat, the dial-in, the "safe" network | B flat | 5 |
| 02 | 0:15–0:30 | "Wau" + anchor — 135,000 marks out, every mark back | B/A | 4 |
| 03 | 0:30–0:45 | Bildschirmtext: the Bundespost's TV-as-terminal | B/A | 5 |
| 04 | 0:45–1:00 | News, weather, banking; "a fortune"; "Btx is secure." | B/A | 5 |
| 05 | 1:00–1:15 | Wau doesn't believe them; the Chaos Computer Club | B/A | 4 |
| 06 | 1:15–1:30 | The argument: "secure" means unbreakable — and they found a way | A | 4 |
| 07 | 1:30–1:45 | The flaw: overfill a page and the system stumbles | A | 4 |
| 08 | 1:45–2:00 | Ghost characters spill; a bank's login in the clear | B | 5 |
| 09 | 2:00–2:15 | Password "USD 70000"; providers may charge per page | B/A | 5 |
| 10 | 2:15–2:30 | 9.97 DM a look; the 31-line program | A/B | 5 |
| 11 | 2:30–2:45 | It loops; they sleep; by morning… | B | 4 |
| 12 | 2:45–3:00 | 13,000+ calls, ~134,000 DM moved | A/B | 4 |
| 13 | 3:00–3:15 | No alarm — nothing "broke"; "They do not keep it" | A/B | 4 |
| 14 | 3:15–3:30 | 19 November: the press conference, the cameras | B | 5 |
| 15 | 3:30–3:45 | They return every mark; "the point was the word" | B | 4 |
| 16 | 3:45–4:00 | Overnight fame; the Bundespost: "minor" | B | 5 |
| 17 | 4:00–4:15 | CCC: "the whole argument"; Btx never recovers | A/B | 5 |
| 18 | 4:15–4:30 | Switched off in 2001; the argument didn't switch off | B | 4 |
| 19 | 4:30–4:45 | "Safe," every year since | A | 5 |
| 20 | 4:45–5:00 | Implicating close — overfill the page, watch what spills | B | 4 |

> Chapters 01–04 are fully built below as the worked pattern. Expand 05–20 identically
> (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per 2–4 s scene), then run
> `tools/build-shotlist.py umbra ep03-ghost-characters` **and** `tools/export-episode.py
> umbra ep03-ghost-characters` (CI regenerates both and fails on drift).

---

## CHAPTER 01 — The dial-in  (0:00–0:15)
**Script covered (37 words ≈ 14.8 s):** "It's the night of the 16th of November, 1984. In a flat in Hamburg, a man sits at a home computer, dials a telephone line, and connects to a network the German state has promised is safe."
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

**Chapter handoff →** hold on the unremarkable room; cut to the name and the anchor line of Chapter 02.

---

## CHAPTER 02 — A hundred and thirty-five thousand marks  (0:15–0:30)
**Script covered (36 words ≈ 14.4 s):** "His name is Herwart Holland. They call him Wau. This is the story of how two men moved a hundred and thirty-five thousand marks out of a bank in one night, and gave every mark back."
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
**Script covered (35 words ≈ 14 s):** "The network is called Bildschirmtext — screen text, Btx for short. It is West Germany's picture of the future: a nationwide system, run by the Deutsche Bundespost, that turns an ordinary television into a terminal."
**SFX:** cheerful 1980s ad jingle fragment, a TV click, a modem chirp · **Ambient:** living-room room tone · **Music:** bright period synth turning cold underneath

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

### Scene ch03_s3 — 3s — the Bundespost runs it
1. **CHARACTERS IN SCENE:** The Bundespost Official (black)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform and peaked cap (small posthorn emblem) standing beside the central node of a white-void
network diagram, a rubber stamp held at rest in one hand, soft contact shadow, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the black official standing motionless by the node 0–3s, the stamp held at rest.
The state, in charge. Hold the color code. No new figures.
```

### Scene ch03_s4 — 3s — an ordinary television becomes a terminal
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of the back of a plain boxy 1980s television
with a small grey modem box and a coiled cable plugged into it, the screen beyond waking from
static, a tidy living room, warm domestic light, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the static on the screen resolves into a blocky Btx menu 0–3s as the modem's
status light settles. An ordinary television, quietly made into something else. No figures. Hold
palette.
```

### Scene ch03_s5 — 3s — the red figure watches the screen (handoff)
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the matte red mannequin at his CRT, the blocky Btx menu
screen reflected across its red eggshell head, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the red figure as the menu screen plays across its head 0–3s. The man who
doesn't believe it. Hold palette. No new figures.
```

**Chapter handoff →** the reflected menu scrolls into the news page that opens Chapter 04.

---

## CHAPTER 04 — The promise  (0:45–1:00)
**Script covered (37 words ≈ 14.8 s):** "You can read the news on it. Check the weather. From 1984, do your banking. The Post Office has spent a fortune building it, and it tells the public one thing above all else. Btx is secure."
**SFX:** soft menu blips, a coin drop, a stamp thud on the last line · **Ambient:** living-room room tone, TV hum · **Music:** bright period synth, turning cold as the stamp lands

### Scene ch04_s1 — 4s — the news, then the weather
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glossy white mannequin seated in a tidy 1980s living room
before a boxy television showing a blocky colorful Btx news page, a small numeric keypad in its
hand, warm domestic light, Mode B, shallow depth of field, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa,
16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the TV page flips from the news page to a blocky weather page with simple sun and
cloud blocks 0–4s as the white mannequin thumbs the keypad. Ordinary, pleasant. Hold palette. No
new figures.
```

### Scene ch04_s2 — 2s — banking
1. **CHARACTERS IN SCENE:** The Btx User (hand)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a glossy white mannequin hand on a numeric keypad
before a television showing a blocky banking page with a column of numerals, warm domestic light,
Mode B, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the white fingers press two keys and the balance digits tick over 0–2s. Money, on
the television. No camera move. Hold palette.
```

### Scene ch04_s3 — 4s — a fortune spent building it (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a tall stack of plain matte
currency blocks beside a growing web of thin cables branching out to many small television icons,
the stack visibly lower than before, cold clinical light, soft contact shadows, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the currency stack sinks 0–4s as cables extend and light the television icons one
by one. A fortune, poured into a promise. No figures. Hold palette.
```

### Scene ch04_s4 — 3s — the Bundespost stamps it
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

### Scene ch04_s5 — 2s — "SECURE" (the word)
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
Locked macro, the wet seal settles on the page 0–2s, edges sharpening. One word, guaranteed. No
figures. Hold palette.
```

**Chapter handoff →** the seal sets and holds on the stamped word; cut to the red figure who does not
believe it (Chapter 05).

---

> **Chapters 05–20:** expand identically (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per scene),
> keeping The Hacker red, Bundespost/Bank black, the public/press white. Then run
> `tools/build-shotlist.py umbra ep03-ghost-characters` and
> `tools/export-episode.py umbra ep03-ghost-characters`.

Type "next" for thumbnail prompts.
