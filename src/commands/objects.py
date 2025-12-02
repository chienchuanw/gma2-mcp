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

    Preset 可用於：
    - 選擇存儲在 preset 中的 fixtures
    - 將 preset 套用到當前選擇的 fixture 或 channel

    如果沒有選擇 fixture/channel，預設功能是 SelFix。
    如果已選擇 fixture/channel，預設功能是 At。

    Args:
        preset_type_or_id: Preset type（字串如 "dimmer"）或 type number（整數）
                           或當只提供一個參數時作為 preset ID
        preset_id: Preset 編號或編號列表（用於多選）
        name: Preset 名稱（使用名稱選擇時）
        end: 結束編號（用於範圍選擇）
        wildcard: 是否使用萬用字元 *（搭配 name 使用）

    Returns:
        str: MA 指令字串

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
    # 情況 1: 只使用名稱（可選萬用字元）
    if name is not None and preset_type_or_id is None:
        if wildcard:
            return f'preset *."{name}"'
        return f'preset "{name}"'

    # 情況 2: 類型 + 名稱（如 preset "color"."Red"）
    if name is not None and preset_type_or_id is not None:
        # 將類型轉為字串表示
        if isinstance(preset_type_or_id, str):
            type_str = f'"{preset_type_or_id}"'
        else:
            type_str = str(preset_type_or_id)
        return f'preset {type_str}."{name}"'

    # 情況 3: 只有 preset ID（如 preset 5）
    if preset_type_or_id is not None and preset_id is None:
        return f"preset {preset_type_or_id}"

    # 情況 4: Type + ID（如 preset 3.2 或 preset "dimmer".1）
    if preset_type_or_id is not None and preset_id is not None:
        # 取得 type 數字
        if isinstance(preset_type_or_id, str):
            type_num = PRESET_TYPES.get(preset_type_or_id.lower(), 1)
        else:
            type_num = preset_type_or_id

        # 處理多選（列表）
        if isinstance(preset_id, list):
            if len(preset_id) == 1:
                return f"preset {type_num}.{preset_id[0]}"
            presets_str = " + ".join(f"{type_num}.{pid}" for pid in preset_id)
            return f"preset {presets_str}"

        # 處理範圍選擇
        if end is not None:
            return f"preset {type_num}.{preset_id} thru {end}"

        # 單一選擇
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

    PresetType 可用於：
    - 在 fixture sheet 和 preset type bar 中呼叫 PresetType
    - 選擇 PresetType 中的 Feature 和 Attribute
    - 為選定的 fixtures 啟用 PresetType

    Preset types 包含 features 和 attributes，可以使用點分隔數字來呼叫。

    Args:
        type_id: PresetType 編號（整數）或變數（如 "$preset"）
        name: PresetType 名稱（如 "Dimmer", "Color"）
        feature: Feature 編號（可選）
        attribute: Attribute 編號（可選，需搭配 feature）

    Returns:
        str: MA 指令字串

    Raises:
        ValueError: 未提供 type_id 或 name 時
        ValueError: 提供 attribute 但未提供 feature 時

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
    # 驗證：不能只有 attribute 沒有 feature
    if attribute is not None and feature is None:
        raise ValueError("Cannot specify attribute without feature")

    # 驗證：必須提供 type_id 或 name
    if type_id is None and name is None:
        raise ValueError("Must provide type_id or name")

    # 情況 1: 使用名稱
    if name is not None:
        base = f'presettype "{name}"'
        if feature is not None:
            base = f"{base}.{feature}"
            if attribute is not None:
                base = f"{base}.{attribute}"
        return base

    # 情況 2: 使用數字或變數
    base = f"presettype {type_id}"
    if feature is not None:
        base = f"{base}.{feature}"
        if attribute is not None:
            base = f"{base}.{attribute}"
    return base


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


# ----------------------------------------------------------------------------
# Layout Object Keyword
# ----------------------------------------------------------------------------


def layout(
    layout_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
) -> str:
    """
    Construct a Layout command to select a layout.

    Layout 是一個物件類型，代表 fixtures 和其他物件的佈局。
    Layout 的預設功能是 Select，表示呼叫 Layout 時會選擇該 Layout，
    並在任何啟用 Link Selected 的 Layout View 中顯示。

    Args:
        layout_id: Layout 編號或 Layout 編號列表
        end: 結束 Layout 編號（用於範圍選擇）

    Returns:
        str: MA 指令字串

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

    # 處理列表選擇（使用 + 連接）
    if isinstance(layout_id, list):
        if len(layout_id) == 1:
            return f"layout {layout_id[0]}"
        layouts_str = " + ".join(str(lid) for lid in layout_id)
        return f"layout {layouts_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if layout_id == end:
            return f"layout {layout_id}"
        return f"layout {layout_id} thru {end}"

    # 單一選擇
    return f"layout {layout_id}"
