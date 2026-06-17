# Progress Log

## Session: 2026-04-10 (Session 1 -- Investigation)

### Phase 1: Project Discovery & Architecture Mapping
- **Status:** complete
- **Started:** 2026-04-10
- Actions taken:
  - Read all root config files: pyproject.toml, Makefile, pytest.ini, .gitignore, connect.sh
  - Read all core source: server.py, telnet_client.py, gma2_client.py, command_sequence.py, tools.py
  - Read commands/__init__.py (862 lines, 200+ exports), constants.py, helpers.py
  - Counted 8,316 total lines across command function/object modules
  - Listed all 48 test files, counted 808 test cases
  - Reviewed git history (20 commits)
  - Mapped 4-layer architecture
  - Cataloged all 17 MCP tools with their parameters
  - Documented all command builder modules and their functions
  - Identified legacy code, potential issues, and improvement areas
- Files created:
  - doc/task_plan.md
  - doc/findings.md
  - doc/progress.md

## Session: 2026-04-10 (Session 2 -- Roadmap & Issue #1)

### Phase 2: grandMA2 Manual Study & Issue Creation
- **Status:** complete
- Actions taken:
  - Read grandMA2 User Manual v3.9 TOC (27 pages), Telnet Remote (34.4), Macros (38), Presets (19)
  - Identified 10 development priorities across P0-P3
  - Created GitHub labels: priority: P0/P1/P2/P3, bug, enhancement, tech-debt
  - Created 10 GitHub issues (#1-#10) with detailed descriptions, affected files, and proposed solutions
- Issues created: #1 through #10

### Phase 3: Issue #1 -- Fix PRESET_TYPES Mapping
- **Status:** complete
- Actions taken:
  - Created branch `issues/1`
  - Created OpenSpec change at `openspec/changes/fix-preset-types/` (proposal, design, specs, tasks)
  - **TDD Red**: Added `TestPresetTypesMapping` class with 10 tests asserting correct IDs per manual Ch.19.2
  - Ran tests: 7 failures confirmed (color=2≠4, beam=4≠5, focus=5≠6, control=6≠7, shapers=7≠8, video=8≠9, duplicate IDs)
  - Committed failing tests: `a932c26`
  - **TDD Green**: Fixed `PRESET_TYPES` in `src/commands/constants.py`
  - Updated 5 test files with corrected assertions: test_objects.py, test_info.py, test_edit.py, test_server_tools.py, test_gma2_client.py
  - Full suite: **818 passed, 0 failures** (+10 new tests)
  - Committed fix: `1deb5a8`
- Files modified:
  - src/commands/constants.py (PRESET_TYPES values)
  - tests/test_objects.py (+64 lines: TestPresetTypesMapping + assertion fix)
  - tests/test_info.py (assertion fix)
  - tests/test_edit.py (assertion fix)
  - tests/test_server_tools.py (2 assertion fixes)
  - tests/test_gma2_client.py (assertion fix)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| PRESET_TYPES mapping | 10 assertions | All pass | All pass | ✓ |
| Full suite after fix | 818 tests | 818 pass | 818 pass | ✓ |

## Session: 2026-04-11 (Session 3 -- Issue #12 Performance)

### Issue #12: Combine store + label into single commands (PR #18)
- **Status:** complete
- Actions taken:
  - Updated `store_group()` in `src/commands/functions/store.py` to accept optional `name` parameter, generating `store group {id} "name"` inline
  - Updated `create_fixture_group()` MCP tool in `src/server.py` to send 2 commands (select + store-with-name) instead of 3 (select + store + label)
  - Updated `build_cue_list()` in `src/gma2_client.py` to use `store_cue(id, name=name)` inline instead of separate `label()` call (1 command per named cue instead of 2)
  - Updated `setup_group_with_preset()` in `src/gma2_client.py` to use `store_group(id, name=name)` inline instead of separate `label_group()` call (3 commands instead of 4)
  - Removed unused `label` and `label_group` imports from `gma2_client.py`
  - 5 new tests added, full suite: **823 tests passing**
- Files modified:
  - src/commands/functions/store.py (optional `name` parameter on `store_group`)
  - src/server.py (`create_fixture_group` reduced from 3 to 2 commands)
  - src/gma2_client.py (`build_cue_list` and `setup_group_with_preset` use inline naming, removed unused label imports)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Full suite after issue #12 | 823 tests | 823 pass | 823 pass | ✓ |

## Session: 2026-04-11 (Session 4 -- Issues #13, #14, #15)

### Issues #13, #14, #15: Macro line editing, sequence-scoped cue labeling, cue CMD assignment
- **Status:** complete
- Actions taken:
  - Created OpenSpec change `issues-13-14-15-macro-cue-tools` with proposal, design, 3 specs, and tasks (TDD plan)
  - Created GitHub linked branches via `gh issue develop` for all 3 issues
  - Implemented all 3 features in parallel using worktree agents
  - **Issue #13**: Added `assign_macro_cmd()` builder + `set_macro_line` MCP tool (3 builder tests + 2 tool tests)
  - **Issue #14**: Added `label_sequence_cue()` builder + `label_sequence_cue` MCP tool (4 builder tests + 2 tool tests)
  - **Issue #15**: Added `assign_cue_cmd()` builder + `set_cue_cmd` MCP tool (2 builder tests + 2 tool tests)
  - Created PRs #23, #24, #25 targeting `issues/12` base branch
  - Addressed PR review comments: lowercase casing consistency, `__all__` exports, stronger test assertions, numeric string handling
  - Archived OpenSpec change to `openspec/changes/archive/2026-04-11-issues-13-14-15-macro-cue-tools/`
  - Updated README (17→20 tools) and doc files
- PRs:
  - PR #23: `13-feat-add-macro-line-editing-mcp-tool` (issue #13)
  - PR #24: `14-feat-add-sequence-scoped-cue-labeling-tool` (issue #14)
  - PR #25: `15-feat-add-cue-cmd-assignment-mcp-tool` (issue #15)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Branch 13 tests | 47 tests | 47 pass | 47 pass | ✓ |
| Branch 14 tests | 49 tests | 49 pass | 49 pass | ✓ |
| Branch 15 tests | 46 tests | 46 pass | 46 pass | ✓ |

## Session: 2026-04-12 (Session 5 -- Issues #19, #20, #21, #22)

### Issues #19-22: Named page fix, appearance tool, destructive warnings, bulk cue ops
- **Status:** complete
- Actions taken:
  - Created OpenSpec change `issues-19-22-assign-appearance-warnings-bulk` with proposal, design, 4 specs (3 new + 1 modified), and tasks (25 items, TDD plan)
  - Created GitHub linked branches via `gh issue develop` for all 4 issues
  - Implemented all 4 features in parallel using worktree agents
  - **Issue #19** (P1 bug): Fixed `assign()` in `assignment.py` to detect quoted page names (leading `"`) and omit target type keyword. 4 tests added.
  - **Issue #20** (P2 feat): Registered `assign_appearance` MCP tool wrapping existing `appearance()` builder. Supports RGB, HSB, hex, range, source-copy, reset. Added `reset=True` + color params guard. 6+1 tests added.
  - **Issue #21** (P2 feat): Added `DESTRUCTIVE_WARNINGS` registry and `_format_warnings()` helper. `delete_cue` now returns warnings about orphaned executors, lost programming, empty sequences. 4 tests added.
  - **Issue #22** (P2 feat): Added 3 `GMA2Client` methods (`store_cue_across_sequences`, `label_cue_across_sequences`, `appearance_cue_across_sequences`) + 3 MCP tool wrappers. 12 tests added.
  - Created PRs #26, #27, #28, #29 targeting `dev` base branch
  - Addressed PR review comments on #27 (docstring casing, reset+color guard) and #29 (docstring casing, end_cue test)
  - Synced delta specs to main openspec/specs/
  - Updated README (20->24 tools) and doc files
  - Archived OpenSpec change to `openspec/changes/archive/2026-04-12-issues-19-22-assign-appearance-warnings-bulk/`
- PRs:
  - PR #26: `19-fix-assign-named-page-executor-addressing` (issue #19) -- Approved
  - PR #27: `20-feat-add-appearance-assignment-mcp-tool` (issue #20) -- Review addressed
  - PR #28: `21-feat-add-destructive-command-safety-warnings` (issue #21) -- Approved
  - PR #29: `22-feat-add-bulk-cue-operations-across-sequence-ranges` (issue #22) -- Review addressed

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Branch 19 tests | 842 tests | 842 pass | 842 pass | ✓ |
| Branch 20 tests | 845 tests | 845 pass | 845 pass | ✓ |
| Branch 21 tests | 842 tests | 842 pass | 842 pass | ✓ |
| Branch 22 tests | 851 tests | 851 pass | 851 pass | ✓ |

## Session: 2026-04-12 (Session 6 -- Issues #2, #3: Connection Resilience & Legacy Cleanup)

### Issue #3: Clean up legacy src/tools.py (PR #30)
- **Status:** complete (merged)
- Actions taken:
  - Created OpenSpec change `connection-resilience-and-tools-cleanup` with proposal, design, 2 specs, and tasks (30 items, TDD plan)
  - Created GitHub linked branch `issues/3` via `gh issue develop`
  - Deleted `src/tools.py` (159 lines) and `tests/test_tools.py` (132 lines)
  - Removed `from src.tools import set_gma2_client` import and `set_gma2_client(_client)` call from `src/server.py`
  - Verified zero remaining references to legacy tools module
  - Created PR #30, approved and merged into `dev`
- Files removed: `src/tools.py`, `tests/test_tools.py`
- Files modified: `src/server.py` (2 lines removed)

### Issue #2: Telnet connection resilience (PR #31)
- **Status:** complete (merged)
- Actions taken:
  - Created GitHub linked branch `issues/2` via `gh issue develop`
  - Implemented in parallel with issue #3 using worktree agents
  - **TDD**: Wrote 15 new tests in `tests/test_telnet_resilience.py` covering state transitions, health check, auto-reconnect, TTL optimization
  - Added `ConnectionState` enum (DISCONNECTED/CONNECTING/CONNECTED/RECONNECTING) and `state` property to `GMA2TelnetClient`
  - Added `check_connection()` health probe (sends newline, reads with timeout)
  - Added `_ensure_connected()` with bounded exponential backoff (default 3 retries, 1s base delay)
  - Added health check TTL optimization (skip probe if last command within 5s)
  - Added `server_lifespan` async context manager for graceful shutdown
  - Added `handle_connection_error` decorator on all 24 MCP tools
  - Replaced `_connected` boolean with `ConnectionState` check in `get_client()`
  - Code review caught 2 critical issues: missing TTL update in `send_command_with_response()`, overly strict `get_client()` guard. Fixed in follow-up commit.
  - Created PR #31, approved and merged into `dev`
- PRs:
  - PR #30: `issues/3` (issue #3) -- 2 commits, approved and merged
  - PR #31: `issues/2` (issue #2) -- 6 commits, approved and merged
- Files created: `tests/test_telnet_resilience.py` (238 lines), `openspec/specs/connection-resilience/spec.md`
- Files modified: `src/telnet_client.py` (+80 lines), `src/server.py` (+60/-7 lines), `tests/test_server_tools.py` (+50 lines)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Issue #3 full suite | 859 tests | 859 pass | 859 pass | ✓ |
| Issue #2 full suite | 884 tests | 884 pass | 884 pass | ✓ |

## Session: 2026-04-12 (Session 7 -- Issues #4, #5: Query/Introspection & Show Management)

### Issue #4: Query/introspection MCP tools (PR #32)
- **Status:** complete
- Actions taken:
  - Created OpenSpec change `add-query-and-show-management-tools` with proposal, design, 2 specs, and tasks (34 items, TDD plan)
  - Read grandMA2 User Manual v3.9 for List (p521), Info (p506), ListShows (p530), ListVar (p533), ListUserVar (p532), SaveShow (p667), LoadShow (p537), NewShow (p577), DeleteShow (p419), Backup (p368) keyword documentation
  - Created GitHub linked branch `issues/4` via `gh issue develop`
  - **TDD Red**: Wrote 29 command builder tests and 31 MCP tool tests (60 total)
  - Updated `list_var`, `list_user_var`, `list_shows` builders to accept optional filter parameter (per manual syntax `ListVar [Filter]`)
  - **TDD Green**: Implemented 7 query MCP tools: `list_groups`, `list_cues`, `list_presets`, `get_cue_annotation`, `get_group_annotation`, `list_variables`, `query_object`
  - All tools use `send_command_with_response()` to capture Telnet output, return raw text (wire format undocumented by MA)
  - Code review caught 2 issues: (1) `Info` keyword misuse -- renamed `get_cue_info`/`get_group_info` to `get_cue_annotation`/`get_group_annotation` since Info reads user annotations not object properties; (2) `end_preset_id` parameter silently ignored -- removed it
  - Created PR #32
- PRs:
  - PR #32: `issues/4` (issue #4) -- 4 commits, review addressed

### Issue #5: Show file management MCP tools (PR #33)
- **Status:** complete
- Actions taken:
  - Created GitHub linked branch `issues/5` via `gh issue develop`, based on `issues/4`
  - Updated `save_show`, `load_show`, `new_show` builders to accept `name` and `/noconfirm` parameters per manual syntax
  - **TDD Red**: Wrote 10 builder tests and 16 MCP tool tests + 2 negative tests (28 total)
  - **TDD Green**: Implemented 4 show management MCP tools: `save_show_tool`, `load_show_tool`, `new_show_tool`, `list_shows_tool`
  - Destructive operations (`load_show`, `new_show`) use `/noconfirm` to suppress GUI popups and include `save_first` parameter
  - `delete_show` excluded (irreversible, too dangerous for AI); `create_backup` excluded (`Backup` opens GUI menu per Manual p368)
  - Code review caught: `save_show` missing `/noconfirm` -- added it for consistency (same Telnet-blocking risk as load/new)
  - Updated README (24 -> 35 tools) with new tool categories and descriptions
  - Created PR #33
- PRs:
  - PR #33: `issues/5` (issue #5) -- 5 commits, review addressed
- Files created:
  - tests/test_query_builders.py, tests/test_query_tools.py, tests/test_show_management_builders.py, tests/test_show_management_tools.py
  - openspec/specs/query-introspection-tools/spec.md, openspec/specs/show-file-management-tools/spec.md
- Files modified:
  - src/server.py (+312 lines: 11 new tools, imports, EMPTY_RESPONSE_MSG)
  - src/commands/functions/list_ext.py (filter params on list_var, list_user_var, list_shows)
  - src/commands/functions/system.py (name/noconfirm params on save_show, load_show, new_show)
  - README.md (24 -> 35 tools, new query and show management sections)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Issue #4 query tests | 60 tests | 60 pass | 60 pass | pass |
| Issue #5 show mgmt tests | 28 tests | 28 pass | 28 pass | pass |
| Full suite after both | 965 tests | 965 pass | 965 pass | pass |

## Session: 2026-04-12 (Session 8 -- Issues #6, #7, #8: Macro, Effect, Workflows)

### Issues #6, #7, #8: Macro management, effect control, expanded workflows (PR #34)
- **Status:** complete
- Actions taken:
  - Created OpenSpec change `macro-effect-workflow-tools` with proposal, design, 5 specs (3 new + 2 modified), and tasks (39 items, TDD plan)
  - Read grandMA2 User Manual v3.9 for Macro Keyword (p.545-546), Clone Keyword (p.394-399), Effect keywords (p.434-448), ListEffectLibrary (p.523), ListMacroLibrary (p.526), Executor Keyword (p.456-458)
  - Created GitHub linked branch `6-macro-management` via `gh issue develop`
  - **Issue #6** (macro management): Added `store_macro()`, `label_macro()`, `delete_macro()` builders. Added 6 MCP tools: `run_macro`, `create_macro`, `label_macro_tool`, `list_macros`, `delete_macro_tool`. `create_macro` chains store→assign lines→label. 14 tests added.
  - **Issue #7** (effect control): Added 8 MCP tools: `apply_effect`, `set_effect_speed`, `set_effect_form`, `set_effect_range`, `set_effect_phase`, `set_effect_width`, `stop_effects`, `sync_effects_tool`. Input validation for speed units and range params. 13 tests added.
  - **Issue #8** (expanded workflows): Added 5 `GMA2Client` methods: `clone_fixtures` (with /overwrite, /merge, /noconfirm), `setup_effect_on_group` (group selection + effect params), `setup_executor_page` (page-qualified addressing), `batch_label`, `create_and_run_macro`. 15 tests added.
  - Added `DESTRUCTIVE_WARNINGS` for macro deletion
  - Code review caught 2 issues: (1) `setup_executor_page` silently ignored `page` parameter -- fixed with page-qualified addressing `Executor [Page].[ID]` per manual p.456; (2) `delete_macro` missing `/noconfirm` -- added default `noconfirm=True`
  - Synced 5 delta specs to main openspec/specs/ (3 new + 2 modified)
  - Updated README (35→49 tools) and doc files
  - Archived OpenSpec change
- PRs:
  - PR #34: `6-macro-management` (issues #6, #7, #8) -- Review addressed, 2 commits
- Files created:
  - openspec/specs/macro-management-tools/spec.md, openspec/specs/effect-control-tools/spec.md, openspec/specs/expanded-workflows/spec.md
- Files modified:
  - src/commands/functions/macro.py (+76 lines: 3 new builders)
  - src/commands/__init__.py (+5 exports), src/commands/functions/__init__.py (+3 exports)
  - src/server.py (+355 lines: 14 new tools, effect/macro imports, DESTRUCTIVE_WARNINGS for macro)
  - src/gma2_client.py (+217 lines: 5 new workflow methods, new imports)
  - tests/test_macro.py (+44 lines: 6 new tests)
  - tests/test_server_tools.py (+320 lines: 22 new tests)
  - tests/test_gma2_client.py (+170 lines: 14 new tests)
  - README.md (+36 lines: new tool table entries, workflow examples)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Macro builder tests | 9 tests | 9 pass | 9 pass | ✓ |
| Macro MCP tool tests | 9 tests | 9 pass | 9 pass | ✓ |
| Effect MCP tool tests | 13 tests | 13 pass | 13 pass | ✓ |
| Workflow method tests | 13 tests | 13 pass | 13 pass | ✓ |
| Full suite after fixes | 1005 tests | 1005 pass | 1005 pass | ✓ |

## Session: 2026-04-13 (Session 9 -- Issues #9, #10: Transport & Cleanup)

### Issue #9: Add HTTP/SSE transport option (PR #35)
- **Status:** complete (merged)
- Actions taken:
  - Created OpenSpec change `transport-and-cleanup` with proposal, design, 2 specs (1 new + 1 modified), and tasks (15 items, TDD plan)
  - Consulted FastMCP docs (MCP Python SDK) for `streamable-http` transport support
  - Consulted grandMA2 official docs -- Telnet Remote (port 30000) is inherently sequential, "accessing fixture setup and schedule functions can lock access for concurrent users"
  - Created GitHub linked branch `9-add-httpsse-transport-option-for-web-based-and-multi-client-access` via `gh issue develop`
  - **TDD Red**: Wrote 5 lock tests (concurrent serialization, mixed calls, no deadlock during reconnection) and 6 transport/config tests
  - **TDD Green**: Added `asyncio.Lock` to `GMA2TelnetClient.__init__()`, wrapped `send_command()` and `send_command_with_response()` with `async with self._lock`
  - Implemented transport selection in `main()`: `MCP_TRANSPORT` env var (stdio/streamable-http), `MCP_HOST`/`MCP_PORT` for HTTP binding
  - Updated `.env.template` with new env vars
  - Created PR #35, merged into dev
- Files created: `tests/test_server_transport.py` (124 lines)
- Files modified: `src/telnet_client.py` (+lock), `src/server.py` (+transport selection), `tests/test_telnet_client.py` (+5 lock tests), `.env.template`

### Issue #10: Remove main.py (PR #36)
- **Status:** complete (merged)
- Actions taken:
  - Created GitHub linked branch `10-update-or-remove-mainpy-uses-deprecated-telnetlib-removed-in-python-313` via `gh issue develop`
  - Deleted `main.py` (53 lines) -- standalone Telnet test using deprecated `telnetlib` (removed in Python 3.13)
  - Verified `pyproject.toml` entry point (`gma2-mcp = "src.server:main"`) references MCP server, not main.py
  - Cleaned up references in README.md, doc/findings.md, doc/task_plan.md, doc/progress.md
  - Created PR #36, merged into dev
- Files removed: `main.py`
- Files modified: `README.md`, `doc/findings.md`, `doc/task_plan.md`, `doc/progress.md`

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Lock serialization tests | 5 tests | 5 pass | 5 pass | ✓ |
| Transport/config tests | 6 tests | 6 pass | 6 pass | ✓ |
| Full suite after issue #9 | 1016 tests | 1016 pass | 1016 pass | ✓ |
| Full suite after issue #10 | 1005 tests | 1005 pass | 1005 pass | ✓ |

## Session: 2026-04-13 (Session 10 -- Issues #16, #17: Read-Back & Music Show Workflows)

### Issue #16: Add read-back tools for show object fields (PR #37)
- **Status:** complete (merged)
- Actions taken:
  - Created OpenSpec change `issues-16-17-readback-and-workflow-tools` with proposal, design, 2 specs, and tasks (29 items, TDD plan)
  - Researched grandMA2 official docs: `List` keyword (displays show data in feedback window, works over Telnet), `Info` keyword (user annotations), Telnet Remote (any local command works over Telnet on port 30000)
  - Confirmed Lua API (`gma.show.property.get`) is console-internal only -- `List` over Telnet is the viable approach
  - Created GitHub linked branch `16-feat-add-read-back-tools-for-show-object-fields` via `gh issue develop`
  - **TDD**: Wrote tests first for all 3 layers: command builders, response parser, MCP tools
  - Added `list_macro(macro_id, pool)` and `list_sequence_cue(sequence_id, cue_id)` command builders
  - Created `src/response_parser.py` with `parse_macro_lines()`, `parse_cue_info()`, `parse_object_label()` -- all return `parsed: False` on unrecognized format
  - Added 3 MCP tools: `read_macro_lines`, `read_cue_info`, `read_object_label` using `send_command_with_response()` + response parser
  - Code review caught 3 issues: (1) `info_preset` docstring wrong (color=4 not 2); (2) `cue_id` missing float type for fractional cues; (3) `read_object_label` needs macro pool-qualified ID note. All fixed.
  - Created PR #37, merged into dev
- Files created: `src/response_parser.py` (150 lines), `tests/test_response_parser.py` (180 lines), `tests/test_server_readback.py` (149 lines)
- Files modified: `src/commands/functions/info.py` (+45 lines: 2 builders + type fixes), `src/commands/__init__.py` (+4 exports), `src/server.py` (+80 lines: 3 tools)

### Issue #17: Add music show workflow tools (PR #38)
- **Status:** complete (merged)
- Actions taken:
  - Created GitHub linked branch `17-feat-add-music-show-workflow-tools` via `gh issue develop`
  - Implemented in parallel with issue #16 using worktree agents
  - **TDD**: Wrote tests first for GMA2Client methods and MCP tools
  - Added 3 `GMA2Client` methods: `create_song_objects()`, `setup_song_macro()`, `build_set_list()`
  - Added 3 MCP tools delegating to GMA2Client (matching existing bulk tool pattern)
  - Code review caught 1 issue: MCP tools bypassed GMA2Client, calling send_command directly (duplicated logic). Refactored to delegate to GMA2Client methods.
  - Created PR #38, merged into dev
- Files created: `tests/test_server_workflows.py` (122 lines)
- Files modified: `src/gma2_client.py` (+95 lines: 3 methods), `src/server.py` (+106 lines: 3 tools)

### Documentation & Archive
- Synced 2 delta specs to main `openspec/specs/` (show-object-readback, music-show-workflows)
- Archived OpenSpec change to `openspec/changes/archive/2026-04-13-issues-16-17-readback-and-workflow-tools/`
- Updated README (35→41 tools, new sections for read-back and workflow tools, response parser layer)
- Updated doc/task_plan.md, doc/progress.md, doc/findings.md

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Issue #16 full suite | 1043 tests | 1043 pass | 1043 pass | pass |
| Issue #17 full suite | 1028 tests | 1028 pass | 1028 pass | pass |
| Combined after merge | 1055 tests | 1055 pass | 1055 pass | pass |

## Session: 2026-04-14 (Session 11 -- Capability Exploration & Roadmap)

### Phase 8: Next-Generation Feature Roadmap
- **Status:** issues created, implementation pending
- Actions taken:
  - Explored codebase from senior grandMA2 lighting designer perspective
  - Audited command builder coverage: found 366 total exports, only 62 used (17%), leaving 304 unused builders
  - Categorized unused builders into 16 feature areas across 4 priority tiers
  - Prioritized from music show workflow perspective (user specializes in SMPTE-synced music shows)
  - Created 16 GitHub issues (#39-#54) with detailed technical approaches, acceptance criteria, and affected files
  - Updated doc/task_plan.md, doc/progress.md, doc/findings.md with new roadmap
- Issues created:
  - **P0**: #39 (timecode/SMPTE), #40 (set/add variables)
  - **P1**: #41 (MAtricks), #42 (cue timing), #43 (flash/swop/stomp), #44 (update cue)
  - **P2**: #45 (blind/preview), #46 (clone fixtures), #47 (rate/speed), #48 (release/top)
  - **P3**: #49 (copy/move), #50 (extended delete), #51 (effect extensions), #52 (park/unpark), #53 (MIDI), #54 (advanced selection)
- Key finding: Most issues (#40, #41, #42, #43, #44, #45, #47, #48, #49, #50, #51, #52, #54) only need MCP tool registration since builders already exist. #46 (clone) is even simpler -- GMA2Client method already exists.
- #39 (timecode) is the most complex -- needs new function builders and research into timecode telnet syntax.
- #53 (MIDI) has minimal stubs that need parameter extensions.

## 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| Where am I? | Phase 8: 16 new issues (#39-#54) created. Previous roadmap (#1-#22) complete. |
| Where am I going? | Implement 16 new features starting with P0 (timecode, variables), then P1 (MAtricks, timing, busking, update). |
| What's the goal? | Expand gma2-mcp from 54 to ~70+ tools, covering timecode, busking, blind programming, MAtricks, and advanced fixture control for music show workflows. |
| What have I learned? | 83% of command builders (304/366) are unused -- massive runway for new tools with minimal new builder code. Most issues just need MCP tool registration. Timecode (#39) is the most complex new feature. |
| What have I done? | 10 sessions: 24 issues resolved, 54 MCP tools, 15 GMA2Client workflows, response parser, connection resilience, configurable transport, 1055 tests. Session 11: capability exploration and 16 new issues created. |

## Session: 2026-06-17 (Session 12 -- Reliability Pivot & Verified Execution Core)

### Live console testing surfaced the real agent failure modes
- Connected to onPC `100.110.79.101:30000`, created a red color preset for Group 3 (LED Par), RGBW 100,0,0,0 (Color 4.1 "Red").
- Found the dominant agent error modes are **not** "too many tools": they are
  **(C) silent failure** (tools fabricate success, swallow `Error #NN`) and
  **(B) wrong argument** (agent can't know show-specific tokens, e.g. White = `COLORRGB5`, not 4).

### Issues filed
- **#55** -- `list_presets` name-based pool addressing (`List Preset "color"`) always errors; numeric `List Preset 4.1` works.
- **#56** -- action tools report hardcoded success without checking the console.
- **#57** -- tracking: tool-surface & reliability optimization (5 pillars, phased).
- **#58** -- verified execution core (Phase 1).
- **#59** -- follow-up: convert remaining ~40 mutating tools + workflow abort-on-error.

### Delivered (PR #60, merged to dev)
- Design doc `doc/design_tool_surface_optimization.md` (consensus from a grilling session).
- Verified execution core: `strip_ansi` + `detect_error` (numbered and bare `Error :`),
  `src/execution.py` (`ExecutionResult` + `build_result`), `GMA2TelnetClient.execute()`,
  and `run_verified()` in the server.
- Converted `send_raw_command`, `store_preset`, `apply_preset` to report real outcomes.
- TDD throughout; suite grew 1055 -> 1078 tests, all passing.

### Roadmap note
- **#39-#54 (one-tool-per-keyword expansion) is paused** pending #57 phases 2-4
  (selector grammar, show-introspection/name-resolution, three-tier surface) and a
  per-item re-triage (workflow vs covered-by-verified-command vs genuine keyword tool).
