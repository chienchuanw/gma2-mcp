"""
Command Builder Module

This module provides high-level functions to construct grandMA2 command strings.
These functions are responsible only for generating correctly formatted commands,
not for sending them.

According to coding-standards.md, these functions are "thin wrappers" that
only construct MA commands without any Telnet logic.
"""

from typing import Optional

# Preset type mappings to numeric IDs
# grandMA2 uses numbers to distinguish preset types
PRESET_TYPES = {
    "dimmer": 1,
    "position": 2,
    "gobo": 3,
    "color": 2,  # color also uses preset type 2
    "beam": 4,
    "focus": 5,
    "control": 6,
    "shapers": 7,
    "video": 8,
}


# ============================================================
# Fixture-related commands
# ============================================================


def select_fixture(start: int, end: Optional[int] = None) -> str:
    """
    Construct a command to select fixtures.

    Args:
        start: Starting fixture number
        end: Ending fixture number (optional; if not specified, selects a single fixture)

    Returns:
        str: MA command to select fixtures

    Examples:
        >>> select_fixture(1)
        'selfix fixture 1'
        >>> select_fixture(1, 10)
        'selfix fixture 1 thru 10'
    """
    if end is None or start == end:
        return f"selfix fixture {start}"
    return f"selfix fixture {start} thru {end}"


def clear_selection() -> str:
    """
    Construct a command to clear the current selection.

    Returns:
        str: MA command to clear selection
    """
    return "clearall"


# ============================================================
# Group-related commands
# ============================================================


def store_group(group_id: int) -> str:
    """
    Construct a command to store a group.

    Args:
        group_id: Group number

    Returns:
        str: MA command to store a group
    """
    return f"store group {group_id}"


def label_group(group_id: int, name: str) -> str:
    """
    Construct a command to label a group.

    Args:
        group_id: Group number
        name: Group name

    Returns:
        str: MA command to label a group
    """
    return f'label group {group_id} "{name}"'


def select_group(group_id: int) -> str:
    """
    Construct a command to select a group.

    Args:
        group_id: Group number

    Returns:
        str: MA command to select a group
    """
    return f"group {group_id}"


def delete_group(group_id: int) -> str:
    """
    Construct a command to delete a group.

    Args:
        group_id: Group number

    Returns:
        str: MA command to delete a group
    """
    return f"delete group {group_id}"


# ============================================================
# Preset-related commands
# ============================================================


def store_preset(preset_type: str, preset_id: int) -> str:
    """
    Construct a command to store a preset.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, focus, control, shapers, video)
        preset_id: Preset number

    Returns:
        str: MA command to store a preset
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f"store preset {type_num}.{preset_id}"


def label_preset(preset_type: str, preset_id: int, name: str) -> str:
    """
    Construct a command to label a preset.

    Args:
        preset_type: Preset type
        preset_id: Preset number
        name: Preset name

    Returns:
        str: MA command to label a preset
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f'label preset {type_num}.{preset_id} "{name}"'


def call_preset(preset_type: str, preset_id: int) -> str:
    """
    Construct a command to call a preset.

    Args:
        preset_type: Preset type
        preset_id: Preset number

    Returns:
        str: MA command to call a preset
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f"preset {type_num}.{preset_id}"


# ============================================================
# Sequence-related commands
# ============================================================


def go_sequence(sequence_id: int) -> str:
    """
    Construct a command to execute a sequence.

    Args:
        sequence_id: Sequence number

    Returns:
        str: MA command to execute a sequence
    """
    return f"go+ sequence {sequence_id}"


def pause_sequence(sequence_id: int) -> str:
    """
    Construct a command to pause a sequence.

    Args:
        sequence_id: Sequence number

    Returns:
        str: MA command to pause a sequence
    """
    return f"pause sequence {sequence_id}"


def goto_cue(sequence_id: int, cue_id: int) -> str:
    """
    Construct a command to jump to a specific cue.

    Args:
        sequence_id: Sequence number
        cue_id: Cue number

    Returns:
        str: MA command to jump to a cue
    """
    return f"goto cue {cue_id} sequence {sequence_id}"
