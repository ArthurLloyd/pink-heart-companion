# Compatibility and validation

## Supported installation

- Windows installer: Windows PowerShell 5.1 or later, current-user installation, no administrator privileges or downloaded dependencies.
- Target: a Codex desktop installation that discovers local custom pets under its active home. The installer uses an explicit `-CodexHome`, then `CODEX_HOME`, then `%USERPROFILE%\.codex`.
- Other desktop platforms: the portable two-file package is available for manual copying. No macOS runtime acceptance is claimed.
- Selecting the pet remains a user action in Settings > Pets / Mini & Pets after refreshing. Installation does not change Codex configuration, app binaries, selection, or login state.

[Official pet documentation](https://learn.chatgpt.com/docs/pets) describes the picker, refreshing custom pets, showing the overlay, reduced motion, and interface differences. Local filesystem details below were checked in the installed Windows app; they are not a guarantee for all future builds.

## Evidence and limits

The previous V1.0 acceptance record reports user-confirmed discovery, appearance and all nine animation states on Windows `OpenAI.Codex` **26.924.2738.0**. That is historical user observation, not a new automated UI test.

On **2026-10-29**, the installed Windows `OpenAI.Codex` **26.1023.6123.0** bundle was inspected read-only. Its local custom-pet loader still searches `pets/<directory>/pet.json`, defaults `spriteVersionNumber` to 1, accepts versions 1 and 2, and defines widths/heights of 1536, 1872 (V1), and 2288 (V2). The renderer still maps V1 to nine rows and V2 to eleven. No app binaries were changed. This checks the file contract; it does not constitute a new interactive runtime acceptance.

V1.1.0 keeps the accepted resource bytes unchanged. Isolated installer tests exercise the actual packaged scripts using Windows PowerShell, with spaces and Chinese characters in package and home paths. They cover default home resolution, `CODEX_HOME`, explicit home precedence, repeat installation, uninstall, unrelated pets, modified files, extra files, relative-path rejection, junction rejection and `.cmd` entrypoints. GitHub Actions repeats validation and packaging on a fresh Windows runner.

## Sprite contract

| Field | Value |
| --- | --- |
| Pet ID / directory | `pink-heart-companion` |
| Display name | Pink Heart Companion |
| `spriteVersionNumber` | `1` |
| Sprite format | Lossless WebP (`VP8L`), transparent, no embedded metadata |
| Atlas | 1536 × 1872 pixels; 8 columns × 9 rows |
| Cell | 192 × 208 pixels |
| Used-frame counts by row | 6, 8, 8, 4, 5, 8, 6, 6, 6 |
| Row order | idle, running-right, running-left, waving, jumping, failed, waiting, running, review |
| Additional gaze rows | None in this V1 asset |

The earlier third-party builder labeled this 8 × 9 geometry as V2. The tested Codex loader calls it V1; V2 requires 8 × 11. Keep `spriteVersionNumber: 1`. The distribution version (1.1.0) is separate from the sprite format version (1).

[animation-map.json](animation-map.json) records frame timing and loop behavior from the earlier renderer audit. These describe the audited build, and may change with future Codex versions.

## Resource checks

`tools/validate_pet.py` checks the exact two-file set and manifest identity, lossless WebP container, atlas geometry, transparency, unused cells, absence of hidden RGB, minimum 8-pixel visible-cell margin, manifest privacy patterns and SHA-256 values.

```text
2848aee07ffc57fe97bc01baabe277962d83d37d97eb1dcf1a1462954902a460  pet.json
cba7fc11fed373503042a8460c667dfe471f0d8e4a78f7deca05f0175541d6a3  spritesheet.webp
```

Source references, previews, scripts and documentation are excluded from the two-file Codex payload. The Windows ZIP contains only installation scripts, the payload, instructions and a payload checksum list. The portable ZIP contains only the pet directory and its two files. Distribution checksums are generated separately in `SHA256SUMS.txt`.

The redundant V1.0 working archives and intermediate exports were removed from the current checkout during V1.1.0 preparation. The previous committed state remains available in Git history at `dd517aa`; canonical source references and the base character image remain in `source/`.
