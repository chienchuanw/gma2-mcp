"""
Server Read-Back Tool Tests

Tests for MCP tools that read back show object data:
- read_macro_lines
- read_cue_info
- read_object_label
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client():
    client = MagicMock()
    client.send_command = AsyncMock()
    client.send_command_with_response = AsyncMock()
    return client


SAMPLE_MACRO_OUTPUT = (
    "No   Name           CMD\n"
    "---  ----           ---\n"
    " 1                  SetVar $song='Opening+Childhood'\n"
    " 2                  Go Sequence 101\n"
)

SAMPLE_CUE_OUTPUT = (
    "No       Name        Fade   OutFade  Delay  OutDelay  CMD\n"
    "------   ----        ----   -------  -----  --------  ---\n"
    " 1       Opening     2.0                               Go Macro 5\n"
)

SAMPLE_OBJECT_OUTPUT = (
    "No   Name\n"
    "---  ----\n"
    " 1   Front Wash\n"
)


class TestReadMacroLines:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_macro_lines_basic(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_MACRO_OUTPUT
        mock_get.return_value = client

        from src.server import read_macro_lines

        result = await read_macro_lines(macro_id=101)

        client.send_command_with_response.assert_called_once_with(
            "list macro 1.101"
        )
        assert result["macro_id"] == 101
        assert result["parsed"] is True
        assert len(result["lines"]) == 2
        assert result["raw_response"] == SAMPLE_MACRO_OUTPUT

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_macro_lines_custom_pool(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_MACRO_OUTPUT
        mock_get.return_value = client

        from src.server import read_macro_lines

        result = await read_macro_lines(macro_id=5, pool=2)

        client.send_command_with_response.assert_called_once_with(
            "list macro 2.5"
        )
        assert result["macro_id"] == 5


class TestReadCueInfo:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_cue_info_basic(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_CUE_OUTPUT
        mock_get.return_value = client

        from src.server import read_cue_info

        result = await read_cue_info(sequence_id=101, cue_id=1)

        client.send_command_with_response.assert_called_once_with(
            "list cue 1 sequence 101"
        )
        assert result["sequence_id"] == 101
        assert result["cue_id"] == 1
        assert result["parsed"] is True
        assert result["label"] == "Opening"
        assert result["raw_response"] == SAMPLE_CUE_OUTPUT

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_cue_info_string_cue(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_CUE_OUTPUT
        mock_get.return_value = client

        from src.server import read_cue_info

        result = await read_cue_info(sequence_id=10, cue_id="2.5")

        client.send_command_with_response.assert_called_once_with(
            "list cue 2.5 sequence 10"
        )


class TestReadObjectLabel:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_object_label_basic(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_OBJECT_OUTPUT
        mock_get.return_value = client

        from src.server import read_object_label

        result = await read_object_label(object_type="group", object_id=1)

        client.send_command_with_response.assert_called_once_with("list group 1")
        assert result["object_type"] == "group"
        assert result["object_id"] == 1
        assert result["parsed"] is True
        assert result["label"] == "Front Wash"
        assert result["raw_response"] == SAMPLE_OBJECT_OUTPUT

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_read_object_label_sequence(self, mock_get):
        client = _mock_client()
        client.send_command_with_response.return_value = SAMPLE_OBJECT_OUTPUT
        mock_get.return_value = client

        from src.server import read_object_label

        result = await read_object_label(object_type="sequence", object_id=5)

        client.send_command_with_response.assert_called_once_with(
            "list sequence 5"
        )
        assert result["object_type"] == "sequence"
        assert result["object_id"] == 5
