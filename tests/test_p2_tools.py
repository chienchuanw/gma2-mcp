"""
MCP tool tests for P2 features: blind/preview (#45), clone (#46),
rate/speed (#47), release/top (#48).
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client():
    from src.execution import ExecutionResult

    client = MagicMock()
    client.send_command = AsyncMock()
    client.execute = AsyncMock(
        return_value=ExecutionResult(
            ok=True, echo="OK", error_code=None, error_text=None, raw="OK"
        )
    )
    return client


class TestBlindPreview:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_blind_global(self, mock_get):
        from src.server import toggle_blind

        client = _mock_client()
        mock_get.return_value = client

        await toggle_blind()

        client.execute.assert_called_once_with("blind")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_blind_executor(self, mock_get):
        from src.server import toggle_blind

        client = _mock_client()
        mock_get.return_value = client

        await toggle_blind(executor_id=3, page=2)

        client.execute.assert_called_once_with("blind executor 2.3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_blind_edit_mode(self, mock_get):
        from src.server import toggle_blind

        client = _mock_client()
        mock_get.return_value = client

        await toggle_blind(edit_mode=True)

        client.execute.assert_called_once_with("blindedit")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_preview_global(self, mock_get):
        from src.server import toggle_preview

        client = _mock_client()
        mock_get.return_value = client

        await toggle_preview()

        client.execute.assert_called_once_with("preview")


class TestCloneFixtures:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_single(self, mock_get):
        from src.server import clone_fixtures

        client = _mock_client()
        mock_get.return_value = client

        result = await clone_fixtures(1, 5)

        cmd = client.send_command.call_args[0][0]
        assert cmd.startswith("clone fixture 1 at fixture 5")
        assert "Cloned" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_range_overwrite(self, mock_get):
        from src.server import clone_fixtures

        client = _mock_client()
        mock_get.return_value = client

        await clone_fixtures(1, 11, source_end=10, target_end=20, mode="overwrite")

        cmd = client.send_command.call_args[0][0]
        assert "thru 10" in cmd
        assert "thru 20" in cmd
        assert "/overwrite" in cmd


class TestRateSpeed:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_rate_double(self, mock_get):
        from src.server import set_executor_rate

        client = _mock_client()
        mock_get.return_value = client

        await set_executor_rate(1, mode="double")

        client.execute.assert_called_once_with("doublerate executor 1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_rate_reset(self, mock_get):
        from src.server import set_executor_rate

        client = _mock_client()
        mock_get.return_value = client

        await set_executor_rate(1, mode="reset")

        client.execute.assert_called_once_with("rate1 executor 1")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_speed_half(self, mock_get):
        from src.server import set_executor_speed

        client = _mock_client()
        mock_get.return_value = client

        await set_executor_speed(2, mode="half", page=1)

        client.execute.assert_called_once_with("halfspeed executor 1.2")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_rate_unknown_mode(self, mock_get):
        from src.server import set_executor_rate

        client = _mock_client()
        mock_get.return_value = client

        result = await set_executor_rate(1, mode="bogus")

        assert "Unknown mode" in result
        client.execute.assert_not_called()


class TestReleaseTop:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_release(self, mock_get):
        from src.server import release_executor

        client = _mock_client()
        mock_get.return_value = client

        await release_executor(3)

        client.execute.assert_called_once_with("release executor 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_top_with_page(self, mock_get):
        from src.server import top_executor

        client = _mock_client()
        mock_get.return_value = client

        await top_executor(3, page=2)

        client.execute.assert_called_once_with("top executor 2.3")
