"""
Tests for store_preset merge/overwrite flags and the build_color_palette
workflow (Issue #72).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _exec_client():
    from src.execution import ExecutionResult

    client = MagicMock()
    client.send_command = AsyncMock()
    client.execute = AsyncMock(
        return_value=ExecutionResult(ok=True, echo="OK", error_code=None, error_text=None, raw="OK")
    )
    return client


class TestStorePresetMerge:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_merge_flag(self, mock_get):
        from src.server import store_preset

        client = _exec_client()
        mock_get.return_value = client

        await store_preset("color", 1, scope="global", merge=True)

        client.execute.assert_called_once_with("store preset 4.1 /global /noconfirm /merge")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_overwrite_flag(self, mock_get):
        from src.server import store_preset

        client = _exec_client()
        mock_get.return_value = client

        await store_preset("color", 2, scope="global", overwrite=True)

        client.execute.assert_called_once_with("store preset 4.2 /global /noconfirm /overwrite")


class TestBuildColorPaletteWorkflow:
    @pytest.mark.asyncio
    async def test_programs_one_color_with_merge(self):
        from src.gma2_client import GMA2Client

        client = _exec_client()
        gma2 = GMA2Client(client)

        result = await gma2.build_color_palette(
            "Group 3",
            [{"id": 7, "name": "Red", "r": 100, "g": 0, "b": 0, "w": 0}],
            scope="global",
            merge=True,
        )

        sent = result["commands_sent"]
        assert "Group 3" in sent
        assert 'attribute "COLORRGB1" at 100' in sent
        assert 'attribute "COLORRGB2" at 0' in sent
        assert 'attribute "COLORRGB3" at 0' in sent
        assert 'attribute "COLORRGB5" at 0' in sent
        assert "store preset 4.7 /global /noconfirm /merge" in sent
        assert 'label preset 4.7 "Red"' in sent
        assert "appearance preset 4.7 /r=100 /g=0 /b=0" in sent

    @pytest.mark.asyncio
    async def test_white_swatch_uses_white_channel(self):
        from src.gma2_client import GMA2Client

        client = _exec_client()
        gma2 = GMA2Client(client)

        result = await gma2.build_color_palette(
            "Group 3",
            [{"id": 2, "name": "White", "r": 0, "g": 0, "b": 0, "w": 100}],
        )
        # W lifts the swatch to white (0-100 scale)
        assert "appearance preset 4.2 /r=100 /g=100 /b=100" in result["commands_sent"]

    @pytest.mark.asyncio
    async def test_no_appearance_or_label(self):
        from src.gma2_client import GMA2Client

        client = _exec_client()
        gma2 = GMA2Client(client)

        result = await gma2.build_color_palette(
            "Group 3",
            [{"id": 7, "r": 100, "g": 0, "b": 0}],
            label=False,
            appearance=False,
        )
        assert not any(s.startswith("label") for s in result["commands_sent"])
        assert not any(s.startswith("appearance") for s in result["commands_sent"])


class TestBuildColorPaletteTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_tool_delegates(self, mock_get):
        from src.server import build_color_palette

        client = _exec_client()
        mock_get.return_value = client

        result = await build_color_palette(
            "Group 4",
            [{"id": 7, "name": "Red", "r": 100, "g": 0, "b": 0}],
            merge=True,
        )

        assert "1" in result  # count in summary
        # selection + store were sent through the client
        sent = [c[0][0] for c in client.send_command.call_args_list]
        assert "Group 4" in sent
