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
runs 2.5 words/s, so every 15 s chapter carries ≤37 words of VO (732 words ≈ 4:53 in total; the
~8 s of slack is absorbed as breathing room). Dense paragraphs therefore span two chapters.

| Ch | Time | Script beat (VO in this window) | Mode | Scenes |
|----|------|---------------------------------|------|--------|
| 01 | 0:00–0:15 | Cold open — the flat, the dial-in, the "safe" network | B flat | 5 |
| 02 | 0:15–0:30 | "Wau" + anchor — 135,000 marks out, every mark back | B/A | 4 |
| 03 | 0:30–0:45 | Bildschirmtext: the Bundespost's TV-as-terminal | B/A | 5 |
| 04 | 0:45–1:00 | News, weather, banking; "a fortune"; "Btx is secure." | B/A | 5 |
| 05 | 1:00–1:15 | Wau doesn't believe them; the Chaos Computer Club's argument | B/A | 4 |
| 06 | 1:15–1:30 | "Secure" means unbreakable — they found a way; the flaw, almost too small to see | A | 4 |
| 07 | 1:30–1:45 | Overfill a page: the system stumbles and spills foreign data | A | 4 |
| 08 | 1:45–2:00 | Ghost characters — by the club's account, a bank's login in the clear | B | 5 |
| 09 | 2:00–2:15 | Password "USD 70000"; providers may charge per page | B/A | 5 |
| 10 | 2:15–2:30 | 9.97 DM a look; the 31-line program | A/B | 5 |
| 11 | 2:30–2:45 | It loops; they sleep; by morning… | B | 4 |
| 12 | 2:45–3:00 | 13,000+ calls, ~134,000 DM moved | A/B | 4 |
| 13 | 3:00–3:15 | No alarm — nothing "broke"; the system did what it was told | A/B | 4 |
| 14 | 3:15–3:30 | They do not keep it; 19 November: the press conference, the cameras | B | 5 |
| 15 | 3:30–3:45 | They return every mark; "the point was the word" | B | 4 |
| 16 | 3:45–4:00 | Overnight fame; the Bundespost: "minor" | B | 5 |
| 17 | 4:00–4:15 | CCC: "the whole argument" — a 19,000-user network, two men | A/B | 5 |
| 18 | 4:15–4:30 | An inquiry never proves how they got the password; Btx dies in 2001 | B | 4 |
| 19 | 4:30–4:45 | "Safe," every year since | A | 5 |
| 20 | 4:45–5:00 | Implicating close — still overfilling the page; no one ever proved the password came from it | B | 4 |

> All 20 chapters are built below (CHARACTERS → IMAGE PROMPT → VIDEO PROMPT per 2–4 s scene).
> After editing any scene, regenerate both artifacts (CI regenerates them and fails on drift):
>
> `tools/build-shotlist.py umbra ep03-ghost-characters`
>
> `tools/export-episode.py umbra ep03-ghost-characters`

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
Cinematic photorealistic 3D render, a calm wide of a small dim 1980s Hamburg flat at night, the
lone matte red mannequin (eggshell head, red cardigan, round red glasses) seated at a cluttered
desk before a boxy beige home computer whose CRT screen is the main light, a low bookshelf and a
ceramic coffee mug nearby, an ordinary night, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
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

## CHAPTER 05 — The man who doesn't believe them  (1:00–1:15)
**Script covered (36 words ≈ 14.4 s):** "Wau Holland does not believe them. He belongs to a small group of hackers who call themselves the Chaos Computer Club, and their argument with the state is simple. A system is not secure because an"
**SFX:** a chair creak, paper rustle, a single typed line · **Ambient:** a cramped club room, rain on a window · **Music:** the drone returns, patient and low

### Scene ch05_s1 — 4s — the red figure turns from the screen
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin (eggshell head, red cardigan, round
red glasses) at his desk turning slightly away from a glowing CRT showing a stamped Btx page,
unconvinced posture, dim 1980s Hamburg flat, Mode B, shallow depth of field, volumetric light,
dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot
on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red mannequin slowly turns its head away from the screen 0–4s. Disbelief,
without a face. No camera move. Hold palette. No new figures.
```

### Scene ch05_s2 — 4s — the club room
1. **CHARACTERS IN SCENE:** The Hacker (two red figures)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a cramped 1980s club room crowded with boxy computers,
cables, and stacked magazines, two matte red mannequins (eggshell heads, 1980s casual
silhouettes) seated side by side at a long table under a single hanging lamp, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow lateral dolly along the table past the two red figures at their machines 0–4s. A small
group, nobody official. Hold palette. No new figures.
```

