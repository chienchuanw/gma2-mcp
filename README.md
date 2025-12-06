# GMA2 MCP

A Model Context Protocol (MCP) server for interacting with grandMA2 lighting control systems via Telnet.

## Overview

GMA2 MCP provides a programmatic interface to communicate with grandMA2 consoles using the Model Context Protocol. This project enables remote control and monitoring of grandMA2 systems through a standardized protocol.

## Features

- Telnet-based communication with grandMA2 consoles
- MCP server implementation for protocol compliance
- User authentication support
- Configurable host and port settings
- Comprehensive command builder following grandMA2 syntax rules

## grandMA2 Keyword Classification

The command builder module (`src/commands/`) follows the official grandMA2 command line syntax rules. Keywords are organized into three categories:

### General Syntax Rules

- Basic syntax: `[Function] [Object]`
- All objects have a default function which is used if no function is given
- Most functions have a default object or object type
- Objects are arranged in a hierarchical tree structure

### 1. Helping Keywords (Prepositions/Conjunctions)

Used to create relations between functions and objects.

| Keyword | Description      | Example             |
| ------- | ---------------- | ------------------- |
| `Thru`  | Range selection  | `Fixture 1 Thru 10` |
| `+`     | Add to selection | `Fixture 1 + 3 + 5` |
| `At`    | Set values       | `At 50`             |

### 2. Object Keywords (Nouns)

Used to allocate objects in your show file. Usually used with numbers, IDs, names, and labels.

| Object       | Function                      | Example                                  |
| ------------ | ----------------------------- | ---------------------------------------- |
| `fixture()`  | Select fixtures by Fixture ID | `fixture(34)` → `fixture 34`             |
| `channel()`  | Select fixtures by Channel ID | `channel(11, sub_id=5)` → `channel 11.5` |
| `group()`    | Select fixtures in a group    | `group(3)` → `group 3`                   |
| `preset()`   | Apply a preset                | `preset("color", 5)` → `preset 2.5`      |
| `cue()`      | Reference a cue               | `cue(5)` → `cue 5`                       |
| `sequence()` | Reference a sequence          | `sequence(3)` → `sequence 3`             |

### 3. Function Keywords (Verbs)

Perform a task or function. Often followed by objects to which the function applies.

| Function            | Description                | Example                                              |
| ------------------- | -------------------------- | ---------------------------------------------------- |
| `store()`           | Store objects in show file | `store("macro", 5)` → `store macro 5`                |
| `store_cue()`       | Store cue with options     | `store_cue(1, merge=True)` → `store cue 1 /merge`    |
| `store_preset()`    | Store preset with options  | `store_preset("dimmer", 3)` → `store preset 1.3`     |
| `store_group()`     | Store a group              | `store_group(1)` → `store group 1`                   |
| `label_group()`     | Label a group              | `label_group(1, "Front")` → `label group 1 "Front"`  |
| `delete_group()`    | Delete a group             | `delete_group(1)` → `delete group 1`                 |
| `select_fixture()`  | SelFix function            | `select_fixture(1, 10)` → `selfix fixture 1 thru 10` |
| `clear()`           | Clear programmer           | `clear()` → `clear`                                  |
| `clear_selection()` | Clear selection only       | `clear_selection()` → `clearselection`               |
| `clear_active()`    | Clear active values        | `clear_active()` → `clearactive`                     |
| `clear_all()`       | Clear all                  | `clear_all()` → `clearall`                           |
| `go_sequence()`     | Start sequence playback    | `go_sequence(1)` → `go+ sequence 1`                  |
| `pause_sequence()`  | Pause sequence             | `pause_sequence(1)` → `pause sequence 1`             |
| `goto_cue()`        | Jump to cue                | `goto_cue(1, 5)` → `goto cue 5 sequence 1`           |

### 4. At Keyword (Special)

`At` is unique - it can function as both a **Function Keyword** and a **Helping Keyword**.

