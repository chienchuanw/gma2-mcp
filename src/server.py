"""
MCP Server Module

This module is responsible for creating and running the MCP server,
integrating all tools together. It uses FastMCP to simplify the MCP server setup.

Usage:
    uv run python -m src.server
"""

import functools
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from src.telnet_client import ConnectionState, GMA2TelnetClient
from src.commands import (
    appearance as cmd_appearance,
    assign,
    assign_cue_cmd,
    assign_macro_cmd,
    attribute_at,
    blackout,
    clear,
    clear_active,
    clear_all,
    clear_selection,
    delete_cue as cmd_delete_cue,
    executor_at,
    fixture,
    fixture_at,
    go_executor,
    go_sequence,
    goto,
    goto_cue,
    highlight,
    kill,
    label,
    label_group,
    label_sequence_cue as cmd_label_sequence_cue,
    off,
    on,
    pause_sequence,
    preset,
    select_fixture,
    store_cue as cmd_store_cue,
    store_group,
    store_preset as cmd_store_preset,
    toggle,
)
from src.commands.constants import PRESET_TYPES
from src.gma2_client import GMA2Client

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

GMA_HOST = os.getenv("GMA_HOST", "127.0.0.1")
GMA_PORT = int(os.getenv("GMA_PORT", "30000"))
GMA_USER = os.getenv("GMA_USER", "administrator")
GMA_PASSWORD = os.getenv("GMA_PASSWORD", "admin")

@asynccontextmanager
async def server_lifespan(app):
    """manage server lifecycle — disconnect telnet on shutdown."""
    yield
    if _client is not None:
        await _client.disconnect()
        logger.info("Telnet connection closed on shutdown")


