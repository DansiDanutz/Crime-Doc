# The Seventy-Five Cent Spy

**Channel:** umbra  ·  **Episode:** `ep04-seventy-five-cents`

**Subject:** Clifford Stoll's 75-cent trace to the Hanover KGB hackers (1986-89) and the death of Karl Koch

**Target:** 5 min (~750 words)  ·  **Status:** storyboarded  ·  **Ending:** 4 — unanswered (nobody has explained the first of June, 1989)

## Production summary
- **Chapters:** 20  ·  **Scenes:** 90  ·  **Runtime (storyboarded):** 5:00
- **Cast:** CHARACTER_ID
- **Aspect ratio:** 16:9  ·  **Image model:** nano_banana_pro  ·  **Video model:** seedance_2_0

---

## STATE 2 — Idea

**Working title:** The Seventy-Five Cent Spy

**Subject:** In 1986 Clifford Stoll, an astronomer turned systems manager at Lawrence Berkeley
Laboratory, chased a 75-cent accounting error (nine seconds of unbilled computer time) to an
intruder in Hanover. The intruder was Markus Hess, part of a group of young West German hackers,
Karl Koch among them, who sold what they found to the KGB. Koch came forward to West German
security, became a witness, disappeared on 23 May 1989, and was found dead near Gifhorn on 1 June
1989. The death was ruled a suicide and has never been explained to his friends' satisfaction.

**Why it fits:** hacking, money (secrets sold for cash), and an open mystery at the end. It is the
same 1980s West German hacker world as EP03, so EP03's rendered clips carry it, and the episode
costs no render credits.

**Mechanism:** an unbilled user, then a borrowed account and a privilege flaw, then keyword
searches of military networks. Stoll records everything and traces the line abroad. The
Bundespost needs a long connection to finish the trace, so the bait is SDInet, a pile of fake
files. Hess is traced and named; the group's KGB deal and Koch's confession follow, then the
arrests (March 1989) and the trial (1990, suspended sentences).

**Provenance caveats (keep the script inside them):** no payment totals and no forensic details
of the death are stated, because sources differ. Only the dates (23 May and 1 June 1989), the
place (a forest near Gifhorn), the ruling (suicide) and the friends' disbelief are used.

**Ending type:** 4 — unanswered: "Nobody has explained the first of June, 1989."


---

## STATE 3 — Script

**Target length:** 5 minutes ≈ 750 words

Each `<!-- chNN -->` marker starts the narration for that 15 s chapter of `04-scenes.md`. The
spine is one open question, planted in ch02 and never closed: *what happened to Karl Koch?*

---

<!-- ch01 -->
It's the summer of 1986. In a flat in Hanover, West Germany, a young man dials a telephone line and connects to a computer six thousand miles away, in California. Nobody there knows he exists.

<!-- ch02 -->
Then a bill comes out wrong by seventy-five cents. This is the story of the spy those cents exposed, the agency that paid him, and a death that nobody has explained.

<!-- ch03 -->
The bill belongs to Lawrence Berkeley Laboratory. The man asked to find the missing seventy-five cents is Clifford Stoll, an astronomer who has just been moved to the computer room. He finds a user nobody pays for.

<!-- ch04 -->
Someone is logging in with the account of a scientist who is out of the country. Then that someone uses a flaw in an ordinary program to make himself the most powerful user on the machine.

<!-- ch05 -->
He is not interested in physics. He searches for other words. Nuclear. Military. SDI. So why would a stranger break into a physics laboratory, only to read about missiles?

<!-- ch06 -->
Stoll does not lock him out. He wants to know who it is. He wires printers to the lines, records every keystroke, and starts sleeping under his desk with a pager on his belt.

<!-- ch07 -->
The trail runs out of California, across the country, under the Atlantic, and into the network of the Deutsche Bundespost. The intruder is not in America at all. He is in West Germany.

<!-- ch08 -->
To trace him to a single telephone, the Bundespost needs him connected for a long time. He never stays long. He takes what he wants, and hangs up. How do you keep a thief in the room?

<!-- ch09 -->
You give him something to read. Stoll and his girlfriend invent a project called SDInet: pages and pages of fake military documents, written to look secret, far too long to steal quickly.

<!-- ch10 -->
The intruder takes the bait. He stays online, reading, for more than an hour. The line is traced to Hanover, and to a name. Markus Hess. But Hess is not working alone.

