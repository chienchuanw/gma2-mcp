

# GMA2 MCP

An MCP server that lets AI assistants control grandMA2 lighting consoles via Telnet. It exposes 101 high-level tools for cue management, fixture control, preset management, executor control, macro editing, appearance assignment, bulk operations, console state queries, show file management, read-back verification, music show workflows, and more through the Model Context Protocol.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [MCP Registration](#mcp-registration)
- [Usage](#usage)
  - [MCP Tools](#mcp-tools)
  - [Command Builder](#command-builder)
  - [Direct Telnet Access](#direct-telnet-access)
- [Command Reference](#command-reference)
  - [Helping Keywords](#1-helping-keywords-prepositionsconjunctions)
  - [Object Keywords](#2-object-keywords-nouns)
  - [Function Keywords](#3-function-keywords-verbs)
  - [At Keyword](#4-at-keyword-special)
  - [Copy and Move](#5-copy-and-move-keywords)
  - [Assign](#6-assign-keyword)
  - [Label](#7-label-keyword)
  - [Appearance](#8-appearance-keyword)
  - [Macro Placeholder](#9-macro-placeholder--character)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)

## Overview

grandMA2 consoles accept commands over Telnet, but building correct command strings requires knowledge of the MA2 syntax rules -- keyword ordering, preset type mappings, option flags, and object hierarchies. This project handles that complexity in layered components:

1. **Command Builder** (`src/commands/`) -- Python functions that construct valid grandMA2 command strings following the official syntax rules. Each function is a thin wrapper that returns a string; it never touches the network.
2. **MCP Server** (`src/server.py`) -- A FastMCP server that exposes 101 tools covering cue management, fixture control, presets, executors, global state, labeling, appearance assignment, macro editing, bulk cue operations, sequence playback, console state queries, show file management, read-back verification, music show workflows, and raw commands over stdio transport. It manages a persistent Telnet connection to the console and delegates command construction to the builder layer.
3. **Response Parser** (`src/response_parser.py`) -- Pure functions for parsing grandMA2 Telnet output: tabular `List` data into structured dicts, and inline `Error #NN: REASON` failures (with ANSI stripping) for the verified execution path.
4. **Execution Core** (`src/execution.py`) -- `ExecutionResult` plus the pure `build_result()` that turns a raw Telnet reply into a structured `{ok, echo, error_code, error_text, raw}`. Mutating tools route through `GMA2TelnetClient.execute()` so they report the console's real outcome instead of fabricating success.
5. **GMA2Client** (`src/gma2_client.py`) -- A high-level orchestration class that composes multiple command builder calls into workflow-level methods (e.g., build an entire cue list, set up a fixture group with a preset, create song objects for music shows).
6. **CommandSequence** (`src/command_sequence.py`) -- A builder-pattern class for composing multiple commands into an ordered batch that can be previewed and executed as a unit.

The command builder covers all grandMA2 command-line keywords organized by category: object keywords (fixtures, channels, groups, presets, cues, sequences, executors), function keywords (store, delete, copy, move, goto, label, assign, and many more), and helping keywords (thru, at, +).

## Features

- **101 MCP tools** -- Cue management (store/update/delete/goto, CMD assignment, timing, bulk operations), fixture control (set values/attributes, clear programmer, advanced selection: next/previous/invert/locate/align/fix), preset management (store/apply), executor control (on/off/go/kill/toggle/release/top, fader, rate/speed, flash/swop/stomp/temp busking), global state (blackout, highlight), blind/preview modes, object labeling, appearance assignment, copy/move and extended delete (group/preset/fixture/show), park/unpark, macro editing, effect control (apply, speed, form, range, phase, width, envelope, seconds, speed group, sync), MAtricks fan effects, show/user variables, timecode (SMPTE), MIDI output (note/control/program), clone fixtures, console state queries, show file management, read-back verification, music show workflows, and raw command execution.
- **Verified command execution** -- grandMA2 reports failures inline in the Telnet reply (`Error #NN: REASON`). Mutating tools route through a verified execution core (`src/execution.py`) that parses the reply and returns the console's real outcome, so the assistant is not given false success on a rejected command. Multi-command tools abort on the first error.
- **Range/batch selectors** -- Object tools accept grandMA2 selection expressions (`1 thru 10`, `1 + 3 + 5`, `1 thru 10 - 4`) validated by `src/commands/selector.py`, so a whole range copies/moves in one call instead of looping per ID.
- **Show-aware name resolution** -- `src/introspection.py` queries `List Attribute` (cached) and resolves friendly, show-specific attribute names (e.g. `White` -> `COLORRGB5`) before sending, rejecting unknown names with suggestions.
- **Fixture-profile resolver** -- `src/profile_resolver.py` parses MA2 fixture-type / GDTF XML and resolves named functions (`open`/`closed`/`strobe`/`random`/`iris`/`frost`/`prism`) to the correct per-fixture-type value, so the same logical preset (e.g. "Strobe Fast") gets the right DMX value on every profile.
- **Palette builders** -- `build_color_palette` and the generalized `build_preset_palette` program whole preset palettes in one call, with per-fixture-type values, Global/Selective scope, and per-type merge (extend a palette to a new fixture group non-destructively).
- **Destructive command safety warnings** -- Delete tools include informational warnings about downstream effects (orphaned executor handles, lost cue programming) to help AI assistants understand impact before confirming.
- **Complete command builder** -- Over 350 Python functions covering all grandMA2 command-line keywords across 30+ modules, each returning a correctly formatted command string.
- **High-level client** -- `GMA2Client` provides workflow-level methods: build cue lists, set up fixture groups with presets, quick look programming, batch executor assignments. Uses grandMA2's inline naming syntax to minimize Telnet round-trips.
- **Command chaining** -- `CommandSequence` lets you compose multiple commands, preview them, and execute them as a batch.
- **Resilient Telnet client** -- Built on `telnetlib3` with automatic login, persistent connections, connection health checking, auto-reconnection with bounded exponential backoff, command serialization via `asyncio.Lock`, and graceful shutdown. If the console restarts or the network drops, the client detects the failure and reconnects transparently before the next command.
- **Connection error surfacing** -- MCP tools catch connection failures and return human-readable error messages instead of unhandled exceptions, so the AI assistant knows when commands are not reaching the console.
- **Configurable transport** -- Supports `stdio` (default, single client) and `streamable-http` (multi-client, web-based access) transports. HTTP host and port are configurable via environment variables.
- **Configurable via environment** -- Host, port, user, password, and transport settings set through `.env` or environment variables.

## Getting Started

### Prerequisites

- Python >= 3.12
- A grandMA2 console (or onPC) with Telnet access enabled
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

On macOS, if you need a Telnet client for manual testing:

```bash
brew install telnet
```

### Installation

```bash
git clone <repository-url>
cd gma2-mcp
```

Using uv:

```bash
uv sync
```

Using pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configuration

Copy the template and fill in your console details:

```bash
cp .env.template .env
```

| Variable       | Description                          | Default         |
|----------------|--------------------------------------|-----------------|
| `GMA_HOST`      | IP address of the grandMA2 onPC                | `127.0.0.1`     |
| `GMA_PORT`      | Telnet port                                    | `30000`         |
| `GMA_USER`      | Login username                                 | `administrator` |
| `GMA_PASSWORD`  | Login password                                 | `admin`         |
| `MCP_TRANSPORT` | MCP transport protocol (`stdio`, `streamable-http`) | `stdio`     |
| `MCP_HOST`      | HTTP bind address (streamable-http only)       | `127.0.0.1`     |
| `MCP_PORT`      | HTTP port (streamable-http only)               | `8000`          |

`GMA_HOST` should be set to the IP address of the machine running grandMA2 onPC. You can find this in the onPC network settings or by checking the machine's network configuration.

Port 30000 is the standard command port. Port 30001 is read-only (log output).

To enable HTTP transport for web-based or multi-client access:

```bash
MCP_TRANSPORT=streamable-http
MCP_HOST=0.0.0.0    # bind to all interfaces (default: 127.0.0.1)
MCP_PORT=3000        # custom port (default: 8000)
```

When using `streamable-http`, concurrent commands from multiple clients are automatically serialized via an internal lock to prevent interleaved Telnet commands, since the grandMA2 console processes commands sequentially.

### MCP Registration

Add the server to your MCP client configuration.

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "gma2": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/gma2-mcp",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "GMA_HOST": "2.0.0.1",
        "GMA_USER": "administrator",
        "GMA_PASSWORD": "admin"
      }
    }
  }
}
```

**Without uv** -- point directly to the virtualenv Python:

```json
{
  "mcpServers": {
    "gma2": {
      "command": "/path/to/gma2-mcp/.venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/gma2-mcp",
      "env": {
        "GMA_HOST": "2.0.0.1",
        "GMA_USER": "administrator",
        "GMA_PASSWORD": "admin"
      }
    }
  }
}
```

**Claude Code (CLI / IDE extensions)**

Claude Code manages MCP servers through its own configuration, separate from Claude Desktop. You can set it up using either the CLI command or by editing the settings file directly.

**Option 1: Using the `claude mcp add` command (recommended)**

Run the following command in your terminal:

```bash
claude mcp add gma2 \
  -e GMA_HOST=2.0.0.1 \
  -e GMA_USER=administrator \
  -e GMA_PASSWORD=admin \
  -- uv --directory /path/to/gma2-mcp run python -m src.server
```

This registers the MCP server with Claude Code. The `-e` flags set environment variables that the server reads at startup. Replace `/path/to/gma2-mcp` with the actual path to your cloned repository, and adjust the `GMA_HOST`, `GMA_USER`, and `GMA_PASSWORD` values to match your console.

To register the server for a specific project only (instead of globally), add the `-s project` flag:

```bash
claude mcp add gma2 -s project \
  -e GMA_HOST=2.0.0.1 \
  -e GMA_USER=administrator \
  -e GMA_PASSWORD=admin \
  -- uv --directory /path/to/gma2-mcp run python -m src.server
```

**Option 2: Editing the settings file manually**

Add the server entry to your Claude Code settings file. The file location depends on the scope:

- **User-level** (available in all projects): `~/.claude/settings.json`
- **Project-level** (available only in the current project): `.claude/settings.json` in the project root

```json
{
  "mcpServers": {
    "gma2": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/gma2-mcp",
        "run",
        "python",
        "-m",
        "src.server"
      ],
      "env": {
        "GMA_HOST": "2.0.0.1",
        "GMA_USER": "administrator",
        "GMA_PASSWORD": "admin"
      }
    }
  }
}
```

**Verifying the setup**

After registering the server, verify it is working:

```bash
# List all registered MCP servers
claude mcp list

# Check the server details
claude mcp get gma2
```

When you start a new Claude Code session, the server starts automatically. You can confirm the tools are available by asking Claude to list its MCP tools or by directly requesting a grandMA2 operation (e.g., "toggle blackout on the console").

**Managing the server**

```bash
# Remove the server
claude mcp remove gma2

# Re-add with different settings
claude mcp add gma2 \
  -e GMA_HOST=192.168.1.100 \
  -- uv --directory /path/to/gma2-mcp run python -m src.server
```

## Usage

### MCP Tools

The server exposes 101 tools:

| Tool                              | Description                                                          |
|-----------------------------------|----------------------------------------------------------------------|
| `capabilities`                    | Report version, registered tools, and profile schema version (contract surface; no console connection) |
| `create_fixture_group`            | Select fixtures and store as a named group (2 commands)              |
| `store_cue`                       | Store current programmer state as a cue                              |
| `delete_cue`                      | Delete a cue (includes downstream safety warnings)                   |
| `goto_cue_tool`                   | Jump to a specific cue (executor or sequence)                        |
| `set_fixture_value`               | Set fixture(s) to a dimmer value (0-100)                             |
| `set_fixture_attribute`           | Set a specific attribute (Pan, Tilt, etc.) on fixture(s)             |
| `clear_programmer`                | Clear the programmer (all, selection, active, default)               |
| `store_preset`                    | Store current values as a preset                                     |
| `apply_preset`                    | Apply an existing preset to the current selection                    |
| `control_executor`                | On/off/go/kill/toggle an executor                                    |
| `set_executor_fader`              | Set executor fader level (0-100)                                     |
| `assign_to_executor`              | Assign a sequence to an executor (supports named page paths)         |
| `toggle_blackout`                 | Toggle grand blackout                                                |
| `toggle_highlight`                | Toggle highlight mode                                                |
| `label_object`                    | Assign a name label to any MA2 object                                |
| `label_sequence_cue`              | Label a cue within a specific sequence                               |
| `assign_appearance`               | Set frame/background colors on pool objects and cues (RGB/HSB/hex)   |
| `set_macro_line`                  | Set the command for a specific macro line                            |
| `run_macro`                       | Execute a macro by ID (Go+ Macro)                                    |
| `create_macro`                    | Create a macro with command lines (store + assign lines + label)     |
| `label_macro_tool`                | Label a macro in the macro pool                                      |
| `list_macros`                     | List macros in the macro pool                                        |
| `delete_macro_tool`               | Delete a macro (with destructive operation warnings)                 |
| `apply_effect`                    | Apply effect from pool to current fixture selection                  |
| `set_effect_speed`                | Set effect speed in BPM or Hz                                        |
| `set_effect_form`                 | Set effect waveform (sine, ramp, square, etc.)                       |
| `set_effect_range`                | Set effect high and/or low values                                    |
| `set_effect_phase`                | Set effect phase offset in degrees                                   |
| `set_effect_width`                | Set effect width (percentage of cycle)                               |
| `stop_effects`                    | Stop running effects for current selection (Off Effect)              |
| `sync_effects_tool`               | Synchronize all running effects                                      |
| `set_cue_cmd`                     | Assign a command to a cue's CMD field                                |
| `store_cue_across_sequences`      | Store a cue across a range of sequences in one call                  |
| `label_cue_across_sequences`      | Label a cue across a range of sequences in one call                  |
| `appearance_cue_across_sequences` | Set cue appearance across a range of sequences in one call           |
| `execute_sequence`                | Go, pause, or goto a cue in a sequence                               |
| `list_groups`                     | List all defined groups (returns raw console response)               |
| `list_cues`                       | List cues in a sequence (returns raw console response)               |
| `list_presets`                    | List presets by type with validation (returns raw console response)   |
| `get_cue_annotation`              | Read user-added annotation text on a cue                             |
| `get_group_annotation`            | Read user-added annotation text on a group                           |
| `list_variables`                  | List show or user variables with optional filter                     |
| `query_object`                    | Generic query for any MA2 object type (list or annotation mode)      |
| `save_show_tool`                  | Save the current show file (optional name)                           |
| `load_show_tool`                  | Load a show file (destructive -- warns about unsaved changes)        |
| `new_show_tool`                   | Create a new empty show (destructive -- warns about unsaved changes) |
| `list_shows_tool`                 | List available show files on the console                             |
| `read_macro_lines`                | Read macro line content (parsed into structured data)                |
| `read_cue_info`                   | Read cue properties: label, CMD, fade (parsed)                       |
| `read_object_label`              | Read the label of any pool object (sequence, page, macro, etc.)      |
| `create_song_objects`             | Create and label a Sequence + Page pair for a song                   |
| `setup_song_macro`                | Create a macro with SetVar command for song variable assignment       |
| `build_set_list`                  | Build a set-list sequence with cue-to-macro links                    |
| `send_raw_command`                | Send any grandMA2 command-line instruction                           |

#### Query / Introspection Tools

The query tools use `send_command_with_response()` to capture the grandMA2 Telnet output and return raw text. The grandMA2 manual does not document the exact Telnet wire format for `List` and `Info` responses, so these tools return unprocessed console output that the AI can interpret directly.

- **`list_groups`**, **`list_cues`**, **`list_presets`** -- Use the grandMA2 `List` keyword to retrieve show data. Accept optional ID ranges (e.g., `list_groups(group_id=1, end_group_id=10)`). `list_presets` validates the preset type against the 9 known types before sending.
- **`get_cue_annotation`**, **`get_group_annotation`** -- Use the grandMA2 `Info` keyword, which reads user-added descriptive text annotations on objects (set via `Info Group 3 "some note"` on the console). These do NOT return object properties like fade times or fixture composition -- use `list_cues` or `list_groups` for that.
- **`list_variables`** -- Routes to `ListVar` (show variables) or `ListUserVar` (user variables) based on the `variable_type` parameter. Supports an optional filter pattern.
- **`query_object`** -- Generic query for any grandMA2 object type not covered by the dedicated tools. Supports `mode="list"` (default) and `mode="annotation"`.

All query tools return a descriptive message instead of an empty string when the console returns no data.

#### Show File Management Tools

- **`save_show_tool`** -- Saves the current show file. Accepts an optional `show_name` to save as a specific name. Uses `/noconfirm` to suppress the overwrite confirmation popup that would block Telnet.
- **`load_show_tool`** -- Loads a show file by name. This is a destructive operation: unsaved changes to the current show are lost. Accepts `save_first=True` to save the current show before loading. Uses `/noconfirm` to suppress the GUI popup.
- **`new_show_tool`** -- Creates a new empty show. Same destructive behavior and `save_first` option as `load_show_tool`.
- **`list_shows_tool`** -- Lists available show files on the console's selected drive. Accepts an optional filter pattern.

#### Read-Back Tools

The read-back tools use `send_command_with_response()` to capture grandMA2 `List` command output and parse it into structured dicts via `src/response_parser.py`. Each tool returns a dict with parsed fields plus a `raw_response` field for debugging. If the response format is unrecognized, the tools return `parsed: False` with the raw output.

- **`read_macro_lines`** -- Sends `List Macro {pool}.{id}` and parses each line's number and CMD content. Returns `{"macro_id": N, "parsed": True, "lines": [{"line_number": 1, "cmd": "..."}], "raw_response": "..."}`.
- **`read_cue_info`** -- Sends `List Cue {id} Sequence {seq}` and extracts label, CMD, and fade time. Returns `{"sequence_id": N, "cue_id": N, "label": "...", "cmd": "...", "fade": "...", "raw_response": "..."}`.
- **`read_object_label`** -- Sends `List {type} {id}` and extracts the object's name/label. Works with any pool object type (sequence, page, group, etc.). For macros, the `object_id` must be pool-qualified (e.g., `"1.5"` for Macro 5 in Pool 1).

#### Music Show Workflow Tools

High-level tools that automate common multi-step patterns for music show programming. These delegate to `GMA2Client` workflow methods.

- **`create_song_objects`** -- Creates and labels a Sequence + Page pair with the same ID and name. This is the standard pattern for per-song programming (e.g., `create_song_objects(song_id=101, song_name="Opening+Childhood")` sends 2 commands).
- **`setup_song_macro`** -- Creates a labeled macro with a `SetVar` command on line 1 for tracking the current song. Accepts an optional `var_name` (default: `$song`). Sends 3 commands: store macro, label, assign CMD.
- **`build_set_list`** -- Creates a set-list sequence with cues linked to song macros. For each song, stores a cue with the song name as label and assigns `Macro {id}` as the cue CMD. Accepts a list of `{cue_id, macro_id, name}` dicts.

`delete_show` is intentionally not exposed as an MCP tool -- it is irreversible and too dangerous for AI-initiated operations. The `Backup` command is also excluded because it opens a GUI menu on the console (per grandMA2 Manual p368), which is not functional over Telnet. Use `save_show_tool` with a specific name as the practical backup mechanism.

### Command Builder

The `src/commands/` module can be used independently to build command strings:

```python
from src.commands import fixture, at_full, store_group, label_group

fixture(1, end=10)              # "fixture 1 thru 10"
at_full()                       # "at full"
store_group(5)                  # "store group 5"
store_group(5, name="Front Wash")  # 'store group 5 "Front Wash"' (inline naming)
label_group(5, "Front Wash")    # 'label group 5 "Front Wash"' (separate label command)
```

### GMA2Client (Workflow Orchestration)

The `GMA2Client` class provides high-level workflow methods that compose multiple commands. These methods use grandMA2's inline naming syntax to minimize the number of Telnet round-trips:

```python
from src.gma2_client import GMA2Client

async with GMA2Client.create("192.168.1.100") as client:
    # Build a cue list with names and fade times
    # Uses inline naming: 1 command per named cue (store cue N "Name"),
    # plus 1 command per fade time
    await client.build_cue_list(1, [
        {"id": 1, "name": "Preset", "fade": 0},
        {"id": 2, "name": "Look 1", "fade": 3.0},
        {"id": 3, "name": "Blackout", "fade": 2.0},
    ])

    # Select fixtures, store as named group, apply a preset (3 commands)
    # Uses inline naming: store group N "Name" in a single command
    await client.setup_group_with_preset(
        fixtures=(1, 10), group_id=1,
        group_name="Front Wash", preset_type="color", preset_id=3,
    )

    # Quick look: set fixtures to a value, optionally store as cue
    await client.quick_look(fixtures=(1, 20), value=75, store_as_cue=5)

    # Batch assign sequences to executors
    await client.assign_sequences_to_executors([(1, 1), (2, 2), (3, 3)])

    # Clone fixture programming (with /noconfirm for telnet)
    await client.clone_fixtures(source_fixture=1, target_fixture=11,
                                source_end=5, target_end=15, mode="overwrite")

    # Apply effect to a group with parameters
    await client.setup_effect_on_group(group_id=1, effect_id=5,
                                       bpm=120, form="sin", high=100, low=0)

    # Set up a full executor page
    await client.setup_executor_page(page=1, assignments=[
        {"executor_id": 1, "sequence_id": 1, "label": "Wash", "fader_level": 80},
        {"executor_id": 2, "sequence_id": 2, "label": "Spots"},
    ])

    # Label multiple objects at once
    await client.batch_label("group", {1: "Wash", 2: "Spots", 3: "Beams"})

    # Create and optionally run a macro
    await client.create_and_run_macro(
        macro_id=10, commands=["Go Sequence 1", "Go Sequence 2"],
        name="Start Show", run=True,
    )

    # Music show workflows: create song objects (sequence + page pair)
    await client.create_song_objects(song_id=101, song_name="Opening+Childhood")

    # Set up a song macro with SetVar on line 1
    await client.setup_song_macro(macro_id=101, song_name="Opening+Childhood")

    # Build a full set list with cue-to-macro links
    await client.build_set_list(
        sequence_id=100, sequence_name="Set List",
        songs=[
            {"cue_id": 1, "macro_id": 101, "name": "Opening+Childhood"},
            {"cue_id": 2, "macro_id": 102, "name": "Nostalgia"},
            {"cue_id": 3, "macro_id": 103, "name": "Finale"},
        ],
    )
```

### CommandSequence (Command Chaining)

The `CommandSequence` class lets you compose multiple commands and execute them as a batch:

```python
from src.command_sequence import CommandSequence
from src.commands import fixture_at, store_group, at_full

seq = CommandSequence()
seq.add(fixture_at(1, 50)).add(at_full()).add(store_group(1))

# Preview before sending
print(seq.preview())  # ['fixture 1 at 50', 'at full', 'store group 1']

# Execute all commands
result = await seq.execute(client)
# {'commands_sent': [...], 'count': 3, 'success': True}
```

### Direct Telnet Access

For manual testing via the Makefile:

```bash
make server    # Connect to grandMA2 command port (30000)
make log       # Connect to log output port (30001)
```

To exit a Telnet session: press `Ctrl + ]`, then type `quit`.

### Running the MCP Server Manually

```bash
uv run python -m src.server
```

## Command Reference

The command builder follows the official grandMA2 command-line syntax. The basic pattern is `[Function] [Object]`. All objects have a default function, and most functions have a default object type. Objects are arranged in a hierarchical tree.

### 1. Helping Keywords (Prepositions/Conjunctions)

Used to create relations between functions and objects.

| Keyword | Description      | Example             |
|---------|------------------|---------------------|
| `Thru`  | Range selection  | `Fixture 1 Thru 10` |
| `+`     | Add to selection | `Fixture 1 + 3 + 5` |
| `At`    | Set values       | `At 50`             |

### 2. Object Keywords (Nouns)

Allocate objects in the show file. Usually combined with numbers, IDs, names, or labels.

| Object       | Function                      | Example                                  |
|--------------|-------------------------------|------------------------------------------|
| `fixture()`  | Select fixtures by Fixture ID | `fixture(34)` -> `fixture 34`            |
| `channel()`  | Select fixtures by Channel ID | `channel(11, sub_id=5)` -> `channel 11.5`|
| `group()`    | Select fixtures in a group    | `group(3)` -> `group 3`                  |
| `preset()`   | Apply a preset                | `preset("color", 5)` -> `preset 4.5`    |
| `cue()`      | Reference a cue               | `cue(5)` -> `cue 5`                     |
| `sequence()` | Reference a sequence          | `sequence(3)` -> `sequence 3`            |

### 3. Function Keywords (Verbs)

Perform a task or function, often followed by the object they apply to.

| Function            | Description                | Example                                              |
|---------------------|----------------------------|------------------------------------------------------|
| `store()`           | Store objects in show file | `store("macro", 5)` -> `store macro 5`               |
| `store_cue()`       | Store cue with optional inline name | `store_cue(1, name="Look")` -> `store cue 1 "Look"`  |
| `store_preset()`    | Store preset with options  | `store_preset("dimmer", 3)` -> `store preset 1.3`    |
| `store_group()`     | Store a group (with optional inline name) | `store_group(1, name="Front")` -> `store group 1 "Front"` |
| `label_group()`     | Label a group              | `label_group(1, "Front")` -> `label group 1 "Front"` |
| `delete_group()`    | Delete a group             | `delete_group(1)` -> `delete group 1`                |
| `select_fixture()`  | SelFix function            | `select_fixture(1, 10)` -> `selfix fixture 1 thru 10`|
| `clear()`           | Clear programmer           | `clear()` -> `clear`                                 |
| `clear_selection()` | Clear selection only       | `clear_selection()` -> `clearselection`              |
| `clear_active()`    | Clear active values        | `clear_active()` -> `clearactive`                    |
| `clear_all()`       | Clear all                  | `clear_all()` -> `clearall`                          |
| `go_sequence()`     | Start sequence playback    | `go_sequence(1)` -> `go+ sequence 1`                 |
| `pause_sequence()`  | Pause sequence             | `pause_sequence(1)` -> `pause sequence 1`             |
| `goto_cue()`        | Jump to cue                | `goto_cue(1, 5)` -> `goto cue 5 sequence 1`          |

### 4. At Keyword (Special)

`At` functions as both a Function Keyword and a Helping Keyword.

| Function           | Description            | Example                                                          |
|--------------------|------------------------|------------------------------------------------------------------|
| `at(75)`           | Set dimmer to value    | `at(75)` -> `at 75`                                             |
| `at(cue=3)`        | Apply cue values       | `at(cue=3)` -> `at cue 3`                                       |
| `at(fade=2)`       | Set fade time          | `at(fade=2)` -> `at fade 2`                                     |
| `at_full()`        | Set to 100%            | `at_full()` -> `at full`                                        |
| `at_zero()`        | Set to 0%              | `at_zero()` -> `at 0`                                           |
| `attribute_at()`   | Set attribute value    | `attribute_at("Pan", 20)` -> `attribute "Pan" at 20`            |
| `fixture_at()`     | Set fixture to value   | `fixture_at(2, 50)` -> `fixture 2 at 50`                        |
| `fixture_at()`     | Copy from fixture      | `fixture_at(2, source_fixture=3)` -> `fixture 2 at fixture 3`   |
| `channel_at()`     | Set channel to value   | `channel_at(1, 75)` -> `channel 1 at 75`                        |
| `group_at()`       | Set group to value     | `group_at(3, 50)` -> `group 3 at 50`                            |
| `executor_at()`    | Set executor fader     | `executor_at(3, 50)` -> `executor 3 at 50`                      |
| `preset_type_at()` | Set preset type values | `preset_type_at(2, 50, end_type=9)` -> `presettype 2 thru 9 at 50` |

### 5. Copy and Move Keywords

Copy creates duplicates. Move relocates objects (swaps if the destination is occupied).

| Function                             | Description          | Example                     |
|--------------------------------------|----------------------|-----------------------------|
| `copy("group", 1, 5)`                | Copy to target       | `copy group 1 at 5`        |
| `copy("group", 1, end=3, target=11)` | Copy range           | `copy group 1 thru 3 at 11`|
| `copy("group", 2, 6, target_end=8)`  | Copy to target range | `copy group 2 at 6 thru 8` |
| `copy("cue", 5)`                     | Copy to clipboard    | `copy cue 5`               |
| `copy_cue(2, 6)`                     | Copy cue             | `copy cue 2 at 6`          |
| `move("group", 5, 9)`                | Move object          | `move group 5 at 9`        |
| `move("group", 1, 10, end=3)`        | Move range           | `move group 1 thru 3 at 10`|

Copy options: `overwrite`, `merge`, `status`, `cueonly`, `noconfirm`

### 6. Assign Keyword

Defines relationships between objects, patching, and property assignment.

| Function                                     | Description               | Example                                |
|----------------------------------------------|---------------------------|----------------------------------------|
| `assign("sequence", 1, "executor", 6)`       | Assign seq to executor    | `assign sequence 1 at executor 6`     |
| `assign("dmx", "2.101", "channel", 5)`       | Patch DMX to channel      | `assign dmx 2.101 at channel 5`       |
| `assign("group", 1, "layout", 1, x=5, y=2)`  | Assign to layout          | `assign group 1 at layout 1 /x=5 /y=2`|
| `assign_function("Toggle", "executor", 101)` | Assign function to button | `assign toggle at executor 101`        |
| `assign_fade(3, 5)`                          | Assign fade time to cue   | `assign fade 3 cue 5`                 |
| `assign_to_layout("group", 1, 1, x=5, y=2)`  | Assign to layout position | `assign group 1 at layout 1 /x=5 /y=2`|
| `assign_macro_cmd(101, 1, "Go Seq 5")`       | Set macro line command    | `assign macro 1.101.1 /cmd="Go Seq 5"`|
| `assign_cue_cmd(1, 100, "Macro 101")`        | Set cue CMD field         | `assign cue 1 sequence 100 /cmd="Macro 101"`|

Assign options: `break_`, `multipatch`, `reset`, `x`, `y`, `noconfirm`, `special`, `cue_mode`, `password`

### 7. Label Keyword

Gives names to objects. Numbers in names auto-enumerate for ranges.

| Function                                   | Description  | Example                              |
|--------------------------------------------|--------------|--------------------------------------|
| `label("group", 3, "All Studiocolors")`    | Label group  | `label group 3 "All Studiocolors"`   |
| `label("fixture", 1, "Mac700 1", end=10)`  | Label range  | `label fixture 1 thru 10 "Mac700 1"` |
| `label("preset", '"color"."Red"', "Dark")` | Label preset | `label preset "color"."Red" "Dark"`  |
| `label_sequence_cue("Set List", 1, "Opening")` | Label cue in sequence | `label sequence "Set List" cue 1 "Opening"` |
| `label_sequence_cue(100, 1, "Act 1", end_cue=5)` | Label cue range | `label sequence 100 cue 1 thru 5 "Act 1"` |

### 8. Appearance Keyword

Changes frame colors of pool objects and background colors of cues.

| Function                                                    | Description      | Example                                   |
|-------------------------------------------------------------|------------------|-------------------------------------------|
| `appearance("preset", "0.1", red=100, green=0, blue=0)`     | Set RGB color    | `appearance preset 0.1 /r=100 /g=0 /b=0` |
| `appearance("preset", "0.1", hue=0, saturation=100)`        | Set HSB color    | `appearance preset 0.1 /h=0 /s=100`      |
| `appearance("group", 1, end=5, color="FF0000")`             | Set hex color    | `appearance group 1 thru 5 /color=FF0000` |
| `appearance("macro", 2, source_type="macro", source_id=13)` | Copy from source | `appearance macro 2 at macro 13`          |
| `appearance("preset", 1, reset=True)`                       | Reset appearance | `appearance preset 1 /reset`              |

### 9. Macro Placeholder (@ Character)

The `@` character (distinct from the `At` keyword) is used as a placeholder for user input in macros.

| Function                    | Description              | Example                                            |
|-----------------------------|--------------------------|----------------------------------------------------|
| `macro_with_input_after()`  | @ at end of macro line   | `macro_with_input_after("Load")` -> `Load @`       |
| `macro_with_input_before()` | @ at start of macro line | `macro_with_input_before("Fade 20")` -> `@ Fade 20`|

## Project Structure

```text
gma2-mcp/
├── src/
│   ├── commands/               # Command builder module
│   │   ├── __init__.py         # Public API exports
│   │   ├── constants.py        # PRESET_TYPES, store option sets
│   │   ├── helpers.py          # Internal helper functions
│   │   └── functions/          # Function keywords by category
│   │       ├── advanced_edit.py    # Flip, CircularCopy, Import, Export
│   │       ├── assignment.py       # Assign keyword functions
│   │       ├── blackout.py         # Blackout, Freeze, Highlight, Solo
│   │       ├── blind.py            # Blind, Preview modes
│   │       ├── call.py             # Call keyword
│   │       ├── conditionals.py     # EndIf, IfActive, IfOutput, Or, With
│   │       ├── crossfade.py        # Crossfade, ManualXFade
│   │       ├── cue_timing.py       # Delay, Fade timing
│   │       ├── edit.py             # Copy, Move, Delete, Remove
│   │       ├── effect.py           # Effect, EffectBPM, EffectForm
│   │       ├── executor_control.py # Off, On, Kill, Flash, Swop
│   │       ├── fixture_control.py  # Align, Fix, Locate, Next, Prev
│   │       ├── flash_swop_ext.py   # FlashGo, SwopGo, StoreLook
│   │       ├── helping.py          # Helping keywords (Thru, +)
│   │       ├── info.py             # List and Info queries
│   │       ├── intensity.py        # Full, Zero, Load, Learn
│   │       ├── labeling.py         # Label and Appearance
│   │       ├── list_ext.py         # ListShows, ListOops, ListVar
│   │       ├── macro.py            # Macro placeholder functions
│   │       ├── matricks.py         # MAtricks keywords
│   │       ├── midi.py             # MIDI control functions
│   │       ├── navigation.py       # Down, Up, NextRow, Search
│   │       ├── network.py          # Remote, Telnet, JoinSession
│   │       ├── park.py             # Park/Unpark functions
│   │       ├── playback.py         # Go, GoBack, Goto, DefGo
│   │       ├── programmer.py       # Block, Clone, Default, Update
│   │       ├── rate_speed.py       # Rate, Speed control
│   │       ├── rdm.py              # RDM functions
│   │       ├── selection.py        # SelFix and Clear functions
│   │       ├── show_data.py        # CrashLog, Lua, PSR, Thru
│   │       ├── step_timing.py      # SnapPercent, StepFade, FadePath
│   │       ├── store.py            # Store functions
│   │       ├── system.py           # Backup, Setup, Shutdown, Login
│   │       ├── values.py           # At and value setting
│   │       └── variables.py        # Variable functions
│   ├── command_sequence.py     # CommandSequence for multi-command batching
│   ├── gma2_client.py          # High-level workflow orchestration client (15 methods)
│   ├── response_parser.py      # Parse grandMA2 Telnet output into structured data
│   ├── execution.py            # Verified execution core (ExecutionResult, build_result)
│   ├── server.py               # MCP server (FastMCP, 101 tools, configurable stdio/streamable-http transport)
│   └── telnet_client.py        # Async Telnet client with health check, auto-reconnect, command lock, state tracking
├── tests/                      # Pytest test suite (one file per module)
├── doc/                        # grandMA2 user manual (PDF)
├── connect.sh                  # Telnet connection script with auto-login
├── Makefile                    # Utility commands (server, log, test)
├── pyproject.toml              # Project metadata and dependencies
└── .env.template               # Environment variable template
```

## Development

### Running Tests

```bash
make test
```

Or directly:

```bash
uv run pytest -v
```

Run a specific test file:

```bash
uv run pytest tests/test_playback.py -v
```

### Dependencies

| Package          | Purpose                         |
|------------------|---------------------------------|
| `mcp>=1.21.0`   | Model Context Protocol library  |
| `python-dotenv`  | Environment variable loading    |
| `telnetlib3`     | Async Telnet client             |
| `pytest`         | Testing framework (dev)         |
| `pytest-asyncio` | Async test support (dev)        |

### Architecture

The project has six layers:

1. **Telnet Client** (`src/telnet_client.py`) -- Low-level async Telnet communication with the console. Includes `ConnectionState` tracking (DISCONNECTED/CONNECTING/CONNECTED/RECONNECTING), health check probing, auto-reconnection with bounded exponential backoff (configurable retries and delay), health check TTL to skip redundant probes during rapid command sequences, `asyncio.Lock`-based command serialization for concurrent access safety, graceful shutdown via the server lifespan hook, and a verified `execute()` that reads and checks the console reply.
2. **Command Builder** (`src/commands/`) -- Pure functions that construct command strings. No network access.
3. **Response Parser** (`src/response_parser.py`) -- Pure functions that parse grandMA2 Telnet output: `List` tables into structured dicts (`parsed: False` on unrecognized formats), and inline `Error #NN` failures via `detect_error()`/`strip_ansi()`.
4. **Execution Core** (`src/execution.py`) -- Pure `build_result()` + `ExecutionResult`; turns a raw reply into `{ok, echo, error_code, error_text, raw}` so mutating tools report real outcomes.
5. **Orchestration** (`src/gma2_client.py`, `src/command_sequence.py`) -- High-level workflow methods (15 methods including music show workflows) and command batching that compose builders + telnet.
6. **MCP Server** (`src/server.py`) -- FastMCP server that exposes 101 tools over configurable transport (`stdio` or `streamable-http`), connecting the builder to the Telnet client.

All console communication goes through the Telnet client layer.

## Troubleshooting

**Connection fails** -- Verify the console IP and port. Ensure Telnet is enabled on the console. Test manually with `make server`.

**Connection drops mid-session** -- The Telnet client auto-reconnects with up to 3 retries (exponential backoff: 1s, 2s, 4s). If all retries fail, tools return a clear error message. Check that the console is running and reachable.

**Authentication errors** -- Check username/password in `.env`. Confirm the user account exists on the console. Login is case-sensitive.

**Fixture setup locked by stale connection** -- If a previous session crashed without calling `disconnect()`, the console may still hold a Telnet lock. Restart the console or wait for its session timeout. The MCP server now calls `disconnect()` on shutdown to prevent this.

**Command not working** -- Verify the syntax against the grandMA2 manual. Ensure referenced objects (fixtures, groups, presets) exist in the current show file.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit your changes
4. Push to the branch and open a Pull Request

Run tests before submitting: `make test`
