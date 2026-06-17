# Design: Beam Preset Palette

**Status:** Implemented with precise per-type values (derived from the fixture
profiles via the #74 resolver). 2026-06-17.
**Related issues:** #72 (merge workflow), #74 (profile/function resolver — done),
#75 (visualizer bridge).

## Goal

A Beam preset palette (grandMA2 preset type 5) for the rig, covering a universal
Strobe/Shutter set plus moving-head beam-shaping (Iris/Frost/Prism).

## Rig context (relevant fixture types)

- **GEIST BSWF (ACME XA-500)** — Spot moving head: Shutter/Strobe, Gobo, Prism,
  Iris, Frost, Focus/Zoom. The only fixture with Iris/Frost/Prism.
- **1940 B-EYE** (×21) — LED beam/wash: Zoom + rotating-lens (Kaleido) macros +
  Strobe. No classic Iris/Frost/Prism.
- **Led-8 Strobe**, **LED PAR 8CH**, **LED 2HEAD**, **LED 7x40** — LED fixtures,
  mostly Shutter/Strobe only.

grandMA2's Beam preset type (5) covers Shutter/Strobe + Iris + Frost + Prism.
Gobo is type 3, Zoom/Focus is type 6 (kept separate).

## Decisions (from grill session)

- **Structure = both sets (C), strobe-first (A) as the core.**
- **A — Strobe/Shutter (6), stored Global from ALL fixtures** (incl. LED Par —
  user wants them included; fixtures without a real shutter simply don't
  contribute). Pool `5.1–5.6`:
  Open, Closed, Strobe Slow, Strobe Medium, Strobe Fast, Strobe Random.
  (No Pulse — user dropped it.)
- **B — Iris/Frost/Prism (11), stored Global; only GEIST contributes.** Pool
  `5.11–5.21`:
  Iris Open/Pinch/Mid, Frost Off/Soft/Full, Prism Off/In/Rotate Slow/Med/Fast.
  Prism rotation is Stop + Slow/Med/Fast (prism in/out on `PRISMA1`, rotation
  speed on `PRISMA1_POS`).
- **B-EYE excluded from Beam presets.** It has no Iris/Frost/Prism; its beam
  character (zoom + rotating-lens macros) belongs to Focus/effects, to be done
  separately. B-EYE IS covered by the A strobe set (it has a shutter).
- **All Global, numbered with a gap** (`5.1–5.6`, then `5.11–5.21`) for room to
  grow.

## Implementation notes

- Attribute tokens (verified via `List Attribute`): `SHUTTER`,
  `MASTERSHUTTERSTROBE`, `IRIS`, `FROST`, `PRISMA1`, `PRISMA1_POS`.
- Per preset: **Clear → select → set only that preset's attribute(s) → Store
  Preset 5.N /global /noconfirm → Label**. Clearing between presets keeps each
  preset's content clean (unlike the color palette, different beam presets touch
  different attributes).
- To extend a set to a new fixture type later, use the merge workflow (#72):
  select that type → set values → `Store … /global /merge`.

### Values: initial approach B, now superseded by precise values

> NOTE: The best-effort values below were the FIRST pass (before the profile
> XMLs were available). They have since been replaced with precise per-type
> values — see "Precise per-type values (from fixture profiles, #74)" at the end.
> This section is kept for history.

grandMA2 Telnet cannot read a profile's channel-function ranges, so strobe rate /
iris direction / prism slot values were initially **starting points that needed
on-site verification**:

- Reliable: Open (`SHUTTER=100`), Closed (`SHUTTER=0`), Frost (0/40/100).
- Verify on stage: Strobe rates (`MASTERSHUTTERSTROBE` 20/50/85; "Random" = 70 is
  the least certain — the value→behavior map is fixture-specific); Iris
  direction (open = high or low?); Prism "in" slot value (`PRISMA1=50` is a
  guess) and rotation speeds (`PRISMA1_POS`).
- Because each profile maps the same value differently, "Strobe Fast" may strobe
  at different rates per fixture type — expected with best-effort.

## Path to precise values

- **#74 fixture-profile resolver** — parse GDTF / show XML to map
  `(fixture_type, attribute, function) → value`, so named functions ("Strobe
  Fast", "Iris Open", "Prism Rotate Slow") resolve to the correct per-type value
  and merge-store automatically. This upgrades approach B → C with no guessing.
- **#75 visualizer bridge** — capture a Depence frame the (multimodal) agent can
  read, for a closed loop on STATIC looks (iris/frost/prism presence, color,
  position). Temporal looks (strobe rate, rotation speed) still need a short
  video / frame sequence.

## Follow-ups

- Provide the show XML to seed #74, then re-derive precise beam values.
- B-EYE zoom / rotating-lens looks → Focus presets (type 6) + effects, separately.
- Consider generalizing `build_color_palette` (#72) into a `build_preset_palette`
  that takes attribute/value sets (would have made this beam build a single call).

## Precise per-type values (from fixture profiles, #74)

The best-effort values were replaced with values derived from each fixture's
profile (MA2 fixture-type XML) via `src/profile_resolver.py`. `resolve(query,
position, feature)` maps a named function to `(attribute, At%)`; `per_type_values`
runs it across all profiles. Shutter-slot queries (open/closed/strobe/random) are
scoped to the SHUTTER feature so they don't match color-wheel / white "open"
slots. Each logical preset is stored once per fixture type and **merged** into one
Global preset.

Patch: GEIST 101–128, B-EYE 201–215, LED 7x40 301–312, LED PAR 401–428,
Led-8 Strobe 801–804.

### A — Strobe/Shutter (attribute @ At%)

| Preset | LED PAR `SHUTTER` | Led-8 `SHUTTER` | LED 7x40 `SHUTTER` | GEIST `SHUTTER` | B-EYE `MASTERSHUTTERSTROBE` |
|---|---|---|---|---|---|
| Open | @0 | @0 | @41 | @4 | @41 |
| Closed | — | — | @0 | @0 | @0 |
| Strobe Slow | @12 | @14 | @6 | @12 | @6 |
| Strobe Medium | @50 | @52 | @21 | @29 | @21 |
| Strobe Fast | @90 | @96 | @39 | @50 | @39 |
| Strobe Random | — | — | @90 | @95 | @90 |

Each value lands in that profile's actual strobe band (e.g. LED PAR strobe spans
0.1–20 Hz, so 12/50/90 ≈ 2.5/10/18 Hz; 7x40/B-EYE are 1–10 Hz). LED PAR and Led-8
have no mechanical closed/random slot, so they are omitted from those presets.

### B — GEIST Iris/Frost/Prism (GEIST only)

| Preset | Attribute(s) @ At% |
|---|---|
| Iris Open / Pinch / Mid | `IRIS` @0 / @90 / @45 |
| Frost Off / Soft / Full | `FROST` @0 / @40 / @100 |
| Prism Off | `PRISMA1` @0 |
| Prism In (stop) | `PRISMA1` @50, `PRISMA1_POS` @75 (Stop ≈ dmx 190–193) |
| Prism Rotate Slow / Med / Fast | `PRISMA1` @50, `PRISMA1_POS` @77 / @88 / @99 |

### Known limitations

- Led-8 Strobe's "open" function is unlabeled in the profile, so the resolver
  can't name-match it (At 0 = open in practice).
- Iris direction and prism rotation direction are assumptions to confirm
  visually (the profile's Iris function has no named open/closed sets).
