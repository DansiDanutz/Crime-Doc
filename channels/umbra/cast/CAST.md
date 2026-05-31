# umbra. — Channel cast (standard recurring ensemble)

Every episode is built from the **same four roles**, re-skinned with episode-specific
wardrobe. This keeps the channel instantly recognizable and makes production fast: you
generate the four figures once, save them as Reference Elements, and re-dress them per story.

All four obey the locked DNA color code (`dna/CHANNEL_DNA.md` §8) — no exceptions:

| Role | Color treatment | Function |
|------|-----------------|----------|
| **THE SUBJECT** (main) | matte **RED** | the one the episode is about |
| **SECONDARY SUBJECTS** | glossy **WHITE** + one photoreal signifier garment | the people around the subject (associate, witness, victim) |
| **POLICE** | matte **BLACK** | the investigating institution |
| **SPECIAL POLICE** (the solvers) | matte **BLACK** + photoreal tactical gear | the unit that makes the capture / ends it |

> "Secondary subjects" stay white (per the code) but each gets **one** photoreal identifying
> item — a coat, an apron, a hard hat, a hospital gown — so the audience can tell them apart
> without giving them red (which is reserved for the single main subject) or facial features.

---

## Generation prompts (STATE 4 — pure white void, one figure each)

Generate each at `count: 4` in Nano Banana Pro, pick the best, save as a Reference Element,
then re-skin the wardrobe per episode. These are the channel defaults — distinct, generic
crime/intelligence archetypes (not tied to any one story).

### 1. THE SUBJECT — main, matte red ("the one")
**Role:** the focal person. Re-dress per episode (the coat below is the default skin).
```
Cinematic photorealistic 3D render, a single matte RED featureless mannequin with a smooth
eggshell head (no eyes, nose, mouth, ears, or hair), realistic adult human proportions,
polished matte red surface, wearing the simple silhouette of a knee-length overcoat over
plain clothes (kept entirely red, no other color), standing with hands in coat pockets, head
tilted slightly down, isolated on a pure white seamless void background, soft contact shadow
beneath, cinematic key light from above, subtle red rim glow, shallow depth of field,
volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens,
shot on ARRI Alexa, 2:3
```

### 2a. SECONDARY — The Associate (white + signifier)
**Role:** partner / accomplice / family — close to the subject.
```
Cinematic photorealistic 3D render, a single glossy WHITE featureless mannequin with a smooth
eggshell head (no facial features), realistic human proportions, polished plastic-white
surface, wearing a single photoreal dark leather jacket as the only colored item over the
white body, standing with arms crossed, isolated on a pure white seamless void background,
soft contact shadow beneath, cinematic key from above, shallow depth of field, volumetric
light, cinematic color grade, Unreal Engine 5, octane render, 8K, anamorphic lens, shot on
ARRI Alexa, 2:3
```

### 2b. SECONDARY — The Witness / Victim (white + signifier)
**Role:** the bystander, witness, or victim the case turns on.
```
Cinematic photorealistic 3D render, a single glossy WHITE featureless mannequin with a smooth
eggshell head (no facial features), realistic human proportions, polished plastic-white
surface, wearing a single photoreal muted-beige raincoat as the only colored item over the
white body, standing nervously, one hand near the collar, isolated on a pure white seamless
void background, soft contact shadow beneath, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 2:3
```

### 3. POLICE — matte black (the institution)
**Role:** investigating detectives / uniformed officers.
```
Cinematic photorealistic 3D render, a single matte BLACK featureless mannequin with a smooth
eggshell head (no facial features), realistic human proportions, polished matte black
surface, wearing the plain silhouette of a detective's suit and overcoat (kept entirely
black, no other color), standing squarely with hands clasped, isolated on a pure white
seamless void background, soft contact shadow beneath, cinematic key from above, shallow
depth of field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 2:3
```

### 4. SPECIAL POLICE — black + photoreal tactical gear (the solvers)
**Role:** the tactical/special unit that makes the raid or capture.
```
Cinematic photorealistic 3D render, a single matte BLACK featureless mannequin with a smooth
eggshell head (no facial features), realistic human proportions, wearing detailed photoreal
black tactical gear — plate carrier vest, duty belt, knee pads, radio, empty holster, a
tactical helmet with the visor up revealing the smooth featureless eggshell head — layered
over the black mannequin body, standing in a ready stance, isolated on a pure white seamless
void background, soft contact shadow beneath, cinematic key from above, shallow depth of
field, volumetric light, cinematic color grade, Unreal Engine 5, octane render, 8K,
anamorphic lens, shot on ARRI Alexa, 2:3
```

---

## Lock rules
- **One** red SUBJECT per episode (red is reserved — never give it to a secondary or police figure).
- Secondary subjects: white body + exactly one photoreal garment as their identifier.
- Police/special police never become red and never get facial features.
- Weapons are implied by stance/holster, never aimed graphically or shown firing (DNA: violence by composition only).
- Generate each figure once → save as a Reference Element → reuse everywhere (CHARACTER LOCK).

## Per-episode re-skinning
In each episode's `03-characters.md`, copy these four prompts and swap only the wardrobe to
fit the story (e.g. SUBJECT's overcoat → a hacker's hoodie, a pilot's uniform silhouette;
SPECIAL POLICE's gear → FBI tactical, military, customs). Keep the color treatment identical.
