"""
MCP Tools Tests

Tests for high-level MCP tools functionality. These are tools that AI can call.
Uses mocks to simulate Telnet connections and avoid actual network calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock


class TestCreateFixtureGroupTool:
    """Tests for the create fixture group MCP tool."""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_basic(self, mock_get_client):
        """Test creating a basic fixture group."""
        from src.tools import create_fixture_group

        # Configure mock
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(start_fixture=1, end_fixture=10, group_id=1)

        # Verify sent commands
        calls = mock_client.send_command.call_args_list
        assert len(calls) == 2
        assert calls[0][0][0] == "selfix fixture 1 thru 10"
        assert calls[1][0][0] == "store group 1"

        # Verify return message
        assert "Group 1" in result
        assert "Fixtures 1" in result
        assert "10" in result

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_with_label(self, mock_get_client):
        """Test creating a fixture group with a label."""
        from src.tools import create_fixture_group

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(
            start_fixture=1, end_fixture=10, group_id=1, group_name="Front Wash"
        )

        # Verify sent commands (including label)
        calls = mock_client.send_command.call_args_list
        assert len(calls) == 3
        assert calls[0][0][0] == "selfix fixture 1 thru 10"
        assert calls[1][0][0] == "store group 1"
        assert calls[2][0][0] == 'label group 1 "Front Wash"'

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_create_fixture_group_with_custom_name(self, mock_get_client):
        """Test creating a fixture group with a custom name."""
        from src.tools import create_fixture_group

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await create_fixture_group(
            start_fixture=1, end_fixture=10, group_id=1, group_name="Front Stage Wash"
        )

        calls = mock_client.send_command.call_args_list
        assert calls[2][0][0] == 'label group 1 "Front Stage Wash"'


class TestExecuteSequenceTool:
    """Tests for the execute sequence MCP tool."""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_go(self, mock_get_client):
        """Test executing a sequence (go)."""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="go")

        mock_client.send_command.assert_called_once_with("go+ sequence 1")

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_pause(self, mock_get_client):
        """Test pausing a sequence."""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="pause")

        mock_client.send_command.assert_called_once_with("pause sequence 1")

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_execute_sequence_goto(self, mock_get_client):
        """Test jumping to a specific cue."""
        from src.tools import execute_sequence

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await execute_sequence(sequence_id=1, action="goto", cue_id=5)

        mock_client.send_command.assert_called_once_with("goto cue 5 sequence 1")


class TestSendRawCommandTool:
    """Tests for the send raw command MCP tool."""

    @pytest.mark.asyncio
    @patch("src.tools.get_gma2_client")
    async def test_send_raw_command(self, mock_get_client):
        """Test sending a raw MA command."""
        from src.tools import send_raw_command

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = await send_raw_command("selfix fixture 1 thru 10")

        mock_client.send_command.assert_called_once_with("selfix fixture 1 thru 10")
        assert "selfix fixture 1 thru 10" in result
