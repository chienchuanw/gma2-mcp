"""
Fixture/Channel Object Keywords for grandMA2 Command Builder

包含與燈具和頻道相關的 Object Keywords：
- fixture: 使用 Fixture ID 存取燈具
- channel: 使用 Channel ID 存取燈具

這些是 grandMA2 中最基礎的物件類型，用於選擇和控制燈具。
"""

from typing import List, Optional, Union


def fixture(
    fixture_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
    *,
    sub_id: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    建構 Fixture 指令以使用 Fixture ID 存取燈具。

    Fixture 是使用 fixture ID 存取燈具的物件關鍵字。
    預設函式是 SelFix，意味著輸入 fixtures 而不指定函式將會選擇它們。

    Args:
        fixture_id: 燈具編號或燈具編號列表
        end: 範圍選擇的結束燈具編號
        sub_id: 子燈具 ID（例如：fixture 11.5 表示第 5 個子燈具）
        select_all: 如果為 True，選擇所有燈具（fixture thru）

    Returns:
        str: MA 選擇燈具的指令

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


def channel(
    channel_id: Optional[Union[int, List[int]]] = None,
    end: Optional[int] = None,
    *,
    sub_id: Optional[int] = None,
    select_all: bool = False,
) -> str:
    """
    建構 Channel 指令以使用 Channel ID 存取燈具。

    Channel 是使用 Channel ID 存取燈具的物件類型。
    預設函式是 SelFix。

    Args:
        channel_id: 頻道編號或頻道編號列表
        end: 範圍選擇的結束頻道編號
        sub_id: 子燈具 ID
        select_all: 如果為 True，選擇所有頻道（channel thru）

    Returns:
        str: MA 選擇頻道的指令

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

