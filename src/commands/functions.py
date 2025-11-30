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
# COPY FUNCTION KEYWORD
# ============================================================================


def copy(
    object_type: str,
    object_id: Union[int, List[int]],
    target: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    target_end: Optional[int] = None,
    overwrite: bool = False,
    merge: bool = False,
    status: Optional[bool] = None,
    cueonly: Optional[bool] = None,
    noconfirm: bool = False,
) -> str:
    """
    Construct a Copy command to create copies of objects.

    If no target is given, the object will be exported to clipboard.xml
    for use with the Paste keyword.

    Args:
        object_type: Type of object (e.g., "group", "macro", "cue")
        object_id: Object ID or list of IDs to copy
        target: Target ID or list of target IDs (None = export to clipboard)
        end: End ID for source range (object_id thru end)
        target_end: End ID for target range (target thru target_end)
        overwrite: Replace existing content
        merge: Add to existing content
        status: Add tracking status to existing content
        cueonly: Prevent changes to track forward
        noconfirm: Suppress confirmation pop-up

    Returns:
        str: MA command to copy object(s)

    Examples:
        >>> copy("group", 1, 5)
        'copy group 1 at 5'
        >>> copy("group", 1, end=3, target=11)
        'copy group 1 thru 3 at 11'
        >>> copy("group", 2, target=6, target_end=8)
        'copy group 2 at 6 thru 8'
        >>> copy("macro", 2, 6)
        'copy macro 2 at 6'
        >>> copy("cue", 5)
        'copy cue 5'
    """
    # Build source part
    if isinstance(object_id, list):
        source = " + ".join(str(i) for i in object_id)
        cmd = f"copy {object_type} {source}"
    elif end is not None:
        cmd = f"copy {object_type} {object_id} thru {end}"
    else:
        cmd = f"copy {object_type} {object_id}"

    # Build target part (if provided)
    if target is not None:
        if isinstance(target, list):
            target_str = " + ".join(str(t) for t in target)
            cmd += f" at {target_str}"
        elif target_end is not None:
            cmd += f" at {target} thru {target_end}"
        else:
            cmd += f" at {target}"

    # Build options
    options = []
    if overwrite:
        options.append("/overwrite")
    if merge:
        options.append("/merge")
    if status is not None:
        options.append(f"/status={'true' if status else 'false'}")
    if cueonly is not None:
        options.append(f"/cueonly={'true' if cueonly else 'false'}")
    if noconfirm:
        options.append("/noconfirm")

    if options:
        cmd += " " + " ".join(options)

    return cmd


def copy_cue(
    cue_id: int,
    target: Optional[int] = None,
    *,
    end: Optional[int] = None,
    target_end: Optional[int] = None,
    overwrite: bool = False,
    merge: bool = False,
    status: Optional[bool] = None,
    cueonly: Optional[bool] = None,
    noconfirm: bool = False,
) -> str:
    """
    Construct a Copy command specifically for cues.

    Cue is the default object type for Copy when no object type is specified.

    Args:
        cue_id: Cue ID to copy
        target: Target cue ID (None = export to clipboard)
        end: End ID for source range
        target_end: End ID for target range
        overwrite: Replace existing content
        merge: Add to existing content
        status: Add tracking status
        cueonly: Prevent changes to track forward
        noconfirm: Suppress confirmation pop-up

    Returns:
        str: MA command to copy cue(s)

    Examples:
        >>> copy_cue(2, 6)
        'copy cue 2 at 6'
        >>> copy_cue(5)
        'copy cue 5'
        >>> copy_cue(1, 10, end=5)
        'copy cue 1 thru 5 at 10'
    """
    return copy(
        "cue",
        cue_id,
        target,
        end=end,
        target_end=target_end,
        overwrite=overwrite,
        merge=merge,
        status=status,
        cueonly=cueonly,
        noconfirm=noconfirm,
    )


# ============================================================================
# MOVE FUNCTION KEYWORD
# ============================================================================