<!-- ch11 -->
He belongs to a small group of young West German hackers. One of them is called Karl Koch. Together they have been selling what they find to the KGB in East Berlin, for cash.

<!-- ch12 -->
And what does the KGB get for its money? Little that was not public, and some files that a man in California had made up. Real money, paid for invented secrets.

<!-- ch13 -->
By 1988, the pressure is too much for Karl Koch. He and another member go to West German security, confess, and ask for the protection the law offers to spies who come forward.

<!-- ch14 -->
In March 1989, the police move. The arrests are on the evening news: West German hackers, a laboratory in California, and the KGB, all in one story. Karl Koch is now a witness.

<!-- ch15 -->
The trial, the next year, ends with suspended sentences. The men who sold the secrets go home. One name is missing from the defendants. Karl Koch never reaches the court.

<!-- ch16 -->
On the 23rd of May, 1989, Koch leaves his job in the morning and takes a car. He does not come back. For a week, nobody knows where he is.

<!-- ch17 -->
On the first of June, in a forest near Gifhorn, police find what is left of him beside a patch of burned ground. The death is ruled a suicide. The file is closed.

<!-- ch18 -->
His friends never accept it. Why would a witness who had just asked for protection end his life a week later? Why in that forest? And who, if anyone, saw him in those seven days?

<!-- ch19 -->
Stoll writes a book about the seventy-five cents. It becomes the story of how networks are hunted: follow the one small number that does not add up, and keep following it.

<!-- ch20 -->
The seventy-five cents were found. The nine seconds of stolen time were explained. The hackers were named and tried. Nobody has explained the first of June, 1989.

---

**Word count:** see `tests` (each chapter ≤37 words, 2.5 words/s)
**Question beats (DNA: rhetorical questions as act pivots):** ch05, ch08, ch12, ch18
**Open loop:** planted ch02 ("a death that nobody has explained"), widened ch14 (Koch becomes a
witness), dropped ch16-17, left open ch18-20
**Ending type used:** 4 — unanswered (last line 8 words, lands on a date)


---

## STATE 4 — Characters

> This episode borrows EP03's rendered clips, so it borrows EP03's cast
> (`../ep03-ghost-characters/03-characters.md`): the red Hacker stands in for Hess and Koch, the
> black institution figures stand in for the Bundespost, the security service and the police, and
> the white figures stand in for the lab and the public. The names are carried by the on-screen
> tags in `production/cards.json`, not by faces. A cast-locked render of a later episode would
> add a white "Astronomer" (Stoll) and a black "Case Officer" (KGB).


---

## STATE 5 — Scene prompts

> Every scene borrows a clip already rendered for EP03 (`REUSE: ep03-ghost-characters/<scene>`),
> so this episode costs no render credits. EP03 clips that show readable text from that story
> (SECURE, 9.97 DM, the password, the date, the counter) are left out. Rendered clips are at
> least 4 s, so every borrowed clip covers its scene.

---

## CHAPTER 01 — The dial-in from Hanover  (0:00–0:15)

### Scene ch01_s1 — 3s — wide, the flat at night
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s1 — borrowed clip, nothing rendered

### Scene ch01_s2 — 3s — the telephone handset into the modem
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s2 — borrowed clip, nothing rendered

### Scene ch01_s3 — 3s — the screen wakes
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s3 — borrowed clip, nothing rendered

### Scene ch01_s4 — 3s — he begins to type
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s4 — borrowed clip, nothing rendered

### Scene ch01_s5 — 3s — the ordinary room around him (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s5 — borrowed clip, nothing rendered

## CHAPTER 02 — Seventy-five cents  (0:15–0:30)

### Scene ch02_s1 — 4s — STYLE ANCHOR / title beat
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s1 — borrowed clip, nothing rendered

### Scene ch02_s2 — 4s — money leaves (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s2 — borrowed clip, nothing rendered

### Scene ch02_s3 — 4s — and all of it back (the line reverses)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s3 — borrowed clip, nothing rendered

### Scene ch02_s4 — 3s — the red figure, unreadable (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s4 — borrowed clip, nothing rendered

## CHAPTER 03 — The astronomer in the computer room  (0:30–0:45)

### Scene ch03_s1 — 4s — the silent alarm
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch13_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch13_s1 — borrowed clip, nothing rendered

### Scene ch03_s2 — 4s — nothing broken (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch13_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch13_s2 — borrowed clip, nothing rendered