| Function           | Description            | Example                                                           |
| ------------------ | ---------------------- | ----------------------------------------------------------------- |
| `at(75)`           | Set dimmer to value    | `at(75)` → `at 75`                                                |
| `at(cue=3)`        | Apply cue values       | `at(cue=3)` → `at cue 3`                                          |
| `at(fade=2)`       | Set fade time          | `at(fade=2)` → `at fade 2`                                        |
| `at_full()`        | Set to 100%            | `at_full()` → `at full`                                           |
| `at_zero()`        | Set to 0%              | `at_zero()` → `at 0`                                              |
| `attribute_at()`   | Set attribute value    | `attribute_at("Pan", 20)` → `attribute "Pan" at 20`               |
| `fixture_at()`     | Set fixture to value   | `fixture_at(2, 50)` → `fixture 2 at 50`                           |
| `fixture_at()`     | Copy from fixture      | `fixture_at(2, source_fixture=3)` → `fixture 2 at fixture 3`      |
| `channel_at()`     | Set channel to value   | `channel_at(1, 75)` → `channel 1 at 75`                           |
| `group_at()`       | Set group to value     | `group_at(3, 50)` → `group 3 at 50`                               |
| `executor_at()`    | Set executor fader     | `executor_at(3, 50)` → `executor 3 at 50`                         |
| `preset_type_at()` | Set preset type values | `preset_type_at(2, 50, end_type=9)` → `presettype 2 thru 9 at 50` |

### 5. Copy and Move Keywords

Copy creates copies of objects. Move relocates objects (swaps if destination is taken).

| Function                             | Description            | Example                     |
| ------------------------------------ | ---------------------- | --------------------------- |
| `copy("group", 1, 5)`                | Copy to target         | `copy group 1 at 5`         |
| `copy("group", 1, end=3, target=11)` | Copy range             | `copy group 1 thru 3 at 11` |
| `copy("group", 2, 6, target_end=8)`  | Copy to target range   | `copy group 2 at 6 thru 8`  |
| `copy("cue", 5)`                     | Copy to clipboard      | `copy cue 5`                |
| `copy_cue(2, 6)`                     | Copy cue (convenience) | `copy cue 2 at 6`           |
| `move("group", 5, 9)`                | Move object            | `move group 5 at 9`         |
| `move("group", 1, 10, end=3)`        | Move range             | `move group 1 thru 3 at 10` |

Copy options: `overwrite`, `merge`, `status`, `cueonly`, `noconfirm`

### 6. Assign Keyword

Assign defines relationships between objects, patching, and property assignment.

| Function                                     | Description               | Example                                |
| -------------------------------------------- | ------------------------- | -------------------------------------- |
| `assign("sequence", 1, "executor", 6)`       | Assign seq to executor    | `assign sequence 1 at executor 6`      |
| `assign("dmx", "2.101", "channel", 5)`       | Patch DMX to channel      | `assign dmx 2.101 at channel 5`        |
| `assign("group", 1, "layout", 1, x=5, y=2)`  | Assign to layout          | `assign group 1 at layout 1 /x=5 /y=2` |
| `assign_function("Toggle", "executor", 101)` | Assign function to button | `assign toggle at executor 101`        |
| `assign_fade(3, 5)`                          | Assign fade time to cue   | `assign fade 3 cue 5`                  |
| `assign_to_layout("group", 1, 1, x=5, y=2)`  | Assign to layout position | `assign group 1 at layout 1 /x=5 /y=2` |

Assign options: `break_`, `multipatch`, `reset`, `x`, `y`, `noconfirm`, `special`, `cue_mode`, `password`

### 7. Label Keyword

Label gives names to objects. Numbers in names auto-enumerate for ranges.

| Function                                   | Description  | Example                              |
| ------------------------------------------ | ------------ | ------------------------------------ |
| `label("group", 3, "All Studiocolors")`    | Label group  | `label group 3 "All Studiocolors"`   |
| `label("fixture", 1, "Mac700 1", end=10)`  | Label range  | `label fixture 1 thru 10 "Mac700 1"` |
| `label("preset", '"color"."Red"', "Dark")` | Label preset | `label preset "color"."Red" "Dark"`  |

### 8. Appearance Keyword

Appearance changes frame colors of pool objects and background colors of cues.

