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


def preset(preset_type: str, preset_id: int) -> str:
    """
    Construct a Preset command to call/apply a preset.

    Args:
        preset_type: Preset type (dimmer, position, gobo, color, beam, etc.)
        preset_id: Preset number

    Returns:
        str: MA command to call a preset

    Examples:
        >>> preset("dimmer", 1)
        'preset 1.1'
        >>> preset("color", 5)
        'preset 2.5'
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f"preset {type_num}.{preset_id}"


# ----------------------------------------------------------------------------
# Cue Object Keyword
# ----------------------------------------------------------------------------


def cue(cue_id: int, sequence_id: Optional[int] = None) -> str:
    """
    Construct a Cue command to reference a cue.

    Args:
        cue_id: Cue number
        sequence_id: Optional sequence number

    Returns:
        str: MA command to reference a cue

    Examples:
        >>> cue(5)
        'cue 5'
        >>> cue(5, sequence_id=3)
        'cue 5 sequence 3'
    """
    if sequence_id is not None:
        return f"cue {cue_id} sequence {sequence_id}"
    return f"cue {cue_id}"


# ----------------------------------------------------------------------------
# Sequence Object Keyword
# ----------------------------------------------------------------------------


def sequence(sequence_id: int) -> str:
    """
    Construct a Sequence command to reference a sequence.

    Args:
        sequence_id: Sequence number

    Returns:
        str: MA command to reference a sequence

    Examples:
        >>> sequence(3)
        'sequence 3'
    """
    return f"sequence {sequence_id}"