### Scene ch05_s3 — 4s — the argument (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a black rubber
stamp icon on the left and a small red padlock icon on the right, a single thin line between
them breaking in the middle, cold clinical light, soft contact shadows, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the line from the stamp to the padlock cracks and parts 0–4s. Saying is not
proving. No figures. Hold palette.
```

### Scene ch05_s4 — 3s — the official, unmoved (handoff)
1. **CHARACTERS IN SCENE:** The Bundespost Official
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform and peaked cap (small posthorn emblem) standing squarely with hands clasped, a stamped
document on a counter beside it, infinite white void, soft contact shadow, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black official stands perfectly still 0–3s as the light dims a step around it. The
state, saying so. Hold the color code. No new figures.
```

**Chapter handoff →** the official's stillness holds; cut to the definition of "secure" in Chapter 06.

---

## CHAPTER 06 — Unbreakable  (1:15–1:30)
**Script covered (36 words ≈ 14.4 s):** "official says it is. It is secure only if it cannot be broken. And they have found a way to break this one. The flaw is almost too small to see. When a Btx page is"
**SFX:** a hairline crack, a low hum, a held breath of silence · **Ambient:** white-void hush · **Music:** a single sustained tone, rising

### Scene ch06_s1 — 4s — a sealed block (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a single solid matte block
labelled only by a blocky Btx emblem, perfectly sealed, resting on the floor of the void, cold
clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the sealed block 0–4s. Solid, closed, unbroken. No figures. Hold palette.
```

### Scene ch06_s2 — 4s — a hairline crack
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, extreme close-up of the same
solid matte block, a single hairline crack running across its surface, catching the light, cold
clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the hairline crack lengthens a few millimetres 0–4s. Something that should not
open, opening. No figures. Hold palette.
```

### Scene ch06_s3 — 4s — the red hand on the keys
1. **CHARACTERS IN SCENE:** The Hacker (hands only)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of matte red mannequin hands resting on a
chunky 1980s keyboard, the cool glow of a CRT on the keys, dim Hamburg flat at night, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, one red finger presses a single key and holds 0–4s. Quiet intent. No camera move.
Hold palette.
```

### Scene ch06_s4 — 3s — a page, magnified (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a blocky 1980s videotex page on a CRT,
coarse coloured mosaic characters filling the screen edge to edge, scanlines visible, dark room,
Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Very slow push-in on the page until the mosaic blocks fill the frame 0–3s. Too small to see,
until you look. No figures. Hold palette.
```

**Chapter handoff →** the mosaic characters fill the frame; the page begins to overfill in Chapter 07.

---

## CHAPTER 07 — Overfill  (1:30–1:45)
**Script covered (37 words ≈ 14.8 s):** "filled with more text than it expects, the system stumbles. For a fraction of a second, the overflow spills onto the screen — fragments of data from somewhere else inside the machine, characters that were never meant"
**SFX:** a modem stutter, a glitch crackle, a flat electronic tick · **Ambient:** CRT whine · **Music:** drone tightening, one detuned note

### Scene ch07_s1 — 4s — too much text (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a single
page-shaped container filling with stacked blocky characters, the stack rising above its rim,
cold clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, characters stack into the page and rise past its edge 0–4s. More than it was
built to hold. No figures. Hold palette.
```

### Scene ch07_s2 — 3s — the system stumbles
1. **CHARACTERS IN SCENE:** The Hacker (over-shoulder)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, over-the-shoulder of a matte red mannequin facing a boxy CRT
where a blocky videotex page has frozen mid-draw, a band of torn scanlines across it, cool green
screen glow, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static over-the-shoulder, the page judders and freezes mid-draw 0–3s. A stumble. No camera move.
Hold palette.
```

### Scene ch07_s3 — 4s — the spill
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a CRT screen where stray blocky
characters in mismatched colours leak below the edge of a videotex page into the black margin,
scanlines visible, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, foreign characters trickle out below the page into the dark margin 0–4s, a
fraction of a second stretched. No figures. Hold palette.
```

### Scene ch07_s4 — 4s — from somewhere else inside the machine (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a black
machine box with many small internal compartments, a few loose characters escaping from one
compartment through a thin line out to a single screen icon, cold clinical light, soft contact
shadows, cinematic key from above, shallow depth of field, volumetric light, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, a few characters slip from one compartment along the line to the screen 0–4s.
Data that was never meant to leave. No figures. Hold palette.
```

**Chapter handoff →** the escaped characters land on the screen; they become the ghost characters of Chapter 08.