### Scene ch03_s3 — 4s — the operator's machine room
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch13_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch13_s3 — borrowed clip, nothing rendered

### Scene ch03_s4 — 3s — the red figure, unreadable (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s4 — borrowed clip, nothing rendered

## CHAPTER 04 — A borrowed account  (0:45–1:00)

### Scene ch04_s1 — 4s — a sealed block (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s1 — borrowed clip, nothing rendered

### Scene ch04_s2 — 4s — a hairline crack
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s2 — borrowed clip, nothing rendered

### Scene ch04_s3 — 4s — the red hand on the keys
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s3 — borrowed clip, nothing rendered

### Scene ch04_s4 — 3s — a page, magnified (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s4 — borrowed clip, nothing rendered

## CHAPTER 05 — Nuclear. Military. SDI.  (1:00–1:15)

### Scene ch05_s1 — 4s — too much text (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s1 — borrowed clip, nothing rendered

### Scene ch05_s2 — 3s — the system stumbles
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s2 — borrowed clip, nothing rendered

### Scene ch05_s3 — 4s — the spill
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s3 — borrowed clip, nothing rendered

### Scene ch05_s4 — 4s — from somewhere else inside the machine (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s4 — borrowed clip, nothing rendered

## CHAPTER 06 — Sleeping under the desk  (1:15–1:30)

### Scene ch06_s1 — 3s — the screen wakes
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s3 — borrowed clip, nothing rendered

### Scene ch06_s2 — 3s — the program
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch10_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch10_s2 — borrowed clip, nothing rendered

### Scene ch06_s3 — 3s — thirty-one lines
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch10_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch10_s3 — borrowed clip, nothing rendered

### Scene ch06_s4 — 3s — it logs in as the bank (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch10_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch10_s4 — borrowed clip, nothing rendered

### Scene ch06_s5 — 3s — and opens the club's page (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch10_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch10_s5 — borrowed clip, nothing rendered

## CHAPTER 07 — Across the Atlantic  (1:30–1:45)

### Scene ch07_s1 — 3s — the living-room terminal
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s1 — borrowed clip, nothing rendered

### Scene ch07_s2 — 3s — a nation of terminals (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s2 — borrowed clip, nothing rendered

### Scene ch07_s3 — 3s — the Bundespost runs it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s3 — borrowed clip, nothing rendered

### Scene ch07_s4 — 3s — an ordinary television becomes a terminal
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s4 — borrowed clip, nothing rendered

### Scene ch07_s5 — 3s — the red figure watches the screen (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s5 — borrowed clip, nothing rendered

## CHAPTER 08 — Keep him on the line  (1:45–2:00)

### Scene ch08_s1 — 4s — the red figure turns from the screen
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s1 — borrowed clip, nothing rendered

### Scene ch08_s2 — 4s — the club room
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s2 — borrowed clip, nothing rendered

### Scene ch08_s3 — 4s — the argument (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s3 — borrowed clip, nothing rendered

### Scene ch08_s4 — 3s — the official, unmoved (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s4 — borrowed clip, nothing rendered

## CHAPTER 09 — SDInet  (2:00–2:15)

### Scene ch09_s1 — 3s — the machine works alone
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch11_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch11_s3 — borrowed clip, nothing rendered

### Scene ch09_s2 — 3s — almost trivial
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch09_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch09_s2 — borrowed clip, nothing rendered

### Scene ch09_s3 — 3s — a page that charges (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch09_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch09_s3 — borrowed clip, nothing rendered

### Scene ch09_s4 — 3s — a few marks a look
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch09_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch09_s4 — borrowed clip, nothing rendered

### Scene ch09_s5 — 3s — the club's own page (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch09_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch09_s5 — borrowed clip, nothing rendered

## CHAPTER 10 — Markus Hess  (2:15–2:30)

### Scene ch10_s1 — 3s — ghost characters
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s1 — borrowed clip, nothing rendered

### Scene ch10_s2 — 3s — one night
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s2 — borrowed clip, nothing rendered

### Scene ch10_s3 — 3s — a login, in the clear
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s3 — borrowed clip, nothing rendered

### Scene ch10_s4 — 3s — the red figure reads it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s4 — borrowed clip, nothing rendered

### Scene ch10_s5 — 3s — the bank (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s5 — borrowed clip, nothing rendered

