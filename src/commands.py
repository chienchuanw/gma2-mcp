"""
Command Builder 模組

這個模組提供高階函式來建構 grandMA2 指令字串。
這些函式只負責產生正確格式的指令，不負責發送。

根據 coding-standards.md，這些函式是「thin wrappers」，
只負責建構 MA 指令，不包含任何 Telnet 邏輯。
"""

from typing import Optional

# Preset 類型對應的編號
# grandMA2 使用數字來區分 preset 類型
PRESET_TYPES = {
    "dimmer": 1,
    "position": 2,
    "gobo": 3,
    "color": 2,  # color 也是使用 preset type 2
    "beam": 4,
    "focus": 5,
    "control": 6,
    "shapers": 7,
    "video": 8,
}


# ============================================================
# Fixture 相關指令
# ============================================================


def select_fixture(start: int, end: Optional[int] = None) -> str:
    """
    建構選取 fixture 的指令

    Args:
        start: 起始 fixture 編號
        end: 結束 fixture 編號（可選，若未指定則只選取單一 fixture）

    Returns:
        str: 選取 fixture 的 MA 指令

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
    建構清除選取的指令

    Returns:
        str: 清除選取的 MA 指令
    """
    return "clearall"


# ============================================================
# Group 相關指令
# ============================================================


def store_group(group_id: int) -> str:
    """
    建構儲存 group 的指令

    Args:
        group_id: Group 編號

    Returns:
        str: 儲存 group 的 MA 指令
    """
    return f"store group {group_id}"


def label_group(group_id: int, name: str) -> str:
    """
    建構為 group 加上標籤的指令

    Args:
        group_id: Group 編號
        name: Group 名稱

    Returns:
        str: 標記 group 的 MA 指令
    """
    return f'label group {group_id} "{name}"'


def select_group(group_id: int) -> str:
    """
    建構選取 group 的指令

    Args:
        group_id: Group 編號

    Returns:
        str: 選取 group 的 MA 指令
    """
    return f"group {group_id}"


def delete_group(group_id: int) -> str:
    """
    建構刪除 group 的指令

    Args:
        group_id: Group 編號

    Returns:
        str: 刪除 group 的 MA 指令
    """
    return f"delete group {group_id}"


# ============================================================
# Preset 相關指令
# ============================================================


def store_preset(preset_type: str, preset_id: int) -> str:
    """
    建構儲存 preset 的指令

    Args:
        preset_type: Preset 類型（dimmer, position, gobo, color, beam, focus, control, shapers, video）
        preset_id: Preset 編號

    Returns:
        str: 儲存 preset 的 MA 指令
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f"store preset {type_num}.{preset_id}"


def label_preset(preset_type: str, preset_id: int, name: str) -> str:
    """
    建構為 preset 加上標籤的指令

    Args:
        preset_type: Preset 類型
        preset_id: Preset 編號
        name: Preset 名稱

    Returns:
        str: 標記 preset 的 MA 指令
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f'label preset {type_num}.{preset_id} "{name}"'


def call_preset(preset_type: str, preset_id: int) -> str:
    """
    建構呼叫 preset 的指令

    Args:
        preset_type: Preset 類型
        preset_id: Preset 編號

    Returns:
        str: 呼叫 preset 的 MA 指令
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f"preset {type_num}.{preset_id}"


# ============================================================
# Sequence 相關指令
# ============================================================


def go_sequence(sequence_id: int) -> str:
    """
    建構執行 sequence 的指令

    Args:
        sequence_id: Sequence 編號

    Returns:
        str: 執行 sequence 的 MA 指令
    """
    return f"go+ sequence {sequence_id}"


def pause_sequence(sequence_id: int) -> str:
    """
    建構暫停 sequence 的指令

    Args:
        sequence_id: Sequence 編號

    Returns:
        str: 暫停 sequence 的 MA 指令
    """
    return f"pause sequence {sequence_id}"


def goto_cue(sequence_id: int, cue_id: int) -> str:
    """
    建構跳轉到指定 cue 的指令

    Args:
        sequence_id: Sequence 編號
        cue_id: Cue 編號

    Returns:
        str: 跳轉 cue 的 MA 指令
    """
    return f"goto cue {cue_id} sequence {sequence_id}"
