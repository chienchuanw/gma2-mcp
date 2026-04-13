# Task Plan: GMA2 MCP Project Development Roadmap

## Goal
Investigate, prioritize, and implement improvements to the gma2-mcp project -- an MCP server that enables AI assistants to control grandMA2 lighting consoles via Telnet.

## Current Phase
Phase 8: Next-generation feature roadmap (16 new issues #39-#54 created from capability exploration)

## Phases

### Phase 1: Project Discovery & Architecture Mapping
- [x] Read all core source files
- [x] Map the 4-layer architecture
- [x] Catalog all 17 MCP tools
- [x] Inventory command builder modules
- [x] Review test suite coverage
- [x] Document findings
- **Status:** complete

### Phase 2: grandMA2 Manual Study & Issue Creation
- [x] Study grandMA2 User Manual v3.9 (1,850 pages) -- TOC, Telnet Remote (34.4), Macros (38), Presets (19), Effects (31)
- [x] Identify gaps between manual capabilities and current implementation
- [x] Prioritize development tasks (P0-P3)
- [x] Create 10 GitHub issues (#1-#10) with labels and detailed descriptions
- **Status:** complete

### Phase 3: P0 Bugfixes & Reliability
- [x] Issue #1: Fix PRESET_TYPES mapping (branch `issues/1`, TDD, 818 tests passing)
- [x] Issue #2: Telnet connection resilience (branch `issues/2`, PR #31, 884 tests passing)
- [x] Issue #3: Clean up legacy src/tools.py (branch `issues/3`, PR #30, 884 tests passing)
- **Status:** complete

### Phase 4: P1 Query & Show Management
- [x] Issue #4: Add query/introspection MCP tools (branch `issues/4`, PR #32, 7 tools, 60 tests)
- [x] Issue #5: Add show file management MCP tools (branch `issues/5`, PR #33, 4 tools, 28 tests)
- **Status:** complete

### Phase 5: P2 Expanded Workflows
- [x] Issue #19: Fix assign() named page executor addressing (PR #26)
- [x] Issue #20: Add appearance assignment MCP tool (PR #27)
- [x] Issue #21: Add destructive command safety warnings (PR #28)
- [x] Issue #22: Add bulk cue operations across sequence ranges (PR #29)
- [x] Issue #6: Macro management MCP tools (PR #34)
- [x] Issue #7: Effect/chaser MCP tools (PR #34)
- [x] Issue #8: Expand GMA2Client workflows (PR #34)
- **Status:** complete

### Phase 6: P3 Transport & Cleanup
- [x] Issue #9: Add HTTP/SSE transport option (PR #35, TDD, 1016 tests passing)
- [x] Issue #10: Remove main.py using deprecated telnetlib (PR #36, 1005 tests passing)
- **Status:** complete

### Phase 7: Read-Back & Music Show Workflows
- [x] Issue #16: Add read-back tools for show object fields (PR #37, TDD, 1043 tests passing)
- [x] Issue #17: Add music show workflow tools (PR #38, TDD, 1028 tests passing)
- **Status:** complete

### Phase 8: Next-Generation Feature Roadmap
- [x] Explore codebase from senior grandMA2 designer perspective
- [x] Audit command builder coverage: 62/366 exports used (17%), 304 unused
- [x] Identify 16 feature areas across 4 priority tiers
- [x] Create 16 GitHub issues (#39-#54) with detailed technical approaches
- [ ] Issue #39 (P0): Timecode MCP tools for SMPTE-synced shows
- [ ] Issue #40 (P0): Set/add variable MCP tools
- [ ] Issue #41 (P1): MAtricks MCP tools
- [ ] Issue #42 (P1): Cue timing MCP tools
- [ ] Issue #43 (P1): Flash, swop, and stomp MCP tools
- [ ] Issue #44 (P1): Update cue MCP tool
- [ ] Issue #45 (P2): Blind and preview MCP tools
- [ ] Issue #46 (P2): Expose clone fixtures as MCP tool
- [ ] Issue #47 (P2): Rate and speed control MCP tools
- [ ] Issue #48 (P2): Executor release and top MCP tools
- [ ] Issue #49 (P3): Copy and move MCP tools
- [ ] Issue #50 (P3): Extended delete MCP tools
- [ ] Issue #51 (P3): Effect extension MCP tools
- [ ] Issue #52 (P3): Park and unpark MCP tools
- [ ] Issue #53 (P3): MIDI output MCP tools
- [ ] Issue #54 (P3): Advanced selection MCP tools
- **Status:** issues created, implementation pending

## Key Questions
1. How many command builder functions exist? **366 exports across 30+ modules (8,316 total lines)**
2. How many MCP tools are exposed? **54 tools** (was 49, +3 read-back tools from #16, +3 workflow tools from #17)
3. How many command builders are used? **62/366 (17%)** -- 304 builders exist but have no MCP tool surface
4. What transport does the MCP server use? **stdio (default) or streamable-http** (configurable via `MCP_TRANSPORT` env var)
5. What is the test coverage? **1055 test cases across 59 test files** (was 1016, +39 tests from #16/#17)
6. Is there a legacy tools module? **No -- `src/tools.py` was removed in issue #3 (PR #30). All tools are in `src/server.py`.**

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Document under `doc/` | User requested planning files go to `doc/` instead of project root |
| TDD approach for bugfixes | Write failing tests first, then fix (used for issue #1) |
| Branch per issue (`issues/N`) | Clean separation, linked to GitHub issues |
| P0 before P1 before P2 | Fix correctness/reliability before adding features |
| PRESET_TYPES: color=4 not 2 | Verified from manual Ch.19.2 screenshot showing numbered preset pools |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (none) | - | - |

## GitHub Issues
| # | Priority | Title | Status |
|---|----------|-------|--------|
| 1 | P0 | Fix PRESET_TYPES mapping | Fixed (branch `issues/1`) |
| 2 | P0 | Telnet connection resilience | Fixed (PR #31) |
| 3 | P0 | Clean up legacy src/tools.py | Fixed (PR #30) |
| 4 | P1 | Query/introspection MCP tools | Fixed (PR #32) |
| 5 | P1 | Show file management MCP tools | Fixed (PR #33) |
| 6 | P2 | Macro management MCP tools | Fixed (PR #34) |
| 7 | P2 | Effect/chaser MCP tools | Fixed (PR #34) |
| 8 | P2 | Expand GMA2Client workflows | Fixed (PR #34) |
| 9 | P3 | HTTP/SSE transport | Fixed (PR #35) |
| 10 | P3 | Update/remove main.py | Fixed (PR #36) |
| 12 | P1 | Combine store + label into single commands (perf) | Fixed (PR #18) |
| 13 | P2 | Add macro line editing MCP tool | Fixed (PR #23) |
| 14 | P2 | Add sequence-scoped cue labeling tool | Fixed (PR #24) |
| 15 | P2 | Add cue CMD assignment MCP tool | Fixed (PR #25) |
| 19 | P1 | Fix assign() named page executor addressing | Fixed (PR #26) |
| 20 | P2 | Add appearance assignment MCP tool | Fixed (PR #27) |
| 21 | P2 | Add destructive command safety warnings | Fixed (PR #28) |
| 22 | P2 | Add bulk cue operations across sequence ranges | Fixed (PR #29) |
| 16 | P2 | Add read-back tools for show object fields | Fixed (PR #37) |
| 17 | P2 | Add music show workflow tools | Fixed (PR #38) |
| 39 | P0 | Timecode MCP tools for SMPTE-synced shows | Open |
| 40 | P0 | Set/add variable MCP tools | Open |
| 41 | P1 | MAtricks MCP tools | Open |
| 42 | P1 | Cue timing MCP tools | Open |
| 43 | P1 | Flash, swop, and stomp MCP tools | Open |
| 44 | P1 | Update cue MCP tool | Open |
| 45 | P2 | Blind and preview MCP tools | Open |
| 46 | P2 | Expose clone fixtures as MCP tool | Open |
| 47 | P2 | Rate and speed control MCP tools | Open |
| 48 | P2 | Executor release and top MCP tools | Open |
| 49 | P3 | Copy and move MCP tools | Open |
| 50 | P3 | Extended delete MCP tools | Open |
| 51 | P3 | Effect extension MCP tools | Open |
| 52 | P3 | Park and unpark MCP tools | Open |
| 53 | P3 | MIDI output MCP tools | Open |
| 54 | P3 | Advanced selection MCP tools | Open |

## Notes
- Previous roadmap complete: issues #1-#10, #12-#17, #19-#22 all resolved.
- New roadmap: 16 issues (#39-#54) created from capability exploration on 2026-04-14.
- Command builder coverage gap: 304/366 exported functions are unused -- most new issues expose existing builders as MCP tools.
- Uses `uv` as package manager with Python 3.12
- grandMA2 manual PDF is stored at `doc/2024-09-30_grandMA2_User_Manual_v3-9.pdf`
- OpenSpec change artifacts archived at `openspec/changes/archive/`
- grandMA2 `Info` keyword reads user annotations, not object properties -- tools renamed accordingly
- `Backup` command opens GUI menu, not functional over Telnet -- excluded from MCP tools
- `SaveShow`/`LoadShow`/`NewShow`/`Delete Macro` require `/noconfirm` for Telnet to avoid GUI popup blocking
- Executor page-qualified addressing: `Executor [Page].[ID]` format per manual p.456
- Macro creation via Telnet: `Store Macro N` + `Assign Macro pool.id.line /cmd="..."` (Edit workflow is GUI-only)
- Effect keywords operate on current fixture selection -- user must select fixtures first
- grandMA2 `List` keyword returns tabular text over Telnet -- format is undocumented, parser uses defensive regex with `parsed: False` fallback
- Lua API (`gma.show.property.get`) is console-internal only, not accessible over Telnet -- `List` command is the viable read-back mechanism
- Music show workflow pattern: Sequence+Page pairs per song, Macro with SetVar on line 1, Set-list sequence with cue-to-macro CMD links
- `Off Effect` stops effects in programmer; `Stomp` is for executor-level assertive playback (different concept)