def handle_connection_error(func):
    """wrap an MCP tool to catch ConnectionError and return a user-friendly message."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConnectionError as e:
            return (
                f"Connection lost: {e}. "
                f"Check that grandMA2 is running and reachable at {GMA_HOST}:{GMA_PORT}."
            )

    return wrapper


mcp = FastMCP(
    name="grandMA2-MCP",
    lifespan=server_lifespan,
    instructions="""
    MCP server for controlling grandMA2 lighting consoles via Telnet.

    Available tools by category:

    Fixture Groups:
      - create_fixture_group: Select fixtures and store as a named group

    Cue Management:
      - store_cue: Store current programmer state as a cue
      - delete_cue: Delete a cue
      - goto_cue_tool: Jump to a specific cue in an executor or sequence
      - set_cue_cmd: Assign a command to a cue's CMD field

    Fixture & Value Control:
      - set_fixture_value: Set fixture(s) to a dimmer value (0-100)
      - set_fixture_attribute: Set a specific attribute (Pan, Tilt, etc.)
      - clear_programmer: Clear the programmer (all, selection, or active)

    Preset Management:
      - store_preset: Store current values as a preset
      - apply_preset: Apply an existing preset to the current selection

    Executor Control:
      - control_executor: On/off/go/kill/toggle an executor
      - set_executor_fader: Set executor fader level (0-100)
      - assign_to_executor: Assign a sequence to an executor

    Global State:
      - toggle_blackout: Toggle grand blackout
      - toggle_highlight: Toggle highlight mode

    Labeling:
      - label_object: Assign a name to any MA2 object

    Appearance:
      - assign_appearance: Set frame/background color on pool objects and cues
      - label_sequence_cue: Label a cue within a specific sequence

    Macro Tools:
      - set_macro_line: Set the command for a macro line

    Bulk Cue Operations:
      - store_cue_across_sequences: Store a cue across a range of sequences
      - label_cue_across_sequences: Label a cue across a range of sequences
      - appearance_cue_across_sequences: Set cue appearance across a range of sequences

    Sequence Playback:
      - execute_sequence: Go/pause/goto on a sequence

    Raw Command:
      - send_raw_command: Send any grandMA2 command-line instruction
    """,
)

DESTRUCTIVE_WARNINGS: dict[str, list[str]] = {
    "cue": [
        "Executor handles assigned to the deleted cue's sequence may reference a missing cue",
        "Any cue programming (values, timing, effects) is permanently lost",
        "Sequences with only this cue will become empty",
    ],
    "sequence": [
        "Executor assignments referencing this sequence will become orphaned",
        "All cue data within this sequence is permanently lost",
        "Pages referencing this sequence may need cleanup",
    ],
    "group": [
        "Presets referencing this group may produce unexpected results",
        "Macros targeting this group will reference a non-existent object",
    ],
}


def _format_warnings(object_type: str) -> str:
    """Format warning messages for a destructive operation on the given object type."""
    warnings = DESTRUCTIVE_WARNINGS.get(object_type, [])
    if not warnings:
        return ""
    lines = "\n".join(f"- {w}" for w in warnings)
    return f"\n\n⚠ Warnings:\n{lines}"


_client: GMA2TelnetClient | None = None


async def get_client() -> GMA2TelnetClient:
    """Get or create the shared telnet client instance."""
    global _client
    if _client is None or _client.state == ConnectionState.DISCONNECTED:
        _client = GMA2TelnetClient(
            host=GMA_HOST,
            port=GMA_PORT,
            user=GMA_USER,
            password=GMA_PASSWORD,
        )
        await _client.connect()
        await _client.login()
        logger.info(f"Connected to grandMA2: {GMA_HOST}:{GMA_PORT}")
    return _client


# ============================================================
# Fixture Group Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def create_fixture_group(
    start_fixture: int,
    end_fixture: int,
    group_id: int,
    group_name: str | None = None,
) -> str:
    """
    Create a group containing a specified range of fixtures.

    This tool selects the specified range of fixtures and saves them as a group.
    Optionally, a name can be assigned to the group.

    Args:
        start_fixture: Starting fixture number
        end_fixture: Ending fixture number
        group_id: Group number to save
        group_name: (Optional) Group name, e.g., "Front Wash"

    Returns:
        str: Operation result message

    Examples:
        - Save fixtures 1 to 10 as group 1
        - Save fixtures 1 to 10 as group 1 with name "Front Wash"
    """
    client = await get_client()

    select_cmd = select_fixture(start_fixture, end_fixture)
    await client.send_command(select_cmd)

    store_cmd = store_group(group_id, name=group_name)
    await client.send_command(store_cmd)

    if group_name:
        return f'Created Group {group_id} "{group_name}" containing Fixtures {start_fixture} to {end_fixture}'

    return (
        f"Created Group {group_id} containing Fixtures {start_fixture} to {end_fixture}"
    )


# ============================================================
# Cue Management Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def store_cue(
    cue_id: int,
    name: str | None = None,
    merge: bool = False,
    overwrite: bool = False,
    noconfirm: bool = False,
) -> str:
    """
    Store the current programmer state as a cue.

    Args:
        cue_id: Cue number to store
        name: (Optional) Name for the cue
        merge: Merge new values into existing cue
        overwrite: Overwrite existing cue entirely
        noconfirm: Suppress store confirmation pop-up

    Returns:
        str: Operation result message

    Examples:
        - Store cue 1
        - Store cue 5 with name "Blackout" and merge enabled
    """
    client = await get_client()
    cmd = cmd_store_cue(
        cue_id, name=name, merge=merge, overwrite=overwrite, noconfirm=noconfirm
    )
    await client.send_command(cmd)
    label_part = f' "{name}"' if name else ""
    return f"Stored Cue {cue_id}{label_part}"


@mcp.tool()
@handle_connection_error
async def delete_cue(cue_id: int) -> str:
    """
    Delete a cue from the current sequence.

    Args:
        cue_id: Cue number to delete

    Returns:
        str: Operation result message

    Examples:
        - Delete cue 3
    """
    client = await get_client()
    cmd = cmd_delete_cue(cue_id)
    await client.send_command(cmd)
    return f"Deleted Cue {cue_id}" + _format_warnings("cue")


@mcp.tool()
@handle_connection_error
async def goto_cue_tool(
    cue_id: int,
    executor: int | None = None,
    sequence: int | None = None,
) -> str:
    """
    Jump to a specific cue.

    Targets either an executor or a sequence. If neither is specified,
    the command applies to the selected executor.

    Args:
        cue_id: Target cue number
        executor: (Optional) Executor number
        sequence: (Optional) Sequence number

    Returns:
        str: Operation result message

    Examples:
        - Goto cue 5 on executor 4
        - Goto cue 3 in sequence 1
    """
    client = await get_client()
    cmd = goto(cue_id, executor=executor, sequence=sequence)
    await client.send_command(cmd)
    target = ""
    if executor is not None:
        target = f" on Executor {executor}"
    elif sequence is not None:
        target = f" in Sequence {sequence}"
    return f"Jumped to Cue {cue_id}{target}"


# ============================================================
# Cue CMD Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def set_cue_cmd(
    cue_id: int,
    sequence_id: int,
    command: str,
) -> str:
    """
    Assign a command to a cue's CMD field.

    When the cue fires, the assigned command will execute automatically.
    Common use: trigger a macro when a cue runs.

    Args:
        cue_id: Cue number
        sequence_id: Sequence number
        command: Command to execute when cue fires (e.g., "Macro 101")

    Returns:
        str: Operation result message

    Examples:
        - Set cue 1 in sequence 100 to trigger "Macro 101"
        - Set cue 5 in sequence 200 to run "Go Sequence 10"
    """
    client = await get_client()
    cmd = assign_cue_cmd(cue_id, sequence_id, command)
    await client.send_command(cmd)
    return f'Set Cue {cue_id} Sequence {sequence_id} CMD to "{command}"'


# ============================================================
# Fixture & Value Control Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def set_fixture_value(
    fixture_id: int,
    value: int,
    end_fixture: int | None = None,
) -> str:
    """
    Set fixture(s) to a dimmer value.

    Args:
        fixture_id: Fixture number (or start of range)
        value: Dimmer percentage (0-100)
        end_fixture: (Optional) End fixture for range

    Returns:
        str: Operation result message

    Examples:
        - Set fixture 1 to 75%
        - Set fixtures 1 thru 10 to 50%
    """
    client = await get_client()
    cmd = fixture_at(fixture_id, value, end=end_fixture)
    await client.send_command(cmd)
    range_part = f" thru {end_fixture}" if end_fixture else ""
    return f"Set Fixture {fixture_id}{range_part} to {value}%"


@mcp.tool()
@handle_connection_error
async def set_fixture_attribute(
    fixture_id: int,
    attribute: str,
    value: int,
    end_fixture: int | None = None,
) -> str:
    """
    Set a specific attribute on fixture(s).

    First selects the fixture(s), then applies the attribute value.

    Args:
        fixture_id: Fixture number (or start of range)
        attribute: Attribute name (e.g., "Pan", "Tilt", "Dimmer")
        value: Value to set
        end_fixture: (Optional) End fixture for range

    Returns:
        str: Operation result message

    Examples:
        - Set Pan to 128 on fixture 1
        - Set Tilt to 50 on fixtures 1 thru 10
    """
    client = await get_client()
    if end_fixture is not None:
        fix_cmd = f"fixture {fixture_id} thru {end_fixture}"
    else:
        fix_cmd = fixture(fixture_id)
    await client.send_command(fix_cmd)
    attr_cmd = attribute_at(attribute, value)
    await client.send_command(attr_cmd)
    range_part = f" thru {end_fixture}" if end_fixture else ""
    return f"Set {attribute} to {value} on Fixture {fixture_id}{range_part}"


@mcp.tool()
@handle_connection_error
async def clear_programmer(
    mode: str = "all",
) -> str:
    """
    Clear the programmer.

    Args:
        mode: Clear mode - "all" (clear everything), "selection" (clear selection only),
              "active" (clear active values only), or "default" (standard clear)

    Returns:
        str: Operation result message

    Examples:
        - Clear all programmer data
        - Clear selection only
    """
    client = await get_client()
    mode_map = {
        "all": clear_all,
        "selection": clear_selection,
        "active": clear_active,
        "default": clear,
    }
    cmd_fn = mode_map.get(mode, clear)
    cmd = cmd_fn()
    await client.send_command(cmd)
    return f"Cleared programmer ({mode})"


# ============================================================
# Preset Management Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def store_preset(
    preset_type: str,
    preset_id: int,
    scope: str | None = None,
) -> str:
    """
    Store current programmer values as a preset.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, focus, control, shapers, video)
        preset_id: Preset number
        scope: (Optional) Scope: "global", "selective", or "universal"

    Returns:
        str: Operation result message

    Examples:
        - Store color preset 1
        - Store global dimmer preset 5
    """
    client = await get_client()
    kwargs = {}
    if scope == "global":
        kwargs["global_scope"] = True
    elif scope == "selective":
        kwargs["selective"] = True
    elif scope == "universal":
        kwargs["universal"] = True
    cmd = cmd_store_preset(preset_type, preset_id, **kwargs)
    await client.send_command(cmd)
    scope_part = f" ({scope})" if scope else ""
    return f"Stored {preset_type} Preset {preset_id}{scope_part}"


@mcp.tool()
@handle_connection_error
async def apply_preset(
    preset_type: str,
    preset_id: int,
) -> str:
    """
    Apply an existing preset to the current selection.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, focus, control, shapers, video)
        preset_id: Preset number

    Returns:
        str: Operation result message

    Examples:
        - Apply color preset 3
        - Apply position preset 1
    """
    client = await get_client()
    cmd = preset(preset_type, preset_id)
    await client.send_command(cmd)
    return f"Applied {preset_type} Preset {preset_id}"


# ============================================================
# Executor Control Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def control_executor(
    executor_id: int,
    action: str,
) -> str:
    """
    Control an executor (on, off, go, kill, toggle).

    Args:
        executor_id: Executor number
        action: Action to perform: "on", "off", "go", "kill", or "toggle"

    Returns:
        str: Operation result message

    Examples:
        - Turn on executor 1
        - Kill executor 3
        - Go on executor 2
    """
    client = await get_client()
    action_map = {
        "on": lambda eid: on(executor=eid),
        "off": lambda eid: off(executor=eid),
        "go": lambda eid: go_executor(eid),
        "kill": lambda eid: kill(f"executor {eid}"),
        "toggle": lambda eid: toggle(f"executor {eid}"),
    }
    cmd_fn = action_map.get(action)
    if cmd_fn is None:
        return f"Unknown action: {action}. Use on, off, go, kill, or toggle."
    cmd = cmd_fn(executor_id)
    await client.send_command(cmd)
    return f"Executor {executor_id}: {action}"


@mcp.tool()
@handle_connection_error
async def set_executor_fader(
    executor_id: int,
    value: int,
) -> str:
    """
    Set an executor's fader level.

    Args:
        executor_id: Executor number
        value: Fader value (0-100)

    Returns:
        str: Operation result message

    Examples:
        - Set executor 1 fader to 75%
    """
    client = await get_client()
    cmd = executor_at(executor_id, value)
    await client.send_command(cmd)
    return f"Set Executor {executor_id} fader to {value}%"


@mcp.tool()
@handle_connection_error
async def assign_to_executor(
    sequence_id: int,
    executor_id: int,
) -> str:
    """
    Assign a sequence to an executor.

    Args:
        sequence_id: Sequence number to assign
        executor_id: Target executor number

    Returns:
        str: Operation result message

    Examples:
        - Assign sequence 1 to executor 6
    """
    client = await get_client()
    cmd = assign("sequence", sequence_id, "executor", executor_id)
    await client.send_command(cmd)
    return f"Assigned Sequence {sequence_id} to Executor {executor_id}"


# ============================================================
# Global State Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def toggle_blackout() -> str:
    """
    Toggle the grand blackout state.

    Returns:
        str: Operation result message
    """
    client = await get_client()
    cmd = blackout()
    await client.send_command(cmd)
    return "Toggled Blackout"


@mcp.tool()
@handle_connection_error
async def toggle_highlight() -> str:
    """
    Toggle highlight mode for fixture programming.

    Returns:
        str: Operation result message
    """
    client = await get_client()
    cmd = highlight()
    await client.send_command(cmd)
    return "Toggled Highlight"


# ============================================================
# Labeling Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def label_object(
    object_type: str,
    object_id: int,
    name: str,
) -> str:
    """
    Assign a name label to a grandMA2 object.

    Args:
        object_type: Object type (e.g., "group", "cue", "sequence", "macro", "preset")
        object_id: Object number
        name: Name to assign

    Returns:
        str: Operation result message

    Examples:
        - Label group 1 as "Front Wash"
        - Label cue 5 as "Intro"
    """
    client = await get_client()
    cmd = label(object_type, object_id, name)
    await client.send_command(cmd)
    return f'Labeled {object_type} {object_id} as "{name}"'


@mcp.tool()
@handle_connection_error
async def label_sequence_cue(
    sequence: str,
    cue_id: int,
    name: str,
    end_cue: int | None = None,
) -> str:
    """
    Label a cue within a specific sequence.

    This tool addresses cues through the sequence context, which is required
    for labeling cues inside named sequences.

    Args:
        sequence: Sequence ID or name (e.g., "100" or "Set List")
        cue_id: Cue number within the sequence
        name: Label to assign
        end_cue: (Optional) End cue for range labeling

    Returns:
        str: Operation result message

    Examples:
        - Label cue 1 in "Set List" as "Opening+Childhood"
        - Label cue 1 in sequence 100 as "Opening+Childhood"
        - Label cues 1 thru 5 in "Set List" as "Act 1"
    """
    client = await get_client()
    try:
        seq_param = int(sequence)
    except (ValueError, TypeError):
        seq_param = sequence
    cmd = cmd_label_sequence_cue(seq_param, cue_id, name, end_cue=end_cue)
    await client.send_command(cmd)
    range_part = f" thru {end_cue}" if end_cue else ""
    return f'Labeled Sequence "{sequence}" Cue {cue_id}{range_part} as "{name}"'


# ============================================================
# Appearance Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def assign_appearance(
    object_type: str,
    object_id: int | str,
    end: int | None = None,
    source_type: str | None = None,
    source_id: int | str | None = None,
    reset: bool = False,
    color: str | None = None,
    red: int | None = None,
    green: int | None = None,
    blue: int | None = None,
    hue: int | None = None,
    saturation: int | None = None,
    brightness: int | None = None,
) -> str:
    """
    Assign an appearance (frame/background color) to a grandMA2 pool object or cue.

    Colors can be specified via RGB (0-100), HSB (hue 0-360, sat/bright 0-100),
    hex color string, or by copying from a source object. Use reset to clear.

    Args:
        object_type: Object type (e.g., "group", "cue", "preset", "macro")
        object_id: Object number or compound ID (e.g., 1 or "0.1")
        end: (Optional) End ID for applying to a range of objects
        source_type: (Optional) Source object type to copy appearance from
        source_id: (Optional) Source object ID to copy appearance from
        reset: Reset appearance to default
        color: Hex color code (e.g., "FF0000") or gel name
        red: Red component (0-100)
        green: Green component (0-100)
        blue: Blue component (0-100)
        hue: Hue (0-360)
        saturation: Saturation (0-100)
        brightness: Brightness (0-100)

    Returns:
        str: Operation result message

    Examples:
        - Set group 1 to red: object_type="group", object_id=1, red=100, green=0, blue=0
        - Set preset 0.1 to hex color: object_type="preset", object_id="0.1", color="FF0000"
        - Copy appearance from macro 13 to macro 2: object_type="macro", object_id=2, source_type="macro", source_id=13
        - Reset group 1 appearance: object_type="group", object_id=1, reset=True
    """
    client = await get_client()
    cmd = cmd_appearance(
        object_type,
        object_id,
        end=end,
        source_type=source_type,
        source_id=source_id,
        reset=reset,
        color=color,
        red=red,
        green=green,
        blue=blue,
        hue=hue,
        saturation=saturation,
        brightness=brightness,
    )
    await client.send_command(cmd)
    return f"Applied appearance to {object_type} {object_id}"


# ============================================================
# Macro Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def set_macro_line(
    macro_id: int,
    line: int,
    command: str,
    pool: int = 1,
) -> str:
    """
    Set the command for a specific line within a macro.

    Args:
        macro_id: Macro number
        line: Line number within the macro
        command: The command string for that line (e.g., "SetVar $song='Opening+Childhood'")
        pool: Macro pool number (default: 1)

    Returns:
        str: Operation result message

    Examples:
        - Set macro 101 line 1 to "SetVar $song='Opening+Childhood'"
        - Set macro 50 line 3 in pool 2 to "Go Sequence 5"
    """
    client = await get_client()
    cmd = assign_macro_cmd(macro_id, line, command, pool=pool)
    await client.send_command(cmd)
    return f'Set Macro {macro_id} Line {line} to "{command}" (Pool {pool})'


# ============================================================
# Bulk Cue Operations Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def store_cue_across_sequences(
    cue_id: float,
    sequence_start: int,
    sequence_end: int,
    cue_name: str | None = None,
) -> dict:
    """
    Store a cue across a range of sequences.

    Iterates over every sequence in the range and stores the specified cue.
    Optionally assigns a name to each stored cue.

    Args:
        cue_id: Cue number to store (e.g., 1, 0.5)
        sequence_start: First sequence number in the range
        sequence_end: Last sequence number in the range (inclusive)
        cue_name: (Optional) Name for the cue

    Returns:
        dict: Result with commands_sent, count, and summary

    Examples:
        - Store cue 0.5 across sequences 101-125 with name "((LOADING SONG))"
        - Store cue 1 in sequence 101
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    return await gma2.store_cue_across_sequences(
        cue_id=cue_id,
        sequence_start=sequence_start,
        sequence_end=sequence_end,
        cue_name=cue_name,
    )


