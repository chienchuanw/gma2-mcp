"""
Command Builder Module

This module provides high-level functions to construct grandMA2 command strings.
These functions are responsible only for generating correctly formatted commands,
not for sending them.

According to coding-standards.md, these functions are "thin wrappers" that
only construct MA commands without any Telnet logic.
"""

from typing import Optional, Union, List

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


def select_fixture(
    ids: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
    *,
    start: Optional[int] = None,
    thru_all: bool = False,
    select_all: bool = False,
) -> str:
    """
    Construct an MA command to select fixtures.

    According to grandMA2 official documentation, the SelFix keyword is used to
    create fixture selections in the programmer. Supports multiple selection modes:
    single, multiple, range, from beginning, to end, and select all.

    Args:
        ids: Fixture number(s), can be:
             - Single integer: select a single fixture
             - List of integers: select multiple non-contiguous fixtures (joined with +)
        end: Ending number (for range selection)
        start: Starting number (for keyword argument form)
        thru_all: If True, select from start to the end (Fixture X Thru)
        select_all: If True, select all fixtures (Fixture Thru)

    Returns:
        str: MA command string

    Examples:
        Single fixture:
        >>> select_fixture(1)
        'selfix fixture 1'

        Multiple fixtures:
        >>> select_fixture([1, 3, 5])
        'selfix fixture 1 + 3 + 5'

        Range selection:
        >>> select_fixture(1, 10)
        'selfix fixture 1 thru 10'

        From beginning to X:
        >>> select_fixture(end=10)
        'selfix fixture thru 10'

        From X to end:
        >>> select_fixture(start=5, thru_all=True)
        'selfix fixture 5 thru'

        Select all:
        >>> select_fixture(select_all=True)
        'selfix fixture thru'
    """
    # Case 1: Select all fixtures (Fixture Thru)
    if select_all:
        return "selfix fixture thru"

    # Case 2: Select from beginning to specified number (Fixture Thru X)
    if ids is None and start is None and end is not None:
        return f"selfix fixture thru {end}"

    # Case 3: Select from specified number to end (Fixture X Thru)
    if thru_all and start is not None:
        return f"selfix fixture {start} thru"

    # Handle ids parameter (can be int or list)
    actual_start: Optional[int] = None

    if ids is not None:
        # If it's a list
        if isinstance(ids, list):
            if len(ids) == 1:
                # Single element list, equivalent to selecting a single fixture
                return f"selfix fixture {ids[0]}"
            # Multiple fixtures, joined with +
            fixtures_str = " + ".join(str(id) for id in ids)
            return f"selfix fixture {fixtures_str}"
        else:
            # Single integer
            actual_start = ids
    elif start is not None:
        actual_start = start

    # Case 4: Range selection (Fixture X Thru Y)
    if actual_start is not None and end is not None:
        if actual_start == end:
            return f"selfix fixture {actual_start}"
        return f"selfix fixture {actual_start} thru {end}"

    # Case 5: Select a single fixture
    if actual_start is not None:
        return f"selfix fixture {actual_start}"

    # Default case (should not reach here)
    raise ValueError("Must provide at least one selection parameter")


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
