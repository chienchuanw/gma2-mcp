"""
MCP tool tests for P3 wrapper features: copy/move (#49), extended delete (#50),
effect extensions (#51), park/unpark (#52), advanced selection (#54).
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


def _calls(client):
    return [c[0][0] for c in client.execute.call_args_list]


class TestCopyMove:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_copy_single(self, mock_get):
        from src.server import copy_object

        client = _mock_client()
        mock_get.return_value = client

        await copy_object("cue", "1", "10")

        client.execute.assert_called_once_with("copy cue 1 at 10")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_move_range_in_one_call(self, mock_get):
        from src.server import move_object

        client = _mock_client()
        mock_get.return_value = client

        result = await move_object("group", "1 thru 10", "21")

        client.execute.assert_called_once_with("move group 1 thru 10 at 21")
        assert "removed from source" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_copy_overwrite(self, mock_get):
        from src.server import copy_object

        client = _mock_client()
        mock_get.return_value = client

        await copy_object("preset", "4.1", "4.5", mode="overwrite")

        assert "/overwrite" in client.execute.call_args[0][0]

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_invalid_selector_rejected(self, mock_get):
        from src.server import copy_object

        client = _mock_client()
        mock_get.return_value = client

        result = await copy_object("cue", "1; delete group 1", "10")

        assert "Invalid selector" in result
        client.execute.assert_not_called()


class TestExtendedDelete:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_group(self, mock_get):
        from src.server import delete_group

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_group(1)

        client.execute.assert_called_once_with("delete group 1")
        assert "⚠ Warnings:" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_preset(self, mock_get):
        from src.server import delete_preset

        client = _mock_client()
        mock_get.return_value = client

        await delete_preset("color", 1)

        client.execute.assert_called_once_with("delete preset 4.1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_fixture(self, mock_get):
        from src.server import delete_fixture

        client = _mock_client()
        mock_get.return_value = client

        await delete_fixture(5)

        client.execute.assert_called_once_with("delete fixture 5")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_show(self, mock_get):
        from src.server import delete_show

        client = _mock_client()
        mock_get.return_value = client

        await delete_show("Old")

        client.execute.assert_called_once_with("deleteshow Old")


class TestEffectExtensions:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_envelope(self, mock_get):
        from src.server import set_effect_envelope

        client = _mock_client()
        mock_get.return_value = client

        await set_effect_envelope(attack=5, fade=3)

        calls = _calls(client)
        assert "effectattack 5" in calls
        assert "effectfade 3" in calls

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_envelope_requires_param(self, mock_get):
        from src.server import set_effect_envelope

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_envelope()

        assert "at least one" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_seconds_and_speed_group(self, mock_get):
        from src.server import set_effect_seconds, set_effect_speed_group

        client = _mock_client()
        mock_get.return_value = client

        await set_effect_seconds(2)
        await set_effect_speed_group(1)

        calls = _calls(client)
        assert "effectsec 2" in calls
        assert "effectspeedgroup 1" in calls


class TestParkUnpark:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_park_at_value(self, mock_get):
        from src.server import park_fixture

        client = _mock_client()
        mock_get.return_value = client

        await park_fixture("fixture 1", at_value=50)

        client.execute.assert_called_once_with("park fixture 1 at 50")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_unpark(self, mock_get):
        from src.server import unpark_fixture

        client = _mock_client()
        mock_get.return_value = client

        await unpark_fixture("fixture 1")

        client.execute.assert_called_once_with("unpark fixture 1")


class TestAdvancedSelection:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_next_previous_invert_locate(self, mock_get):
        from src.server import (
            invert_selection,
            locate_fixtures,
            next_fixture,
            previous_fixture,
        )

        client = _mock_client()
        mock_get.return_value = client

        await next_fixture()
        await previous_fixture()
        await invert_selection()
        await locate_fixtures()

        calls = _calls(client)
        assert calls == ["next", "previous", "invert", "locate"]

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_align_and_fix(self, mock_get):
        from src.server import align_selection, fix_selection

        client = _mock_client()
        mock_get.return_value = client

        await align_selection()
        await fix_selection()

        calls = _calls(client)
        assert "align" in calls
        assert "fix" in calls
