# Final visual and animation QA

Status: pass after inspecting the decoded WebP contact sheet and each row at 192 × 208 cell size.

The same chibi girl appears throughout: stable warm-brown crown braid and long curls, pink heart bow on its consistent anatomical side, heart earrings, brown-pink eyes, white blouse, pink heart pinafore, and white bow boots. Side-facing rows were generated independently. No text, UI, scenery, floor shadow, detached icon, or extra character was accepted.

| Row | Frames | Visual and semantic result | Revisions |
| --- | ---: | --- | ---: |
| idle | 6 | Calm breathing and blink; first frame works as a still, loop closes. | 2 |
| running-right | 8 | Screen-right gait with alternating boots and trailing hair. | 2 |
| running-left | 8 | Independently drawn screen-left gait and compact full-length hair. | 2 |
| waving | 4 | Prep, raised palm, outward wave, return. | 1 |
| jumping | 5 | Crouch, lift, airborne peak, descent, land. | 1 |
| failed | 8 | Concern, slump, crouch, sit, hold, half-rise, recover. | 3 |
| waiting | 6 | Clasped hands, lean, head tilt, expectant expression; distinct from idle. | 2 |
| running | 6 | Attached horizontal tablet and active finger taps; no foot running. | 2 |
| review | 6 | Attached vertical notepad, inspection, thinking, nod; distinct from waiting and active work. | 1 |

The decoded atlas has 8-pixel or larger margins in every used cell. No exact duplicate adjacent frames were found. The sitting-height change in `failed` is pose-driven; other standing rows have stable frame scale. The final WebP is lossless RGBA, exactly 1536 × 1872, with zero hidden RGB and fully zero unused cells. Cyan-dominant visible pixels after the single final-atlas spill pass: zero.

Limitation: desktop UI selection was not exercised in a separate app instance. The isolated test covered filesystem discovery, validation, replacement, backup, rollback, staging cleanup, and hashes.
