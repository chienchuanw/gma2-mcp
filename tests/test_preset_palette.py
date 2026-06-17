"""
Tests for the generalized build_preset_palette workflow (#79).
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _client():
    from src.execution import ExecutionResult

    c = MagicMock()
    c.send_command = AsyncMock()
    c.execute = AsyncMock(
        return_value=ExecutionResult(
            ok=True, echo="OK", error_code=None, error_text=None, raw="OK"
        )
    )
    return c


class TestBuildPresetPalette:
    @pytest.mark.asyncio
    async def test_single_target_preset(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "beam",
            [{"id": 1, "name": "Open", "by_target": [
                {"target": "Fixture 401 Thru 428", "attrs": [("SHUTTER", 0)]},
            ]}],
            scope="global",
        )
        sent = result["commands_sent"]
        assert "Clear" in sent
        assert "Fixture 401 Thru 428" in sent
        assert 'attribute "SHUTTER" at 0' in sent
        assert "store preset 5.1 /global /noconfirm" in sent
        assert 'label preset 5.1 "Open"' in sent

    @pytest.mark.asyncio
    async def test_multi_target_merges_subsequent(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "beam",
            [{"id": 3, "name": "Strobe", "by_target": [
                {"target": "Fixture 401 Thru 428", "attrs": [("SHUTTER", 50)]},
                {"target": "Fixture 201 Thru 215", "attrs": [("MASTERSHUTTERSTROBE", 21)]},
            ]}],
            scope="global",
        )
        sent = result["commands_sent"]
        # first target: plain store; second target: merge
        assert "store preset 5.3 /global /noconfirm" in sent
        assert "store preset 5.3 /global /noconfirm /merge" in sent
        assert 'attribute "MASTERSHUTTERSTROBE" at 21' in sent

    @pytest.mark.asyncio
    async def test_selective_scope(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "focus",
            [{"id": 1, "name": "V.Narrow", "by_target": [
                {"target": "Fixture 101 Thru 128", "attrs": [("ZOOM", 0), ("FOCUS", 100)]},
            ]}],
            scope="selective",
        )
        sent = result["commands_sent"]
        assert "store preset 6.1 /selective /noconfirm" in sent
        assert 'attribute "ZOOM" at 0' in sent
        assert 'attribute "FOCUS" at 100' in sent

    @pytest.mark.asyncio
    async def test_extend_merge_first_target(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "beam",
            [{"id": 1, "name": "Open", "by_target": [
                {"target": "Group 4", "attrs": [("SHUTTER", 41)]},
            ]}],
            scope="global",
            merge=True,
        )
        # first (only) target merges into the existing preset
        assert "store preset 5.1 /global /noconfirm /merge" in result["commands_sent"]

    @pytest.mark.asyncio
    async def test_label_off(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "beam",
            [{"id": 1, "name": "Open", "by_target": [
                {"target": "Group 1", "attrs": [("SHUTTER", 0)]},
            ]}],
            label=False,
        )
        assert not any(s.startswith("label") for s in result["commands_sent"])

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_mcp_tool_delegates(self, mock_get):
        from src.server import build_preset_palette

        mock_get.return_value = _client()
        result = await build_preset_palette(
            "beam",
            [{"id": 1, "name": "Open", "by_target": [
                {"target": "Group 1", "attrs": [["SHUTTER", 0]]},
            ]}],
        )
        assert "1" in result  # count in summary


class TestCommandOrder:
    @pytest.mark.asyncio
    async def test_per_target_sequence_order(self):
        from src.gma2_client import GMA2Client

        gma2 = GMA2Client(_client())
        result = await gma2.build_preset_palette(
            "beam",
            [{"id": 1, "name": "Open", "by_target": [
                {"target": "Group 1", "attrs": [("SHUTTER", 0)]},
            ]}],
        )
        # Clear -> select -> set -> store -> label, in order
        assert result["commands_sent"] == [
            "Clear",
            "Group 1",
            'attribute "SHUTTER" at 0',
            "store preset 5.1 /global /noconfirm",
            'label preset 5.1 "Open"',
        ]
