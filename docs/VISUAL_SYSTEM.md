# VISUAL_SYSTEM — the mannequin world (derived from DNA §6–8)

Every frame in every episode obeys this. It is what makes the channel recognizable.

## Color code (inviolable)
| Color | Who |
|-------|-----|
| Glossy **white** mannequin | civilians, crowds, bystanders, the world at stake |
| Solid matte **RED** mannequin | the protagonist / focal subject — "the one" |
| Solid matte **BLACK** mannequin | institutional antagonist (FBI, police, military, the system) |
| Photoreal clothing over a white body | a role where the uniform itself carries the info |

Rule of thumb: if the figure represents *power acting on the protagonist*, it's black or
uniformed. If it represents *the protagonist*, it's red. Everyone else is white.

## The figures
- Glossy white featureless mannequins. Smooth **eggshell heads** — NO eyes, mouth, nose,
  ears, or hair. Realistic human proportions. Polished plastic surface.
- Protagonist = same body, **matte red**. Institution = same body, **matte black**.
- Where a uniform matters, layer photoreal clothing over the mannequin (e.g. Soviet
  general's dress uniform: black body, photoreal olive-and-gold tunic).

## Environments
- **Mode A — white void:** infinite seamless white, soft contact shadows only. Used for
  character refs, isolation beats, "the one" moments.
- **Mode B — sparse photoreal location:** a real environment (bunker, hangar, plaza, jet
  interior) with mannequins inserted. Keep it sparse — props that carry meaning only.

## Render language (append to every image/keyframe prompt)
```
shallow depth of field, volumetric light, dust particles in air, cinematic color grade,
Unreal Engine 5, octane render, 8K, anamorphic lens, shot on ARRI Alexa
```

## Lighting
Cinematic key from above. Soft contact shadows. Volumetric atmosphere. One optional accent
color (the channel's red or green glow). **Never** horror lighting, never gore. Violence is
implied through composition — a raised arm, a drawn weapon, a body on the ground in
silhouette — never depicted graphically.

## Consistency (CHARACTER LOCK)
- Generate each recurring figure once as a reference (white void), save it as a **Reference
  Element**, then pass that element into every scene that figure appears in.
- Same render, same color, same wardrobe per character for the whole episode.
- STYLE ANCHOR (palette + render language + lighting) stays identical across all scenes.

See `docs/PRODUCTION_PIPELINE.md` for the exact generation-tool calls.
