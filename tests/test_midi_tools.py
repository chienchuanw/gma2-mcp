"""MCP tool tests for MIDI output (Issue #53)."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client():
    from src.execution import ExecutionResult

    client = MagicMock()
    client.execute = AsyncMock(
        return_value=ExecutionResult(
            ok=True, echo="OK", error_code=None, error_text=None, raw="OK"
        )
    )
    return client


class TestMidiTools:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_note(self, mock_get):
        from src.server import send_midi_note
        client = _mock_client(); mock_get.return_value = client
        await send_midi_note(60, velocity=100, channel=2)
        client.execute.assert_called_once_with("midinote 2.60 100")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_note_off(self, mock_get):
        from src.server import send_midi_note
        client = _mock_client(); mock_get.return_value = client
        await send_midi_note(60, off=True)
        client.execute.assert_called_once_with("midinote 60 Off")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_control(self, mock_get):
        from src.server import send_midi_control
        client = _mock_client(); mock_get.return_value = client
        await send_midi_control(1, 64, channel=3)
        client.execute.assert_called_once_with("midicontrol 3.1 64")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_program(self, mock_get):
        from src.server import send_midi_program
        client = _mock_client(); mock_get.return_value = client
        await send_midi_program(5)
        client.execute.assert_called_once_with("midiprogram 5")