---

## CHAPTER 08 — Ghost characters  (1:45–2:00)
**Script covered (37 words ≈ 14.8 s):** "for your eyes. Ghost characters. And one night, the club says, that spill shows them something remarkable: the login and the password of another Btx account, printed in the clear. The account belongs to the Hamburger Sparkasse."
**SFX:** a faint static hiss, a keyboard stops, one low hit on "Sparkasse" · **Ambient:** the night flat, a distant car · **Music:** drone drops to near silence

### Scene ch08_s1 — 3s — ghost characters
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a dark CRT where faint, half-formed
blocky characters hang over a videotex page like an afterimage, pale and translucent, scanlines
visible, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the faint characters flicker in and out like an afterimage 0–3s. Ghosts on glass.
No figures. Hold palette.
```

### Scene ch08_s2 — 3s — one night
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a wide of the dim Hamburg flat at night, the matte red
mannequin leaning very close to the glowing CRT, the room otherwise dark, Mode B, shallow depth
of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red figure leans in toward the screen and stops 0–3s. Something has appeared.
No camera move. Hold palette. No new figures.
```

### Scene ch08_s3 — 3s — a login, in the clear
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a CRT showing two lines of blocky green
text, an account login and a password field filled in plainly, no masking, scanlines visible,
Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the two lines of text settle into focus 0–3s. Nothing hidden. No figures. Hold
palette.
```

### Scene ch08_s4 — 3s — the red figure reads it
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a close shot of the matte red mannequin's eggshell head and
round red glasses, the green lines of a CRT reflected across them, dark room, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static close, the reflected green text crawls across the red head 0–3s. Reading. No camera move.
Hold palette.
```

### Scene ch08_s5 — 3s — the bank (handoff)
1. **CHARACTERS IN SCENE:** The Banker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a plain 1980s banker's
three-piece suit holding a slim ledger, standing stiffly before a tall blank black vault door,
infinite white void, soft contact shadow, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the black banker standing still before the vault 0–3s. The account belongs to a
bank. Hold the color code. No new figures.
```

**Chapter handoff →** the vault door holds; the password itself fills the screen in Chapter 09.

---

## CHAPTER 09 — USD 70000  (2:00–2:15)
**Script covered (36 words ≈ 14.4 s):** "A bank. The password is "USD 70000." After that, the rest is almost trivial. On Btx, a provider is allowed to charge visitors to open its page — a few marks a look. The Chaos Computer"
**SFX:** one dry key clack per character of the password, then a coin drop · **Ambient:** room tone · **Music:** drone steps up, a dry pulse

### Scene ch09_s1 — 3s — the password
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a CRT showing a single line of blocky
green characters reading USD 70000 in a plain password field, scanlines visible, dark room, Mode
B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the characters U S D 7 0 0 0 0 appear one at a time 0–3s. That is all it is. No
figures. Hold palette.
```

### Scene ch09_s2 — 3s — almost trivial
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a medium shot of the matte red mannequin sitting back in his
chair at the glowing desk, hands resting in his lap, the CRT showing the login screen, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure leans back from the keyboard 0–3s. The hard part is over. No
camera move. Hold palette. No new figures.
```

### Scene ch09_s3 — 3s — a page that charges (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a single page
icon with a small coin slot on its edge, a thin line from a viewer screen icon passing through
the slot, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, a coin drops through the slot as the line opens the page 0–3s. Pay to look. No
figures. Hold palette.
```

### Scene ch09_s4 — 3s — a few marks a look
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glossy white mannequin in a tidy 1980s living room opening
a page on a boxy television, a small coin-shaped charge notice in the corner of the blocky
screen, warm domestic light, Mode B, shallow depth of field, volumetric light, dust particles,
cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa,
16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the white mannequin presses a key and the charge notice blinks on the TV 0–3s.
Ordinary, priced. Hold palette. No new figures.
```

### Scene ch09_s5 — 3s — the club's own page (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a CRT showing a blocky videotex page with a
plain red header block and a price in the corner, dark room, scanlines visible, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the red-headed page paints in line by line 0–3s. A page of their own. No figures. Hold
palette.
```

**Chapter handoff →** the price in the corner holds; Chapter 10 reads it out.

---

## CHAPTER 10 — Thirty-one lines  (2:15–2:30)
**Script covered (36 words ≈ 14.4 s):** "Club owns such a page. It costs nine marks and ninety-seven pfennig to open. So they write a short program. Thirty-one lines. It logs in as the Hamburger Sparkasse, and it opens the club's own page."
**SFX:** dot-matrix printer chatter, rapid key clacks, a modem connect tone · **Ambient:** night flat, the printer's carriage · **Music:** a steady mechanical pulse begins

