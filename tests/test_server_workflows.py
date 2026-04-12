"""Tests for music show workflow MCP tools in server.py."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def _mock_client():
    client = MagicMock()
    client.send_command = AsyncMock()
    client.send_command_with_response = AsyncMock()
    return client


class TestCreateSongObjectsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_creates_sequence_and_page(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import create_song_objects

        result = await create_song_objects(song_id=101, song_name="Opening+Childhood")

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == 'store sequence 101 "Opening+Childhood"'
        assert calls[1] == 'store page 101 "Opening+Childhood"'
        assert "Sequence 101" in result
        assert "Page 101" in result
        assert "Opening+Childhood" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_sends_exactly_two_commands(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import create_song_objects

        await create_song_objects(song_id=5, song_name="Finale")

        assert client.send_command.call_count == 2


class TestSetupSongMacroTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_creates_macro_with_setvar(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import setup_song_macro

        result = await setup_song_macro(
            macro_id=101, song_name="Opening+Childhood"
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "store macro 101"
        assert calls[1] == 'label macro 101 "Opening+Childhood"'
        assert "SetVar $song='Opening+Childhood'" in calls[2]
        assert "Macro 101" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_custom_var_name(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import setup_song_macro

        result = await setup_song_macro(
            macro_id=10, song_name="Test", var_name="$current"
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert "SetVar $current='Test'" in calls[2]
        assert "$current" in result


class TestBuildSetListTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_builds_set_list(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import build_set_list

        songs = [
            {"cue_id": 1, "macro_id": 101, "name": "Opening"},
            {"cue_id": 2, "macro_id": 102, "name": "Finale"},
        ]
        result = await build_set_list(
            sequence_id=100, sequence_name="Main Set", songs=songs
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == 'store sequence 100 "Main Set"'
        assert calls[1] == 'store sequence 100 cue 1 "Opening"'
        assert calls[2] == 'assign cue 1 sequence 100 /cmd="Macro 101"'
        assert calls[3] == 'store sequence 100 cue 2 "Finale"'
        assert calls[4] == 'assign cue 2 sequence 100 /cmd="Macro 102"'
        assert "Main Set" in result
        assert "2 songs" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_empty_songs(self, mock_get):
        client = _mock_client()
        mock_get.return_value = client

        from src.server import build_set_list

        result = await build_set_list(
            sequence_id=100, sequence_name="Empty Set", songs=[]
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert len(calls) == 1
        assert calls[0] == 'store sequence 100 "Empty Set"'
        assert "0 songs" in result
