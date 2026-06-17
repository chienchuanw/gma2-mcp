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
    delete_macro as cmd_delete_macro,
    effect as cmd_effect,
    effect_bpm,
    effect_form as cmd_effect_form,
    effect_high,
    effect_hz,
    effect_low,
    effect_phase as cmd_effect_phase,
    effect_width as cmd_effect_width,
    executor_at,
    fixture,
    fixture_at,
    go_executor,
    go_sequence,
    goto,
    goto_cue,
    highlight,
    info as cmd_info,
    info_cue as cmd_info_cue,
    info_group as cmd_info_group,
    kill,
    label,
    label_group,
    label_macro as cmd_label_macro,
    label_sequence_cue as cmd_label_sequence_cue,
    list_cue as cmd_list_cue,
    list_group as cmd_list_group,
    list_macro as cmd_list_macro,
    list_objects as cmd_list_objects,
    list_preset as cmd_list_preset,
    list_sequence_cue as cmd_list_sequence_cue,
    list_shows as cmd_list_shows,
    list_user_var,
    list_var,
    load_show as cmd_load_show,
    new_show as cmd_new_show,
    off,
    on,
    pause_sequence,
    preset,
    select_fixture,
    save_show as cmd_save_show,
    store_cue as cmd_store_cue,
    store_group,
    store_macro as cmd_store_macro,
    store_preset as cmd_store_preset,
    sync_effects,
    toggle,
)
from src.commands.constants import PRESET_TYPES
from src.gma2_client import GMA2Client
from src.response_parser import parse_macro_lines, parse_cue_info, parse_object_label

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


