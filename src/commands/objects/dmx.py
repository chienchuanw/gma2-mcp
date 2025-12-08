"""
DMX Object Keywords for grandMA2 Command Builder

包含與 DMX 相關的 Object Keywords：
- dmx: 參照 DMX 位址
- dmx_universe: 參照 DMX universe

DMX 是用於直接控制 DMX 輸出的物件類型。
"""

from typing import List, Optional, Union


def dmx(
    address: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    universe: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    建構 DMX 指令以參照 DMX 位址。

    DMX 是用於直接控制 DMX 輸出的物件類型。
    DMX 位址可以使用 universe.address 語法來指定。

    Args:
        address: DMX 位址（1-512）或位址列表
        end: 結束位址（用於範圍選擇）
        universe: DMX universe 編號（用於 universe.address 語法）
        select_all: 如果為 True，選擇所有 DMX 位址（dmx thru）

    Returns:
        str: MA 參照 DMX 位址的指令

    Raises:
        ValueError: 當未提供 address 且 select_all 為 False 時

    Examples:
        >>> dmx(100)
        'dmx 100'
        >>> dmx(1, end=10)
        'dmx 1 thru 10'
        >>> dmx([1, 5, 10])
        'dmx 1 + 5 + 10'
        >>> dmx(100, universe=2)
        'dmx 2.100'
        >>> dmx(1, end=10, universe=2)
        'dmx 2.1 thru 10'
        >>> dmx([1, 5, 10], universe=2)
        'dmx 2.1 + 2.5 + 2.10'
        >>> dmx(select_all=True)
        'dmx thru'
    """
    # 處理 select_all
    if select_all:
        return "dmx thru"

    if address is None:
        raise ValueError("Must provide address")

    # 處理 universe 語法（universe.address）
    if universe is not None:
        # 處理列表選擇（使用 + 連接）
        if isinstance(address, list):
            if len(address) == 1:
                return f"dmx {universe}.{address[0]}"
            addrs_str = " + ".join(f"{universe}.{addr}" for addr in address)
            return f"dmx {addrs_str}"

        # 處理範圍選擇（使用 thru）
        if end is not None:
            if address == end:
                return f"dmx {universe}.{address}"
            return f"dmx {universe}.{address} thru {end}"

        # 單一選擇
        return f"dmx {universe}.{address}"

    # 處理列表選擇（使用 + 連接）
    if isinstance(address, list):
        if len(address) == 1:
            return f"dmx {address[0]}"
        addrs_str = " + ".join(str(addr) for addr in address)
        return f"dmx {addrs_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if address == end:
            return f"dmx {address}"
        return f"dmx {address} thru {end}"

    # 單一選擇
    return f"dmx {address}"


def dmx_universe(
    universe_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
) -> str:
    """
    建構 DmxUniverse 指令以參照 DMX universe。

    DmxUniverse 是用於參照整個 DMX universe 的物件類型。

    Args:
        universe_id: Universe 編號或 universe 編號列表
        end: 結束 universe 編號（用於範圍選擇）

    Returns:
        str: MA 參照 DMX universe 的指令

    Raises:
        ValueError: 當未提供 universe_id 時

    Examples:
        >>> dmx_universe(1)
        'dmxuniverse 1'
        >>> dmx_universe(1, end=4)
        'dmxuniverse 1 thru 4'
        >>> dmx_universe([1, 3, 5])
        'dmxuniverse 1 + 3 + 5'
    """
    if universe_id is None:
        raise ValueError("Must provide universe_id")

    # 處理列表選擇（使用 + 連接）
    if isinstance(universe_id, list):
        if len(universe_id) == 1:
            return f"dmxuniverse {universe_id[0]}"
        univs_str = " + ".join(str(uid) for uid in universe_id)
        return f"dmxuniverse {univs_str}"

    # 處理範圍選擇（使用 thru）
    if end is not None:
        if universe_id == end:
            return f"dmxuniverse {universe_id}"
        return f"dmxuniverse {universe_id} thru {end}"

    # 單一選擇
    return f"dmxuniverse {universe_id}"