### Scene ch10_s1 — 3s — 9.97 DM
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a blocky videotex price field on a CRT
reading 9,97 DM, coarse mosaic characters, scanlines visible, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the price field blinks once and holds 0–3s. A small number. No figures. Hold
palette.
```

### Scene ch10_s2 — 3s — the program
1. **CHARACTERS IN SCENE:** The Hacker (hands only)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of matte red mannequin hands typing quickly
on a chunky 1980s keyboard, short lines of green code scrolling on a CRT behind, cool desk
light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the red fingers type in short bursts 0–3s as lines of code scroll up. Small work.
No camera move. Hold palette.
```

### Scene ch10_s3 — 3s — thirty-one lines
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a dot-matrix printout of a short
program, a column of numbered lines ending at 31, the tractor-feed paper curling over a desk
edge, dim light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow tilt down the printout from line 1 to line 31 0–3s. That is the whole of it. No figures.
Hold palette.
```

### Scene ch10_s4 — 3s — it logs in as the bank (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a small red
program icon wearing a black bank-vault badge, passing through a black gate toward a Btx node,
cold clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the red program icon slides through the black gate wearing the bank's badge
0–3s. Let in as someone else. No figures. Hold palette.
```

### Scene ch10_s5 — 3s — and opens the club's page (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a thin line
running from a black bank-vault icon to a single page icon with a red header and a small coin
slot, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the line connects and the page opens 0–3s; one coin drops. Once. No figures.
Hold palette.
```

**Chapter handoff →** the single coin settles; the loop begins in Chapter 11.

---

## CHAPTER 11 — Again  (2:30–2:45)
**Script covered (36 words ≈ 14.4 s):** "Then it does it again. And again. They leave it running, and they go to sleep. By morning, the bank has opened a single page more than thirteen thousand times, and paid the Chaos Computer Club"
**SFX:** a modem tone repeating on a loop, a light switch, a clock ticking · **Ambient:** an empty room, the machine humming alone · **Music:** the pulse repeats, unchanging

### Scene ch11_s1 — 4s — again, and again (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a circular
loop arrow running from a black bank-vault icon to a red-headed page icon and back, a stream of
small coins dropping at the page, cold clinical light, soft contact shadows, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the loop cycles again and again 0–4s, a coin dropping on every pass. No figures.
Hold palette.
```

### Scene ch11_s2 — 4s — they go to sleep
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a wide of the dim Hamburg flat at night, the matte red
mannequin standing at the doorway with one hand on the light switch, the CRT still glowing on
the desk, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red figure flicks the switch off and leaves the frame 0–4s; only the screen
stays lit. No camera move. Hold palette. No new figures.
```

### Scene ch11_s3 — 4s — the machine works alone
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the empty dark desk, a boxy home computer and acoustic modem
alone in a pool of CRT light, the status LED blinking, an empty chair pushed back, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the modem LED blinks in a steady rhythm and the screen refreshes 0–4s. Nobody watching.
No figures. Hold palette.
```

### Scene ch11_s4 — 3s — by morning (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the same empty desk at first light, pale grey dawn through
the window, the CRT still glowing, a cold cup of coffee, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static, dawn light slowly rises across the desk 0–3s while the screen keeps refreshing. Hours
have passed. No figures. Hold palette.
```

**Chapter handoff →** the screen refreshes one more time; the counter appears in Chapter 12.

---

## CHAPTER 12 — Thirteen thousand times  (2:45–3:00)
**Script covered (37 words ≈ 14.8 s):** "nine marks and ninety-seven pfennig for every one. The total is a little over a hundred and thirty-four thousand marks. The money has moved out of one of Germany's largest banks and into the account of a"
**SFX:** an accelerating counter tick, coins pouring, then a hard stop · **Ambient:** morning room tone · **Music:** pulse holds, then a low swell

### Scene ch12_s1 — 4s — the counter
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a blocky videotex counter on a CRT,
digits rolling past 13000, scanlines visible, pale dawn light on the glass, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the counter rolls upward past thirteen thousand 0–4s. Every one billed. No
figures. Hold palette.
```

