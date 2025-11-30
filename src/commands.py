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
    建構選取 fixture 的 MA 指令。

    根據 grandMA2 官方文件，SelFix 關鍵字用於在 programmer 中建立 fixture 選取。
    支援多種選取方式：單一、多個、範圍、從頭開始、到最後、全選。

    Args:
        ids: Fixture 編號，可以是：
             - 單個整數：選取單一 fixture
             - 整數列表：選取多個不連續的 fixtures（用 + 連接）
        end: 結束編號（用於範圍選取）
        start: 起始編號（用於關鍵字參數形式）
        thru_all: 若為 True，表示從 start 選取到最後（Fixture X Thru）
        select_all: 若為 True，選取全部 fixtures（Fixture Thru）

    Returns:
        str: MA 指令字串

    Examples:
        單一 fixture:
        >>> select_fixture(1)
        'selfix fixture 1'

        多個 fixtures:
        >>> select_fixture([1, 3, 5])
        'selfix fixture 1 + 3 + 5'

        範圍選取:
        >>> select_fixture(1, 10)
        'selfix fixture 1 thru 10'

        從頭選取到 X:
        >>> select_fixture(end=10)
        'selfix fixture thru 10'

        從 X 選取到最後:
        >>> select_fixture(start=5, thru_all=True)
        'selfix fixture 5 thru'

        選取全部:
        >>> select_fixture(select_all=True)
        'selfix fixture thru'
    """
    # 情況 1：選取全部 fixtures（Fixture Thru）
    if select_all:
        return "selfix fixture thru"

    # 情況 2：從頭選取到指定編號（Fixture Thru X）
    if ids is None and start is None and end is not None:
        return f"selfix fixture thru {end}"

    # 情況 3：從指定編號選取到最後（Fixture X Thru）
    if thru_all and start is not None:
        return f"selfix fixture {start} thru"

    # 處理 ids 參數（可能是 int 或 list）
    actual_start: Optional[int] = None

    if ids is not None:
        # 如果是列表
        if isinstance(ids, list):
            if len(ids) == 1:
                # 單一元素列表，等同於選取單一 fixture
                return f"selfix fixture {ids[0]}"
            # 多個 fixtures，用 + 連接
            fixtures_str = " + ".join(str(id) for id in ids)
            return f"selfix fixture {fixtures_str}"
        else:
            # 單一整數
            actual_start = ids
    elif start is not None:
        actual_start = start

    # 情況 4：範圍選取（Fixture X Thru Y）
    if actual_start is not None and end is not None:
        if actual_start == end:
            return f"selfix fixture {actual_start}"
        return f"selfix fixture {actual_start} thru {end}"

    # 情況 5：選取單一 fixture
    if actual_start is not None:
        return f"selfix fixture {actual_start}"

    # 預設情況（不應該到達這裡）
    raise ValueError("必須提供至少一個選取參數")


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
