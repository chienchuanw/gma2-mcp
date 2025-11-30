"""
Command Builder Module

This module provides high-level functions to construct grandMA2 command strings.
These functions are responsible only for generating correctly formatted commands,
not for sending them.

According to coding-standards.md, these functions are "thin wrappers" that
only construct MA commands without any Telnet logic.
"""

from typing import Optional, Union, List, Tuple, Dict, Any

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

# Store options that require no value (flag-only options)
STORE_FLAG_OPTIONS = {
    "merge",
    "overwrite",
    "remove",
    "noconfirm",
    "global",
    "selective",
    "universal",
    "auto",
    "trackingshield",
    "embedded",
}

# Store options that require a boolean value
STORE_BOOL_OPTIONS = {
    "cueonly",
    "tracking",
    "keepactive",
    "presetfilter",
    "addnewcontent",
    "originalcontent",
    "effects",
    "values",
    "valuetimes",
}

# Store options that require a specific value
STORE_VALUE_OPTIONS = {
    "source",  # Prog, Output, DmxIn
    "useselection",  # Active, Allforselected, Activeforselected, All, Look
    "screen",  # 1..6
    "x",  # x coordinate
    "y",  # y coordinate
}


def _build_store_options(**kwargs: Any) -> str:
    """
    Build option string for store commands.

    Handles three types of options:
    1. Flag options (no value): /merge, /overwrite, /noconfirm
    2. Boolean options: /cueonly=true, /tracking=false
    3. Value options: /source=output, /screen=1

    Args:
        **kwargs: Option name-value pairs

    Returns:
        str: Formatted option string (e.g., " /merge /cueonly=true")
    """
    options_parts = []

    for key, value in kwargs.items():
        if value is None:
            continue

        # Normalize key (remove underscores, convert to lowercase)
        option_key = key.replace("_", "").lower()

        # Handle flag options (no value needed)
        if option_key in STORE_FLAG_OPTIONS:
            if value:  # Only add if True
                options_parts.append(f"/{option_key}")

        # Handle boolean options (need =true or =false)
        elif option_key in STORE_BOOL_OPTIONS:
            bool_value = "true" if value else "false"
            options_parts.append(f"/{option_key}={bool_value}")

        # Handle value options
        elif option_key in STORE_VALUE_OPTIONS:
            options_parts.append(f"/{option_key}={value}")

    if options_parts:
        return " " + " ".join(options_parts)
    return ""


# ============================================================
# Store commands (general)
# ============================================================


def store(
    object_type: str,
    object_id: Union[int, str],
    name: Optional[str] = None,
    **options: Any,
) -> str:
    """
    Construct a generic store command for any object type.

    This function provides a flexible way to store any grandMA2 object type
    with optional naming and store options.

    Args:
        object_type: The type of object to store (e.g., "macro", "effect", "view")
        object_id: The ID or identifier of the object
        name: Optional name for the stored object
        **options: Store options (merge, overwrite, noconfirm, etc.)

    Returns:
        str: MA command to store the object

    Examples:
        >>> store("macro", 5)
        'store macro 5'
        >>> store("macro", 5, name="Reset All")
        'store macro 5 "Reset All"'
        >>> store("effect", 1, noconfirm=True)
        'store effect 1 /noconfirm'
    """
    cmd = f"store {object_type} {object_id}"

    if name:
        cmd += f' "{name}"'

    cmd += _build_store_options(**options)

    return cmd


def store_cue(
    cue_id: Optional[int] = None,
    end: Optional[int] = None,
    *,
    ranges: Optional[List[Tuple[int, int]]] = None,
    name: Optional[str] = None,
    # Flag options (no value)
    merge: bool = False,
    overwrite: bool = False,
    remove: bool = False,
    noconfirm: bool = False,
    trackingshield: bool = False,
    # Boolean options
    cueonly: Optional[bool] = None,
    tracking: Optional[bool] = None,
    keepactive: Optional[bool] = None,
    addnewcontent: Optional[bool] = None,
    originalcontent: Optional[bool] = None,
    effects: Optional[bool] = None,
    values: Optional[bool] = None,
    valuetimes: Optional[bool] = None,
    # Value options
    source: Optional[str] = None,
    useselection: Optional[str] = None,
) -> str:
    """
    Construct a store cue command with full option support.

    The Store keyword stores functions in the show file. When no object type
    is specified, Cue is the default for the sequence of the selected executor.

    Args:
        cue_id: The cue number to store
        end: End cue number for range (cue_id thru end)
        ranges: List of (start, end) tuples for multiple ranges
        name: Optional name for the cue
        merge: Merge new values into existing (new values have priority)
        overwrite: Remove stored values and store new values
        remove: Remove stored values for attributes with active programmer values
        noconfirm: Suppress store confirmation pop-up
        trackingshield: Use tracking shield for store
        cueonly: Prevent changes to track forward (True/False)
        tracking: Store with tracking (False is same as cueonly)
        keepactive: Keep values active after store
        addnewcontent: Add new content (False is same as originalcontent)
        originalcontent: Store original content of preset/effect/cue
        effects: Filter or enable effect layer
        values: Filter or enable value layer
        valuetimes: Filter or enable value times layer
        source: Data source (Prog, Output, DmxIn)
        useselection: Selection mode (Active, Allforselected, Activeforselected, All, Look)

    Returns:
        str: MA command to store cue(s)

    Examples:
        >>> store_cue(7)
        'store cue 7'
        >>> store_cue(1, end=10)
        'store cue 1 thru 10'
        >>> store_cue(ranges=[(1, 10), (20, 30)])
        'store cue 1 thru 10 + 20 thru 30'
        >>> store_cue(1, merge=True, noconfirm=True)
        'store cue 1 /merge /noconfirm'
    """
    # Build the cue identifier part
    if ranges:
        # Multiple ranges: "1 thru 10 + 20 thru 30"
        range_parts = [f"{start} thru {end}" for start, end in ranges]
        cue_part = " + ".join(range_parts)
    elif cue_id is not None and end is not None:
        # Single range: "1 thru 10"
        cue_part = f"{cue_id} thru {end}"
    elif cue_id is not None:
        # Single cue
        cue_part = str(cue_id)
    else:
        raise ValueError("Must provide cue_id or ranges")

    cmd = f"store cue {cue_part}"

    if name:
        cmd += f' "{name}"'

    # Build options
    cmd += _build_store_options(
        merge=merge,
        overwrite=overwrite,
        remove=remove,
        noconfirm=noconfirm,
        trackingshield=trackingshield,
        cueonly=cueonly,
        tracking=tracking,
        keepactive=keepactive,
        addnewcontent=addnewcontent,
        originalcontent=originalcontent,
        effects=effects,
        values=values,
        valuetimes=valuetimes,
        source=source,
        useselection=useselection,
    )

    return cmd


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


