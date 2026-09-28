# Current local Codex Desktop pet contract

Audited from the running Windows `OpenAI.Codex` package, version `26.924.2738.0`, specifically its bundled custom pet loader and renderer. The locally installed CLI reports `codex-cli 0.158.0-alpha.2.1`. No app binaries were modified.

- Custom pets are discovered under the active Codex home in `pets/<directory-name>/pet.json`; the directory name becomes `custom:<directory-name>` internally.
- The bundled home resolver uses `CODEX_HOME` when set and otherwise joins the Windows user home with `.codex`. The current shell has no `CODEX_HOME` override, and the existing home and pets directory were confirmed before installation. The resolved private path is represented as `%USERPROFILE%\.codex` in reports.
- The loader accepts optional `id` and `displayName`, nullable `description`, `spritesheetPath` defaulting to `spritesheet.webp`, and `spriteVersionNumber` equal to 1 or 2. Omitted version defaults to 1. This package keeps all five explicit fields.
- Version 1 requires an 8 × 9 atlas, 1536 × 1872 pixels. Version 2 requires an 8 × 11 atlas, 1536 × 2288 pixels. Cells are 192 × 208 pixels.
- The first nine row frame counts in both versions are 6, 8, 8, 4, 5, 8, 6, 6, 6. Version 2 adds two rows of eight cells each for the additional view behavior.
- The current loader checks PNG or WebP headers, exact atlas dimensions according to version, a manifest whose sprite path stays inside the pet directory, and valid JSON. Invalid custom pets are skipped. The current UI advertises transparent PNG or WebP and a 20 MiB upload limit.
- The current renderer uses the nine state timings recorded in `handoff/animation-map.json`. The existing atlas preserves them without image conversion.

## Difference from the previous builder skill

The prior third-party `codex-desktop-pet-builder/references/animation-contract.md` labels an 8 × 9, 1536 × 1872 atlas as V2 and requires `spriteVersionNumber: 2`. The running Codex loader defines that geometry as V1. Therefore the previous release's `spriteVersionNumber: 2` and image height disagreed. The corrected final package sets `spriteVersionNumber: 1` and leaves every sprite byte unchanged. No V2 padding or invented direction rows were added.

The builder's `audit-pet-release.ps1` also hard-codes version 2, so it is not a valid contract validator for this V1 package. The local V1 validator checks the exact two-file payload, manifest, WebP chunks, pixel geometry, alpha, unused cells, hidden RGB, margins, and privacy patterns.