| Function                                                    | Description      | Example                                   |
| ----------------------------------------------------------- | ---------------- | ----------------------------------------- |
| `appearance("preset", "0.1", red=100, green=0, blue=0)`     | Set RGB color    | `appearance preset 0.1 /r=100 /g=0 /b=0`  |
| `appearance("preset", "0.1", hue=0, saturation=100)`        | Set HSB color    | `appearance preset 0.1 /h=0 /s=100`       |
| `appearance("group", 1, end=5, color="FF0000")`             | Set hex color    | `appearance group 1 thru 5 /color=FF0000` |
| `appearance("macro", 2, source_type="macro", source_id=13)` | Copy from source | `appearance macro 2 at macro 13`          |
| `appearance("preset", 1, reset=True)`                       | Reset appearance | `appearance preset 1 /reset`              |

### 9. Macro Placeholder (@ Character)

The `@` character is different from the `At` keyword - it's used as a placeholder for user input in macros.

| Function                    | Description              | Example                                            |
| --------------------------- | ------------------------ | -------------------------------------------------- |
| `macro_with_input_after()`  | @ at end of macro line   | `macro_with_input_after("Load")` → `Load @`        |
| `macro_with_input_before()` | @ at start of macro line | `macro_with_input_before("Fade 20")` → `@ Fade 20` |

## Requirements

- Python 3.12 or higher
- grandMA2 console with Telnet access enabled
- Telnet client installed on your system

### Installing Telnet

On macOS:

```bash
brew install telnet
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd gma2-mcp
   ```

2. Create and activate a virtual environment:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
GMA_HOST=<grandMA2-console-ip>
GMA_USER=<username>
GMA_PASSWORD=<password>
```

Default values:

- `GMA_USER`: administrator
- `GMA_PASSWORD`: admin
- `GMA_PORT`: 30000 (standard port, 30001 for read-only)

## MCP Registration

To use this MCP server with Claude Desktop or other MCP-compatible clients, you need to register it in your MCP settings.

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

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

Replace `/path/to/gma2-mcp` with the actual path to your project directory.

### Alternative: Using Python Directly

If you prefer not to use `uv`, you can configure the server with Python directly:

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

### Running the MCP Server Manually

For testing or development, you can run the MCP server directly:

```bash
# Using uv
uv run python -m src.server

