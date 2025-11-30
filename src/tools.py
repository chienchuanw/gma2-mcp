"""
MCP Tools 模組

這個模組定義 AI 可以呼叫的高階工具函式。
這些 tools 會整合 telnet_client 和 commands 模組，
提供簡單易用的介面給 AI 使用。

每個 tool 都是 async 函式，讓 MCP server 可以非同步處理請求。
"""

import logging
from typing import Optional, Literal

from src.commands import (
    select_fixture,
    store_group,
    label_group,
    go_sequence,
    pause_sequence,
    goto_cue,
)

logger = logging.getLogger(__name__)

# 全域的 GMA2 client 實例
# 這會在 server.py 中初始化
_gma2_client = None


def set_gma2_client(client) -> None:
    """
    設定全域的 GMA2 client 實例

    Args:
        client: GMA2TelnetClient 實例
    """
    global _gma2_client
    _gma2_client = client


def get_gma2_client():
    """
    取得全域的 GMA2 client 實例

    Returns:
        GMA2TelnetClient: 全域的 client 實例

    Raises:
        RuntimeError: 尚未設定 client
    """
    global _gma2_client
    if _gma2_client is None:
        raise RuntimeError("GMA2 client 尚未初始化，請先呼叫 set_gma2_client()")
    return _gma2_client


# ============================================================
# MCP Tools
# ============================================================


async def create_fixture_group(
    start_fixture: int,
    end_fixture: int,
    group_id: int,
    group_name: Optional[str] = None,
) -> str:
    """
    建立一個包含指定 fixture 範圍的 group

    這個工具會執行以下步驟：
    1. 選取指定範圍的 fixtures
    2. 將選取的 fixtures 儲存為一個 group
    3. (可選) 為 group 加上名稱標籤

    Args:
        start_fixture: 起始 fixture 編號
        end_fixture: 結束 fixture 編號
        group_id: 要儲存的 group 編號
        group_name: (可選) group 的名稱

    Returns:
        str: 操作結果訊息
    """
    client = get_gma2_client()

    # 步驟 1: 選取 fixtures
    select_cmd = select_fixture(start_fixture, end_fixture)
    client.send_command(select_cmd)
    logger.info(f"已選取 Fixture {start_fixture} 到 {end_fixture}")

    # 步驟 2: 儲存為 group
    store_cmd = store_group(group_id)
    client.send_command(store_cmd)
    logger.info(f"已儲存為 Group {group_id}")

    # 步驟 3: (可選) 加上標籤
    if group_name:
        label_cmd = label_group(group_id, group_name)
        client.send_command(label_cmd)
        logger.info(f'已將 Group {group_id} 命名為 "{group_name}"')
        return f'已建立 Group {group_id} "{group_name}"，包含 Fixture {start_fixture} 到 {end_fixture}'

    return f"已建立 Group {group_id}，包含 Fixture {start_fixture} 到 {end_fixture}"


async def execute_sequence(
    sequence_id: int,
    action: Literal["go", "pause", "goto"],
    cue_id: Optional[int] = None,
) -> str:
    """
    執行 sequence 相關操作

    Args:
        sequence_id: Sequence 編號
        action: 操作類型（go=執行, pause=暫停, goto=跳轉到指定 cue）
        cue_id: (僅 goto 時需要) 目標 cue 編號

    Returns:
        str: 操作結果訊息
    """
    client = get_gma2_client()

    if action == "go":
        cmd = go_sequence(sequence_id)
        client.send_command(cmd)
        return f"已執行 Sequence {sequence_id}"

    elif action == "pause":
        cmd = pause_sequence(sequence_id)
        client.send_command(cmd)
        return f"已暫停 Sequence {sequence_id}"

    elif action == "goto":
        if cue_id is None:
            return "錯誤：goto 操作需要指定 cue_id"
        cmd = goto_cue(sequence_id, cue_id)
        client.send_command(cmd)
        return f"已跳轉到 Sequence {sequence_id} 的 Cue {cue_id}"

    return f"未知的操作: {action}"


async def send_raw_command(command: str) -> str:
    """
    發送原始 MA 指令

    這是一個底層工具，允許發送任何 grandMA2 指令。
    建議優先使用其他高階工具，只在需要時才使用此工具。

    Args:
        command: 要發送的原始 MA 指令

    Returns:
        str: 操作結果訊息
    """
    client = get_gma2_client()
    client.send_command(command)
    logger.info(f"已發送指令: {command}")
    return f"已發送指令: {command}"
