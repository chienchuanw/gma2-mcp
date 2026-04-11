# Findings: GMA2 MCP Project

## Project Overview

**gma2-mcp** is an MCP (Model Context Protocol) server that lets AI assistants control grandMA2 lighting consoles over Telnet. It converts high-level AI tool calls into valid grandMA2 command-line syntax and sends them to the console.

- **Language:** Python 3.12+
- **Package manager:** uv
- **Key dependencies:** `mcp>=1.21.0`, `python-dotenv`, `telnetlib3`
- **Dev dependencies:** `pytest`, `pytest-asyncio`

---

## Architecture (4 Layers)

```
Layer 4: MCP Server         (src/server.py)         -- FastMCP, 24 tools, stdio transport
Layer 3: Orchestration      (src/gma2_client.py,     -- GMA2Client workflows, CommandSequence batching
                             src/command_sequence.py)
Layer 2: Command Builder    (src/commands/)          -- 200+ pure functions, returns command strings
Layer 1: Telnet Client      (src/telnet_client.py)   -- Async Telnet via telnetlib3
```

All console communication flows through Layer 1. Layers 2-4 never touch the network directly (except Layer 3's `execute()` which delegates to Layer 1).

---

## Layer 1: Telnet Client (`src/telnet_client.py`)

**Class:** `GMA2TelnetClient`

| Method | Purpose |
|--------|---------|
| `connect()` | Establish async Telnet connection via `telnetlib3.open_connection()` |
| `login()` | Send `login "user" "password"` command |
| `send_command(cmd, delay=0.3)` | Send command + CRLF, wait for processing |
| `send_command_with_response(cmd, timeout=2.0)` | Send and read response (for `list`, `info` queries) |
| `disconnect()` | Close writer, clear state |

- Supports async context manager (`async with`)
- Sync fallback via `run_sync()` (uses `asyncio.get_event_loop()`)
- Default config: port 30000, user "administrator", password "admin"

---

## Layer 2: Command Builder (`src/commands/`)

### Module Structure

```
src/commands/
  __init__.py           -- Public API, exports 200+ functions
  constants.py          -- PRESET_TYPES, STORE_*_OPTIONS
  helpers.py            -- _build_store_options() internal helper
  functions/            -- Function keywords (verbs) -- 30 modules
  objects/              -- Object keywords (nouns) -- 8 modules
```

### Total: ~8,316 lines across all command modules

### Object Keyword Modules (`src/commands/objects/`)

| Module | Objects |
|--------|---------|
| `fixtures.py` | fixture, channel, attribute, feature |
| `groups.py` | group |
| `presets.py` | preset, preset_type |
| `cues.py` | cue, cue_part |
| `executors.py` | executor, sequence |
| `layouts.py` | layout |
| `dmx.py` | dmx, dmx_universe |
| `time.py` | timecode, timecode_slot, timer |
| `executor_objects.py` | fader, fader_page, button_page, channel_fader, etc. |
| `misc_objects.py` | camera, macro, mask, master, plugin, view, world, etc. |

### Function Keyword Modules (`src/commands/functions/`)

| Module | Functions |
|--------|-----------|
| `values.py` | at, at_full, at_zero, attribute_at, fixture_at, channel_at, group_at, executor_at, preset_type_at |
| `store.py` | store, store_cue, store_group (accepts optional `name` for inline naming), store_preset |
| `selection.py` | select_fixture, select_group, clear, clear_selection, clear_active, clear_all |
| `playback.py` | go, go_executor, go_sequence, go_back, goto, goto_cue, pause_sequence, def_go_*, go_fast_* |
| `edit.py` | copy, copy_cue, move, delete, delete_cue, delete_fixture, delete_group, delete_preset, remove, remove_* |
| `labeling.py` | label, label_group, label_preset, label_sequence_cue, appearance |
| `assignment.py` | assign, assign_fade, assign_function, assign_to_layout, assign_macro_cmd, assign_cue_cmd, empty, temp_fader |
| `info.py` | list_objects, list_attribute, list_cue, list_group, list_preset, info, info_cue, info_group, info_preset |
| `helping.py` | add_to_selection, remove_from_selection, at_relative, page_next, page_previous, condition_and, if_condition |
| `blackout.py` | blackout, black, freeze, highlight, full_highlight, solo |
| `blind.py` | blind, blind_edit, preview, preview_edit |
| `cue_timing.py` | delay, out_delay, fade, out_fade |
| `fixture_control.py` | align, all_keyword, fix, locate, next_keyword, previous, invert |
| `executor_control.py` | off, on, kill, flash, swop, stomp, temp, toggle, release, top, select |
| `programmer.py` | block, unblock, clone, default, extract, insert, record, replace, update, oops |
| `intensity.py` | full, to_full, zero, to_zero, load, learn |
| `crossfade.py` | crossfade, crossfade_a, crossfade_b, manual_xfade |
| `rate_speed.py` | rate, rate1, double_rate, half_rate, double_speed, half_speed, speed |
| `matricks.py` | matricks, matricks_blocks, matricks_filter, matricks_groups, matricks_interleave, matricks_reset, matricks_wings |
| `effect.py` | effect, effect_attack, effect_bpm, effect_decay, effect_delay, effect_fade, effect_form, effect_high, effect_hz, effect_id, effect_low, effect_phase, effect_sec, effect_speed_group, effect_width, sync_effects |
| `system.py` | backup, shutdown, reboot, login, logout, lock, unlock, setup, save_show, load_show, new_show, delete_show, etc. |
| `network.py` | remote, telnet, join_session, leave_session, chat, invite_station, etc. |
| `macro.py` | macro_with_input_after, macro_with_input_before |
| `park.py` | park, unpark |
| `call.py` | call, call_preset |
| `variables.py` | set_var, set_user_var, add_var, add_user_var |
| `list_ext.py` | list_shows, list_oops, list_var, list_user_var, list_library, etc. |
| `advanced_edit.py` | flip, circular_copy, import_keyword, export_keyword, shuffle_selection, etc. |
| `conditionals.py` | end_if, if_active, if_output, if_prog, or_keyword, with_keyword |
| `navigation.py` | down, up, next_row, search, move_3d, rotate_3d, etc. |
| `show_data.py` | crash_log_*, lua, psr, thru, update_firmware, update_software, etc. |
| `rdm.py` | rdm_automatch, rdm_autopatch, rdm_fixture_type, rdm_info, etc. |
| `midi.py` | midi_control, midi_note, midi_program |
| `step_timing.py` | snap_percent, step_fade, step_in_fade, step_out_fade, fade_path |
| `flash_swop_ext.py` | flash_go, flash_on, swop_go, swop_on, store_look |

### Constants (`src/commands/constants.py`)

- `PRESET_TYPES`: Maps names to IDs -- dimmer=1, position=2, gobo=3, color=4, beam=5, focus=6, control=7, shapers=8, video=9 (fixed in issue #1; was incorrectly color=2, beam=4, etc.)
- `STORE_FLAG_OPTIONS`: merge, overwrite, remove, noconfirm, global, selective, universal, auto, trackingshield, embedded
- `STORE_BOOL_OPTIONS`: cueonly, tracking, keepactive, presetfilter, addnewcontent, originalcontent, effects, values, valuetimes
- `STORE_VALUE_OPTIONS`: source, useselection, screen, x, y

---

## Layer 3: Orchestration

### GMA2Client (`src/gma2_client.py`)

High-level workflows that compose multiple command builder calls:

| Method | Workflow |
|--------|----------|
| `build_cue_list(seq_id, cues)` | Store cues with inline names, assign fade times (1 command per named cue via `store_cue(id, name=name)` instead of separate `label()` call) |
| `setup_group_with_preset(fixtures, group_id, ...)` | Select fixtures -> store group with inline name -> apply preset (3 commands instead of 4, uses `store_group(id, name=name)` instead of separate `label_group()`) |
| `quick_look(fixtures, value, store_as_cue)` | Select fixtures -> set value -> optionally store cue |
| `assign_sequences_to_executors(assignments)` | Batch assign sequence/executor pairs |

- Factory: `GMA2Client.create(host, port, user, password)` -- async
- Supports async context manager
- All methods return `dict` with `commands_sent`, `count`, `summary`

### CommandSequence (`src/command_sequence.py`)

Builder-pattern for composing command batches:

| Method | Purpose |
|--------|---------|
| `add(cmd)` | Append command, returns self for chaining |
| `preview()` | Return command list without executing |
| `clear()` | Reset command list |
| `execute(client, delay=None)` | Send all commands via telnet client |

- Implements `__len__`, `__iter__`, `__str__`, `__repr__`
- Returns `dict` with `commands_sent`, `count`, `success`

---

## Layer 4: MCP Server (`src/server.py`)

**Server name:** `grandMA2-MCP`
**Transport:** stdio
**Framework:** FastMCP (`mcp.server.fastmcp`)

### 24 MCP Tools

| Category | Tool | Args |
|----------|------|------|
| **Fixture Groups** | `create_fixture_group` | start_fixture, end_fixture, group_id, group_name? (uses inline store-with-name: 2 commands instead of 3) |
| **Cue Management** | `store_cue` | cue_id, name?, merge?, overwrite?, noconfirm? |
| | `delete_cue` | cue_id |
| | `goto_cue_tool` | cue_id, executor?, sequence? |
| **Fixture Control** | `set_fixture_value` | fixture_id, value, end_fixture? |
| | `set_fixture_attribute` | fixture_id, attribute, value, end_fixture? |
| | `clear_programmer` | mode (all/selection/active/default) |
| **Preset Management** | `store_preset` | preset_type, preset_id, scope? |
| | `apply_preset` | preset_type, preset_id |
| **Executor Control** | `control_executor` | executor_id, action (on/off/go/kill/toggle) |
| | `set_executor_fader` | executor_id, value |
| | `assign_to_executor` | sequence_id, executor_id |
| **Global State** | `toggle_blackout` | (none) |
| | `toggle_highlight` | (none) |
| **Labeling** | `label_object` | object_type, object_id, name |
| | `label_sequence_cue` | sequence, cue_id, name, end_cue? |
| **Macro Tools** | `set_macro_line` | macro_id, line, command, pool? |
| **Cue CMD** | `set_cue_cmd` | cue_id, sequence_id, command |
| **Sequence Playback** | `execute_sequence` | sequence_id, action (go/pause/goto), cue_id? |
| **Appearance** | `assign_appearance` | object_type, object_id, end?, red?, green?, blue?, hue?, saturation?, brightness?, color?, source_type?, source_id?, reset? |
| **Bulk Cue Ops** | `store_cue_across_sequences` | cue_id, sequence_start, sequence_end, cue_name? |
| | `label_cue_across_sequences` | cue_id, sequence_start, sequence_end, label |
| | `appearance_cue_across_sequences` | cue_id, sequence_start, sequence_end, red?, green?, blue?, color? |
| **Raw Command** | `send_raw_command` | command |

### Connection Management

- Lazy singleton: `get_client()` creates and connects on first call
- Global `_client` and `_connected` state
- Config from env: `GMA_HOST`, `GMA_PORT`, `GMA_USER`, `GMA_PASSWORD`

---

## Legacy Module: `src/tools.py`

Original tool implementations before MCP migration. Contains:
- `create_fixture_group()`, `execute_sequence()`, `send_raw_command()`
- Uses global `_gma2_client` via `set_gma2_client()` / `get_gma2_client()`
- Missing `await` on `send_command()` calls (sync-style but functions are async)
- Still referenced by `src/server.py` (for `set_gma2_client`) and some tests

---

## Test Suite

- **850+ test cases** across **48+ test files**
- Config: `pytest.ini` with `asyncio_mode = auto`
- Tests cover:
  - Every command builder module (unit tests for string output)
  - `CommandSequence` class
  - `GMA2Client` orchestration (mocked telnet)
  - `GMA2TelnetClient` (mocked telnetlib3)
  - MCP server tools (`test_server_tools.py`)
  - Legacy tools module (`test_tools.py`)

---

## Configuration & Scripts

### Environment (`.env` / `.env.template`)
```
GMA_HOST=2.0.0.1
GMA_PORT=30000
GMA_USER=administrator
GMA_PASSWORD=admin
```

### Makefile Targets
| Target | Command |
|--------|---------|
| `server` | `./connect.sh` (Telnet + auto-login via expect) |
| `log` | `telnet 2.0.0.166 30001` (read-only log port) |
| `test` | `uv run pytest -v` |

### Entry Points
- MCP server: `uv run python -m src.server` or `gma2-mcp` (via pyproject.toml `[project.scripts]`)
- Login test: `python main.py` (standalone, uses deprecated `telnetlib`)

---

## Project File Tree

```
gma2-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py               # MCP server (FastMCP, 24 tools)
│   ├── telnet_client.py        # Async Telnet client (telnetlib3)
│   ├── gma2_client.py          # High-level workflow orchestration
│   ├── command_sequence.py     # Command batch builder
│   ├── tools.py                # Legacy tool implementations
│   └── commands/
│       ├── __init__.py         # Public API (200+ exports)
│       ├── constants.py        # PRESET_TYPES, store options
│       ├── helpers.py          # _build_store_options()
│       ├── functions/          # 30 modules -- function keywords
│       │   ├── __init__.py
│       │   ├── values.py, store.py, selection.py, playback.py,
│       │   │   edit.py, labeling.py, assignment.py, info.py,
│       │   │   helping.py, blackout.py, blind.py, cue_timing.py,
│       │   │   fixture_control.py, executor_control.py, programmer.py,
│       │   │   intensity.py, crossfade.py, rate_speed.py, matricks.py,
│       │   │   effect.py, system.py, network.py, macro.py, park.py,
│       │   │   call.py, variables.py, list_ext.py, advanced_edit.py,
│       │   │   conditionals.py, navigation.py, show_data.py, rdm.py,
│       │   │   midi.py, step_timing.py, flash_swop_ext.py
│       │   └── ...
│       └── objects/            # 8+ modules -- object keywords
│           ├── __init__.py
│           ├── fixtures.py, groups.py, presets.py, cues.py,
│           │   executors.py, layouts.py, dmx.py, time.py,
│           │   executor_objects.py, misc_objects.py, attributes.py
│           └── ...
├── tests/                      # 48 test files, 808 tests
├── doc/
│   └── 2024-09-30_grandMA2_User_Manual_v3-9.pdf
├── main.py                     # Standalone login test
├── connect.sh                  # Telnet auto-login script (expect)
├── Makefile                    # server, log, test targets
├── pyproject.toml              # Project metadata, deps, entry point
├── pytest.ini                  # Test config
├── .env.template               # Env var template
├── .env                        # Actual env vars (gitignored)
├── .gitignore
├── .python-version             # 3.12
├── uv.lock
└── README.md                   # Comprehensive docs
```

---

## Observations & Potential Improvements

1. ~~**`PRESET_TYPES` collision**: Both "position" and "color" map to ID 2.~~ **FIXED** in issue #1 -- color is now correctly 4, all types shifted to match manual.
2. ~~**Legacy `src/tools.py`**: Contains functions that don't `await` async calls.~~ **FIXED** in issue #3 (PR #30) -- deleted `src/tools.py` and `tests/test_tools.py`, removed `set_gma2_client` import from `server.py`.
3. **`main.py` uses deprecated `telnetlib`**: This standalone test script uses the stdlib `telnetlib` (removed in Python 3.13), unlike the main codebase which uses `telnetlib3`. (Issue #10)
4. ~~**No error handling in MCP tools**: Most tools don't handle cases where the telnet connection drops mid-session.~~ **FIXED** in issue #2 (PR #31) -- added `ConnectionState` enum, `check_connection()` health probe, `_ensure_connected()` with bounded exponential backoff, health check TTL, graceful shutdown via `server_lifespan`, and `handle_connection_error` decorator on all 24 MCP tools.
5. **No response parsing**: `send_command()` is fire-and-forget. The server never confirms whether a command was accepted by the console. (Issue #4)
6. **GMA2Client.create() is not a context manager factory**: The `create()` classmethod returns a `GMA2Client` but you need to wrap it in `async with` separately. The README example `async with GMA2Client.create(...) as client:` works because `__aenter__` returns `self`.

## grandMA2 Manual Key Findings (v3.9)

- **1,850 pages** covering the complete console feature set
- **Telnet Remote (Ch.34.4)**: Any command-line command can be sent via Telnet on port 30000. Login is case-sensitive. Accessing fixture setup via Telnet locks access for other users.
- **Preset Pools (Ch.19.2)**: 9 numbered preset types (1-9) plus "Dynamic" and "All" (unnumbered, UI-only). Each pool stores values of its type.
- **Macros (Ch.38)**: Stored command sequences with variables (`$name`), conditionals, timing (wait/follow/go). Executed as command-line input. Can use `@` for user input prompts. Predefined variables: `$SELECTEDEXEC`, `$SHOWFILE`, `$USER`, etc.
- **Effects (Ch.31)**: Continuous parameter modulation with configurable BPM/Hz, waveform, phase, width. Can be stored in cues or assigned to executors.
- **Chasers (Ch.30)**: Step-based sequences that cycle through cues automatically.
- **Timecode (Ch.35)**: Record and play back timecode shows synchronized to external time sources.
