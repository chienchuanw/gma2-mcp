"""
Time Object Keywords for grandMA2 Command Builder

包含與時間相關的 Object Keywords：
- timecode: 參照 timecode show
- timecode_slot: 參照 timecode slot
- timer: 參照 timer

這些物件類型用於時間相關的控制和同步。
"""

from typing import List, Optional, Union


def timecode(
    timecode_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    slot: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    建構 Timecode 指令以參照 timecode show。

    Timecode 是用於時間碼同步的物件類型。
    可以使用 timecode.slot 語法來指定特定的 slot。

    Args:
        timecode_id: Timecode show 編號或編號列表
        end: 結束編號（用於範圍選擇）
        slot: Timecode slot 編號（用於 timecode.slot 語法）
        select_all: 如果為 True，選擇所有 timecode（timecode thru）

    Returns:
        str: MA 參照 timecode 的指令

    Raises:
        ValueError: 當未提供 timecode_id 且 select_all 為 False 時
        ValueError: 當 slot 與多個 timecodes 一起使用時
        ValueError: 當 end 與列表一起使用時

    Examples:
        >>> timecode(1)
        'timecode 1'
        >>> timecode(1, end=3)
        'timecode 1 thru 3'
        >>> timecode([1, 2, 3])
        'timecode 1 + 2 + 3'
        >>> timecode(1, slot=2)
        'timecode 1.2'
        >>> timecode(select_all=True)
        'timecode thru'
    """
    # 處理 select_all
    if select_all:
        return "timecode thru"

    if timecode_id is None:
        raise ValueError("Must provide timecode_id")

    # 處理 slot 語法（timecode.slot）
    if slot is not None:
        if isinstance(timecode_id, list):
            raise ValueError("Cannot use slot with multiple timecodes")
        return f"timecode {timecode_id}.{slot}"

    # 處理列表選擇（使用 + 連接）
    if isinstance(timecode_id, list):
        # 驗證：不能同時使用列表和 end
        if end is not None:
            raise ValueError("Cannot use 'end' with list")
        if len(timecode_id) == 1:
            return f"timecode {timecode_id[0]}"
        tcs_str = " + ".join(str(tid) for tid in timecode_id)
        return f"timecode {tcs_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if timecode_id == end:
            return f"timecode {timecode_id}"
        return f"timecode {timecode_id} thru {end}"

    # 單一選擇
    return f"timecode {timecode_id}"


def timecode_slot(
    slot_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
) -> str:
    """
    建構 TimecodeSlot 指令以參照 timecode slot。

    TimecodeSlot 代表 8 個不同的可能 timecode 串流。

    Args:
        slot_id: Slot 編號或 slot 編號列表
        end: 結束 slot 編號（用於範圍選擇）

    Returns:
        str: MA 參照 timecode slot 的指令

    Raises:
        ValueError: 當未提供 slot_id 時

    Examples:
        >>> timecode_slot(3)
        'timecodeslot 3'
        >>> timecode_slot(1, end=4)
        'timecodeslot 1 thru 4'
        >>> timecode_slot([1, 3, 5])
        'timecodeslot 1 + 3 + 5'
    """
    if slot_id is None:
        raise ValueError("Must provide slot_id")

    # 處理列表選擇（使用 + 連接）
    if isinstance(slot_id, list):
        if len(slot_id) == 1:
            return f"timecodeslot {slot_id[0]}"
        slots_str = " + ".join(str(sid) for sid in slot_id)
        return f"timecodeslot {slots_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if slot_id == end:
            return f"timecodeslot {slot_id}"
        return f"timecodeslot {slot_id} thru {end}"

    # 單一選擇
    return f"timecodeslot {slot_id}"


def timer(
    timer_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    建構 Timer 指令以參照 timer。

    Timer 是用於計時器功能的物件類型。

    Args:
        timer_id: Timer 編號或 timer 編號列表
        end: 結束 timer 編號（用於範圍選擇）
        select_all: 如果為 True，選擇所有 timer（timer thru）

    Returns:
        str: MA 參照 timer 的指令

    Raises:
        ValueError: 當未提供 timer_id 且 select_all 為 False 時
        ValueError: 當 end 與列表一起使用時

    Examples:
        >>> timer(1)
        'timer 1'
        >>> timer(1, end=3)
        'timer 1 thru 3'
        >>> timer([1, 2, 3])
        'timer 1 + 2 + 3'
        >>> timer(select_all=True)
        'timer thru'
    """
    # 處理 select_all
    if select_all:
        return "timer thru"

    if timer_id is None:
        raise ValueError("Must provide timer_id")

    # 處理列表選擇（使用 + 連接）
    if isinstance(timer_id, list):
        # 驗證：不能同時使用列表和 end
        if end is not None:
            raise ValueError("Cannot use 'end' with list")
        if len(timer_id) == 1:
            return f"timer {timer_id[0]}"
        timers_str = " + ".join(str(tid) for tid in timer_id)
        return f"timer {timers_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if timer_id == end:
            return f"timer {timer_id}"
        return f"timer {timer_id} thru {end}"

    # 單一選擇
    return f"timer {timer_id}"
