# GMA2 MCP

A Model Context Protocol (MCP) server for interacting with grandMA2 lighting control systems via Telnet.

## Overview

GMA2 MCP provides a programmatic interface to communicate with grandMA2 consoles using the Model Context Protocol. This project enables remote control and monitoring of grandMA2 systems through a standardized protocol.

## Features

- Telnet-based communication with grandMA2 consoles
- MCP server implementation for protocol compliance
- User authentication support
- Configurable host and port settings

## Requirements

- Python 3.12 or higher
- grandMA2 console with Telnet access enabled

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd gma2-mcp
```

1. Create and activate a virtual environment:

```bash
source .venv/bin/activate
```

On Windows, use:

```bash
python3.12 -m venv venv
venv\Scripts\activate
```

1. Install dependencies using uv:

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
```

## Project Structure

```text
gma2-mcp/
├── main.py              # Entry point with login test functionality
├── src/
│   ├── __init__.py
│   ├── gma2_client.py   # grandMA2 client implementation
│   ├── server.py        # MCP server implementation
│   └── tools.py         # Tool definitions for MCP
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
├── Makefile             # Utility commands
└── README.md            # This file
```

## Dependencies

- `mcp>=1.21.0` - Model Context Protocol library
- `dotenv>=0.9.9` - Environment variable management

## Development

### Running Tests

Tests can be executed using the project's test suite (if configured).

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
