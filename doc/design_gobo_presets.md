# Design: Gobo Preset Palette

**Status:** Implemented (live, Global). 2026-06-17.
**Related issues:** #74 (profile resolver — values), #79 (build_preset_palette — built with it).

## Goal

A Gobo preset palette (grandMA2 preset type 3) for the GEIST spot's two gobo
wheels, modular so wheels and rotation compose freely.

## Rig context

- Gobo presets are **GEIST-only** (101–128). B-EYE and 7x40 are washes with no
  gobo wheels.
- GEIST has **two gobo wheels**:
  - **GOBO1** (rotating wheel): `open`, Gobo 1–7, Shake G1–7, plus whole-wheel
    spin. Individual rotating-gobo index/spin is on the separate **`GOBO1_POS`**
    channel (`Spot`=stop ≈ dmx 190–193; CW dmx 128–189; CCW dmx 194–255).
  - **GOBO2** (fixed wheel): `Open`, Gobo 1–8, Shake Gobo 1–8, whole-wheel spin.
    No per-gobo rotation.

## Decisions (from grill session)

- **Content (option C): static gobos + rotation.** Shake variants deferred.
- **One shared Open** (both wheels open) — `3.1`.
- **Wheel 1** static gobos `3.11–3.17` (Gobo 1–7); **Wheel 2** `3.21–3.28`
  (Gobo 1–8).
- **Rotation** (gobo-agnostic, single direction, 4): `Gobo Stop / Rotate Slow /
  Med / Fast` — `3.31–3.34`. Sets only `GOBO1_POS`, applied on top of whatever
  gobo is on wheel 1.
- **Modular:** each wheel's gobo presets set **only that wheel's** attribute
  (`GOBO1` or `GOBO2`); rotation presets set **only `GOBO1_POS`**. So wheel-1 +
  wheel-2 + rotation can be layered, and changing the gobo never disturbs an
  applied rotation.
- **Scope: Global** — the wheel slot is identical on every GEIST fixture (unlike
  Focus, which is per-fixture Selective).

## Values (from the GEIST profile, slot midpoints)

`At%` = midpoint of each named ChannelSet's DMX range / 255. Examples:

| Preset | Attribute @ At% |
|---|---|
| Open | `GOBO1` @1 (open 0–7) + `GOBO2` @1 (Open 0–7) |
| W1 Gobo 1…7 | `GOBO1` @ ~5/8/11/14/17/20/23 (slots dmx 8–63) |
| W2 Gobo 1…8 | `GOBO2` @ ~4/7/10/13/15/18/21/24 (slots dmx 8–63) |
| Gobo Stop | `GOBO1_POS` @75 (Spot, dmx 190–193) |
| Gobo Rotate Slow/Med/Fast | `GOBO1_POS` @76 / 88 / 99 (CCW dmx 194→255) |

## Implementation

- Built with **`build_preset_palette`** (#79): one preset per entry, single GEIST
  target, `scope="global"`. This dogfooded the tool live on the console.
- Per-gobo `At%` derived by parsing the GEIST fixture-type XML with
  `src/profile_resolver.py` and taking each gobo ChannelSet's midpoint.

## Known limitations / follow-ups

- Gobo names are the profile's generic `Gobo N` (no artwork names) — relabel if
  desired.
- Rotation uses the CCW segment; direction/speed feel to confirm on site.
- Shake variants and whole-wheel spin not included (add as a second layer or via
  effects if wanted).