# Or using the virtual environment
.venv/bin/python -m src.server
```

## Usage

### Running the Login Test

To test the connection to your grandMA2 console:

```bash
python main.py
```

This will attempt to connect to the configured grandMA2 host and authenticate with the provided credentials.

### Telnet Connection

Use the provided Makefile commands for direct Telnet access:

```bash
make server    # Connect to grandMA2 server (port 30000)
make log       # Connect to grandMA2 log output (port 30001)
make test      # Run all tests
```

To exit a Telnet session:

1. Press `Ctrl + ]` to enter Telnet command mode
2. Type `quit` and press Enter

## Project Structure

```text
gma2-mcp/
├── main.py                  # Entry point with login test functionality
├── connect.sh               # Telnet connection script with auto-login
├── src/
│   ├── __init__.py
│   ├── commands/            # Command builder module
│   │   ├── __init__.py      # Public API exports
│   │   ├── constants.py     # PRESET_TYPES, STORE_*_OPTIONS
│   │   ├── helpers.py       # Internal helper functions
│   │   ├── objects.py       # Object Keywords (fixture, channel, group, etc.)
│   │   └── functions/       # Function Keywords organized by category
│   │       ├── __init__.py
│   │       ├── assignment.py    # Assign keyword functions
│   │       ├── edit.py          # Copy, Move, Delete, Remove functions
│   │       ├── info.py          # List and Info query functions
│   │       ├── labeling.py      # Label and Appearance functions
│   │       ├── macro.py         # Macro placeholder functions
│   │       ├── playback.py      # Go, GoBack, Goto, GoFast, DefGo functions
│   │       ├── selection.py     # SelFix and Clear functions
│   │       ├── store.py         # Store functions
│   │       └── values.py        # At and value setting functions
│   ├── gma2_client.py       # High-level grandMA2 client interface
│   ├── telnet_client.py     # Telnet connection management
│   ├── server.py            # MCP server implementation
│   └── tools.py             # MCP tool definitions
├── tests/
│   ├── conftest.py          # Pytest configuration and fixtures
│   ├── test_assignment.py   # Assign keyword tests
│   ├── test_edit.py         # Copy, Move, Delete tests
│   ├── test_info.py         # List and Info query tests
│   ├── test_labeling.py     # Label and Appearance tests
│   ├── test_macro.py        # Macro placeholder tests
│   ├── test_objects.py      # Object Keywords tests
│   ├── test_playback.py     # Playback control tests
│   ├── test_selection.py    # Selection and Clear tests
│   ├── test_store.py        # Store function tests
│   ├── test_telnet_client.py # Telnet client tests
│   ├── test_tools.py        # MCP tool tests
│   └── test_values.py       # Value setting tests
├── doc/                     # Documentation files
├── pyproject.toml           # Project configuration
├── pytest.ini               # Pytest configuration
├── uv.lock                  # Dependency lock file
├── Makefile                 # Utility commands
└── README.md                # This file
```

## Dependencies

### Core Dependencies

- `mcp>=1.21.0` - Model Context Protocol library
- `python-dotenv>=1.0.0` - Environment variable management
- `telnetlib3>=2.0.8` - Async Telnet client library

### Development Dependencies

- `pytest>=9.0.1` - Testing framework
- `pytest-asyncio>=1.3.0` - Async test support

## Development

### Running Tests

Run all tests using the Makefile:

```bash
make test
```

Or directly with pytest:

```bash
uv run pytest -v
```

Run specific test file:

```bash
uv run pytest tests/test_playback.py -v
```

Run tests with coverage:

```bash
uv run pytest --cov=src tests/
```

### Code Style and Standards

This project follows Python best practices and PEP 8 conventions. See `.augment/rules/coding-standards.md` for detailed coding standards including:

- Naming conventions (snake_case for functions, PascalCase for classes)
- Import organization and explicit imports
- Error handling and logging practices
- Telnet interaction rules
- Documentation standards with docstrings
- Testing standards with mocked Telnet layer
- Security practices (no hardcoded credentials)

### Project Architecture

The project is organized into three main layers:

1. **Telnet Client Layer** (`src/telnet_client.py`): Low-level Telnet communication
2. **Command Builder Layer** (`src/commands/`): High-level command construction following grandMA2 syntax
3. **MCP Server Layer** (`src/server.py`, `src/tools.py`): Model Context Protocol interface

All communication with grandMA2 must go through the Telnet Client module to ensure consistency and proper error handling.

## Troubleshooting

### Connection Issues

- Verify the grandMA2 console IP address and port are correct
- Ensure the console has Telnet access enabled
- Check firewall rules allow connections to the specified port
- Try connecting manually using the `make server` command to test connectivity
- Check that the console is powered on and network is accessible

### Authentication Errors

- Confirm the username and password are correct
- Verify the user account exists on the grandMA2 console
- Check user permissions for the required operations
- Ensure credentials in `.env` file are properly formatted (no extra spaces)

### Command Execution Issues

- Verify the command syntax follows grandMA2 command line rules
- Check that referenced objects (fixtures, groups, presets) exist in the show file
- Ensure the console is in a state that allows the command (e.g., not in a dialog)
- Review the grandMA2 User Manual for command-specific requirements

### Testing Issues

- Ensure all dependencies are installed: `uv sync`
- Check that pytest is properly configured: `uv run pytest --version`
- Run tests with verbose output for more details: `uv run pytest -vv`

## Quick Start Example

```python
from src.commands import fixture, at_full, store_group

# Build a command to select fixtures 1-10 and set them to full
cmd1 = fixture(1, end=10)  # "fixture 1 thru 10"
cmd2 = at_full()            # "at full"

# Store the current selection as group 5
cmd3 = store_group(5)       # "store group 5"

# These commands can be sent to grandMA2 via the Telnet client
```

## Documentation

- See `.augment/rules/project-overview.md` for detailed project architecture and design principles
- See `.augment/rules/coding-standards.md` for coding standards and conventions
- See `doc/` directory for additional documentation and references

## License

Specify your license here.

## Contributing

Contributions are welcome. Please ensure code follows project conventions and includes appropriate documentation.
