"""
MCP tool tests for query/introspection tools (Issue #4).

Tests for list_groups, list_cues, list_presets, get_cue_info,
get_group_info, list_variables, and query_object MCP tools.

All tests mock get_client and verify:
- Correct command sent via send_command_with_response
- Proper return values including raw response text
- Empty response handling
- Connection error handling via @handle_connection_error
- Input validation (e.g., invalid preset types)
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client(response=""):
    """create a mock client with send_command_with_response support."""
    client = MagicMock()
    client.send_command = AsyncMock()
    client.send_command_with_response = AsyncMock(return_value=response)
    return client


# ============================================================
# list_groups
# ============================================================


class TestListGroupsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_all_groups(self, mock_get):
        from src.server import list_groups

        client = _mock_client("Group 1 'Front Wash'\nGroup 2 'Back Light'")
        mock_get.return_value = client

        result = await list_groups()

        client.send_command_with_response.assert_called_once_with("list group")
        assert "Front Wash" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_groups_with_range(self, mock_get):
        from src.server import list_groups

        client = _mock_client("Group 1\nGroup 2")
        mock_get.return_value = client

        result = await list_groups(group_id=1, end_group_id=10)

        client.send_command_with_response.assert_called_once_with(
            "list group 1 thru 10"
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_groups_specific(self, mock_get):
        from src.server import list_groups

        client = _mock_client("Group 5 'Spots'")
        mock_get.return_value = client

        result = await list_groups(group_id=5)

        client.send_command_with_response.assert_called_once_with("list group 5")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_groups_empty_response(self, mock_get):
        from src.server import list_groups

        client = _mock_client("")
        mock_get.return_value = client

        result = await list_groups()

        assert "no data" in result.lower() or "empty" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_groups_connection_error(self, mock_get):
        from src.server import list_groups

        client = _mock_client()
        client.send_command_with_response.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await list_groups()

        assert "Connection lost" in result


# ============================================================
# list_cues
# ============================================================


class TestListCuesTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_all_cues(self, mock_get):
        from src.server import list_cues

        client = _mock_client("Cue 1 'Opening'\nCue 2 'Scene 1'")
        mock_get.return_value = client

        result = await list_cues()

        client.send_command_with_response.assert_called_once_with("list cue")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_cues_with_sequence(self, mock_get):
        from src.server import list_cues

        client = _mock_client("Cue 1")
        mock_get.return_value = client

        result = await list_cues(sequence_id=3)

        client.send_command_with_response.assert_called_once_with(
            "list cue sequence 3"
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_cues_with_range(self, mock_get):
        from src.server import list_cues

        client = _mock_client("Cue 1\nCue 5")
        mock_get.return_value = client

        result = await list_cues(cue_id=1, end_cue_id=5)

        client.send_command_with_response.assert_called_once_with(
            "list cue 1 thru 5"
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_cues_empty_response(self, mock_get):
        from src.server import list_cues

        client = _mock_client("")
        mock_get.return_value = client

        result = await list_cues()

        assert "no data" in result.lower() or "empty" in result.lower()


# ============================================================
# list_presets
# ============================================================


class TestListPresetsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_color_presets(self, mock_get):
        from src.server import list_presets

        client = _mock_client("Preset 4.1 'Red'\nPreset 4.2 'Blue'")
        mock_get.return_value = client

        result = await list_presets(preset_type="color")

        client.send_command_with_response.assert_called_once_with(
            'list preset "color"'
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_position_presets(self, mock_get):
        from src.server import list_presets

        client = _mock_client("Preset 2.1")
        mock_get.return_value = client

        result = await list_presets(preset_type="position")

        client.send_command_with_response.assert_called_once_with(
            'list preset "position"'
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_presets_with_id(self, mock_get):
        from src.server import list_presets

        client = _mock_client("Preset 4.1 'Red'")
        mock_get.return_value = client

        result = await list_presets(preset_type="color", preset_id=1)

        client.send_command_with_response.assert_called_once_with(
            'list preset "color".1'
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_presets_invalid_type(self, mock_get):
        from src.server import list_presets

        client = _mock_client()
        mock_get.return_value = client

        result = await list_presets(preset_type="invalid")

        client.send_command_with_response.assert_not_called()
        assert "invalid" in result.lower() or "valid" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_presets_empty_response(self, mock_get):
        from src.server import list_presets

        client = _mock_client("")
        mock_get.return_value = client

        result = await list_presets(preset_type="gobo")

        assert "no data" in result.lower() or "empty" in result.lower()


# ============================================================
# get_cue_info
# ============================================================


class TestGetCueInfoTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_get_cue_info_basic(self, mock_get):
        from src.server import get_cue_info

        client = _mock_client("Cue 3: Fade 2s")
        mock_get.return_value = client

        result = await get_cue_info(cue_id=3)

        client.send_command_with_response.assert_called_once_with("info cue 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_get_cue_info_with_sequence(self, mock_get):
        from src.server import get_cue_info

        client = _mock_client("Cue 3 Seq 1")
        mock_get.return_value = client

        result = await get_cue_info(cue_id=3, sequence_id=1)

        client.send_command_with_response.assert_called_once_with(
            "info cue 3 sequence 1"
        )

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_get_cue_info_empty_response(self, mock_get):
        from src.server import get_cue_info

        client = _mock_client("")
        mock_get.return_value = client

        result = await get_cue_info(cue_id=99)

        assert "no data" in result.lower() or "empty" in result.lower()


# ============================================================
# get_group_info
# ============================================================


class TestGetGroupInfoTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_get_group_info_basic(self, mock_get):
        from src.server import get_group_info

        client = _mock_client("Group 5: Front Wash fixtures")
        mock_get.return_value = client

        result = await get_group_info(group_id=5)

        client.send_command_with_response.assert_called_once_with("info group 5")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_get_group_info_empty_response(self, mock_get):
        from src.server import get_group_info

        client = _mock_client("")
        mock_get.return_value = client

        result = await get_group_info(group_id=99)

        assert "no data" in result.lower() or "empty" in result.lower()


# ============================================================
# list_variables
# ============================================================


class TestListVariablesTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_show_variables(self, mock_get):
        from src.server import list_variables

        client = _mock_client("MYVAR=100\nOTHER=200")
        mock_get.return_value = client

        result = await list_variables(variable_type="show")

        client.send_command_with_response.assert_called_once_with("listvar")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_user_variables(self, mock_get):
        from src.server import list_variables

        client = _mock_client("USERVAR=50")
        mock_get.return_value = client

        result = await list_variables(variable_type="user")

        client.send_command_with_response.assert_called_once_with("listuservar")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_variables_with_filter(self, mock_get):
        from src.server import list_variables

        client = _mock_client("FADE_TIME=3")
        mock_get.return_value = client

        result = await list_variables(variable_type="show", filter="f*")

        client.send_command_with_response.assert_called_once_with("listvar f*")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_user_variables_with_filter(self, mock_get):
        from src.server import list_variables

        client = _mock_client("MY_VAR=10")
        mock_get.return_value = client

        result = await list_variables(variable_type="user", filter="my_*")

        client.send_command_with_response.assert_called_once_with("listuservar my_*")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_variables_invalid_type(self, mock_get):
        from src.server import list_variables

        client = _mock_client()
        mock_get.return_value = client

        result = await list_variables(variable_type="invalid")

        client.send_command_with_response.assert_not_called()
        assert "show" in result.lower() and "user" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_variables_empty_response(self, mock_get):
        from src.server import list_variables

        client = _mock_client("")
        mock_get.return_value = client

        result = await list_variables(variable_type="show")

        assert "no data" in result.lower() or "empty" in result.lower()


# ============================================================
# query_object
# ============================================================


class TestQueryObjectTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_mode(self, mock_get):
        from src.server import query_object

        client = _mock_client("Executor 1\nExecutor 2")
        mock_get.return_value = client

        result = await query_object(object_type="executor", mode="list")

        client.send_command_with_response.assert_called_once_with("list executor")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_info_mode(self, mock_get):
        from src.server import query_object

        client = _mock_client("Sequence 1 details")
        mock_get.return_value = client

        result = await query_object(
            object_type="sequence", object_id=1, mode="info"
        )

        client.send_command_with_response.assert_called_once_with("info sequence 1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_default_mode_is_list(self, mock_get):
        from src.server import query_object

        client = _mock_client("Effect 1")
        mock_get.return_value = client

        result = await query_object(object_type="effect")

        client.send_command_with_response.assert_called_once_with("list effect")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_with_id(self, mock_get):
        from src.server import query_object

        client = _mock_client("Sequence 1")
        mock_get.return_value = client

        result = await query_object(object_type="sequence", object_id=1)

        client.send_command_with_response.assert_called_once_with("list sequence 1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_empty_response(self, mock_get):
        from src.server import query_object

        client = _mock_client("")
        mock_get.return_value = client

        result = await query_object(object_type="effect")

        assert "no data" in result.lower() or "empty" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_connection_error(self, mock_get):
        from src.server import query_object

        client = _mock_client()
        client.send_command_with_response.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await query_object(object_type="executor")

        assert "Connection lost" in result
