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
├── main.py              # Entry point with login test functionality
├── src/
│   ├── __init__.py
│   ├── commands/        # Command builder module
│   │   ├── __init__.py  # Public API exports
│   │   ├── constants.py # PRESET_TYPES, STORE_*_OPTIONS
│   │   ├── helpers.py   # Internal helper functions
│   │   ├── objects.py   # Object Keywords (fixture, channel, group, etc.)
│   │   └── functions.py # Function Keywords (store, clear, go, etc.)
│   ├── telnet_client.py # Telnet connection management
│   ├── server.py        # MCP server implementation
│   └── tools.py         # MCP tool definitions
├── tests/
│   ├── test_commands.py # Command builder tests
│   ├── test_telnet_client.py
│   └── test_tools.py
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
├── Makefile             # Utility commands
└── README.md            # This file
```

## Dependencies

- `mcp>=1.21.0` - Model Context Protocol library
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework

## Development

### Running Tests

```bash
make test
```

Or directly with pytest:

```bash
uv run pytest -v
```

### Code Style

This project follows Python best practices and PEP 8 conventions.

## Troubleshooting

### Connection Issues

- Verify the grandMA2 console IP address and port are correct
- Ensure the console has Telnet access enabled
- Check firewall rules allow connections to the specified port

### Authentication Errors

- Confirm the username and password are correct
- Verify the user account exists on the grandMA2 console
- Check user permissions for the required operations

## License

Specify your license here.

## Contributing

Contributions are welcome. Please ensure code follows project conventions and includes appropriate documentation.
