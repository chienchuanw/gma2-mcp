# GMA2 MCP

An MCP server that lets AI assistants control grandMA2 lighting consoles via Telnet. It exposes high-level tools for fixture grouping, sequence playback, and raw command execution through the Model Context Protocol.

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

grandMA2 consoles accept commands over Telnet, but building correct command strings requires knowledge of the MA2 syntax rules -- keyword ordering, preset type mappings, option flags, and object hierarchies. This project handles that complexity in two layers:

1. **Command Builder** (`src/commands/`) -- Python functions that construct valid grandMA2 command strings following the official syntax rules. Each function is a thin wrapper that returns a string; it never touches the network.
2. **MCP Server** (`src/server.py`) -- A FastMCP server that exposes three tools (`create_fixture_group`, `execute_sequence`, `send_raw_command`) over stdio transport. It manages a persistent Telnet connection to the console and delegates command construction to the builder layer.

The command builder covers all grandMA2 command-line keywords organized by category: object keywords (fixtures, channels, groups, presets, cues, sequences, executors), function keywords (store, delete, copy, move, goto, label, assign, and many more), and helping keywords (thru, at, +).

## Features

- **MCP tool interface** -- Three tools for AI assistants: create fixture groups, control sequence playback (go/pause/goto), and send arbitrary raw commands.
- **Complete command builder** -- Over 200 Python functions covering all grandMA2 command-line keywords across 30+ modules, each returning a correctly formatted command string.
- **Async Telnet client** -- Built on `telnetlib3` with automatic login handling and persistent connections.
- **Configurable via environment** -- Host, port, user, and password set through `.env` or environment variables.

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
| `GMA_HOST`     | IP address of the grandMA2 console   | `127.0.0.1`     |
| `GMA_PORT`     | Telnet port                          | `30000`         |
| `GMA_USER`     | Login username                       | `administrator` |
| `GMA_PASSWORD`  | Login password                       | `admin`         |

Port 30000 is the standard command port. Port 30001 is read-only (log output).

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

## Usage

### MCP Tools

The server exposes three tools:

| Tool                   | Description                                     |
|------------------------|-------------------------------------------------|
| `create_fixture_group` | Select a range of fixtures and store as a group  |
| `execute_sequence`     | Go, pause, or goto a cue in a sequence           |
| `send_raw_command`     | Send any grandMA2 command-line instruction        |

### Command Builder

The `src/commands/` module can be used independently to build command strings:

```python
from src.commands import fixture, at_full, store_group, label_group

fixture(1, end=10)              # "fixture 1 thru 10"
at_full()                       # "at full"
store_group(5)                  # "store group 5"
label_group(5, "Front Wash")    # 'label group 5 "Front Wash"'
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
| `preset()`   | Apply a preset                | `preset("color", 5)` -> `preset 2.5`    |
| `cue()`      | Reference a cue               | `cue(5)` -> `cue 5`                     |
| `sequence()` | Reference a sequence          | `sequence(3)` -> `sequence 3`            |

### 3. Function Keywords (Verbs)

Perform a task or function, often followed by the object they apply to.

| Function            | Description                | Example                                              |
|---------------------|----------------------------|------------------------------------------------------|
| `store()`           | Store objects in show file | `store("macro", 5)` -> `store macro 5`               |
| `store_cue()`       | Store cue with options     | `store_cue(1, merge=True)` -> `store cue 1 /merge`   |
| `store_preset()`    | Store preset with options  | `store_preset("dimmer", 3)` -> `store preset 1.3`    |
| `store_group()`     | Store a group              | `store_group(1)` -> `store group 1`                  |
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

Assign options: `break_`, `multipatch`, `reset`, `x`, `y`, `noconfirm`, `special`, `cue_mode`, `password`

### 7. Label Keyword

Gives names to objects. Numbers in names auto-enumerate for ranges.

| Function                                   | Description  | Example                              |
|--------------------------------------------|--------------|--------------------------------------|
| `label("group", 3, "All Studiocolors")`    | Label group  | `label group 3 "All Studiocolors"`   |
| `label("fixture", 1, "Mac700 1", end=10)`  | Label range  | `label fixture 1 thru 10 "Mac700 1"` |
| `label("preset", '"color"."Red"', "Dark")` | Label preset | `label preset "color"."Red" "Dark"`  |

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
│   ├── gma2_client.py          # High-level grandMA2 client interface
│   ├── server.py               # MCP server (FastMCP, stdio transport)
│   ├── telnet_client.py        # Async Telnet connection management
│   └── tools.py                # MCP tool definitions
├── tests/                      # Pytest test suite (one file per module)
├── doc/                        # grandMA2 user manual (PDF)
├── main.py                     # Standalone login test script
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

The project has three layers:

1. **Telnet Client** (`src/telnet_client.py`) -- Low-level async Telnet communication with the console.
2. **Command Builder** (`src/commands/`) -- Pure functions that construct command strings. No network access.
3. **MCP Server** (`src/server.py`, `src/tools.py`) -- FastMCP server that connects the builder to the Telnet client and exposes tools over stdio.

All console communication goes through the Telnet client layer.

## Troubleshooting

**Connection fails** -- Verify the console IP and port. Ensure Telnet is enabled on the console. Test manually with `make server`.

**Authentication errors** -- Check username/password in `.env`. Confirm the user account exists on the console.

**Command not working** -- Verify the syntax against the grandMA2 manual. Ensure referenced objects (fixtures, groups, presets) exist in the current show file.

## License

This project does not currently include a license file.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/name`)
3. Commit your changes
4. Push to the branch and open a Pull Request

Run tests before submitting: `make test`
