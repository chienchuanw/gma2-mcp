# Task Plan: GMA2 MCP Project Development Roadmap

## Goal
Investigate, prioritize, and implement improvements to the gma2-mcp project -- an MCP server that enables AI assistants to control grandMA2 lighting consoles via Telnet.

## Current Phase
Phase 5 (Issues #19-22, #2, #3 complete -- all P0 issues resolved)

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
- [ ] Issue #4: Add query/introspection MCP tools
- [ ] Issue #5: Add show file management MCP tools
- **Status:** pending

### Phase 5: P2 Expanded Workflows
- [x] Issue #19: Fix assign() named page executor addressing (PR #26)
- [x] Issue #20: Add appearance assignment MCP tool (PR #27)
- [x] Issue #21: Add destructive command safety warnings (PR #28)
- [x] Issue #22: Add bulk cue operations across sequence ranges (PR #29)
- [ ] Issue #6: Macro management MCP tools
- [ ] Issue #7: Effect/chaser MCP tools
- [ ] Issue #8: Expand GMA2Client workflows
- **Status:** in_progress

## Key Questions
1. How many command builder functions exist? **200+ across 30+ modules (8,316 total lines)**
2. How many MCP tools are exposed? **24 tools** (was 20, +1 appearance tool, +3 bulk cue tools from issues #19-22)
3. What transport does the MCP server use? **stdio**
4. What is the test coverage? **~884 test cases across 48+ test files** (was ~850, +15 resilience tests from #2, +3 server tool tests from #2, -16 removed tests from #3)
5. Is there a legacy tools module? **No -- `src/tools.py` was removed in issue #3 (PR #30). All tools are in `src/server.py`.**

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
| 4 | P1 | Query/introspection MCP tools | Open |
| 5 | P1 | Show file management MCP tools | Open |
| 6 | P2 | Macro management MCP tools | Open |
| 7 | P2 | Effect/chaser MCP tools | Open |
| 8 | P2 | Expand GMA2Client workflows | Open |
| 9 | P3 | HTTP/SSE transport | Open |
| 10 | P3 | Update/remove main.py | Open |
| 12 | P1 | Combine store + label into single commands (perf) | Fixed (PR #18) |
| 13 | P2 | Add macro line editing MCP tool | Fixed (PR #23) |
| 14 | P2 | Add sequence-scoped cue labeling tool | Fixed (PR #24) |
| 15 | P2 | Add cue CMD assignment MCP tool | Fixed (PR #25) |
| 19 | P1 | Fix assign() named page executor addressing | Fixed (PR #26) |
| 20 | P2 | Add appearance assignment MCP tool | Fixed (PR #27) |
| 21 | P2 | Add destructive command safety warnings | Fixed (PR #28) |
| 22 | P2 | Add bulk cue operations across sequence ranges | Fixed (PR #29) |

## Notes
- All P0 issues resolved (issues #1, #2, #3). Next: P1 issues (#4, #5).
- Uses `uv` as package manager with Python 3.12
- grandMA2 manual PDF is stored at `doc/2024-09-30_grandMA2_User_Manual_v3-9.pdf`
- OpenSpec change artifacts archived at `openspec/changes/archive/`