def clear() -> str:
    """
    Construct a Clear command.

    The Clear command has three sequential functions depending on programmer status:
    1. Clear selection (deselects all fixtures)
    2. Clear active values (deactivates all values)
    3. Clear all (empties programmer)

    Returns:
        str: MA command to clear

    Example:
        >>> clear()
        'clear'
    """
    return "clear"


def clear_selection() -> str:
    """
    Construct a ClearSelection command to deselect all fixtures.

    This function clears the selection without affecting active values
    or other programmer content. Equivalent to pressing Clear once.

    Returns:
        str: MA command to clear selection

    Example:
        >>> clear_selection()
        'clearselection'
    """
    return "clearselection"


def clear_active() -> str:
    """
    Construct a ClearActive command to inactivate all values in programmer.

    This function deactivates any active values in the programmer without
    clearing the selection or emptying the programmer.
    Equivalent to pressing Clear twice.

    Returns:
        str: MA command to clear active values

    Example:
        >>> clear_active()
        'clearactive'
    """
    return "clearactive"


def clear_all() -> str:
    """
    Construct a ClearAll command to empty the entire programmer.

    This function clears the selection and discards all values in the programmer.
    Equivalent to pressing Clear for slightly over two seconds.

    Returns:
        str: MA command to clear all

    Example:
        >>> clear_all()
        'clearall'
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


def store_preset(
    preset_type: str,
    preset_id: int,
    *,
    # Scope options (flag-only)
    global_scope: bool = False,
    selective: bool = False,
    universal: bool = False,
    auto: bool = False,
    # Other flag options
    embedded: bool = False,
    noconfirm: bool = False,
    merge: bool = False,
    overwrite: bool = False,
    # Boolean options
    presetfilter: Optional[bool] = None,
    keepactive: Optional[bool] = None,
    addnewcontent: Optional[bool] = None,
    originalcontent: Optional[bool] = None,
) -> str:
    """
    Construct a command to store a preset with full option support.

    Supports preset scope options (global, selective, universal) and
    various store modifiers.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, focus, control, shapers, video)
        preset_id: Preset number
        global_scope: Store preset with global values
        selective: Store preset with selective values
        universal: Store preset with universal values
        auto: Store preset values with default preset scope
        embedded: Create embedded preset
        noconfirm: Suppress store confirmation pop-up
        merge: Merge new values into existing
        overwrite: Remove stored values and store new
        presetfilter: Set preset filter on or off
        keepactive: Keep values active
        addnewcontent: Add new content
        originalcontent: Store original content

    Returns:
        str: MA command to store a preset

    Examples:
        >>> store_preset("dimmer", 3)
        'store preset 1.3'
        >>> store_preset("dimmer", 3, global_scope=True)
        'store preset 1.3 /global'
        >>> store_preset("dimmer", 3, presetfilter=False, keepactive=True)
        'store preset 1.3 /presetfilter=false /keepactive=true'
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    cmd = f"store preset {type_num}.{preset_id}"

    # Build options using the helper, mapping global_scope to global
    cmd += _build_store_options(
        **{"global": global_scope},  # 'global' is a Python keyword, so use dict
        selective=selective,
        universal=universal,
        auto=auto,
        embedded=embedded,
        noconfirm=noconfirm,
        merge=merge,
        overwrite=overwrite,
        presetfilter=presetfilter,
        keepactive=keepactive,
        addnewcontent=addnewcontent,
        originalcontent=originalcontent,
    )

    return cmd


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
