"""
Object Keywords for grandMA2 Command Builder

Object keywords are the "nouns" of the console. They are used to allocate
objects in your show file. Usually used with numbers, IDs, names, and labels.

Examples: Fixture, Channel, Group, Preset, Cue, Sequence, Executor
"""

from typing import List, Optional, Union

from .constants import PRESET_TYPES


# ----------------------------------------------------------------------------
# Fixture Object Keyword
# ----------------------------------------------------------------------------


def fixture(
    fixture_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
    *,
    sub_id: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    Construct a Fixture command to access fixtures by Fixture ID.

    Fixture is an object keyword to access fixtures with a fixture ID.
    The default function is SelFix, meaning entering fixtures without
    any function specified will select them.

    Args:
        fixture_id: Fixture number or list of fixture numbers
        end: End fixture number for range selection
        sub_id: Sub-fixture ID (e.g., fixture 11.5 for 5th subfixture)
        select_all: If True, select all fixtures (fixture thru)

    Returns:
        str: MA command to select fixture(s)

    Examples:
        >>> fixture(34)
        'fixture 34'
        >>> fixture(11, sub_id=5)
        'fixture 11.5'
        >>> fixture(1, end=10)
        'fixture 1 thru 10'
        >>> fixture([1, 5, 10])
        'fixture 1 + 5 + 10'
        >>> fixture(select_all=True)
        'fixture thru'
    """
    if select_all:
        return "fixture thru"

    if fixture_id is None:
        raise ValueError("Must provide fixture_id or set select_all=True")

    if isinstance(fixture_id, list):
        if len(fixture_id) == 1:
            return f"fixture {fixture_id[0]}"
        fixtures_str = " + ".join(str(f) for f in fixture_id)
        return f"fixture {fixtures_str}"

    if sub_id is not None:
        return f"fixture {fixture_id}.{sub_id}"

    if end is not None:
        if fixture_id == end:
            return f"fixture {fixture_id}"
        return f"fixture {fixture_id} thru {end}"

    return f"fixture {fixture_id}"


# ----------------------------------------------------------------------------
# Channel Object Keyword
# ----------------------------------------------------------------------------


def channel(
    channel_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
    *,
    sub_id: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    Construct a Channel command to access fixtures by Channel ID.

    Channel is an object type used to access fixtures with a Channel ID.
    The default function is SelFix.

    Args:
        channel_id: Channel number or list of channel numbers
        end: End channel number for range selection
        sub_id: Sub-fixture ID
        select_all: If True, select all channels (channel thru)

    Returns:
        str: MA command to select channel(s)

    Examples:
        >>> channel(34)
        'channel 34'
        >>> channel(11, sub_id=5)
        'channel 11.5'
        >>> channel(1, end=10)
        'channel 1 thru 10'
    """
    if select_all:
        return "channel thru"

    if channel_id is None:
        raise ValueError("Must provide channel_id or set select_all=True")

    if isinstance(channel_id, list):
        if len(channel_id) == 1:
            return f"channel {channel_id[0]}"
        channels_str = " + ".join(str(c) for c in channel_id)
        return f"channel {channels_str}"

    if sub_id is not None:
        return f"channel {channel_id}.{sub_id}"

    if end is not None:
        return f"channel {channel_id} thru {end}"

    return f"channel {channel_id}"


# ----------------------------------------------------------------------------
# Group Object Keyword
# ----------------------------------------------------------------------------


def group(
    group_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
) -> str:
    """
    Construct a Group command to select a group.

    Group is an object type that contains a collection of fixtures
    and a selection sequence. The default function is SelFix.

    Args:
        group_id: Group number or list of group numbers
        end: End group number for range selection

    Returns:
        str: MA command to select group(s)

    Examples:
        >>> group(3)
        'group 3'
        >>> group(1, end=5)
        'group 1 thru 5'
        >>> group([1, 3, 5])
        'group 1 + 3 + 5'
    """
    if group_id is None:
        raise ValueError("Must provide group_id")

    if isinstance(group_id, list):
        if len(group_id) == 1:
            return f"group {group_id[0]}"
        groups_str = " + ".join(str(g) for g in group_id)
        return f"group {groups_str}"

    if end is not None:
        if group_id == end:
            return f"group {group_id}"
        return f"group {group_id} thru {end}"

    return f"group {group_id}"


# ----------------------------------------------------------------------------
# Preset Object Keyword
# ----------------------------------------------------------------------------


def preset(
    preset_type_or_id: Optional[Union[int, str]] = None,
    preset_id: Optional[Union[int, List[int]]] = None,
    *,
    name: Optional[str] = None,
    end: Optional[int] = None,
    wildcard: bool = False,
) -> str:
    """
    Construct a Preset command to select or apply a preset.

    Preset can be used for:
    - Selecting fixtures stored in a preset
    - Applying a preset to currently selected fixtures or channels

    If no fixtures/channels are selected, the default function is SelFix.
    If fixtures/channels are already selected, the default function is At.

    Args:
        preset_type_or_id: Preset type (string like "dimmer") or type number (integer)
                           or preset ID when only one parameter is provided
        preset_id: Preset number or list of numbers (for multiple selection)
        name: Preset name (when selecting by name)
        end: End number (for range selection)
        wildcard: Whether to use wildcard * (used with name)

    Returns:
        str: MA command string

    Examples:
        >>> preset(5)
        'preset 5'
        >>> preset("dimmer", 1)
        'preset 1.1'
        >>> preset(3, 2)
        'preset 3.2'
        >>> preset(name="DarkRed")
        'preset "DarkRed"'
        >>> preset(name="DarkRed", wildcard=True)
        'preset *."DarkRed"'
        >>> preset("color", name="Red")
        'preset "color"."Red"'
        >>> preset(1, 1, end=5)
        'preset 1.1 thru 5'
        >>> preset(1, [1, 3, 5])
        'preset 1.1 + 1.3 + 1.5'
    """
    # Case 1: Name only (optional wildcard)
    if name is not None and preset_type_or_id is None:
        if wildcard:
            return f'preset *."{name}"'
        return f'preset "{name}"'

    # Case 2: Type + name (e.g., preset "color"."Red")
    if name is not None and preset_type_or_id is not None:
        # Convert type to string representation
        if isinstance(preset_type_or_id, str):
            type_str = f'"{preset_type_or_id}"'
        else:
            type_str = str(preset_type_or_id)
        return f'preset {type_str}."{name}"'

    # Case 3: Preset ID only (e.g., preset 5)
    if preset_type_or_id is not None and preset_id is None:
        return f"preset {preset_type_or_id}"

    # Case 4: Type + ID (e.g., preset 3.2 or preset "dimmer".1)
    if preset_type_or_id is not None and preset_id is not None:
        # Get type number
        if isinstance(preset_type_or_id, str):
            type_num = PRESET_TYPES.get(preset_type_or_id.lower(), 1)
        else:
            type_num = preset_type_or_id

        # Handle multiple selection (list)
        if isinstance(preset_id, list):
            if len(preset_id) == 1:
                return f"preset {type_num}.{preset_id[0]}"
            presets_str = " + ".join(f"{type_num}.{pid}" for pid in preset_id)
            return f"preset {presets_str}"

        # Handle range selection
        if end is not None:
            return f"preset {type_num}.{preset_id} thru {end}"

        # Single selection
        return f"preset {type_num}.{preset_id}"

    raise ValueError("Must provide preset_type_or_id, preset_id, or name")


# ----------------------------------------------------------------------------
# PresetType Object Keyword
# ----------------------------------------------------------------------------


def preset_type(
    type_id: Optional[Union[int, str]] = None,
    *,
    name: Optional[str] = None,
    feature: Optional[int] = None,
    attribute: Optional[int] = None,
) -> str:
    """
    Construct a PresetType command to call or select a preset type.

    PresetType can be used for:
    - Calling PresetType in fixture sheet and preset type bar
    - Selecting Features and Attributes in PresetType
    - Enabling PresetType for selected fixtures

    Preset types contain features and attributes, which can be called
    using dot-separated numbers.

    Args:
        type_id: PresetType number (integer) or variable (e.g., "$preset")
        name: PresetType name (e.g., "Dimmer", "Color")
        feature: Feature number (optional)
        attribute: Attribute number (optional, requires feature)

    Returns:
        str: MA command string

    Raises:
        ValueError: When neither type_id nor name is provided
        ValueError: When attribute is provided without feature

    Examples:
        >>> preset_type(3)
        'presettype 3'
        >>> preset_type(name="Dimmer")
        'presettype "Dimmer"'
        >>> preset_type(3, feature=1)
        'presettype 3.1'
        >>> preset_type(name="Color", feature=2)
        'presettype "Color".2'
        >>> preset_type(3, feature=2, attribute=1)
        'presettype 3.2.1'
        >>> preset_type("$preset", feature=2)
        'presettype $preset.2'
    """
    # Validation: Cannot have attribute without feature
    if attribute is not None and feature is None:
        raise ValueError("Cannot specify attribute without feature")

    # Validation: Must provide type_id or name
    if type_id is None and name is None:
        raise ValueError("Must provide type_id or name")

    # Case 1: Using name
    if name is not None:
        base = f'presettype "{name}"'
        if feature is not None:
            base = f"{base}.{feature}"
            if attribute is not None:
                base = f"{base}.{attribute}"
        return base

    # Case 2: Using number or variable
    base = f"presettype {type_id}"
    if feature is not None:
        base = f"{base}.{feature}"
        if attribute is not None:
            base = f"{base}.{attribute}"
    return base


# ----------------------------------------------------------------------------
# Cue Object Keyword
# ----------------------------------------------------------------------------


def cue(
    cue_id: Optional[Union[int, float, List[Union[int, float]]]] = None,
    *,
    end: Optional[Union[int, float]] = None,
    part: Optional[int] = None,
    executor: Optional[int] = None,
    sequence: Optional[int] = None,
) -> str:
    """
    Construct a Cue command to reference a cue.

    Cue is the only object type that accepts numerical ID as decimal fractions.
    The ID allowed for cues ranges from 0.001 to 9999.999.
    The default function for cue objects is SelFix.

    Args:
        cue_id: Cue number (int or float) or list of cue numbers
        end: End cue number (for range selection)
        part: Part number within the cue
        executor: Executor number to specify which executor
        sequence: Sequence number to specify which sequence

    Returns:
        str: MA command to reference a cue

    Raises:
        ValueError: When cue_id is not provided

    Examples:
        >>> cue(5)
        'cue 5'
        >>> cue(3.5)
        'cue 3.5'
        >>> cue(1, end=10)
        'cue 1 thru 10'
        >>> cue([1, 3, 5])
        'cue 1 + 3 + 5'
        >>> cue(3, part=2)
        'cue 3 part 2'
        >>> cue(3, executor=1)
        'cue 3 executor 1'
        >>> cue(5, sequence=3)
        'cue 5 sequence 3'
    """
    if cue_id is None:
        raise ValueError("Must provide cue_id")

    # Helper to format cue ID (preserve decimal precision)
    def format_cue_id(cid: Union[int, float]) -> str:
        if isinstance(cid, float):
            # Format float to remove trailing zeros but keep precision
            formatted = f"{cid:.3f}".rstrip("0").rstrip(".")
            return formatted
        return str(cid)

    # Handle list selection (using + to connect)
    if isinstance(cue_id, list):
        if len(cue_id) == 1:
            return f"cue {format_cue_id(cue_id[0])}"
        cues_str = " + ".join(format_cue_id(cid) for cid in cue_id)
        return f"cue {cues_str}"

    # Build base command
    base = f"cue {format_cue_id(cue_id)}"

    # Handle range selection (using thru)
    if end is not None:
        if cue_id == end:
            pass  # Same start and end, just use single cue
        else:
            base = f"cue {format_cue_id(cue_id)} thru {format_cue_id(end)}"

    # Add part if specified
    if part is not None:
        base = f"{base} part {part}"

    # Add executor if specified
    if executor is not None:
        base = f"{base} executor {executor}"

    # Add sequence if specified
    if sequence is not None:
        base = f"{base} sequence {sequence}"

    return base


def cue_part(
    cue_id: Union[int, float],
    part_id: int,
    *,
    executor: Optional[int] = None,
    sequence: Optional[int] = None,
) -> str:
    """
    Convenience function to reference a cue part.

    Parts segment cues to assign different timings for groups of fixture parameters.

    Args:
        cue_id: Cue number (int or float)
        part_id: Part number within the cue
        executor: Executor number to specify which executor
        sequence: Sequence number to specify which sequence

    Returns:
        str: MA command to reference a cue part

    Examples:
        >>> cue_part(3, 2)
        'cue 3 part 2'
        >>> cue_part(2.5, 1)
        'cue 2.5 part 1'
        >>> cue_part(3, 2, executor=1)
        'cue 3 part 2 executor 1'
        >>> cue_part(3, 2, sequence=5)
        'cue 3 part 2 sequence 5'
    """
    return cue(cue_id, part=part_id, executor=executor, sequence=sequence)


# ----------------------------------------------------------------------------
# Sequence Object Keyword
# ----------------------------------------------------------------------------


def sequence(
    sequence_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    pool: Optional[int] = None,
) -> str:
    """
    Construct a Sequence command to reference a sequence.

    The default function of the sequence keyword is SelFix.
    If the Sequence keyword is used with an ID, all fixtures in the sequence
    will be selected.

    Args:
        sequence_id: Sequence number or list of sequence numbers
        end: End sequence number (for range selection)
        pool: Sequence pool number (for pool.id syntax)

    Returns:
        str: MA command to reference a sequence

    Raises:
        ValueError: When sequence_id is not provided
        ValueError: When pool is used with multiple sequences

    Examples:
        >>> sequence(3)
        'sequence 3'
        >>> sequence(1, end=5)
        'sequence 1 thru 5'
        >>> sequence([1, 3, 5])
        'sequence 1 + 3 + 5'
        >>> sequence(5, pool=2)
        'sequence 2.5'
    """
    if sequence_id is None:
        raise ValueError("Must provide sequence_id")

    # Handle pool syntax (pool.id)
    if pool is not None:
        if isinstance(sequence_id, list):
            raise ValueError("Cannot use pool with multiple sequences")
        return f"sequence {pool}.{sequence_id}"

    # Handle list selection (using + to connect)
    if isinstance(sequence_id, list):
        if len(sequence_id) == 1:
            return f"sequence {sequence_id[0]}"
        seqs_str = " + ".join(str(sid) for sid in sequence_id)
        return f"sequence {seqs_str}"

    # Handle range selection (using thru)
    if end is not None:
        if sequence_id == end:
            return f"sequence {sequence_id}"
        return f"sequence {sequence_id} thru {end}"

    # Single selection
    return f"sequence {sequence_id}"


# ----------------------------------------------------------------------------
# Executor Object Keyword
# ----------------------------------------------------------------------------


def executor(
    executor_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    page: Optional[int] = None,
) -> str:
    """
    Construct an Executor command to reference an executor.

    Executor is an object type that can hold sequences, chasers, or other objects.

    Args:
        executor_id: Executor number or list of executor numbers
        end: End executor number (for range selection)
        page: Executor page number (for page.id syntax)

    Returns:
        str: MA command to reference an executor

    Raises:
        ValueError: When executor_id is not provided
        ValueError: When page is used with multiple executors

    Examples:
        >>> executor(3)
        'executor 3'
        >>> executor(1, end=5)
        'executor 1 thru 5'
        >>> executor([1, 3, 5])
        'executor 1 + 3 + 5'
        >>> executor(5, page=2)
        'executor 2.5'
    """
    if executor_id is None:
        raise ValueError("Must provide executor_id")

    # Handle page syntax (page.id)
    if page is not None:
        if isinstance(executor_id, list):
            raise ValueError("Cannot use page with multiple executors")
        return f"executor {page}.{executor_id}"

    # Handle list selection (using + to connect)
    if isinstance(executor_id, list):
        if len(executor_id) == 1:
            return f"executor {executor_id[0]}"
        execs_str = " + ".join(str(eid) for eid in executor_id)
        return f"executor {execs_str}"

    # Handle range selection (using thru)
    if end is not None:
        if executor_id == end:
            return f"executor {executor_id}"
        return f"executor {executor_id} thru {end}"

    # Single selection
    return f"executor {executor_id}"


# ----------------------------------------------------------------------------
# Layout Object Keyword
# ----------------------------------------------------------------------------


def layout(
    layout_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
) -> str:
    """
    Construct a Layout command to select a layout.

    Layout is an object type representing the layout of fixtures and other objects.
    The default function for Layout is Select, meaning calling a Layout will select it
    and display it in any Layout View with Link Selected enabled.

    Args:
        layout_id: Layout number or list of layout numbers
        end: End layout number (for range selection)

    Returns:
        str: MA command string

    Examples:
        >>> layout(3)
        'layout 3'
        >>> layout(1, end=5)
        'layout 1 thru 5'
        >>> layout([1, 3, 5])
        'layout 1 + 3 + 5'
    """
    if layout_id is None:
        raise ValueError("Must provide layout_id")

    # Handle list selection (using + to connect)
    if isinstance(layout_id, list):
        if len(layout_id) == 1:
            return f"layout {layout_id[0]}"
        layouts_str = " + ".join(str(lid) for lid in layout_id)
        return f"layout {layouts_str}"

    # Handle range selection (using thru)
    if end is not None:
        if layout_id == end:
            return f"layout {layout_id}"
        return f"layout {layout_id} thru {end}"

    # Single selection
    return f"layout {layout_id}"