@mcp.tool()
@handle_connection_error
async def label_cue_across_sequences(
    cue_id: float,
    sequence_start: int,
    sequence_end: int,
    label: str,
) -> dict:
    """
    Label a cue across a range of sequences.

    Iterates over every sequence in the range and labels the specified cue.

    Args:
        cue_id: Cue number to label (e.g., 1, 0.5)
        sequence_start: First sequence number in the range
        sequence_end: Last sequence number in the range (inclusive)
        label: Label text to assign

    Returns:
        dict: Result with commands_sent, count, and summary

    Examples:
        - Label cue 0.5 across sequences 101-125 as "((LOADING SONG))"
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    return await gma2.label_cue_across_sequences(
        cue_id=cue_id,
        sequence_start=sequence_start,
        sequence_end=sequence_end,
        label=label,
    )


@mcp.tool()
@handle_connection_error
async def appearance_cue_across_sequences(
    cue_id: float,
    sequence_start: int,
    sequence_end: int,
    red: int | None = None,
    green: int | None = None,
    blue: int | None = None,
    color: str | None = None,
) -> dict:
    """
    Set appearance (color) on a cue across a range of sequences.

    Iterates over every sequence in the range and applies the color to the
    specified cue. Supports RGB values (0-100) or hex color codes.

    Args:
        cue_id: Cue number (e.g., 1, 0.5)
        sequence_start: First sequence number in the range
        sequence_end: Last sequence number in the range (inclusive)
        red: (Optional) Red component (0-100)
        green: (Optional) Green component (0-100)
        blue: (Optional) Blue component (0-100)
        color: (Optional) Hex color code (e.g., "FF0000")

    Returns:
        dict: Result with commands_sent, count, and summary

    Examples:
        - Set cue 0.5 to black across sequences 101-125 (red=0, green=0, blue=0)
        - Set cue 1 to red across sequences 101-103 (color="FF0000")
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    kwargs = {}
    if red is not None:
        kwargs["red"] = red
    if green is not None:
        kwargs["green"] = green
    if blue is not None:
        kwargs["blue"] = blue
    if color is not None:
        kwargs["color"] = color
    return await gma2.appearance_cue_across_sequences(
        cue_id=cue_id,
        sequence_start=sequence_start,
        sequence_end=sequence_end,
        **kwargs,
    )