### Scene ch12_s2 — 4s — the total (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of thousands of
tiny coins pouring into a single tall column that rises beside a numeric scale, the column
nearly reaching its top mark, cold clinical light, soft contact shadows, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the coin column fills toward the top mark 0–4s and stops. A little over a
hundred and thirty-four thousand. No figures. Hold palette.
```

### Scene ch12_s3 — 4s — out of the bank
1. **CHARACTERS IN SCENE:** The Banker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a plain 1980s banker's
three-piece suit standing beside a tall black vault, a slim ledger open in its hands, a thin
line of coins flowing out of the vault past it, infinite white void, soft contact shadow,
cinematic key from above, shallow depth of field, volumetric light, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, coins stream out of the vault past the motionless black banker 0–4s. It does not
move. Hold the color code. No new figures.
```

### Scene ch12_s4 — 3s — into the club's account (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a thin stream
of coins arriving into a small red folder icon, the folder filling, the black vault icon far
behind it, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the last coins settle into the red folder 0–3s. Moved, not stolen. No figures.
Hold palette.
```

**Chapter handoff →** the folder fills; Chapter 13 waits for an alarm that never comes.

---

## CHAPTER 13 — No alarm  (3:00–3:15)
**Script covered (37 words ≈ 14.8 s):** "hacker club, and not one alarm has sounded — because nothing was broken. The system did exactly what it was told to do. Here is the part that does not belong in the story of a robbery."
**SFX:** near silence, a single relay click, an alarm bell that does not ring · **Ambient:** a quiet machine room · **Music:** music drops out

### Scene ch13_s1 — 4s — the silent alarm
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a red 1980s alarm bell mounted on a pale
institutional wall, perfectly still, dust in the light, no motion, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the alarm bell stays perfectly still 0–4s; dust drifts past it. Nothing rings. No
figures. Hold palette.
```

### Scene ch13_s2 — 4s — nothing broken (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a complete
unbroken black lock icon with a red key turned in it, the lock open, everything intact, cold
clinical light, soft contact shadows, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the key turns and the lock opens cleanly 0–4s. No damage anywhere. No figures.
Hold palette.
```

### Scene ch13_s3 — 4s — the operator's machine room
1. **CHARACTERS IN SCENE:** The Postal Investigator
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in 1980s technician's kit
with a wired headset and a clipboard, standing in a dim machine room of tall grey computer
cabinets, all status lights steady green, Mode B, shallow depth of field, volumetric light, dust
particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on
ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the black technician among the cabinets 0–4s, every light steady. Everything
normal. Hold the color code. No new figures.
```

### Scene ch13_s4 — 3s — not a robbery (handoff)
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a close, near-symmetrical shot of the matte red mannequin's
eggshell head in the pale morning light of the flat, utterly still, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static close, the red head holds still as morning light shifts across it 0–3s. Something else is
coming. No camera move. Hold palette.
```

**Chapter handoff →** the red head holds; Chapter 14 shows what they do instead.

---

## CHAPTER 14 — The press conference  (3:15–3:30)
**Script covered (37 words ≈ 14.8 s):** "They do not keep it. On the 19th of November, three days later, the Chaos Computer Club calls a press conference. In front of television cameras, they explain what they did, how they did it, and to"
**SFX:** camera shutters, a microphone thump, murmuring press · **Ambient:** a crowded hall · **Music:** a restrained, formal pulse

### Scene ch14_s1 — 3s — they do not keep it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a small red
folder icon full of coins with a thin return arrow curving from it back toward a black vault
icon, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the return arrow draws itself from the red folder toward the vault 0–3s. Not
theirs to keep. No figures. Hold palette.
```

### Scene ch14_s2 — 3s — 19 November, three days later
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a 1980s desk calendar page reading 19 November
on a plain table, morning light, a press badge beside it, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, a calendar page turns to 19 November 0–3s. Three days. No figures. Hold palette.
```

### Scene ch14_s3 — 3s — the cameras
1. **CHARACTERS IN SCENE:** The Journalist
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a row of glossy white mannequins holding 1980s reporter's
microphones and shoulder press cameras, packed into a plain hall, all facing the same way, flash
bulbs mid-burst, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, flashes pop along the row of white figures 0–3s. The press, assembled. Hold
palette. No new figures.
```

### Scene ch14_s4 — 3s — the two red figures at the table
1. **CHARACTERS IN SCENE:** The Hacker (two red figures) and The Journalist
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, two matte red mannequins seated at a plain table covered in
1980s microphones, a row of glossy white press mannequins with cameras in the foreground, flat
hall light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in past the white cameras toward the two red figures at the table 0–3s. They explain.
Hold palette. No new figures.
```

### Scene ch14_s5 — 3s — how, and to whom (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of three linked
icons in a row — a small red program icon, a black bank-vault icon, and a red-headed page icon —
joined by thin lines, cold clinical light, soft contact shadows, cinematic key from above,
shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the three icons light up one after another along the line 0–3s. What, how, to
whom. No figures. Hold palette.
```

