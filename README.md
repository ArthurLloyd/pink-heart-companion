# Pink Heart Companion

Codex Desktop custom pet, verified on the Windows `OpenAI.Codex` build `26.924.2738.0`. The installed asset is **V1**: nine animation rows in an 8 × 9, 1536 × 1872 lossless WebP atlas. All nine states passed asset QA and user-confirmed runtime acceptance.

## Repository layout

| Path | Purpose |
| --- | --- |
| `release/pink-heart-companion/` | Installable two-file Codex pet payload |
| `archive/v1.0/` | Frozen source, previews, QA, local contract summary, and handoff map |
| `source/references/` | Four generic-name character references with PNG metadata removed |
| `tools/` | Read-only payload and archive validators |

The private local `figs/` originals, downloaded third-party builder, and earlier production workspace are excluded from Git. No raw reference image is part of the installable payload.

## Install

Copy the **folder** `release/pink-heart-companion` into `%USERPROFILE%\.codex\pets\` so the target is `%USERPROFILE%\.codex\pets\pink-heart-companion\`. In Codex Desktop, open **Settings → Mini & Pets → My pets**, click **Refresh**, then choose **Pink Heart Companion**. Some layouts label this area **Pets → Pick a pet**. Do not overwrite another pet or alter Codex configuration files.

The package manifest sets `spriteVersionNumber` to `1`. The earlier third-party builder called the same 1536 × 1872 geometry V2, but the tested Codex loader defines that geometry as V1; its V2 requires 1536 × 2288. The V1 asset has no extra gaze rows. See `archive/v1.0/04-contract/current-codex-contract.md` for the local contract audit.

## Verify

```powershell
python tools/validate_pet.py release/pink-heart-companion
python tools/verify_archive.py archive/v1.0
```

`validate_pet.py` requires Pillow and NumPy. The release WebP is byte-identical to the installed and user-accepted asset:

- `pet.json` SHA-256: `2848aee07ffc57fe97bc01baabe277962d83d37d97eb1dcf1a1462954902a460`
- `spritesheet.webp` SHA-256: `cba7fc11fed373503042a8460c667dfe471f0d8e4a78f7deca05f0175541d6a3`

The repository export removed provenance metadata from source PNGs while verifying identical decoded pixels. The two-file pet payload and its hashes did not change.