# ============================================================
# Sequence Playback Tools (existing)
# ============================================================


@mcp.tool()
@handle_connection_error
async def execute_sequence(
    sequence_id: int,
    action: str,
    cue_id: int | None = None,
) -> str:
    """
    Execute sequence-related operations.

    Args:
        sequence_id: Sequence number
        action: Operation type: "go" (execute), "pause" (pause), or "goto" (jump to cue)
        cue_id: (Required for goto) Target cue number

    Returns:
        str: Operation result message

    Examples:
        - Execute sequence 1
        - Pause sequence 2
        - Jump to cue 5 of sequence 1
    """
    client = await get_client()

    if action == "go":
        cmd = go_sequence(sequence_id)
        await client.send_command(cmd)
        return f"Executed Sequence {sequence_id}"

    elif action == "pause":
        cmd = pause_sequence(sequence_id)
        await client.send_command(cmd)
        return f"Paused Sequence {sequence_id}"

    elif action == "goto":
        if cue_id is None:
            return "Error: goto action requires cue_id to be specified"
        cmd = goto_cue(sequence_id, cue_id)
        await client.send_command(cmd)
        return f"Jumped to Cue {cue_id} of Sequence {sequence_id}"

    return f"Unknown action: {action}, use go, pause, or goto"


# ============================================================
# Raw Command Tool (existing)
# ============================================================


@mcp.tool()
@handle_connection_error
async def send_raw_command(command: str) -> str:
    """
    Send a raw MA command to grandMA2.

    This is a low-level tool that allows sending any grandMA2 command-line instruction.
    It is recommended to use other high-level tools first; use this tool only when
    special commands are needed.

    Args:
        command: Raw MA command to send

    Returns:
        str: Operation result message

    Examples:
        - blackout
        - go+ executor 1.1
        - store sequence 1 cue 1
    """
    client = await get_client()
    await client.send_command(command)
    return f"Sent command: {command}"


# ============================================================
# Server Startup
# ============================================================


def main():
    """MCP Server entry point."""
    logger.info("Starting grandMA2 MCP Server...")
    logger.info(f"Connecting to grandMA2: {GMA_HOST}:{GMA_PORT}")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
