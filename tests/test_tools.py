"""
MCP Tools 測試

測試 MCP tools 的高階功能，這些是 AI 可以呼叫的工具。
使用 mock 來模擬 Telnet 連線，避免實際網路呼叫。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock


class TestCreateFixtureGroupTool:
    """測試建立 fixture group 的 MCP tool"""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_basic(self, mock_get_client):
        """測試建立基本的 fixture group"""
        from src.tools import create_fixture_group

        # 設定 mock
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(
            start_fixture=1,
            end_fixture=10,
            group_id=1
        )

        # 驗證發送的指令
        calls = mock_client.send_command.call_args_list
        assert len(calls) == 2
        assert calls[0][0][0] == "selfix fixture 1 thru 10"
        assert calls[1][0][0] == "store group 1"

        # 驗證回傳訊息
        assert "Group 1" in result
        assert "Fixture 1" in result
        assert "10" in result

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_with_label(self, mock_get_client):
        """測試建立 fixture group 並加上標籤"""
        from src.tools import create_fixture_group

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(
            start_fixture=1,
            end_fixture=10,
            group_id=1,
            group_name="Front Wash"
        )

        # 驗證發送的指令（包含 label）
        calls = mock_client.send_command.call_args_list
        assert len(calls) == 3
        assert calls[0][0][0] == "selfix fixture 1 thru 10"
        assert calls[1][0][0] == "store group 1"
        assert calls[2][0][0] == 'label group 1 "Front Wash"'

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_with_chinese_name(self, mock_get_client):
        """測試使用中文名稱建立 fixture group"""
        from src.tools import create_fixture_group

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(
            start_fixture=1,
            end_fixture=10,
            group_id=1,
            group_name="前區洗牆燈"
        )

        calls = mock_client.send_command.call_args_list
        assert calls[2][0][0] == 'label group 1 "前區洗牆燈"'


class TestExecuteSequenceTool:
    """測試執行 sequence 的 MCP tool"""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_go(self, mock_get_client):
        """測試執行 sequence (go)"""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="go")

        mock_client.send_command.assert_called_once_with("go+ sequence 1")

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_pause(self, mock_get_client):
        """測試暫停 sequence"""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="pause")

        mock_client.send_command.assert_called_once_with("pause sequence 1")

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_goto(self, mock_get_client):
        """測試跳轉到指定 cue"""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="goto", cue_id=5)

        mock_client.send_command.assert_called_once_with("goto cue 5 sequence 1")


class TestSendRawCommandTool:
    """測試發送原始指令的 MCP tool"""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_send_raw_command(self, mock_get_client):
        """測試發送原始 MA 指令"""
        from src.tools import send_raw_command

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await send_raw_command("selfix fixture 1 thru 10")

        mock_client.send_command.assert_called_once_with("selfix fixture 1 thru 10")
        assert "selfix fixture 1 thru 10" in result

