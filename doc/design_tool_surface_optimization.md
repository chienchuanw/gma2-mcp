# Design: Tool Surface & Reliability Optimization

**Status:** Delivered (2026-06-17). See "Delivery status" at the end.
**Related issues:** #55 (list_presets), #56 (silent success), #39-#54 (keyword-tool roadmap — delivered)

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

## Delivery status

All five pillars are implemented (PRs #60–#69):

1. **Verified execution core** — `ExecutionResult`/`build_result`/`execute()`/
   `run_verified()`/`run_verified_sequence()`; every mutating tool reports the
   console's real outcome; `detect_error` handles numbered and bare errors.
   (#58, #59, #56)
2. **Three-tier surface** — workflow tools (GMA2Client-backed), a verified
   command tool (`send_raw_command`), and discovery/read tools. Keyword tools
   remain as the fallback smallest unit. The #39–#54 roadmap was implemented
   (not as reflexive 1:1 wrappers but consolidated where it added value, e.g.
   `set_matricks`, `set_cue_timing`, mode-parameterized busking/rate tools).
3. **Selector grammar** — `src/commands/selector.py::normalize_selector`
   (thru / + / -, dotted pool.ids, injection-safe); wired into copy/move so a
   range moves in one call. Full retrofit across *all* object tools remains a
   future extension. (#57 phase 2, #49)
4. **Show introspection + name resolution** — `src/introspection.py` caches
   `List Attribute` and resolves friendly names (e.g. White → COLORRGB5);
   `set_fixture_attribute` resolves before sending and rejects unknowns with
   suggestions, degrading gracefully when introspection is unavailable.
   (#57 phase 3)
5. **Guidance** — working-principles block in the MCP server instructions
   (trust the result, batch with ranges, discover before guessing, destructive
   tool caution); destructive tools surface inline warnings. (#57 phase 4)

### Acceptance criteria (issue #57)

- [x] A rejected command surfaces as a failure (verified core).
- [x] A range operation is expressible in a single call (selector + copy/move).
- [x] An invalid/show-specific name is resolved or rejected with suggestions
      before sending (attribute resolution).
- [x] This design doc reflects the implemented state.

### Known follow-ups (not blocking)

- Extend the selector to every object-addressing tool (currently copy/move).
- Extend name resolution beyond attributes (groups, presets) and expose the
  introspection cache as MCP resources.