async def run_verified(client, command: str, success: str) -> str:
    """Execute a mutating command and report the console's actual outcome.

    Returns ``success`` only when the console accepted the command; otherwise
    returns the console's error (e.g. ``Error #14: OBJECT DOES NOT EXIST``)
    instead of fabricating success. See #56.
    """
    result = await client.execute(command)
    return success if result.ok else result.summary()


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
    "macro": [
        "All macro lines and their commands are permanently lost",
        "Cue CMD triggers referencing this macro will fail silently",
        "Other macros calling this macro via 'Macro N' will reference a non-existent object",
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
    scope_part = f" ({scope})" if scope else ""
    return await run_verified(
        client, cmd, f"Stored {preset_type} Preset {preset_id}{scope_part}"
    )


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
    return await run_verified(
        client, cmd, f"Applied {preset_type} Preset {preset_id}"
    )


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


@mcp.tool()
@handle_connection_error
async def run_macro(
    macro_id: int,
    pool: int = 1,
) -> str:
    """
    Execute a macro by ID.

    Starts the specified macro using the Go+ command.

    Args:
        macro_id: Macro number to execute
        pool: Macro pool number (default: 1)

    Returns:
        str: Operation result message

    Examples:
        - Run macro 5 from default pool
        - Run macro 10 from pool 2
    """
    client = await get_client()
    cmd = f"go+ macro {pool}.{macro_id}"
    await client.send_command(cmd)
    return f"Executed Macro {macro_id} (Pool {pool})"


@mcp.tool()
@handle_connection_error
async def create_macro(
    macro_id: int,
    commands: list[str],
    name: str | None = None,
    pool: int = 1,
) -> str:
    """
    Create a macro with command lines.

    Stores an empty macro, then assigns each command to sequential lines.
    Optionally labels the macro.

    Args:
        macro_id: Macro number to create
        commands: List of command strings for each macro line
        name: Optional label for the macro
        pool: Macro pool number (default: 1)

    Returns:
        str: Operation result message

    Examples:
        - Create macro 10 with commands ["Go Sequence 1", "Go Sequence 2"]
        - Create macro 10 named "Start Show" with one command
    """
    if not commands:
        return "Error: at least one command is required to create a macro."

    client = await get_client()

    # Store empty macro
    await client.send_command(cmd_store_macro(macro_id))

    # Assign each command to a line
    for i, command in enumerate(commands, start=1):
        cmd = assign_macro_cmd(macro_id, i, command, pool=pool)
        await client.send_command(cmd)

    # Optionally label the macro
    if name is not None:
        await client.send_command(cmd_label_macro(macro_id, name))

    label_msg = f' "{name}"' if name else ""
    return f"Created Macro {macro_id}{label_msg} with {len(commands)} lines (Pool {pool})"


@mcp.tool()
@handle_connection_error
async def label_macro_tool(
    macro_id: int,
    name: str,
) -> str:
    """
    Label a macro in the macro pool.

    Args:
        macro_id: Macro number to label
        name: Label text for the macro

    Returns:
        str: Operation result message

    Examples:
        - Label macro 5 as "Blackout All"
    """
    client = await get_client()
    cmd = cmd_label_macro(macro_id, name)
    await client.send_command(cmd)
    return f'Labeled Macro {macro_id} as "{name}"'


@mcp.tool()
@handle_connection_error
async def list_macros() -> str:
    """
    List macros in the macro pool.

    Returns raw console output from the List Macro command.

    Returns:
        str: Raw console response with macro listing
    """
    client = await get_client()
    cmd = cmd_list_objects("macro")
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def delete_macro_tool(
    macro_id: int,
    pool: int = 1,
) -> str:
    """
    Delete a macro from the macro pool.

    WARNING: This is a destructive operation that permanently removes the macro.

    Args:
        macro_id: Macro number to delete
        pool: Macro pool number (default: 1)

    Returns:
        str: Operation result message with warnings
    """
    client = await get_client()
    cmd = cmd_delete_macro(macro_id, pool=pool)
    await client.send_command(cmd)
    return f"Deleted Macro {macro_id} (Pool {pool}){_format_warnings('macro')}"


# ============================================================
# Effect Control Tools (Issue #7)
# ============================================================


@mcp.tool()
@handle_connection_error
async def apply_effect(
    effect_id: int,
) -> str:
    """
    Apply a predefined effect from the effect pool to the current fixture selection.

    Fixtures must be selected first using set_fixture_value or create_fixture_group.

    Args:
        effect_id: Effect number from the effect pool

    Returns:
        str: Operation result message

    Examples:
        - Apply effect 5 to selected fixtures
    """
    client = await get_client()
    cmd = cmd_effect(effect_id)
    await client.send_command(cmd)
    return f"Applied Effect {effect_id} to current selection"


@mcp.tool()
@handle_connection_error
async def set_effect_speed(
    value: float,
    unit: str = "bpm",
) -> str:
    """
    Set the effect speed for the current selection.

    Args:
        value: Speed value
        unit: Speed unit — "bpm" (beats per minute) or "hz" (hertz)

    Returns:
        str: Operation result message

    Examples:
        - Set effect speed to 120 BPM
        - Set effect speed to 2.5 Hz
    """
    unit_lower = unit.lower()
    if unit_lower not in ("bpm", "hz"):
        return f"Invalid unit '{unit}'. Valid units: bpm, hz"

    client = await get_client()
    if unit_lower == "bpm":
        cmd = effect_bpm(value)
    else:
        cmd = effect_hz(value)
    await client.send_command(cmd)
    return f"Set effect speed to {value} {unit.upper()}"


@mcp.tool()
@handle_connection_error
async def set_effect_form(
    form: str,
) -> str:
    """
    Set the effect waveform for the current selection.

    Args:
        form: Waveform type — name (e.g., "sin", "ramp", "square") or number

    Returns:
        str: Operation result message

    Examples:
        - Set effect form to "sin"
        - Set effect form to 6
    """
    client = await get_client()
    cmd = cmd_effect_form(form)
    await client.send_command(cmd)
    return f"Set effect form to {form}"


@mcp.tool()
@handle_connection_error
async def set_effect_range(
    high: float | None = None,
    low: float | None = None,
) -> str:
    """
    Set effect high and/or low values for the current selection.

    At least one of high or low must be provided.

    Args:
        high: Effect high value (optional)
        low: Effect low value (optional)

    Returns:
        str: Operation result message

    Examples:
        - Set effect range high=100, low=0
        - Set only effect high to 80
    """
    if high is None and low is None:
        return "Error: at least one of high or low must be provided."

    client = await get_client()
    parts = []
    if high is not None:
        await client.send_command(effect_high(high))
        parts.append(f"high={high}")
    if low is not None:
        await client.send_command(effect_low(low))
        parts.append(f"low={low}")
    return f"Set effect range: {', '.join(parts)}"


@mcp.tool()
@handle_connection_error
async def set_effect_phase(
    phase: float,
) -> str:
    """
    Set the effect phase offset for the current selection.

    Args:
        phase: Phase value in degrees (e.g., 0, 90, 180, 270)

    Returns:
        str: Operation result message
    """
    client = await get_client()
    cmd = cmd_effect_phase(phase)
    await client.send_command(cmd)
    return f"Set effect phase to {phase} degrees"


@mcp.tool()
@handle_connection_error
async def set_effect_width(
    width: float,
) -> str:
    """
    Set the effect width for the current selection.

    Args:
        width: Width value (percentage of cycle)

    Returns:
        str: Operation result message
    """
    client = await get_client()
    cmd = cmd_effect_width(width)
    await client.send_command(cmd)
    return f"Set effect width to {width}"


@mcp.tool()
@handle_connection_error
async def stop_effects() -> str:
    """
    Stop all running effects for the current selection.

    Removes effect values from the programmer using the Off command.

    Returns:
        str: Operation result message
    """
    client = await get_client()
    await client.send_command("off effect")
    return "Stopped all effects for current selection (Off Effect)"


@mcp.tool()
@handle_connection_error
async def sync_effects_tool() -> str:
    """
    Synchronize all running effects.

    Resets effect timing so all running effects align their phase.

    Returns:
        str: Operation result message
    """
    client = await get_client()
    cmd = sync_effects()
    await client.send_command(cmd)
    return "Synchronized all running effects"


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
# Query / Introspection Tools (Issue #4)
# ============================================================

EMPTY_RESPONSE_MSG = (
    "No data returned. The list may be empty or the console did not respond."
)


@mcp.tool()
@handle_connection_error
async def list_groups(
    group_id: int | None = None, end_group_id: int | None = None
) -> str:
    """
    list all defined groups on the grandMA2 console.

    returns raw console output from the List Group command.

    Args:
        group_id: specific group ID or start of range (optional)
        end_group_id: end group ID for range query (optional, requires group_id)

    Returns:
        str: raw console response with group listing
    """
    client = await get_client()
    cmd = cmd_list_group(group_id, end=end_group_id)
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def list_cues(
    cue_id: int | float | None = None,
    end_cue_id: int | float | None = None,
    sequence_id: int | None = None,
) -> str:
    """
    list cues on the grandMA2 console.

    lists cues of the selected executor, or a specific sequence if sequence_id is provided.

    Args:
        cue_id: specific cue ID or start of range (optional)
        end_cue_id: end cue ID for range query (optional)
        sequence_id: sequence to list cues from (optional)

    Returns:
        str: raw console response with cue listing
    """
    client = await get_client()
    cmd = cmd_list_cue(cue_id, end=end_cue_id, sequence_id=sequence_id)
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def list_presets(
    preset_type: str,
    preset_id: int | None = None,
) -> str:
    """
    list presets of a given type on the grandMA2 console.

    valid preset types: dimmer, position, gobo, color, beam, focus, control, shapers, video.

    Args:
        preset_type: type of preset (e.g. "color", "position", "dimmer")
        preset_id: specific preset ID (optional)

    Returns:
        str: raw console response with preset listing
    """
    valid_types = set(PRESET_TYPES.keys())
    if preset_type.lower() not in valid_types:
        return (
            f"Invalid preset type '{preset_type}'. "
            f"Valid types: {', '.join(sorted(valid_types))}"
        )

    client = await get_client()
    cmd = cmd_list_preset(preset_type, preset_id)
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def get_cue_annotation(
    cue_id: int | float, sequence_id: int | None = None
) -> str:
    """
    read the user-added annotation text on a cue.

    in grandMA2, the Info keyword reads or writes user-added descriptive text
    annotations on objects. this tool reads the annotation. if no annotation has
    been set on the cue, the response will be empty.

    note: this does NOT return cue properties (fade time, values, etc.).
    to see cue properties, use list_cues with a specific cue_id instead.

    Args:
        cue_id: cue ID to read annotation from
        sequence_id: sequence containing the cue (optional)

    Returns:
        str: the user annotation text, or empty response message if none set
    """
    client = await get_client()
    cmd = cmd_info_cue(cue_id, sequence_id=sequence_id)
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def get_group_annotation(group_id: int) -> str:
    """
    read the user-added annotation text on a group.

    in grandMA2, the Info keyword reads or writes user-added descriptive text
    annotations on objects. this tool reads the annotation. if no annotation has
    been set on the group, the response will be empty.

    note: this does NOT return group composition or fixture details.
    to see group details, use list_groups with a specific group_id instead.

    Args:
        group_id: group ID to read annotation from

    Returns:
        str: the user annotation text, or empty response message if none set
    """
    client = await get_client()
    cmd = cmd_info_group(group_id)
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def list_variables(
    variable_type: str, filter: str | None = None
) -> str:
    """
    list show variables or user variables on the grandMA2 console.

    Args:
        variable_type: "show" for show variables (ListVar), "user" for user variables (ListUserVar)
        filter: optional filter pattern (e.g. "f*" to list variables starting with f)

    Returns:
        str: raw console response with variable listing
    """
    if variable_type.lower() == "show":
        cmd = list_var(filter)
    elif variable_type.lower() == "user":
        cmd = list_user_var(filter)
    else:
        return (
            f"Invalid variable type '{variable_type}'. "
            f"Valid types: show, user"
        )

    client = await get_client()
    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


@mcp.tool()
@handle_connection_error
async def query_object(
    object_type: str,
    object_id: int | str | None = None,
    mode: str = "list",
) -> str:
    """
    generic query for any grandMA2 object type.

    use this for object types without a dedicated tool (e.g. executors, sequences, effects).
    for groups, cues, and presets, prefer the specific tools.

    Args:
        object_type: MA2 object type (e.g. "executor", "sequence", "effect", "macro")
        object_id: object ID to query (optional)
        mode: "list" to list objects, "annotation" to read user-added text annotation (default: "list").
              note: "annotation" mode reads user-added descriptive text, NOT object properties.

    Returns:
        str: raw console response
    """
    client = await get_client()
    if mode == "annotation":
        if object_id is None:
            return "object_id is required when using annotation mode."
        cmd = cmd_info(object_type, object_id)
    else:
        cmd = cmd_list_objects(object_type, object_id)

    response = await client.send_command_with_response(cmd)
    return response if response.strip() else EMPTY_RESPONSE_MSG


# ============================================================
# Show File Management Tools (Issue #5)
# ============================================================


@mcp.tool()
@handle_connection_error
async def save_show_tool(show_name: str | None = None) -> str:
    """
    save the current show file on the grandMA2 console.

    if no name is provided, saves under the current show name.
    uses /noconfirm to suppress the overwrite confirmation popup
    that would otherwise block Telnet when a show with the same name exists.

    Args:
        show_name: name to save the show as (optional)

    Returns:
        str: confirmation message
    """
    client = await get_client()
    cmd = cmd_save_show(show_name, noconfirm=True)
    await client.send_command(cmd)
    if show_name:
        return f"Show saved as '{show_name}'."
    return "Show saved successfully."


@mcp.tool()
@handle_connection_error
async def load_show_tool(show_name: str, save_first: bool = False) -> str:
    """
    load a show file on the grandMA2 console.

    WARNING: this is a DESTRUCTIVE operation. any unsaved changes to the current
    show will be lost. set save_first=True to save the current show before loading.

    Args:
        show_name: name of the show file to load
        save_first: if True, saves the current show before loading the new one

    Returns:
        str: confirmation message with warning about unsaved changes
    """
    client = await get_client()
    if save_first:
        await client.send_command(cmd_save_show(noconfirm=True))
    cmd = cmd_load_show(show_name, noconfirm=True)
    await client.send_command(cmd)
    msg = f"Loading show '{show_name}'."
    if not save_first:
        msg += " WARNING: Any unsaved changes to the previous show were lost."
    else:
        msg += " Previous show was saved first."
    return msg


@mcp.tool()
@handle_connection_error
async def new_show_tool(show_name: str | None = None, save_first: bool = False) -> str:
    """
    create a new empty show on the grandMA2 console.

    WARNING: this is a DESTRUCTIVE operation. any unsaved changes to the current
    show will be lost. set save_first=True to save the current show before creating a new one.

    note: per the grandMA2 manual, NewShow requires a show name. omitting the
    name may work on some console versions but this behavior is undocumented.
    providing a name is recommended.

    Args:
        show_name: name for the new show (recommended — required per official manual)
        save_first: if True, saves the current show before creating a new one

    Returns:
        str: confirmation message with warning about unsaved changes
    """
    client = await get_client()
    if save_first:
        await client.send_command(cmd_save_show(noconfirm=True))
    cmd = cmd_new_show(show_name, noconfirm=True)
    await client.send_command(cmd)
    name_part = f" '{show_name}'" if show_name else ""
    msg = f"Created new show{name_part}."
    if not save_first:
        msg += " WARNING: Any unsaved changes to the previous show were lost."
    else:
        msg += " Previous show was saved first."
    return msg


@mcp.tool()
@handle_connection_error
async def list_shows_tool(filter: str | None = None) -> str:
    """
    list available show files on the grandMA2 console.

    Args:
        filter: optional filter pattern (e.g. "Mac*" to list shows starting with Mac)

    Returns:
        str: raw console response with show file listing
    """
    client = await get_client()
    cmd = cmd_list_shows(filter)
    response = await client.send_command_with_response(cmd)
    if not response.strip():
        return "No show files found on the selected drive."
    return response


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
    result = await client.execute(command)
    return result.summary()


# ============================================================
# Read-Back Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def read_macro_lines(macro_id: int, pool: int = 1) -> dict:
    """Read macro line content for a given macro.

    Retrieves and parses all lines of a macro, returning each line's
    number and command string.

    Args:
        macro_id: Macro ID to read
        pool: Macro pool number (default 1)

    Returns:
        dict with parsed macro lines and raw response
    """
    client = await get_client()
    cmd = cmd_list_macro(macro_id, pool=pool)
    raw = await client.send_command_with_response(cmd)
    result = parse_macro_lines(raw)
    result["macro_id"] = macro_id
    result["raw_response"] = raw
    return result


@mcp.tool()
@handle_connection_error
async def read_cue_info(sequence_id: int, cue_id: int | str) -> dict:
    """Read cue information for a specific cue in a sequence.

    Retrieves and parses cue data including label, fade time, and CMD field.

    Args:
        sequence_id: Sequence ID containing the cue
        cue_id: Cue ID (int or str for decimal cue numbers like "2.5")

    Returns:
        dict with parsed cue info and raw response
    """
    client = await get_client()
    cmd = cmd_list_sequence_cue(sequence_id, cue_id)
    raw = await client.send_command_with_response(cmd)
    result = parse_cue_info(raw)
    result["sequence_id"] = sequence_id
    result["cue_id"] = cue_id
    result["raw_response"] = raw
    return result


@mcp.tool()
@handle_connection_error
async def read_object_label(object_type: str, object_id: int | str) -> dict:
    """Read the label/name of any grandMA2 show object.

    Uses the generic list command to retrieve an object's name field.

    Note: For macros, object_id must be pool-qualified (e.g., "1.5" for
    Macro 5 in Pool 1) since grandMA2 addresses macros as pool.id.
    For most other object types, a plain integer ID is sufficient.

    Args:
        object_type: Object type (e.g., "group", "sequence", "macro", "page")
        object_id: Object ID (int for most types, or "pool.id" string for macros)

    Returns:
        dict with parsed label and raw response
    """
    client = await get_client()
    cmd = cmd_list_objects(object_type, object_id)
    raw = await client.send_command_with_response(cmd)
    result = parse_object_label(raw)
    result["object_type"] = object_type
    result["object_id"] = object_id
    result["raw_response"] = raw
    return result


# ============================================================
# Music Show Workflow Tools
# ============================================================


@mcp.tool()
@handle_connection_error
async def create_song_objects(song_id: int, song_name: str) -> str:
    """
    Create and label a Sequence + Page pair for a song.

    Stores a sequence and a page with the same ID and name, which is the
    standard pattern for per-song programming in music show workflows.

    Args:
        song_id: ID for both the sequence and page
        song_name: Name to assign to both objects

    Returns:
        str: Operation result message

    Examples:
        - Create sequence 101 and page 101 named "Opening+Childhood"
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    result = await gma2.create_song_objects(song_id=song_id, song_name=song_name)
    return result["summary"]


@mcp.tool()
@handle_connection_error
async def setup_song_macro(
    macro_id: int,
    song_name: str,
    var_name: str = "$song",
) -> str:
    """
    Create a macro that sets a user variable to the song name.

    Stores a macro, labels it with the song name, and assigns a SetVar
    command on line 1. This is used to track the current song in
    music show workflows.

    Args:
        macro_id: Macro number to create
        song_name: Song name used for label and variable value
        var_name: Variable name for the SetVar command (default: "$song")

    Returns:
        str: Operation result message

    Examples:
        - Create macro 101 that sets $song to "Opening+Childhood"
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    result = await gma2.setup_song_macro(
        macro_id=macro_id, song_name=song_name, var_name=var_name
    )
    return result["summary"]


@mcp.tool()
@handle_connection_error
async def build_set_list(
    sequence_id: int,
    sequence_name: str,
    songs: list[dict],
) -> str:
    """
    Create a set-list sequence with cue-to-macro links.

    Stores a sequence, then for each song creates a cue and assigns a
    macro trigger to its CMD field. Each song dict must contain:
        cue_id (int): Cue number in the set-list sequence
        macro_id (int): Macro to trigger via cue CMD
        name (str): Name for the cue

    Args:
        sequence_id: Sequence number for the set list
        sequence_name: Label for the set-list sequence
        songs: List of song definition dicts

    Returns:
        str: Operation result message

    Examples:
        - Build a set list with 3 songs linking cues to macros
    """
    telnet = await get_client()
    gma2 = GMA2Client(telnet)
    result = await gma2.build_set_list(
        sequence_id=sequence_id, sequence_name=sequence_name, songs=songs
    )
    return result["summary"]


# ============================================================
# Server Startup
# ============================================================


def main():
    """MCP Server entry point."""
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    valid_transports = {"stdio", "streamable-http"}
    if transport not in valid_transports:
        logger.warning(
            f"Invalid MCP_TRANSPORT '{transport}'. "
            f"Valid: {', '.join(sorted(valid_transports))}. Falling back to stdio."
        )
        transport = "stdio"

    logger.info(f"Starting grandMA2 MCP Server (transport: {transport})...")
    logger.info(f"Connecting to grandMA2: {GMA_HOST}:{GMA_PORT}")

    kwargs = {"transport": transport}
    if transport == "streamable-http":
        kwargs["host"] = os.environ.get("MCP_HOST", "127.0.0.1")
        kwargs["port"] = int(os.environ.get("MCP_PORT", "8000"))
        logger.info(f"HTTP server binding to {kwargs['host']}:{kwargs['port']}")

    mcp.run(**kwargs)


if __name__ == "__main__":
    main()
