"""
Layout/View Object Keywords for grandMA2 Command Builder

包含與 Layout 和 View 相關的 Object Keywords：
- layout: 選擇 layout

Layout 是代表燈具和其他物件佈局的物件類型。
"""

from typing import List, Optional, Union


def layout(
    layout_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
) -> str:
    """
    建構 Layout 指令以選擇 layout。

    Layout 是代表燈具和其他物件佈局的物件類型。
    Layout 的預設函式是 Select，意味著呼叫 Layout 會選擇它
    並在任何啟用 Link Selected 的 Layout View 中顯示它。

    Args:
        layout_id: Layout 編號或 layout 編號列表
        end: 結束 layout 編號（用於範圍選擇）

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

