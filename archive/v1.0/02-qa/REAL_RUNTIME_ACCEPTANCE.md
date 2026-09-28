# Real Codex Desktop runtime acceptance

Status: **PASS (user confirmed)**. The user reported checking the full real Codex Desktop checklist and finding the effects good. This records user observation; no automated screen capture was used.

In the current app build, open **Settings → Mini & Pets → My pets**. The app also contains an older **Pets → Pick a pet** settings layout; use whichever appears. Click the **Refresh** icon for local custom pets, then choose **Pink Heart Companion**. If the pet is hidden, enable its visible state or wake Mini. Do not edit the manifest or app database to select it.

For each item, record PASS, FAIL, or NOT_TRIGGERED and a short observation. A state that cannot be triggered is not an asset failure.

| Check | Expected observation | Result |
| --- | --- | --- |
| Discovery and appearance | Pet appears in the grid; preview is sharp at the chosen size; transparent edges have no white or cyan fringe. | PASS (user confirmed) |
| idle | Breathing and blink are calm; position and scale do not jump. | PASS (user confirmed) |
| running-right | Rightward drag or movement shows a rightward gait, not backwards running. | PASS (user confirmed) |
| running-left | Leftward drag or movement shows a leftward gait. | PASS (user confirmed) |
| waving | Attention event shows a real hand wave with stable hair accessory. | PASS (user confirmed) |
| jumping | Hover or successful completion shows anticipation, airborne peak, descent, and landing. | PASS (user confirmed) |
| failed | Safe failed-task event shows the intended slump and recovery. | PASS (user confirmed) |
| waiting | Input or approval wait visibly differs from idle and review. | PASS (user confirmed) |
| running | A short ordinary Codex task shows active work with the attached tablet, not foot running. | PASS (user confirmed) |
| review | A review or checking phase shows the small notepad and differs from waiting and active work. | PASS (user confirmed) |

V1 has no extra gaze-direction rows; gaze is not an acceptance requirement for this release.

If drag, DPI alignment, click behavior, initial overlay size, or cursor gaze seems wrong, repeat the same action with a bundled Codex pet. If the bundled pet has the same problem, mark **CODEX_RUNTIME_ISSUE**. If only Pink Heart Companion fails, investigate **PET_ASSET** or **PET_MANIFEST**. Keep unresolved cases as **UNKNOWN**.

This checklist is recorded as passed, so `archive/v1.0/` may now be frozen. Preserve screenshots or notes in the workspace only, never in the two-file payload.