## CHAPTER 11 — Sold to the KGB  (2:30–2:45)

### Scene ch11_s1 — 4s — the operator's machine room
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch13_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch13_s3 — borrowed clip, nothing rendered

### Scene ch11_s2 — 4s — the red hand on the keys
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s3 — borrowed clip, nothing rendered

### Scene ch11_s3 — 4s — out of the bank
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch12_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch12_s3 — borrowed clip, nothing rendered

### Scene ch11_s4 — 3s — money leaves (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s2 — borrowed clip, nothing rendered

## CHAPTER 12 — Invented secrets  (2:45–3:00)

### Scene ch12_s1 — 4s — and all of it back (the line reverses)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s3 — borrowed clip, nothing rendered

### Scene ch12_s2 — 4s — the bank (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s5). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s5 — borrowed clip, nothing rendered

### Scene ch12_s3 — 4s — not the money
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch15_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch15_s3 — borrowed clip, nothing rendered

### Scene ch12_s4 — 3s — the spill
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s3 — borrowed clip, nothing rendered

## CHAPTER 13 — Karl Koch comes forward  (3:00–3:15)

### Scene ch13_s1 — 3s — an isolated case (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch17_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch17_s1 — borrowed clip, nothing rendered

### Scene ch13_s2 — 3s — a nation of terminals (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s2 — borrowed clip, nothing rendered

### Scene ch13_s3 — 3s — nineteen thousand users
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch17_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch17_s3 — borrowed clip, nothing rendered

### Scene ch13_s4 — 3s — the club room
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s2 — borrowed clip, nothing rendered

### Scene ch13_s5 — 3s — the official, unmoved (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch05_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch05_s4 — borrowed clip, nothing rendered

## CHAPTER 14 — The arrests  (3:15–3:30)

### Scene ch14_s1 — 3s — and all of it back (the line reverses)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s3 — borrowed clip, nothing rendered

### Scene ch14_s2 — 3s — the red figure reads it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s4 — borrowed clip, nothing rendered

### Scene ch14_s3 — 3s — the cameras
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch14_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch14_s3 — borrowed clip, nothing rendered

### Scene ch14_s4 — 3s — the two red figures at the table
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch14_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch14_s4 — borrowed clip, nothing rendered

### Scene ch14_s5 — 3s — it logs in as the bank (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch10_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch10_s4 — borrowed clip, nothing rendered

## CHAPTER 15 — Suspended sentences  (3:30–3:45)

### Scene ch15_s1 — 3s — the Bundespost runs it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch03_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch03_s3 — borrowed clip, nothing rendered

### Scene ch15_s2 — 3s — overnight
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch16_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch16_s2 — borrowed clip, nothing rendered

### Scene ch15_s3 — 3s — on every television
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch16_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch16_s3 — borrowed clip, nothing rendered

### Scene ch15_s4 — 3s — the two red figures at the table
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch14_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch14_s4 — borrowed clip, nothing rendered

### Scene ch15_s5 — 3s — the Bundespost stamps it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch04_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch04_s4 — borrowed clip, nothing rendered

## CHAPTER 16 — 23 May 1989  (3:45–4:00)

### Scene ch16_s1 — 4s — the operator's machine room
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch13_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch13_s3 — borrowed clip, nothing rendered

### Scene ch16_s2 — 4s — sixteen years (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch18_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch18_s2 — borrowed clip, nothing rendered

### Scene ch16_s3 — 4s — switched off
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch18_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch18_s3 — borrowed clip, nothing rendered

### Scene ch16_s4 — 3s — switched off
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch18_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch18_s3 — borrowed clip, nothing rendered

## CHAPTER 17 — The forest near Gifhorn  (4:00–4:15)

### Scene ch17_s1 — 4s — again, and again (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch11_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch11_s1 — borrowed clip, nothing rendered

### Scene ch17_s2 — 4s — they go to sleep
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch11_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch11_s2 — borrowed clip, nothing rendered

### Scene ch17_s3 — 4s — the machine works alone
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch11_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch11_s3 — borrowed clip, nothing rendered

### Scene ch17_s4 — 3s — by morning (handoff)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch11_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch11_s4 — borrowed clip, nothing rendered