def move(
    object_type: str,
    object_id: Union[int, List[int]],
    target: Union[int, List[int]],
    *,
    end: Optional[int] = None,
    target_end: Optional[int] = None,
) -> str:
    """
    Construct a Move command to move objects and give them a new ID.

    If the destination is already taken, the moved object and the
    destination object will swap positions.

    Note: If the destination is a list, the number of elements in the
    destination list must be the same as in the source list.

    Args:
        object_type: Type of object (e.g., "group", "macro", "cue")
        object_id: Object ID or list of IDs to move
        target: Target ID or list of target IDs
        end: End ID for source range (object_id thru end)
        target_end: End ID for target range (target thru target_end)

    Returns:
        str: MA command to move object(s)

    Examples:
        >>> move("group", 5, 9)
        'move group 5 at 9'
        >>> move("group", 1, 10, end=3)
        'move group 1 thru 3 at 10'
        >>> move("cue", 5, 1)
        'move cue 5 at 1'
        >>> move("preset", [1, 3, 5], [10, 12, 14])
        'move preset 1 + 3 + 5 at 10 + 12 + 14'
    """
    # Build source part
    if isinstance(object_id, list):
        source = " + ".join(str(i) for i in object_id)
        cmd = f"move {object_type} {source}"
    elif end is not None:
        cmd = f"move {object_type} {object_id} thru {end}"
    else:
        cmd = f"move {object_type} {object_id}"

    # Build target part
    if isinstance(target, list):
        target_str = " + ".join(str(t) for t in target)
        cmd += f" at {target_str}"
    elif target_end is not None:
        cmd += f" at {target} thru {target_end}"
    else:
        cmd += f" at {target}"

    return cmd


# ============================================================================
# ASSIGN FUNCTION KEYWORD
# ============================================================================
# Assign defines relationships between objects or gives values to properties.
# This is a versatile keyword with many use cases:
# - Assign objects to executors, layouts
# - Assign DMX addresses to fixtures/channels
# - Assign functions (Go, Toggle, etc.) to executor buttons
# - Assign properties to objects
# ============================================================================


