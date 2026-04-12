"""
MCP tool tests for show file management tools (Issue #5).

Tests for save_show, load_show, new_show, and list_shows MCP tools.
Also includes negative tests verifying delete_show and create_backup
are NOT registered as MCP tools.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client(response=""):
    """create a mock client with both send_command and send_command_with_response."""
    client = MagicMock()
    client.send_command = AsyncMock()
    client.send_command_with_response = AsyncMock(return_value=response)
    return client


# ============================================================
# save_show
# ============================================================


class TestSaveShowTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_save_show_no_name(self, mock_get):
        from src.server import save_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await save_show_tool()

        client.send_command.assert_called_once_with("saveshow")
        assert "saved" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_save_show_with_name(self, mock_get):
        from src.server import save_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await save_show_tool(show_name="MyShow")

        client.send_command.assert_called_once_with('saveshow "MyShow"')
        assert "MyShow" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_save_show_connection_error(self, mock_get):
        from src.server import save_show_tool

        client = _mock_client()
        client.send_command.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await save_show_tool()

        assert "Connection lost" in result


# ============================================================
# load_show
# ============================================================


class TestLoadShowTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_load_show_basic(self, mock_get):
        from src.server import load_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await load_show_tool(show_name="Macbeth")

        client.send_command.assert_called_once_with('loadshow "Macbeth" /noconfirm')
        assert "Macbeth" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_load_show_with_save_first(self, mock_get):
        from src.server import load_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await load_show_tool(show_name="Macbeth", save_first=True)

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "saveshow"
        assert calls[1] == 'loadshow "Macbeth" /noconfirm'

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_load_show_connection_error(self, mock_get):
        from src.server import load_show_tool

        client = _mock_client()
        client.send_command.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await load_show_tool(show_name="Macbeth")

        assert "Connection lost" in result


# ============================================================
# new_show
# ============================================================


class TestNewShowTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_new_show_with_name(self, mock_get):
        from src.server import new_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await new_show_tool(show_name="NewProject")

        client.send_command.assert_called_once_with('newshow "NewProject" /noconfirm')
        assert "NewProject" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_new_show_without_name(self, mock_get):
        from src.server import new_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await new_show_tool()

        client.send_command.assert_called_once_with("newshow /noconfirm")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_new_show_with_save_first(self, mock_get):
        from src.server import new_show_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await new_show_tool(show_name="NewProject", save_first=True)

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "saveshow"
        assert calls[1] == 'newshow "NewProject" /noconfirm'

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_new_show_connection_error(self, mock_get):
        from src.server import new_show_tool

        client = _mock_client()
        client.send_command.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await new_show_tool()

        assert "Connection lost" in result


# ============================================================
# list_shows
# ============================================================


class TestListShowsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_shows_no_filter(self, mock_get):
        from src.server import list_shows_tool

        client = _mock_client("show1.show.gz\nshow2.show.gz")
        mock_get.return_value = client

        result = await list_shows_tool()

        client.send_command_with_response.assert_called_once_with("listshows")
        assert "show1" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_shows_with_filter(self, mock_get):
        from src.server import list_shows_tool

        client = _mock_client("Macbeth.show.gz")
        mock_get.return_value = client

        result = await list_shows_tool(filter="Mac*")

        client.send_command_with_response.assert_called_once_with("listshows Mac*")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_shows_empty_response(self, mock_get):
        from src.server import list_shows_tool

        client = _mock_client("")
        mock_get.return_value = client

        result = await list_shows_tool()

        assert "no" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_shows_connection_error(self, mock_get):
        from src.server import list_shows_tool

        client = _mock_client()
        client.send_command_with_response.side_effect = ConnectionError("lost")
        mock_get.return_value = client

        result = await list_shows_tool()

        assert "Connection lost" in result


# ============================================================
# Negative tests: excluded tools
# ============================================================


class TestExcludedTools:
    def test_no_delete_show_tool(self):
        """delete_show must NOT be registered as an MCP tool."""
        import src.server as server

        assert not hasattr(server, "delete_show_tool")

    def test_no_create_backup_tool(self):
        """create_backup must NOT be registered as an MCP tool."""
        import src.server as server

        assert not hasattr(server, "create_backup")
        assert not hasattr(server, "create_backup_tool")
