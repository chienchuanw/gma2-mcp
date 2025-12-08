"""
Executor Object Keywords for grandMA2 Command Builder

包含與 Executor 相關的 Object Keywords：
- executor: 參照 executor

Executor 是可以容納 sequences、chasers 或其他物件的物件類型。
"""

from typing import List, Optional, Union


def executor(
    executor_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    page: Optional[int] = None,
) -> str:
    """
    建構 Executor 指令以參照 executor。

    Executor 是可以容納 sequences、chasers 或其他物件的物件類型。

    Args:
        executor_id: Executor 編號或 executor 編號列表
        end: 結束 executor 編號（用於範圍選擇）
        page: Executor page 編號（用於 page.id 語法）

    Returns:
        str: MA 參照 executor 的指令

    Raises:
        ValueError: 當未提供 executor_id 時
        ValueError: 當 page 與多個 executors 一起使用時

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

    # 處理 page 語法（page.id）
    if page is not None:
        if isinstance(executor_id, list):
            raise ValueError("Cannot use page with multiple executors")
        return f"executor {page}.{executor_id}"

    # 處理列表選擇（使用 + 連接）
    if isinstance(executor_id, list):
        if len(executor_id) == 1:
            return f"executor {executor_id[0]}"
        execs_str = " + ".join(str(eid) for eid in executor_id)
        return f"executor {execs_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if executor_id == end:
            return f"executor {executor_id}"
        return f"executor {executor_id} thru {end}"

    # 單一選擇
    return f"executor {executor_id}"

