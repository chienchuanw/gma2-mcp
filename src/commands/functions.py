"""
Function Keywords for grandMA2 Command Builder

Function keywords are the "verbs" of the console. They perform a task or
function and are often followed by objects to which the function applies.
Some functions are global and do not need to be followed by objects.

Examples: Store, Delete, Copy, Goto, Clear, Label, SelFix, Go, Pause
"""

from typing import Any, List, Optional, Tuple, Union

from .constants import PRESET_TYPES
from .helpers import _build_store_options
from .objects import group, preset


# ============================================================================
# STORE FUNCTION KEYWORD
# ============================================================================


def store(
    object_type: str,
    object_id: Union[int, str],
    name: Optional[str] = None,
    **options: Any,
) -> str:
    """
    Construct a generic store command for any object type.

    Args:
        object_type: The type of object to store (e.g., "macro", "effect")
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
    merge: bool = False,
    overwrite: bool = False,
    remove: bool = False,
    noconfirm: bool = False,
    trackingshield: bool = False,
    cueonly: Optional[bool] = None,
    tracking: Optional[bool] = None,
    keepactive: Optional[bool] = None,
    addnewcontent: Optional[bool] = None,
    originalcontent: Optional[bool] = None,
    effects: Optional[bool] = None,
    values: Optional[bool] = None,
    valuetimes: Optional[bool] = None,
    source: Optional[str] = None,
    useselection: Optional[str] = None,
) -> str:
    """
    Construct a store cue command with full option support.

    Args:
        cue_id: The cue number to store
        end: End cue number for range (cue_id thru end)
        ranges: List of (start, end) tuples for multiple ranges
        name: Optional name for the cue
        merge: Merge new values into existing
        overwrite: Remove stored values and store new values
        remove: Remove stored values for attributes with active values
        noconfirm: Suppress store confirmation pop-up
        trackingshield: Use tracking shield for store
        cueonly: Prevent changes to track forward (True/False)
        tracking: Store with tracking
        keepactive: Keep values active after store
        addnewcontent: Add new content
        originalcontent: Store original content
        effects: Filter or enable effect layer
        values: Filter or enable value layer
        valuetimes: Filter or enable value times layer
        source: Data source (Prog, Output, DmxIn)
        useselection: Selection mode

    Returns:
        str: MA command to store cue(s)

    Examples:
        >>> store_cue(7)
        'store cue 7'
        >>> store_cue(1, end=10)
        'store cue 1 thru 10'
        >>> store_cue(ranges=[(1, 10), (20, 30)])
        'store cue 1 thru 10 + 20 thru 30'
    """
    if ranges:
        range_parts = [f"{start} thru {end}" for start, end in ranges]
        cue_part = " + ".join(range_parts)
    elif cue_id is not None and end is not None:
        cue_part = f"{cue_id} thru {end}"
    elif cue_id is not None:
        cue_part = str(cue_id)
    else:
        raise ValueError("Must provide cue_id or ranges")

    cmd = f"store cue {cue_part}"

    if name:
        cmd += f' "{name}"'

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


def store_group(group_id: int) -> str:
    """
    Construct a command to store a group.

    Args:
        group_id: Group number

    Returns:
        str: MA command to store a group
    """
    return f"store group {group_id}"


def store_preset(
    preset_type: str,
    preset_id: int,
    *,
    global_scope: bool = False,
    selective: bool = False,
    universal: bool = False,
    auto: bool = False,
    embedded: bool = False,
    noconfirm: bool = False,
    merge: bool = False,
    overwrite: bool = False,
    presetfilter: Optional[bool] = None,
    keepactive: Optional[bool] = None,
    addnewcontent: Optional[bool] = None,
    originalcontent: Optional[bool] = None,
) -> str:
    """
    Construct a command to store a preset with full option support.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, etc.)
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
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    cmd = f"store preset {type_num}.{preset_id}"

    cmd += _build_store_options(
        **{"global": global_scope},
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


# ============================================================================
# SELFIX FUNCTION KEYWORD
# ============================================================================


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

    Args:
        ids: Fixture number(s), single int or list
        end: Ending number (for range selection)
        start: Starting number (for keyword argument form)
        thru_all: If True, select from start to the end
        select_all: If True, select all fixtures

    Returns:
        str: MA command string

    Examples:
        >>> select_fixture(1)
        'selfix fixture 1'
        >>> select_fixture([1, 3, 5])
        'selfix fixture 1 + 3 + 5'
        >>> select_fixture(1, 10)
        'selfix fixture 1 thru 10'
    """
    if select_all:
        return "selfix fixture thru"

    if ids is None and start is None and end is not None:
        return f"selfix fixture thru {end}"

    if thru_all and start is not None:
        return f"selfix fixture {start} thru"

    actual_start: Optional[int] = None

    if ids is not None:
        if isinstance(ids, list):
            if len(ids) == 1:
                return f"selfix fixture {ids[0]}"
            fixtures_str = " + ".join(str(id) for id in ids)
            return f"selfix fixture {fixtures_str}"
        else:
            actual_start = ids
    elif start is not None:
        actual_start = start

    if actual_start is not None and end is not None:
        if actual_start == end:
            return f"selfix fixture {actual_start}"
        return f"selfix fixture {actual_start} thru {end}"

    if actual_start is not None:
        return f"selfix fixture {actual_start}"

    raise ValueError("Must provide at least one selection parameter")


# ============================================================================
# CLEAR FUNCTION KEYWORD
# ============================================================================


def clear() -> str:
    """
    Construct a Clear command.

    The Clear command has three sequential functions depending on programmer status:
    1. Clear selection (deselects all fixtures)
    2. Clear active values (deactivates all values)
    3. Clear all (empties programmer)

    Returns:
        str: MA command to clear
    """
    return "clear"


def clear_selection() -> str:
    """
    Construct a ClearSelection command to deselect all fixtures.

    Returns:
        str: MA command to clear selection
    """
    return "clearselection"


def clear_active() -> str:
    """
    Construct a ClearActive command to inactivate all values in programmer.

    Returns:
        str: MA command to clear active values
    """
    return "clearactive"


def clear_all() -> str:
    """
    Construct a ClearAll command to empty the entire programmer.

    Returns:
        str: MA command to clear all
    """
    return "clearall"


# ============================================================================
# LABEL FUNCTION KEYWORD
# ============================================================================


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


# ============================================================================
# DELETE FUNCTION KEYWORD
# ============================================================================


def delete_group(group_id: int) -> str:
    """
    Construct a command to delete a group.

    Args:
        group_id: Group number

    Returns:
        str: MA command to delete a group
    """
    return f"delete group {group_id}"


# ============================================================================
# GO / PAUSE / GOTO FUNCTION KEYWORDS
# ============================================================================


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


# ============================================================================
# AT FUNCTION KEYWORD
# ============================================================================
# At is unique: it can be both a Function Keyword and a Helping Keyword.
# - As a Function Keyword: applies values to the current selection
# - As a Helping Keyword: indicates destinations for other functions
#
# Note: The "@" character is different from "At" keyword.
# "@" is used as a placeholder for user input in macros.
# ============================================================================


def at(
    value: Optional[Union[int, float]] = None,
    *,
    cue: Optional[int] = None,
    sequence: Optional[int] = None,
    fade: Optional[float] = None,
    delay: Optional[float] = None,
    layer: Optional[str] = None,
    ignoreselection: bool = False,
    values: Optional[bool] = None,
    valuetimes: Optional[bool] = None,
    effects: Optional[bool] = None,
    disablecolortransform: bool = False,
    prefercolorwheel: bool = False,
    prefermixcolor: bool = False,
    prefercolorboth: bool = False,
    status: Optional[bool] = None,
) -> str:
    """
    Construct an At command to apply values to the current selection.

    At is "the exception that proves the rule" - it's one of the few
    functional keywords which accept objects before the function.

    Args:
        value: Percentage value (0-100) or absolute value
        cue: Cue ID to apply values from
        sequence: Sequence ID (used with cue parameter)
        fade: Fade time value (when used as value type)
        delay: Delay time value (when used as value type)
        layer: Destination layer
        ignoreselection: Ignore current selection
        values: Filter by value layer
        valuetimes: Filter by fade and delay layer
        effects: Filter by effect layers
        disablecolortransform: Disable color transformation
        prefercolorwheel: Prefer transforming colors to color wheel
        prefermixcolor: Prefer transforming color to MIXColor
        prefercolorboth: Prefer transforming color to both MIXColor and color wheel
        status: At with tracking values

    Returns:
        str: MA command to apply values

    Examples:
        >>> at(75)
        'at 75'
        >>> at(cue=3)
        'at cue 3'
        >>> at(cue=3, sequence=1)
        'at cue 3 sequence 1'
        >>> at(fade=2)
        'at fade 2'
        >>> at(delay=2)
        'at delay 2'
    """
    parts = ["at"]

    # Value type (Fade or Delay)
    if fade is not None:
        parts.append(f"fade {fade}")
    elif delay is not None:
        parts.append(f"delay {delay}")
    # Cue reference
    elif cue is not None:
        parts.append(f"cue {cue}")
        if sequence is not None:
            parts.append(f"sequence {sequence}")
    # Direct value
    elif value is not None:
        parts.append(str(value))
    else:
        raise ValueError("Must provide value, cue, fade, or delay")

    # Options
    options = []
    if layer is not None:
        options.append(f"/layer={layer}")
    if ignoreselection:
        options.append("/ignoreselection")
    if values is not None:
        options.append(f"/values={'true' if values else 'false'}")
    if valuetimes is not None:
        options.append(f"/valuetimes={'true' if valuetimes else 'false'}")
    if effects is not None:
        options.append(f"/effects={'true' if effects else 'false'}")
    if disablecolortransform:
        options.append("/disablecolortransform")
    if prefercolorwheel:
        options.append("/prefercolorwheel")
    if prefermixcolor:
        options.append("/prefermixcolor")
    if prefercolorboth:
        options.append("/prefercolorboth")
    if status is not None:
        options.append(f"/status={'true' if status else 'false'}")

    if options:
        parts.append(" ".join(options))

    return " ".join(parts)


def at_full() -> str:
    """
    Set current selection to full (100%).

    Returns:
        str: MA command "at full"

    Example:
        >>> at_full()
        'at full'
    """
    return "at full"


def at_zero() -> str:
    """
    Set current selection to zero (0%).

    Returns:
        str: MA command "at 0"

    Example:
        >>> at_zero()
        'at 0'
    """
    return "at 0"


def attribute_at(
    attribute: str,
    value: Union[int, float],
) -> str:
    """
    Set a specific attribute to a value.

    Args:
        attribute: Attribute name (e.g., "Pan", "Tilt", "Dimmer")
        value: Value to set

    Returns:
        str: MA command to set attribute

    Example:
        >>> attribute_at("Pan", 20)
        'attribute "Pan" at 20'
        >>> attribute_at("Tilt", 50)
        'attribute "Tilt" at 50'
    """
    return f'attribute "{attribute}" at {value}'


def fixture_at(
    fixture_id: int,
    value: Optional[Union[int, float]] = None,
    *,
    source_fixture: Optional[int] = None,
    end: Optional[int] = None,
) -> str:
    """
    Set fixture(s) to a value or copy values from another fixture.

    When using value, sets the fixture to that percentage.
    When using source_fixture, copies all values from the source.

    Args:
        fixture_id: Fixture ID to modify
        value: Percentage or value to set
        source_fixture: Source fixture ID to copy values from
        end: End fixture ID for range

    Returns:
        str: MA command to set fixture values

    Examples:
        >>> fixture_at(2, 50)
        'fixture 2 at 50'
        >>> fixture_at(2, source_fixture=3)
        'fixture 2 at fixture 3'
        >>> fixture_at(1, 100, end=10)
        'fixture 1 thru 10 at 100'
    """
    if value is None and source_fixture is None:
        raise ValueError("Must provide either value or source_fixture")

    if end is not None:
        fixture_part = f"fixture {fixture_id} thru {end}"
    else:
        fixture_part = f"fixture {fixture_id}"

    if source_fixture is not None:
        return f"{fixture_part} at fixture {source_fixture}"

    return f"{fixture_part} at {value}"


def channel_at(
    channel_id: int,
    value: Optional[Union[int, float]] = None,
    *,
    source_channel: Optional[int] = None,
    end: Optional[int] = None,
) -> str:
    """
    Set channel(s) to a value or copy values from another channel.

    Args:
        channel_id: Channel ID to modify
        value: Percentage or value to set
        source_channel: Source channel ID to copy values from
        end: End channel ID for range

    Returns:
        str: MA command to set channel values

    Examples:
        >>> channel_at(1, 75)
        'channel 1 at 75'
        >>> channel_at(1, source_channel=10)
        'channel 1 at channel 10'
        >>> channel_at(1, 100, end=10)
        'channel 1 thru 10 at 100'
    """
    if value is None and source_channel is None:
        raise ValueError("Must provide either value or source_channel")

    if end is not None:
        channel_part = f"channel {channel_id} thru {end}"
    else:
        channel_part = f"channel {channel_id}"

    if source_channel is not None:
        return f"{channel_part} at channel {source_channel}"

    return f"{channel_part} at {value}"


def group_at(
    group_id: int,
    value: Union[int, float],
) -> str:
    """
    Select group and set to a value.

    Args:
        group_id: Group ID
        value: Percentage or value to set

    Returns:
        str: MA command to set group value

    Example:
        >>> group_at(3, 50)
        'group 3 at 50'
    """
    return f"group {group_id} at {value}"


def executor_at(
    executor_id: int,
    value: Union[int, float],
) -> str:
    """
    Set executor fader to a value.

    Args:
        executor_id: Executor ID
        value: Fader value (0-100)

    Returns:
        str: MA command to set executor fader

    Example:
        >>> executor_at(3, 50)
        'executor 3 at 50'
    """
    return f"executor {executor_id} at {value}"


def preset_type_at(
    start_type: int,
    value: Union[int, float],
    *,
    end_type: Optional[int] = None,
    fade: Optional[float] = None,
    delay: Optional[float] = None,
) -> str:
    """
    Apply value/time to preset type range.

    Args:
        start_type: Start preset type ID
        value: Value to apply (or time if fade/delay specified)
        end_type: End preset type ID for range
        fade: If set, apply as fade time
        delay: If set, apply as delay time

    Returns:
        str: MA command for preset type at

    Examples:
        >>> preset_type_at(2, 50, end_type=9)
        'presettype 2 thru 9 at 50'
        >>> preset_type_at(2, 2, end_type=9, delay=True)
        'presettype 2 thru 9 at delay 2'
    """
    if end_type is not None:
        type_part = f"presettype {start_type} thru {end_type}"
    else:
        type_part = f"presettype {start_type}"

    if fade is not None:
        return f"{type_part} at fade {fade}"
    elif delay is not None:
        return f"{type_part} at delay {delay}"

    return f"{type_part} at {value}"


# ============================================================================
# MACRO PLACEHOLDER (@ Character)
# ============================================================================
# The @ character is used in macros as a placeholder for user input.
# This is completely different from the "At" keyword.
# - @ at the end: user input comes after the command
# - @ at the start: user input comes before the command (CLI must be disabled)
# ============================================================================


def macro_with_input_after(command: str) -> str:
    """
    Create a macro line with user input placeholder at the end.

    The @ at the end means the user will provide input after
    executing the macro.

    Args:
        command: The command prefix before user input

    Returns:
        str: Macro line with @ placeholder at the end

    Examples:
        >>> macro_with_input_after("Load")
        'Load @'
        >>> macro_with_input_after("Attribute Pan At")
        'Attribute Pan At @'
    """
    return f"{command} @"


def macro_with_input_before(command: str) -> str:
    """
    Create a macro line with user input placeholder at the beginning.

    The @ at the beginning means the user's previous command line
    input will be prepended. Note: CLI must be disabled for this to work.

    Args:
        command: The command suffix after user input

    Returns:
        str: Macro line with @ placeholder at the beginning

    Examples:
        >>> macro_with_input_before("Fade 20")
        '@ Fade 20'
    """
    return f"@ {command}"


# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# Alias: select_group -> group (for backward compatibility)
select_group = group

# Alias: call_preset -> preset (for backward compatibility)
call_preset = preset
