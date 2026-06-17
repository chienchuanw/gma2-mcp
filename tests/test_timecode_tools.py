"""
MCP tool + GMA2Client workflow tests for timecode (Issue #39).
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client():
    from src.execution import ExecutionResult

    client = MagicMock()
    client.send_command = AsyncMock()
    client.execute = AsyncMock(
        return_value=ExecutionResult(
            ok=True, echo="OK", error_code=None, error_text=None, raw="OK"
        )
    )
    client.send_command_with_response = AsyncMock(return_value="Timecode 1 'Act 1'")
    return client


class TestSetupTimecodeWorkflow:
    @pytest.mark.asyncio
    async def test_store_name_and_slot(self):
        from src.gma2_client import GMA2Client

        client = _mock_client()
        gma2 = GMA2Client(client)

        result = await gma2.setup_timecode(1, name="Act 1", slot=2)

        assert result["commands_sent"] == [
            "store timecode 1",
            'assign timecode 1 /name = "Act 1"',
            "assign timecode 1 /slot = 2",
        ]
        assert "Timecode 1" in result["summary"]

    @pytest.mark.asyncio
    async def test_store_only(self):
        from src.gma2_client import GMA2Client

        client = _mock_client()
        gma2 = GMA2Client(client)

        result = await gma2.setup_timecode(3)

        assert result["commands_sent"] == ["store timecode 3"]


class TestTimecodeTools:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_assign_slot(self, mock_get):
        from src.server import assign_timecode_slot

        client = _mock_client()
        mock_get.return_value = client

        await assign_timecode_slot(1, 3)

        client.execute.assert_called_once_with("assign timecode 1 /slot = 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_control_go(self, mock_get):
        from src.server import control_timecode

        client = _mock_client()
        mock_get.return_value = client

        await control_timecode(2, "go")

        client.execute.assert_called_once_with("go timecode 2")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_control_record(self, mock_get):
        from src.server import control_timecode

        client = _mock_client()
        mock_get.return_value = client

        await control_timecode(2, "record")

        client.execute.assert_called_once_with("record timecode 2")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_control_unknown_action(self, mock_get):
        from src.server import control_timecode

        client = _mock_client()
        mock_get.return_value = client

        result = await control_timecode(2, "frobnicate")

        assert "Unknown action" in result
        client.execute.assert_not_called()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_query(self, mock_get):
        from src.server import query_timecode

        client = _mock_client()
        mock_get.return_value = client

        result = await query_timecode(1)

        client.send_command_with_response.assert_called_once_with("list timecode 1")
        assert "Timecode 1" in result
