# Task Plan: GMA2 MCP Project Development Roadmap

## Goal
Investigate, prioritize, and implement improvements to the gma2-mcp project -- an MCP server that enables AI assistants to control grandMA2 lighting consoles via Telnet.

## Current Phase
Phase 3 (Issue #1 complete, remaining P0 issues next)

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
- [ ] Issue #2: Telnet connection resilience
- [ ] Issue #3: Clean up legacy src/tools.py
- **Status:** in_progress

### Phase 4: P1 Query & Show Management
- [ ] Issue #4: Add query/introspection MCP tools
- [ ] Issue #5: Add show file management MCP tools
- **Status:** pending

### Phase 5: P2 Expanded Workflows
- [ ] Issue #6: Macro management MCP tools
- [ ] Issue #7: Effect/chaser MCP tools
- [ ] Issue #8: Expand GMA2Client workflows
- **Status:** pending

## Key Questions
1. How many command builder functions exist? **200+ across 30+ modules (8,316 total lines)**
2. How many MCP tools are exposed? **17 tools**
3. What transport does the MCP server use? **stdio**
4. What is the test coverage? **818 test cases across 48 test files** (was 808, +10 from issue #1)
5. Is there a legacy tools module? **Yes -- `src/tools.py` contains the original pre-MCP tool implementations, still used by some tests**

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
| 2 | P0 | Telnet connection resilience | Open |
| 3 | P0 | Clean up legacy src/tools.py | Open |
| 4 | P1 | Query/introspection MCP tools | Open |
| 5 | P1 | Show file management MCP tools | Open |
| 6 | P2 | Macro management MCP tools | Open |
| 7 | P2 | Effect/chaser MCP tools | Open |
| 8 | P2 | Expand GMA2Client workflows | Open |
| 9 | P3 | HTTP/SSE transport | Open |
| 10 | P3 | Update/remove main.py | Open |

## Notes
- Current branch: `issues/1` (2 commits ahead of `main`)
- Uses `uv` as package manager with Python 3.12
- grandMA2 manual PDF is stored at `doc/2024-09-30_grandMA2_User_Manual_v3-9.pdf`
- OpenSpec change artifacts at `openspec/changes/fix-preset-types/`
