"""
Timecode Function Keyword Builders for grandMA2 Command Builder

Pure functions that construct grandMA2 timecode command strings. Verified
against the grandMA2 manual command-line syntax:

- Store/Go/Pause/Off/Top/Record Timecode <id>
- Assign Timecode <id> /<param> = <value>   (e.g. /Slot, /Length, /Name)

Timecode events are recorded in real time via Record mode (see record_timecode);
grandMA2 does not expose a documented single command-line call to insert an
individual event at an arbitrary HH:MM:SS:FF timestamp.
"""

from __future__ import annotations

from typing import Union


def _timecode_action(action: str, tc_id: int) -> str:
    return f"{action} timecode {tc_id}"


def store_timecode(tc_id: int) -> str:
    """Create/store a timecode show in the timecode pool."""
    return _timecode_action("store", tc_id)


def go_timecode(tc_id: int) -> str:
    """Start playback of a timecode show."""
    return _timecode_action("go", tc_id)


def pause_timecode(tc_id: int) -> str:
    """Pause a running timecode show."""
    return _timecode_action("pause", tc_id)


def off_timecode(tc_id: int) -> str:
    """Stop a timecode show."""
    return _timecode_action("off", tc_id)


def top_timecode(tc_id: int) -> str:
    """Rewind a timecode show to its beginning."""
    return _timecode_action("top", tc_id)


def record_timecode(tc_id: int) -> str:
    """Arm/record real-time events into a timecode show (toggles record mode)."""
    return _timecode_action("record", tc_id)


def assign_timecode_param(
    tc_id: int,
    param: str,
    value: Union[int, str],
) -> str:
    """Assign a configuration parameter to a timecode show.

    Args:
        tc_id: Timecode show ID
        param: Parameter name (e.g. "slot", "length", "name")
        value: Parameter value. String values are quoted unless they are a
                duration/numeric token (e.g. "1h30m0s").

    Examples:
        >>> assign_timecode_param(1, "slot", 3)
        'assign timecode 1 /slot = 3'
        >>> assign_timecode_param(1, "name", "MyShow")
        'assign timecode 1 /name = "MyShow"'
    """
    if isinstance(value, str) and param.lower() == "name":
        value_part = f'"{value}"'
    else:
        value_part = str(value)
    return f"assign timecode {tc_id} /{param.lower()} = {value_part}"