**Chapter handoff →** the diagram completes; Chapter 15 returns the money.

---

## CHAPTER 15 — Every mark back  (3:30–3:45)
**Script covered (37 words ≈ 14.8 s):** "whom. Then they return the hundred and thirty-four thousand marks to the Hamburger Sparkasse, in full. The money was never the point. The point was the word "secure," and the fact that a state had used it"
**SFX:** coins pouring in reverse, a vault door closing, a stamp thud · **Ambient:** the hall emptying · **Music:** the pulse eases into the drone

### Scene ch15_s1 — 4s — returned in full (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a stream of
small coins flowing out of a red folder icon back into a black bank-vault icon, the folder
emptying completely, cold clinical light, soft contact shadows, cinematic key from above,
shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, every coin flows back into the vault 0–4s until the folder is empty. In full. No
figures. Hold palette.
```

### Scene ch15_s2 — 4s — the banker receives it
1. **CHARACTERS IN SCENE:** The Banker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a plain 1980s banker's
three-piece suit standing beside a closed black vault, a slim ledger shut in its hands, infinite
white void, soft contact shadow, cinematic key from above, shallow depth of field, volumetric
light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI
Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black banker closes the ledger 0–4s and stands still. Accounted for. Hold the color
code. No new figures.
```

### Scene ch15_s3 — 4s — not the money
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a medium shot of the matte red mannequin standing at a plain
table, an empty red folder lying open in front of it, flat hall light, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the red figure closes the empty folder and leaves its hand on it 0–4s. It was
never the point. No camera move. Hold palette.
```

### Scene ch15_s4 — 3s — the word (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, extreme close-up of the stamped
official document from before, a single blocky seal reading as a bold mark, cold clinical light,
white void, cold clinical light, soft contact shadows, cinematic key from above, shallow depth
of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the light slowly hardens across the stamped seal 0–3s. One word, used to sell
something. No figures. Hold palette.
```

**Chapter handoff →** the seal holds; Chapter 16 shows what the word was used to sell.

---

## CHAPTER 16 — Minor  (3:45–4:00)
**Script covered (37 words ≈ 14.8 s):** "to sell a system it did not understand. The effect is immediate. Overnight, the Chaos Computer Club goes from a handful of enthusiasts to the most famous hackers in the country. The Bundespost calls the flaw minor,"
**SFX:** newspaper presses, a TV broadcast sting, a rubber stamp · **Ambient:** newsroom clatter · **Music:** the drone, colder

### Scene ch16_s1 — 3s — a system it did not understand
1. **CHARACTERS IN SCENE:** The Bundespost Official
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform and peaked cap standing beside a tall tangled machine of cables and grey boxes, looking
up at it, infinite white void, soft contact shadow, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the black official looks up at the tangled machine 0–3s and does not move. Owner,
not author. Hold the color code. No new figures.
```

### Scene ch16_s2 — 3s — overnight
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, close-up of a 1980s newspaper printing press running at
speed, a blurred stream of front pages, headline blocks unreadable, warm industrial light, Mode
B, shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal
Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the pages race through the press 0–3s. Overnight. No figures. Hold palette.
```

### Scene ch16_s3 — 3s — on every television
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glossy white mannequin in a tidy 1980s living room
watching a boxy television that shows two small red figures at a press table, warm domestic
light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the white mannequin leans toward the TV as the red figures appear on screen 0–3s.
Famous by morning. Hold palette. No new figures.
```

### Scene ch16_s4 — 3s — the most famous hackers
1. **CHARACTERS IN SCENE:** The Hacker (two red figures)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, two matte red mannequins standing in a doorway lit by a
burst of camera flashes from out of frame, 1980s casual silhouettes, night street, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static, flashes strobe across the two red figures 0–3s. A handful of enthusiasts, suddenly seen.
Hold palette. No new figures.
```

### Scene ch16_s5 — 3s — "minor" (handoff)
1. **CHARACTERS IN SCENE:** The Bundespost Official
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform and peaked cap pressing a small rubber stamp onto a short typed statement on a counter,
infinite white void, soft contact shadow, cinematic key from above, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black official stamps the statement and holds 0–3s. Minor. An isolated case. Hold
the color code. No new figures.
```

**Chapter handoff →** the stamp lifts; Chapter 17 gives the hackers' answer.

---

## CHAPTER 17 — The whole argument  (4:00–4:15)
**Script covered (37 words ≈ 14.8 s):** "an isolated case. The hackers call it the whole argument: a national network of nineteen thousand users, opened by two men and a home computer, using nothing but a mistake the operator had sworn did not exist."
**SFX:** a single isolated tone, then many linked tones, a modem chirp · **Ambient:** white-void hush · **Music:** drone widens

### Scene ch17_s1 — 3s — an isolated case (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a single small
dot circled in black ink, isolated in empty space, cold clinical light, soft contact shadows,
cinematic key from above, shallow depth of field, volumetric light, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the black circle closes tightly around the single dot 0–3s. Contained, they say.
No figures. Hold palette.
```