## CHAPTER 18 — Why?  (4:15–4:30)

### Scene ch18_s1 — 4s — the news, then the weather
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch04_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch04_s1 — borrowed clip, nothing rendered

### Scene ch18_s2 — 2s — banking
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch04_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch04_s2 — borrowed clip, nothing rendered

### Scene ch18_s3 — 4s — a fortune spent building it (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch04_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch04_s3 — borrowed clip, nothing rendered

### Scene ch18_s4 — 3s — the Bundespost stamps it
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch04_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch04_s4 — borrowed clip, nothing rendered

### Scene ch18_s5 — 2s — the screen wakes
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch01_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch01_s3 — borrowed clip, nothing rendered

## CHAPTER 19 — The book  (4:30–4:45)

### Scene ch19_s1 — 3s — STYLE ANCHOR / title beat
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch02_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch02_s1 — borrowed clip, nothing rendered

### Scene ch19_s2 — 3s — every year since (white-void diagram)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch19_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch19_s2 — borrowed clip, nothing rendered

### Scene ch19_s3 — 3s — out of the bank
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch12_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch12_s3 — borrowed clip, nothing rendered

### Scene ch19_s4 — 3s — your data is safe
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch19_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch19_s4 — borrowed clip, nothing rendered

### Scene ch19_s5 — 3s — a hairline crack
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch06_s2). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch06_s2 — borrowed clip, nothing rendered

## CHAPTER 20 — The first of June  (4:45–5:00)

### Scene ch20_s1 — 4s — someone, somewhere
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch20_s1). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch20_s1 — borrowed clip, nothing rendered

### Scene ch20_s2 — 4s — the spill
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch07_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch07_s3 — borrowed clip, nothing rendered

### Scene ch20_s3 — 4s — a login, in the clear
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch08_s3). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch08_s3 — borrowed clip, nothing rendered

### Scene ch20_s4 — 3s — the page (final)
1. **CHARACTERS IN SCENE:** No recurring characters
2. **IMAGE PROMPT:**
```
Reused EP03 shot (ch20_s4). Mannequin-world palette, 16:9.
```
3. **VIDEO PROMPT:**
```
Reused footage, trimmed to the scene length. No captions, titles or subtitle text.
```
4. **REUSE:** ep03-ghost-characters/ch20_s4 — borrowed clip, nothing rendered


---

## STATE 6 — Thumbnail

Made for free from the EP03 "WHO?" render, which is already in the library: the red hacker at
the CRT with three black watchers, plus a large red "$0.75" figure added in the umbra. style. No
new generation was made. If the series goes ahead, a new Nano Banana Pro render would show the
75-cent bill, the trace map, or the forest.


---

## STATE 7 — Upload package

Final cut: `production/output/ep04-seventy-five-cents-roughcut.mp4`. It runs 5:12: the 5:00 story,
then the 12 s channel outro.

## Title (pick one)
1. **The Seventy-Five Cent Spy** *(recommended)*
2. A 75-Cent Error Exposed a KGB Hacker. Then a Witness Disappeared.
3. The Astronomer Who Caught a Spy With a Phone Bill

## Description
```
Summer 1986. A bill at a California laboratory is wrong by seventy-five cents. The astronomer asked
to find it follows the missing cents across the Atlantic, to a flat in Hanover and a group of
hackers selling secrets to the KGB. One of them, Karl Koch, becomes a witness. A week after the
case breaks he disappears, and on the first of June, 1989, he is found dead.

00:00 The dial-in
00:30 Part I — The error
01:30 Part II — The trace
02:30 Part III — The buyer
03:45 Part IV — The week

Sources: Clifford Stoll, "The Cuckoo's Egg" (1989); reporting on the 1990 Celle trial and on Karl
Koch's death (June 1989).

Which case should we open next? Tell us in the comments, and subscribe for more.
```

## Tags
Clifford Stoll, The Cuckoo's Egg, Karl Koch, Markus Hess, KGB hack, Hanover hackers, 1980s hacking,
Lawrence Berkeley Laboratory, cyber espionage, hacker documentary, cold war, true crime, mystery

## Checklist before publishing
- [ ] Watch the full cut once with headphones
- [x] Thumbnail made from library images (no new credits)
- [ ] Set the "altered or synthetic content" disclosure to **yes** (the visuals and the voice are AI-generated)


---
