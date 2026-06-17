"""
MCP tool tests for P1 features: MAtricks (#41), cue timing (#42),
flash/swop/stomp/temp (#43), update cue (#44).
"""

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


def _calls(client):
    return [c[0][0] for c in client.execute.call_args_list]


class TestMAtricks:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_blocks_and_wings(self, mock_get):
        from src.server import set_matricks

        client = _mock_client()
        mock_get.return_value = client

        await set_matricks(blocks=4, wings=2)

        calls = _calls(client)
        assert calls[0] == "matricks"
        assert "matricksblocks 4" in calls
        assert "matrickswings 2" in calls

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_no_params_errors(self, mock_get):
        from src.server import set_matricks

        client = _mock_client()
        mock_get.return_value = client

        result = await set_matricks()

        assert "at least one" in result.lower()
        client.execute.assert_not_called()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_reset(self, mock_get):
        from src.server import reset_matricks

        client = _mock_client()
        mock_get.return_value = client

        await reset_matricks()

        client.execute.assert_called_once_with("matricksreset")


class TestCueTiming:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_fade_and_delay_with_target(self, mock_get):
        from src.server import set_cue_timing

        client = _mock_client()
        mock_get.return_value = client

        await set_cue_timing(fade=3, delay=1, target="cue 5")

        calls = _calls(client)
        assert "fade 3 cue 5" in calls
        assert "delay 1 cue 5" in calls

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_requires_a_value(self, mock_get):
        from src.server import set_cue_timing

        client = _mock_client()
        mock_get.return_value = client

        result = await set_cue_timing()

        assert "at least one" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_step_timing(self, mock_get):
        from src.server import set_step_timing

        client = _mock_client()
        mock_get.return_value = client

        await set_step_timing(snap_percent=50, step_fade=2)

        calls = _calls(client)
        assert "snappercent 50" in calls
        assert "stepfade 2" in calls


class TestBusking:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_flash_default(self, mock_get):
        from src.server import flash_executor

        client = _mock_client()
        mock_get.return_value = client

        await flash_executor(3)

        client.execute.assert_called_once_with("flash executor 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_flash_go_with_page(self, mock_get):
        from src.server import flash_executor

        client = _mock_client()
        mock_get.return_value = client

        await flash_executor(3, page=2, mode="flash_go")

        client.execute.assert_called_once_with("flashgo executor 2.3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_swop_on(self, mock_get):
        from src.server import swop_executor

        client = _mock_client()
        mock_get.return_value = client

        await swop_executor(1, mode="swop_on")

        client.execute.assert_called_once_with("swopon executor 1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_unknown_mode(self, mock_get):
        from src.server import flash_executor

        client = _mock_client()
        mock_get.return_value = client

        result = await flash_executor(1, mode="bogus")

        assert "Unknown mode" in result
        client.execute.assert_not_called()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_stomp_and_temp(self, mock_get):
        from src.server import stomp_executor, temp_executor

        client = _mock_client()
        mock_get.return_value = client

        await stomp_executor(5)
        await temp_executor(6, page=1)

        calls = _calls(client)
        assert "stomp executor 5" in calls
        assert "temp executor 1.6" in calls


class TestUpdateCue:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_basic(self, mock_get):
        from src.server import update_cue

        client = _mock_client()
        mock_get.return_value = client

        await update_cue(3)

        client.execute.assert_called_once_with("update cue 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_with_sequence_and_flags(self, mock_get):
        from src.server import update_cue

        client = _mock_client()
        mock_get.return_value = client

        await update_cue(3, sequence_id=2, merge=True, cueonly=True)

        cmd = client.execute.call_args[0][0]
        assert cmd.startswith("update cue 3 sequence 2")
        assert "/merge" in cmd
        assert "/cueonly" in cmd

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_surfaces_error(self, mock_get):
        from src.server import update_cue
        from src.execution import ExecutionResult

        client = _mock_client()
        client.execute = AsyncMock(
            return_value=ExecutionResult(
                ok=False, echo="", error_code=2, error_text="NO CUE", raw=""
            )
        )
        mock_get.return_value = client

        result = await update_cue(99)

        assert "Error #2" in result


class TestSetupFanEffectWorkflow:
    @pytest.mark.asyncio
    async def test_sends_matricks_then_params(self):
        from src.gma2_client import GMA2Client

        client = MagicMock()
        client.send_command = AsyncMock()
        gma2 = GMA2Client(client)

        result = await gma2.setup_fan_effect(blocks=4, wings=2)

        assert result["commands_sent"][0] == "matricks"
        assert "matricksblocks 4" in result["commands_sent"]
        assert "matrickswings 2" in result["commands_sent"]
