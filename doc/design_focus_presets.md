# Design: Focus Preset Palette

**Status:** Implemented (Depence placeholder focus; on-site recalibration pending). 2026-06-17.
**Related issues:** #72 (merge), #74 (profile resolver), #75 (visualizer bridge).

## Goal

A Focus preset palette (grandMA2 preset type 6) covering Zoom for all zoom-capable
fixtures and (sharpness) Focus for the spot, organised so per-gobo focus can be
recalibrated on site.

## Rig context

Group → fixture mapping (confirmed with the user):

| Group | Name | Type | IDs | Focus-feature attrs |
|---|---|---|---|---|
| 1 | Spot | GEIST BSWF | 101–128 | ZOOM + **FOCUS** (sharpness) |
| 2 | Q4 | B-EYE | 201–215 | ZOOM only |
| 4 | Wash | LED 7x40 | 301–312 | ZOOM only |
| 3 | LED Par | LED PAR | 401–428 | — |
| 5 | Strobe | Led-8 | 801–804 | — |

- Only **GEIST** has a real FOCUS (sharpness) attribute; it also has **two gobo
  wheels** (`GOBO1`, `GOBO2`) and **no animation wheel** (checked).
- Zoom direction differs per profile: **B-EYE / GEIST** are `0 = narrow → 100 =
  wide`; **7x40 is inverted** (`wide` = At 0). The #74 resolver reads each
  profile's named `wide`/`narrow` channel-sets, so the logical scale is honoured
  on every fixture.

## Decisions (from grill session)

- **Zoom = 5 steps**: Very Narrow / Narrow / Medium / Wide / Very Wide (linear
  25% increments).
- **Focus is baked into the zoom presets** (not a separate set); GEIST gets
  `FOCUS = 100` (sharpest) in every preset. Only one focus value (100) — the
  Depence convention "100 = sharpest, 0 = softest".
- **Per-gobo focus sets.** Because a spot's in-focus plane differs by gobo wheel,
  there are three parallel 5-step sets so each can be recalibrated independently
  on site:
  - **Base** `6.1–6.5` (open beam) — GEIST + B-EYE + 7x40.
  - **Gobo 1** `6.11–6.15` — GEIST only.
  - **Gobo 2** `6.21–6.25` — GEIST only.
- **Stored Selective** (not Global): on site every individual fixture's focus
  differs slightly, so values are stored per fixture for per-lamp calibration.
- Gobo focus presets do **not** select the gobo itself (that is preset type 3);
  they only hold the zoom+focus to use while that wheel is in.

## Per-type zoom values (At%)

Wideness step → `At%` per type (via #74 resolver; 7x40 auto-inverted):

| Step | GEIST `ZOOM` | B-EYE `ZOOM` | 7x40 `ZOOM` |
|---|---|---|---|
| Very Narrow | 0 | 0 | 100 |
| Narrow | 25 | 25 | 75 |
| Medium | 50 | 50 | 50 |
| Wide | 75 | 75 | 25 |
| Very Wide | 100 | 100 | 0 |

GEIST `FOCUS` = 100 in every preset (placeholder for Depence; recalibrate on site
per set — base / G1 / G2).

## Implementation notes

- Per preset, per fixture type: `Clear → select type → set ZOOM (+ FOCUS on
  GEIST) → Store Preset 6.N /selective [/merge] → Label`.
- Focus preset type filters to FOCUS-feature attributes (ZOOM, FOCUS) on store.
- Selection by fixture-ID range per type (101–128 / 201–215 / 301–312).

## Follow-ups

- On-site: recalibrate `FOCUS` per fixture for base / Gobo 1 / Gobo 2, then
  Update the presets (per-fixture Selective values).
- Generalize the hand-written color/beam/focus build scripts into a
  `build_preset_palette` tool (resolver-driven, per-type/per-fixture merge,
  scope global|selective).
- GEIST also has framing blades (SHAPER) — candidate for a future Shapers
  preset type (8).
