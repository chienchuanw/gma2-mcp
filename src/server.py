"""
MCP Server 模組

這個模組負責建立和運行 MCP server，將所有工具整合在一起。
使用 FastMCP 來簡化 MCP server 的建立過程。

使用方式:
    uv run python -m src.server
"""

import logging
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from src.telnet_client import GMA2TelnetClient
from src.tools import set_gma2_client
from src.commands import (
    select_fixture,
    store_group,
    label_group,
    go_sequence,
    pause_sequence,
    goto_cue,
)

# 載入環境變數
load_dotenv()

# 設定 logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 從環境變數取得設定
GMA_HOST = os.getenv("GMA_HOST", "127.0.0.1")
GMA_PORT = int(os.getenv("GMA_PORT", "30000"))
GMA_USER = os.getenv("GMA_USER", "administrator")
GMA_PASSWORD = os.getenv("GMA_PASSWORD", "admin")

# 建立 MCP server
mcp = FastMCP(
    name="grandMA2-MCP",
    instructions="""
    這是一個用於控制 grandMA2 燈光控台的 MCP server。
    你可以使用以下工具來操作 grandMA2：
    
    1. create_fixture_group - 建立 fixture group
       例如：將 fixture 1 到 10 存成 group 1，並命名為 "前區洗牆燈"
    
    2. execute_sequence - 執行 sequence 操作
       例如：執行 sequence 1、暫停 sequence 2、跳到 sequence 1 的 cue 5
    
    3. send_raw_command - 發送原始 MA 指令
       例如：發送 "blackout" 或 "go+ executor 1.1"
    """,
)

# 全域的 telnet client
_client: GMA2TelnetClient | None = None


def get_client() -> GMA2TelnetClient:
    """取得或建立 telnet client"""
    global _client
    if _client is None:
        _client = GMA2TelnetClient(
            host=GMA_HOST,
            port=GMA_PORT,
            user=GMA_USER,
            password=GMA_PASSWORD,
        )
        _client.connect()
        _client.login()
        set_gma2_client(_client)
        logger.info(f"已連線到 grandMA2: {GMA_HOST}:{GMA_PORT}")
    return _client


# ============================================================
# MCP Tools 定義
# ============================================================


@mcp.tool()
def create_fixture_group(
    start_fixture: int,
    end_fixture: int,
    group_id: int,
    group_name: str | None = None,
) -> str:
    """
    建立一個包含指定 fixture 範圍的 group。

    這個工具會選取指定範圍的 fixtures，然後儲存為一個 group。
    可以選擇性地為 group 加上名稱。

    Args:
        start_fixture: 起始 fixture 編號
        end_fixture: 結束 fixture 編號
        group_id: 要儲存的 group 編號
        group_name: (可選) group 的名稱，例如 "前區洗牆燈"

    Returns:
        str: 操作結果訊息

    Examples:
        - 將 fixture 1 到 10 存成 group 1
        - 將 fixture 1 到 10 存成 group 1，並命名為 "前區洗牆燈"
    """
    client = get_client()

    # 選取 fixtures
    select_cmd = select_fixture(start_fixture, end_fixture)
    client.send_command(select_cmd)

    # 儲存為 group
    store_cmd = store_group(group_id)
    client.send_command(store_cmd)

    # 加上標籤（如果有提供名稱）
    if group_name:
        label_cmd = label_group(group_id, group_name)
        client.send_command(label_cmd)
        return f'已建立 Group {group_id} "{group_name}"，包含 Fixture {start_fixture} 到 {end_fixture}'

    return f"已建立 Group {group_id}，包含 Fixture {start_fixture} 到 {end_fixture}"


@mcp.tool()
def execute_sequence(
    sequence_id: int,
    action: str,
    cue_id: int | None = None,
) -> str:
    """
    執行 sequence 相關操作。

    Args:
        sequence_id: Sequence 編號
        action: 操作類型，可以是 "go"（執行）、"pause"（暫停）或 "goto"（跳轉）
        cue_id: (僅 goto 時需要) 目標 cue 編號

    Returns:
        str: 操作結果訊息

    Examples:
        - 執行 sequence 1
        - 暫停 sequence 2
        - 跳到 sequence 1 的 cue 5
    """
    client = get_client()

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

    return f"未知的操作: {action}，請使用 go、pause 或 goto"


@mcp.tool()
def send_raw_command(command: str) -> str:
    """
    發送原始 MA 指令到 grandMA2。

    這是一個底層工具，允許發送任何 grandMA2 命令行指令。
    建議優先使用其他高階工具，只在需要特殊指令時才使用此工具。

    Args:
        command: 要發送的原始 MA 指令

    Returns:
        str: 操作結果訊息

    Examples:
        - blackout
        - go+ executor 1.1
        - store sequence 1 cue 1
    """
    client = get_client()
    client.send_command(command)
    return f"已發送指令: {command}"


# ============================================================
# Server 啟動
# ============================================================


def main():
    """MCP Server 進入點"""
    logger.info("啟動 grandMA2 MCP Server...")
    logger.info(f"將連線到 grandMA2: {GMA_HOST}:{GMA_PORT}")

    # 使用 stdio transport 啟動 server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
