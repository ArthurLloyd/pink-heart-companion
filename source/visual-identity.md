# Visual Identity Contract

Canonical visual reference for future edits. The released asset remains unchanged.

## Source roles

- `source/references/identity-front.png`: primary full-body identity and face.
- `source/references/identity-reference.png`: front, side, back, costume construction, and palette.
- `source/references/expression-reference.png`: expression vocabulary only.
- `source/references/motion-reference.png`: motion semantics only; its panels are not animation frames.

All four images depict the same character. The front illustration and character sheet agree on the stable design; the sheets add detail rather than a competing design.

## Immutable identity

- A gentle pastel anime chibi girl, about 3.5 heads tall, with a large head, small body, soft blush, large brown-pink eyes, and a warm pink, white, and brown palette.
- Long, voluminous warm-brown wavy hair with an upper crown braid. The part, braid path, hair length, and volume stay stable across poses.
- A pink heart ornament with a bow and hanging ribbon on the viewer's right side of her head in a front-facing pose. Its anatomical side stays fixed through turns.
- Heart-shaped dangling earrings. Natural occlusion in a side pose is acceptable; jewelry must not change design or side unexpectedly.
- White high-collar long-sleeve blouse with full sleeves and gathered cuffs; pink-white pinafore dress with heart strap hardware and a heart waist buckle.
- White knee-high boots with small pink bows on their outer sides. Boot height, bow placement, and skirt silhouette remain consistent.
- Clean warm line art, polished soft pastel shading, readable silhouette, and no 3D, pixel, realistic, or Western-cartoon restyle.

## Allowed motion changes

Face expression, blink, head angle, limb pose, hair and skirt secondary motion, and small attached hand-held work or review props may change only to express the assigned state. They must preserve the character's face, costume, proportions, and orientation-specific accessory placement.

## Excluded from animation art

No text, labels, UI, panel border, dialogue, floating symbols, tears, hearts, stars, punctuation, action lines, ground shadow, scenery, furniture, other person or animal, large effects, or detached object. A necessary prop must be small, attached to the character, and structurally consistent across its row.

## Production contract

- Final installed contract, verified against the running Codex Desktop loader: 192 × 208 cell; 8 columns × 9 rows; 1536 × 1872 V1 atlas. The earlier third-party builder labeled this geometry V2; see `docs/compatibility.md` for the corrected version mapping.
- Row order: idle, running-right, running-left, waving, jumping, failed, waiting, running (active work), review.
- Chroma key: flat saturated cyan `#00C9D8`. The generated source's small cyan variation was normalized deterministically after confirming foreground separation.
- Canonical base: one centered, full-body, front-facing character with complete hair, hands, and boots; no crop, text, props, effects, or shadow.
- Release id: `pink-heart-companion`; display name: `Pink Heart Companion`.

Canonical base image: `source/canonical-base.png`. Reference metadata and file hashes are recorded in `source/reference-index.json`.