### Scene ch17_s2 — 3s — the whole argument
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram that pulls back
from the circled dot to reveal it is one node in a vast web of thousands of linked television
icons, cold clinical light, soft contact shadows, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow pull-back from the circled dot until the whole web of linked TVs fills the frame 0–3s. Not
isolated. No figures. Hold palette.
```

### Scene ch17_s3 — 3s — nineteen thousand users
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a wide overhead view of many glossy white mannequins seated
in neat rows, each before its own small boxy television, receding into haze, Mode B, shallow
depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow crane up over the rows of white figures at their TVs 0–3s. Everyone who trusted it. Hold
palette. No new figures.
```

### Scene ch17_s4 — 3s — two men and a home computer
1. **CHARACTERS IN SCENE:** The Hacker (two red figures)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, two matte red mannequins at a single cluttered desk with one
boxy home computer and an acoustic modem, dim 1980s flat, the only light the CRT, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the two red figures sit at one small machine 0–3s. That was all it took. No
camera move. Hold palette. No new figures.
```

### Scene ch17_s5 — 3s — the mistake that did not exist (handoff)
1. **CHARACTERS IN SCENE:** The Bundespost Official
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a 1980s postal-service
uniform standing with one hand raised flat as if swearing an oath, beside the cracked solid
block from before, infinite white void, soft contact shadow, cinematic key from above, shallow
depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black official holds the oath pose while the crack in the block beside it widens
0–3s. Sworn, and wrong. Hold the color code. No new figures.
```

**Chapter handoff →** the crack holds; Chapter 18 asks the question no inquiry answered.

---

## CHAPTER 18 — Never established  (4:15–4:30)
**Script covered (37 words ≈ 14.8 s):** "An official inquiry never establishes how the password reached them. Btx never recovered. It ran on for another sixteen years, always about to become the future, and was quietly switched off in 2001, having never arrived. But"
**SFX:** file drawers, a TV switching off with a fading whine · **Ambient:** an empty office, then an empty living room · **Music:** drone thins to one note

### Scene ch18_s1 — 4s — the inquiry
1. **CHARACTERS IN SCENE:** The Postal Investigator
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in 1980s technician's kit
with a clipboard, seated at a long table stacked with file boxes, one open folder in front of it
with a blank page, Mode B, shallow depth of field, volumetric light, dust particles, cinematic
color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the black investigator turns a page and finds it blank 0–4s. Never established.
Hold the color code. No new figures.
```

### Scene ch18_s2 — 4s — sixteen years (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a long
horizontal timeline from 1984 to 2001 with a single Btx emblem moving along it, a faint finish
line labelled with a blocky future marker always just ahead, cold clinical light, soft contact
shadows, cinematic key from above, shallow depth of field, volumetric light, cinematic color
grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the emblem travels the timeline 0–4s while the future marker keeps sliding ahead
of it. Always about to arrive. No figures. Hold palette.
```

### Scene ch18_s3 — 4s — switched off
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a boxy 1980s television in an empty tidy living room, its
screen collapsing to a single bright horizontal line as it switches off, dusk light, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the picture collapses to a line, then a point, then dark 0–4s. 2001. No figures. Hold
palette.
```

### Scene ch18_s4 — 3s — never arrived (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, the same empty living room, the dark television, a small
numeric keypad left on the armrest of an empty chair, dusk light, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, dust settles over the keypad on the empty chair 0–3s. Nobody waiting any more. No
figures. Hold palette.
```

**Chapter handoff →** the room stays dark; Chapter 19 picks the word back up.

---

## CHAPTER 19 — Safe  (4:30–4:45)
**Script covered (37 words ≈ 14.8 s):** "the argument it started did not switch off with it. Every year since, a new system has been built and sold with the same single word. Your money is safe. Your data is safe. Your account cannot"
**SFX:** a stamp thud repeating at a slow interval, a cash register chime, a notification ping · **Ambient:** white-void hush · **Music:** drone returns underneath, steady