def assign(
    source_type: str,
    source_id: Union[int, str, List[int]],
    target_type: Optional[str] = None,
    target_id: Optional[Union[int, str, List[int]]] = None,
    *,
    source_end: Optional[int] = None,
    target_end: Optional[int] = None,
    break_: Optional[int] = None,
    multipatch: Optional[int] = None,
    reset: bool = False,
    x: Optional[int] = None,
    y: Optional[int] = None,
    noconfirm: bool = False,
    special: Optional[str] = None,
    cue_mode: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Construct an Assign command to define relationships between objects.

    Args:
        source_type: Type of source object (e.g., "sequence", "group", "dmx")
        source_id: Source object ID (can be compound like "2.101" for DMX)
        target_type: Target object type (e.g., "executor", "channel", "layout")
        target_id: Target object ID
        source_end: End ID for source range
        target_end: End ID for target range
        break_: Patch break value (1-8)
        multipatch: Multipatch slot (0-10000)
        reset: Remove existing patch
        x: X-coordinate for layout (-10000 to +10000)
        y: Y-coordinate for layout (-10000 to +10000)
        noconfirm: Suppress confirmation popup
        special: Preset special mode (normal, default, highlight)
        cue_mode: Cue mode (assert, xassert, break, xbreak, release)
        password: Password value for user assignment

    Returns:
        str: MA command for assign operation

    Examples:
        >>> assign("sequence", 1, "executor", 6, source_end=5, target_end=10)
        'assign sequence 1 thru 5 at executor 6 thru 10'
        >>> assign("dmx", "2.101", "channel", 5)
        'assign dmx 2.101 at channel 5'
        >>> assign("group", 1, "layout", 1, x=5, y=2)
        'assign group 1 at layout 1 /x=5 /y=2'
    """
    # 建立 source 部分
    if isinstance(source_id, list):
        source = " + ".join(str(i) for i in source_id)
        cmd = f"assign {source_type} {source}"
    elif source_end is not None:
        cmd = f"assign {source_type} {source_id} thru {source_end}"
    else:
        cmd = f"assign {source_type} {source_id}"

    # 建立 target 部分（如果有）
    if target_type is not None and target_id is not None:
        if isinstance(target_id, list):
            target_str = " + ".join(str(t) for t in target_id)
            cmd += f" at {target_type} {target_str}"
        elif target_end is not None:
            cmd += f" at {target_type} {target_id} thru {target_end}"
        else:
            cmd += f" at {target_type} {target_id}"
    elif target_type is not None:
        cmd += f" {target_type}"

    # 建立選項
    options = []
    if break_ is not None:
        options.append(f"/break={break_}")
    if multipatch is not None:
        options.append(f"/multipatch={multipatch}")
    if reset:
        options.append("/reset")
    if x is not None:
        options.append(f"/x={x}")
    if y is not None:
        options.append(f"/y={y}")
    if noconfirm:
        options.append("/noconfirm")
    if special is not None:
        options.append(f"/special={special}")
    if cue_mode is not None:
        options.append(f"/cue_mode={cue_mode}")
    if password is not None:
        options.append(f'/password="{password}"')

    if options:
        cmd += " " + " ".join(options)

    return cmd


def assign_function(
    function: str,
    target_type: str,
    target_id: Union[int, str],
    *,
    cue_mode: Optional[str] = None,
) -> str:
    """
    Assign a function (Go, Toggle, etc.) to an object.

    Args:
        function: Function name (e.g., "Toggle", "Go", "Pause")
        target_type: Target type (e.g., "executor", "execbutton1")
        target_id: Target ID
        cue_mode: Cue mode (assert, xassert, break, xbreak, release)

    Returns:
        str: MA command to assign function

    Examples:
        >>> assign_function("Toggle", "executor", 101)
        'assign toggle at executor 101'
        >>> assign_function("Go", "execbutton1", "1.1", cue_mode="xassert")
        'assign go at execbutton1 1.1 /cue_mode=xassert'
    """
    cmd = f"assign {function.lower()} at {target_type} {target_id}"
    if cue_mode is not None:
        cmd += f" /cue_mode={cue_mode}"
    return cmd


def assign_fade(
    fade_time: float,
    cue_id: int,
    *,
    sequence_id: Optional[int] = None,
) -> str:
    """
    Assign fade time to a cue.

    Args:
        fade_time: Fade time in seconds
        cue_id: Cue ID
        sequence_id: Sequence ID (optional, uses selected executor if not given)

    Returns:
        str: MA command to assign fade time

    Examples:
        >>> assign_fade(3, 5)
        'assign fade 3 cue 5'
        >>> assign_fade(2.5, 3, sequence_id=1)
        'assign fade 2.5 cue 3 sequence 1'
    """
    cmd = f"assign fade {fade_time} cue {cue_id}"
    if sequence_id is not None:
        cmd += f" sequence {sequence_id}"
    return cmd


def assign_to_layout(
    object_type: str,
    object_id: Union[int, List[int]],
    layout_id: int,
    *,
    x: Optional[int] = None,
    y: Optional[int] = None,
    end: Optional[int] = None,
) -> str:
    """
    Assign an object to a layout at a specific position.

    Args:
        object_type: Type of object (e.g., "group", "macro")
        object_id: Object ID or list of IDs
        layout_id: Layout ID
        x: X-coordinate (-10000 to +10000)
        y: Y-coordinate (-10000 to +10000)
        end: End ID for range

    Returns:
        str: MA command to assign to layout

    Examples:
        >>> assign_to_layout("group", 1, 1, x=5, y=2)
        'assign group 1 at layout 1 /x=5 /y=2'
        >>> assign_to_layout("macro", 1, 2, x=0, y=0, end=5)
        'assign macro 1 thru 5 at layout 2 /x=0 /y=0'
    """
    return assign(object_type, object_id, "layout", layout_id, source_end=end, x=x, y=y)


# ============================================================================
# LABEL FUNCTION KEYWORD
# ============================================================================
# Label gives names to objects.
# Note: We already have label_group() and label_preset() - this is a generic version.
# If multiple objects are labeled with a numbered name, numbers will enumerate.
# ============================================================================


def label(
    object_type: str,
    object_id: Union[int, str, List[int]],
    name: str,
    *,
    end: Optional[int] = None,
) -> str:
    """
    Construct a Label command to give names to objects.

    If multiple objects are labeled and the name contains a number,
    the number will be automatically enumerated for each object.

    Args:
        object_type: Type of object (e.g., "fixture", "group", "preset")
        object_id: Object ID (can be compound like '"color"."Red"')
        name: Name to assign (in quotes)
        end: End ID for range labeling

    Returns:
        str: MA command to label object(s)

    Examples:
        >>> label("group", 3, "All Studiocolors")
        'label group 3 "All Studiocolors"'
        >>> label("fixture", 1, "Mac700 1", end=10)
        'label fixture 1 thru 10 "Mac700 1"'
        >>> label("preset", '"color"."Red"', "Dark Red")
        'label preset "color"."Red" "Dark Red"'
    """
    # 建立物件參照
    if isinstance(object_id, list):
        obj_str = " + ".join(str(i) for i in object_id)
        cmd = f"label {object_type} {obj_str}"
    elif end is not None:
        cmd = f"label {object_type} {object_id} thru {end}"
    else:
        cmd = f"label {object_type} {object_id}"

    # 加入名稱（確保有引號）
    if name.startswith('"') and name.endswith('"'):
        cmd += f" {name}"
    else:
        cmd += f' "{name}"'

    return cmd


# ============================================================================
# APPEARANCE FUNCTION KEYWORD
# ============================================================================
# Appearance changes frame colors of pool objects and background colors of cues.
# Can set colors via RGB (0-100), HSB (hue 0-360, sat/bright 0-100), or hex.
# Can also copy appearance from a source object.
# ============================================================================


def appearance(
    object_type: str,
    object_id: Union[int, str, List[int]],
    *,
    end: Optional[int] = None,
    source_type: Optional[str] = None,
    source_id: Optional[Union[int, str]] = None,
    reset: bool = False,
    color: Optional[str] = None,
    red: Optional[int] = None,
    green: Optional[int] = None,
    blue: Optional[int] = None,
    hue: Optional[int] = None,
    saturation: Optional[int] = None,
    brightness: Optional[int] = None,
) -> str:
    """
    Construct an Appearance command to change frame/background colors.

    Colors can be set via RGB (0-100), HSB (hue 0-360, sat/bright 0-100),
    hex color code, or by copying from a source object.

    Args:
        object_type: Type of object (e.g., "preset", "group", "cue", "macro")
        object_id: Object ID (can be compound like "0.1" for preset pool)
        end: End ID for range
        source_type: Source object type (for copying appearance)
        source_id: Source object ID (for copying appearance)
        reset: Reset appearance to default
        color: Hex color (000000-FFFFFF) or gel name
        red: Red component (0-100)
        green: Green component (0-100)
        blue: Blue component (0-100)
        hue: Hue (0-360)
        saturation: Saturation (0-100)
        brightness: Brightness (0-100)

    Returns:
        str: MA command for appearance

    Examples:
        >>> appearance("preset", "0.1", red=100, green=0, blue=0)
        'appearance preset 0.1 /r=100 /g=0 /b=0'
        >>> appearance("preset", "0.1", hue=0, saturation=100, brightness=50)
        'appearance preset 0.1 /h=0 /s=100 /br=50'
        >>> appearance("macro", 2, source_type="macro", source_id=13)
        'appearance macro 2 at macro 13'
        >>> appearance("group", 1, end=5, color="FF0000")
        'appearance group 1 thru 5 /color=FF0000'
    """
    # 建立物件參照
    if isinstance(object_id, list):
        obj_str = " + ".join(str(i) for i in object_id)
        cmd = f"appearance {object_type} {obj_str}"
    elif end is not None:
        cmd = f"appearance {object_type} {object_id} thru {end}"
    else:
        cmd = f"appearance {object_type} {object_id}"

    # 從來源物件複製外觀
    if source_type is not None and source_id is not None:
        cmd += f" at {source_type} {source_id}"
        return cmd

    # 建立選項
    options = []
    if reset:
        options.append("/reset")
    if color is not None:
        options.append(f"/color={color}")
    if red is not None:
        options.append(f"/r={red}")
    if green is not None:
        options.append(f"/g={green}")
    if blue is not None:
        options.append(f"/b={blue}")
    if hue is not None:
        options.append(f"/h={hue}")
    if saturation is not None:
        options.append(f"/s={saturation}")
    if brightness is not None:
        options.append(f"/br={brightness}")

    if options:
        cmd += " " + " ".join(options)

    return cmd


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
