"""
Cue/Sequence Object Keywords for grandMA2 Command Builder

包含與 Cue 和 Sequence 相關的 Object Keywords：
- cue: 參照 cue
- cue_part: 參照 cue part 的便利函式
- sequence: 參照 sequence

Cue 是唯一接受小數 ID 的物件類型（範圍 0.001 到 9999.999）。
"""

from typing import List, Optional, Union


def cue(
    cue_id: Optional[Union[int, float, List[Union[int, float]]]] = None,
    *,
    end: Optional[Union[int, float]] = None,
    part: Optional[int] = None,
    executor: Optional[int] = None,
    sequence: Optional[int] = None,
) -> str:
    """
    建構 Cue 指令以參照 cue。

    Cue 是唯一接受小數 ID 的物件類型。
    允許的 ID 範圍從 0.001 到 9999.999。
    cue 物件的預設函式是 SelFix。

    Args:
        cue_id: Cue 編號（int 或 float）或 cue 編號列表
        end: 結束 cue 編號（用於範圍選擇）
        part: Cue 內的 part 編號
        executor: 指定哪個 executor 的編號
        sequence: 指定哪個 sequence 的編號

    Returns:
        str: MA 參照 cue 的指令

    Raises:
        ValueError: 當未提供 cue_id 時

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

    # 輔助函式：格式化 cue ID（保留小數精度）
    def format_cue_id(cid: Union[int, float]) -> str:
        if isinstance(cid, float):
            formatted = f"{cid:.3f}".rstrip("0").rstrip(".")
            return formatted
        return str(cid)

    # 處理列表選擇（使用 + 連接）
    if isinstance(cue_id, list):
        if len(cue_id) == 1:
            return f"cue {format_cue_id(cue_id[0])}"
        cues_str = " + ".join(format_cue_id(cid) for cid in cue_id)
        return f"cue {cues_str}"

    # 建構基本指令
    base = f"cue {format_cue_id(cue_id)}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if cue_id == end:
            pass  # 相同的起始和結束，只使用單一 cue
        else:
            base = f"cue {format_cue_id(cue_id)} thru {format_cue_id(end)}"

    # 如果有指定 part 則加入
    if part is not None:
        base = f"{base} part {part}"

    # 如果有指定 executor 則加入
    if executor is not None:
        base = f"{base} executor {executor}"

    # 如果有指定 sequence 則加入
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
    參照 cue part 的便利函式。

    Parts 將 cues 分段，為不同的燈具參數群組指定不同的時間。

    Args:
        cue_id: Cue 編號（int 或 float）
        part_id: Cue 內的 part 編號
        executor: 指定哪個 executor 的編號
        sequence: 指定哪個 sequence 的編號

    Returns:
        str: MA 參照 cue part 的指令

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


def sequence(
    sequence_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    pool: Optional[int] = None,
) -> str:
    """
    建構 Sequence 指令以參照 sequence。

    sequence 關鍵字的預設函式是 SelFix。
    如果 Sequence 關鍵字與 ID 一起使用，sequence 中的所有燈具將被選擇。

    Args:
        sequence_id: Sequence 編號或 sequence 編號列表
        end: 結束 sequence 編號（用於範圍選擇）
        pool: Sequence pool 編號（用於 pool.id 語法）

    Returns:
        str: MA 參照 sequence 的指令

    Raises:
        ValueError: 當未提供 sequence_id 時
        ValueError: 當 pool 與多個 sequences 一起使用時

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

    # 處理 pool 語法（pool.id）
    if pool is not None:
        if isinstance(sequence_id, list):
            raise ValueError("Cannot use pool with multiple sequences")
        return f"sequence {pool}.{sequence_id}"

    # 處理列表選擇（使用 + 連接）
    if isinstance(sequence_id, list):
        if len(sequence_id) == 1:
            return f"sequence {sequence_id[0]}"
        seqs_str = " + ".join(str(sid) for sid in sequence_id)
        return f"sequence {seqs_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if sequence_id == end:
            return f"sequence {sequence_id}"
        return f"sequence {sequence_id} thru {end}"

    # 單一選擇
    return f"sequence {sequence_id}"