### Scene ch19_s1 — 3s — the argument did not switch off
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin standing alone in a pool of light at
the center of a vast dark space, unmoved, the only lit object, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the light around the red figure stays on as the space around it goes dark 0–3s.
Still there. No camera move. Hold palette. No new figures.
```

### Scene ch19_s2 — 3s — every year since (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a row of plain
device icons from a 1980s terminal to a modern phone, each one receiving the same small black
stamp in turn, cold clinical light, soft contact shadows, cinematic key from above, shallow
depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static diagram, the black stamp comes down on each device in turn along the row 0–3s. The same
word, every year. No figures. Hold palette.
```

### Scene ch19_s3 — 3s — your money is safe
1. **CHARACTERS IN SCENE:** The Banker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single matte black mannequin in a plain banker's
three-piece suit standing behind a counter, one hand resting on a closed black vault box, a
small stamped card on the counter, infinite white void, soft contact shadow, cinematic key from
above, shallow depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane
render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked, the black banker taps the vault box once and holds 0–3s. Safe. Hold the color code. No
new figures.
```

### Scene ch19_s4 — 3s — your data is safe
1. **CHARACTERS IN SCENE:** The Btx User (white)
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a glossy white mannequin in a plain modern room holding a
slim phone, its screen showing a padlock icon, soft cool light, Mode B, shallow depth of field,
volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static medium, the white figure glances at the padlock on the phone and lowers it 0–3s.
Reassured. Hold palette. No new figures.
```

### Scene ch19_s5 — 3s — your account cannot be reached (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, in an infinite white void, a clean diagram of a single
closed black padlock icon in empty space, perfectly centered, a thin crack barely visible along
its shackle, cold clinical light, soft contact shadows, cinematic key from above, shallow depth
of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Slow push-in on the padlock 0–3s; the hairline crack catches the light at the very end. No
figures. Hold palette.
```

**Chapter handoff →** the crack catches the light; Chapter 20 returns to the screen.

---

## CHAPTER 20 — Still overfilling the page  (4:45–5:00)
**Script covered (37 words ≈ 14.8 s):** "be reached. And every year, somewhere, someone quietly overfills the page, and waits to see what spills onto the screen. Maybe the password was there the whole time. No one ever proved it came from the page."
**SFX:** a single key clack, a soft glitch crackle, then silence · **Ambient:** a quiet night room · **Music:** the drone holds one cold note and cuts

### Scene ch20_s1 — 4s — someone, somewhere
1. **CHARACTERS IN SCENE:** The Hacker
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a matte red mannequin seated alone at a modern desk at
night, a slim laptop screen the only light, a dark city window behind, Mode B sparse, Mode B,
shallow depth of field, volumetric light, dust particles, cinematic color grade, Unreal Engine
5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static wide, the red figure types a long unbroken line 0–4s. Quietly. No camera move. Hold
palette. No new figures.
```

### Scene ch20_s2 — 4s — waits to see what spills
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of a modern screen where a page of text
overfills its box and a few stray characters spill below the edge into the dark margin, cool
light, Mode B, shallow depth of field, volumetric light, dust particles, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, a few foreign characters drip below the page edge 0–4s. Watching for ghosts. No
figures. Hold palette.
```

### Scene ch20_s3 — 4s — maybe it was there the whole time
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, extreme close-up of the old 1980s CRT from the first
chapter, two lines of blocky green text — a login and a password field — faintly visible beneath
the surface of the glass, scanlines, dark room, Mode B, shallow depth of field, volumetric
light, dust particles, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic
lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Locked macro, the faint green lines surface on the old glass and hold 0–4s. Unexplained. No
figures. Hold palette.
```

### Scene ch20_s4 — 3s — the page (final)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Cinematic photorealistic 3D render, a single blank glowing page on a dark screen, perfectly
centered, nothing on it, cold light, deep shadow around the edges, Mode B, shallow depth of
field, volumetric light, dust particles, cinematic color grade, Unreal Engine 5, octane render,
8K, anamorphic lens, shot on ARRI Alexa, 16:9
```
3. **VIDEO PROMPT:**
```
Static, the blank page glows and holds 0–3s; hard cut to black on the last word. No figures.
Hold palette.
```

**End →** hard cut to black on "page." No end card over the image; the last word is the last thing.

---

> **EP03 storyboard complete — 20 chapters, 90 scenes.** Regenerate with
> `tools/build-shotlist.py umbra ep03-ghost-characters` and
> `tools/export-episode.py umbra ep03-ghost-characters`.

Type "next" for thumbnail prompts.
