"""
MCP tool tests for variable write tools (Issue #40).

set_variable, set_user_variable, add_variable, add_user_variable.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _mock_client():
    from src.execution import ExecutionResult

    client = MagicMock()
    client.execute = AsyncMock(
        return_value=ExecutionResult(ok=True, echo="OK", error_code=None, error_text=None, raw="OK")
    )
    return client


class TestSetVariable:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_numeric(self, mock_get):
        from src.server import set_variable

        client = _mock_client()
        mock_get.return_value = client

        result = await set_variable("$count", 5)

        client.execute.assert_called_once_with("setvar $count = 5")
        assert "$count" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_text(self, mock_get):
        from src.server import set_variable

        client = _mock_client()
        mock_get.return_value = client

        await set_variable("$name", "John")

        client.execute.assert_called_once_with('setvar $name = "John"')

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_with_none(self, mock_get):
        from src.server import set_variable

        client = _mock_client()
        mock_get.return_value = client

        await set_variable("$count", None)

        client.execute.assert_called_once_with("setvar $count =")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_input_dialog(self, mock_get):
        from src.server import set_variable

        client = _mock_client()
        mock_get.return_value = client

        await set_variable("$song", "Which song?", input_dialog=True)

        client.execute.assert_called_once_with('setvar $song = ("Which song?")')


class TestSetUserVariable:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_numeric(self, mock_get):
        from src.server import set_user_variable

        client = _mock_client()
        mock_get.return_value = client

        await set_user_variable("$count", 7)

        client.execute.assert_called_once_with("setuservar $count = 7")


class TestAddVariable:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_numeric(self, mock_get):
        from src.server import add_variable

        client = _mock_client()
        mock_get.return_value = client

        await add_variable("$count", 6)

        client.execute.assert_called_once_with("addvar $count = 6")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_surfaces_error(self, mock_get):
        from src.execution import ExecutionResult
        from src.server import add_variable

        client = _mock_client()
        client.execute = AsyncMock(
            return_value=ExecutionResult(ok=False, echo="", error_code=3, error_text="BAD", raw="")
        )
        mock_get.return_value = client

        result = await add_variable("$count", 6)

        assert "Error #3" in result


class TestAddUserVariable:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_text_concat(self, mock_get):
        from src.server import add_user_variable

        client = _mock_client()
        mock_get.return_value = client

        await add_user_variable("$name", " Doe")

        client.execute.assert_called_once_with('adduservar $name = " Doe"')
