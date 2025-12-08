"""
Group/Selection Object Keywords for grandMA2 Command Builder

包含與群組和選擇相關的 Object Keywords：
- group: 選擇燈具群組

Group 是包含燈具集合和選擇順序的物件類型。
"""

from typing import List, Optional, Union


def group(
    group_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
) -> str:
    """
    建構 Group 指令以選擇群組。

    Group 是包含燈具集合和選擇順序的物件類型。
    預設函式是 SelFix。

    Args:
        group_id: 群組編號或群組編號列表
        end: 範圍選擇的結束群組編號

    Returns:
        str: MA 選擇群組的指令

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

