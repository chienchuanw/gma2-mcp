# Design: Tool Surface & Reliability Optimization

**Status:** Proposed (consensus reached 2026-06-17)
**Related issues:** #55 (list_presets), #56 (silent success), #39-#54 (keyword-tool roadmap — to be re-triaged)

## Problem

Agents driving the gma2-mcp server error frequently and operate inefficiently.
The current trajectory is "one MCP tool per grandMA2 keyword" (54 tools today,
#39-#54 would push toward ~70, on top of 359 builder functions). Live testing
(creating a red color preset for an LED Par group) surfaced the real failure
modes, which are **not** primarily "too many tools to choose from":

- **(C) Silent failure — most severe.** Mutating tools call `send_command()`
  (fire-and-forget) and fabricate a success string (`"Stored color Preset 1"`)
  regardless of the console's actual response. An invalid `Attribute "Red" At
  100` reported success while doing nothing. Verification was also broken
  (`list_presets` name-addressing). See #55, #56.
- **(B) Wrong argument — second most severe.** The agent could not know that on
  this show White = `COLORRGB5` (not `COLORRGB4`), and that there is no `Red`/
  `Green`/`Blue` attribute name. This mapping is **show-specific** (depends on
  patched fixture types), so it cannot be a static enum.
- Efficiency: a large tool schema costs tokens/selection latency, and tools that
  only take scalar IDs force the agent to loop (e.g. moving Group 1 thru 10 to
  21 was done one-by-one instead of one `Move Group 1 Thru 10 At 21`).

### Protocol constraints (from grandMA2 v3.9 manual + live testing)

- Telnet (port **30000**) is the only command channel. Feedback is plaintext:
  `Executing : <cmd>` echo; failures as `Error : <cmd>` / `Error #NN: <REASON>`.
- No structured/JSON API and no rich programmer-value readback. Discovery must go
  through `List …` commands (e.g. `List Attribute` exposed `COLORRGB5 = White`).
- Port **30001** is a read-only System Monitor stream (potential verification
  side-channel).
- Object pools must be listed numerically: `List Preset 4.1` works,
  `List Preset "color"` errors (root cause of #55).

Conclusion: both B and C are **our** wrapper's responsibility; a better console
API will not hand them to us.

## Decisions

### 1. Verified execution core (foundation)

Every command — including `send_raw_command` and all future tools — routes
through one layer that sends via `send_command_with_response()` and parses the
reply into a structured result:

```
execute(cmd) -> { ok, echo, error_code, error_text, raw }
```

Error-line parsing (`Error :` / `Error #NN`) lives in exactly one place
(`response_parser.py` already does ~80% of this; it just isn't on the write
path). No tool fabricates success. Fixes the root of #55/#56.

### 2. Three-tier tool surface

1. **Workflow tools** — a small set for genuinely multi-step, correctness-
   critical flows (build cue list, "color preset for group X", song setup).
   Their reason to exist is saving round-trips and encoding syntax.
2. **Verified command tool** — the now-safe raw core plus a guided/validating
   builder. This is the escape hatch for the long tail, and what replaces filing
   N separate keyword-tool issues.
3. **Discovery / read tools** — kept and strengthened.

**Keyword tools are retained as the fallback "smallest unit"**, but new ones are
added only where they add real value (validation, safety warnings, naming) — not
as reflexive 1:1 mappings.

### 3. Shared `selector` (batch/range as a first-class default)

All "which object" parameters accept one MA2 selection grammar **string**:
`"1 thru 10"`, `"1 + 3 + 5"`, `"1 thru 10 - 4"`. Parsing/validation lives in one
place (tied to the introspection layer in §4); the tool composes the correct MA2
command. Batch becomes a default capability **everywhere**, killing the
"loop N times" pattern. Rationale for string (vs structured): it matches console
mental model, is easiest for the agent to write, and validation is delegated to
the verified core's `Error` detection.

### 4. Show-introspection cache (drives both resolution and resources)

One cached layer queries `List Attribute` / `List Group` / patch, and:

- **In-tool name resolution** — tools accept friendly names (`"White"`) and
  resolve to console tokens (`COLORRGB5`) before sending. Unknown enumerable
  names are **blocked pre-flight with suggestions**; everything else is sent and
  the console is trusted as final judge (hybrid (i)+(ii)).
- **MCP resources** — the same cache is exposed as resources (groups, fixtures,
  attributes, presets) for the agent to browse.
- Cache refreshes on "name not found" or on explicit request (patch changes).

### 5. Guidance delivery (hybrid)

- Core mental model centralized in the **MCP server instructions + a usage-guide
  resource**: "discover before acting", "use `thru`/`+` once instead of looping",
  "trust the verified core's report, never assume success".
- **High-risk tools** (move/copy/delete/bulk) additionally carry a short
  near-call reminder in their own description.

## Rollout (phased)

1. **Verified execution core** (§1) — unblocks #55/#56 and everything else.
2. **`selector` grammar** (§3) — biggest efficiency win; depends on §1 for
   validation.
3. **Show-introspection cache + resolution + resources** (§4) — closes B.
4. **Tier reclassification + guidance** (§2, §5).
5. **Re-triage #39-#54** — only after §1+§3 land. Per item ask: "workflow,
   already covered by the verified command tool, or a keyword genuinely worth a
   discrete tool?" Pause the as-written 1:1 expansion until then.

## Non-goals

- Replacing Telnet (no better transport exists for command control).
- Static attribute enums (mappings are show-specific; must be queried live).
- Removing keyword tools (retained as fallback).
