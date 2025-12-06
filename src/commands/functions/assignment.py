"""
Assign Function Keywords for grandMA2 Command Builder

Assign is used to define relationships between objects or assign values to properties.
This is a versatile keyword with many use cases:
- Assign objects to Executor, Layout
- Assign DMX addresses to Fixture/Channel
- Assign functions (Go, Toggle, etc.) to Executor buttons
- Assign properties to objects

Included functions:
- assign: Generic assign command
- assign_function: Assign function to object
- assign_fade: Assign fade time to cue
- assign_to_layout: Assign object to layout
"""

from typing import List, Optional, Union


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
    # Build source part
    if isinstance(source_id, list):
        source = " + ".join(str(i) for i in source_id)
        cmd = f"assign {source_type} {source}"
    elif source_end is not None:
        cmd = f"assign {source_type} {source_id} thru {source_end}"
    else:
        cmd = f"assign {source_type} {source_id}"

    # Build target part (if provided)
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

    # Build options
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
