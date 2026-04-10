import pytest
from unittest.mock import patch, AsyncMock, MagicMock


def _mock_client():
    client = MagicMock()
    client.send_command = AsyncMock()
    return client


class TestStoreCueTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_cue_basic(self, mock_get):
        from src.server import store_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await store_cue(cue_id=1)

        client.send_command.assert_called_once_with("store cue 1")
        assert "Cue 1" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_cue_with_name_and_merge(self, mock_get):
        from src.server import store_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await store_cue(cue_id=5, name="Blackout", merge=True)

        client.send_command.assert_called_once_with('store cue 5 "Blackout" /merge')
        assert "Blackout" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_cue_overwrite_noconfirm(self, mock_get):
        from src.server import store_cue

        client = _mock_client()
        mock_get.return_value = client

        await store_cue(cue_id=3, overwrite=True, noconfirm=True)

        cmd = client.send_command.call_args[0][0]
        assert "/overwrite" in cmd
        assert "/noconfirm" in cmd


class TestDeleteCueTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_cue(self, mock_get):
        from src.server import delete_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_cue(cue_id=3)

        client.send_command.assert_called_once_with("delete cue 3")
        assert "Cue 3" in result


class TestGotoCueTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_goto_cue_with_executor(self, mock_get):
        from src.server import goto_cue_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await goto_cue_tool(cue_id=5, executor=4)

        client.send_command.assert_called_once_with("goto cue 5 executor 4")
        assert "Cue 5" in result
        assert "Executor 4" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_goto_cue_with_sequence(self, mock_get):
        from src.server import goto_cue_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await goto_cue_tool(cue_id=3, sequence=1)

        client.send_command.assert_called_once_with("goto cue 3 sequence 1")
        assert "Sequence 1" in result


class TestSetFixtureValueTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_single_fixture(self, mock_get):
        from src.server import set_fixture_value

        client = _mock_client()
        mock_get.return_value = client

        result = await set_fixture_value(fixture_id=1, value=75)

        client.send_command.assert_called_once_with("fixture 1 at 75")
        assert "75" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_fixture_range(self, mock_get):
        from src.server import set_fixture_value

        client = _mock_client()
        mock_get.return_value = client

        result = await set_fixture_value(fixture_id=1, value=50, end_fixture=10)

        client.send_command.assert_called_once_with("fixture 1 thru 10 at 50")
        assert "thru 10" in result


class TestSetFixtureAttributeTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_attribute_on_fixture(self, mock_get):
        from src.server import set_fixture_attribute

        client = _mock_client()
        mock_get.return_value = client

        result = await set_fixture_attribute(fixture_id=1, attribute="Pan", value=128)

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "fixture 1"
        assert calls[1] == 'attribute "Pan" at 128'
        assert "Pan" in result


class TestClearProgrammerTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_clear_all(self, mock_get):
        from src.server import clear_programmer

        client = _mock_client()
        mock_get.return_value = client

        result = await clear_programmer(mode="all")

        client.send_command.assert_called_once_with("clearall")
        assert "all" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_clear_selection(self, mock_get):
        from src.server import clear_programmer

        client = _mock_client()
        mock_get.return_value = client

        await clear_programmer(mode="selection")

        client.send_command.assert_called_once_with("clearselection")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_clear_default(self, mock_get):
        from src.server import clear_programmer

        client = _mock_client()
        mock_get.return_value = client

        await clear_programmer(mode="default")

        client.send_command.assert_called_once_with("clear")


class TestStorePresetTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_color_preset(self, mock_get):
        from src.server import store_preset

        client = _mock_client()
        mock_get.return_value = client

        result = await store_preset(preset_type="color", preset_id=1)

        client.send_command.assert_called_once_with("store preset 4.1")
        assert "color" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_global_dimmer_preset(self, mock_get):
        from src.server import store_preset

        client = _mock_client()
        mock_get.return_value = client

        result = await store_preset(preset_type="dimmer", preset_id=5, scope="global")

        client.send_command.assert_called_once_with("store preset 1.5 /global")
        assert "global" in result


class TestApplyPresetTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_apply_color_preset(self, mock_get):
        from src.server import apply_preset

        client = _mock_client()
        mock_get.return_value = client

        result = await apply_preset(preset_type="color", preset_id=3)

        client.send_command.assert_called_once_with("preset 4.3")
        assert "color" in result


class TestControlExecutorTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_executor_on(self, mock_get):
        from src.server import control_executor

        client = _mock_client()
        mock_get.return_value = client

        result = await control_executor(executor_id=1, action="on")

        client.send_command.assert_called_once_with("on executor 1")
        assert "on" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_executor_off(self, mock_get):
        from src.server import control_executor

        client = _mock_client()
        mock_get.return_value = client

        await control_executor(executor_id=3, action="off")

        client.send_command.assert_called_once_with("off executor 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_executor_go(self, mock_get):
        from src.server import control_executor

        client = _mock_client()
        mock_get.return_value = client

        await control_executor(executor_id=2, action="go")

        client.send_command.assert_called_once_with("go executor 2")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_executor_kill(self, mock_get):
        from src.server import control_executor

        client = _mock_client()
        mock_get.return_value = client

        await control_executor(executor_id=3, action="kill")

        client.send_command.assert_called_once_with("kill executor 3")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_executor_unknown_action(self, mock_get):
        from src.server import control_executor

        client = _mock_client()
        mock_get.return_value = client

        result = await control_executor(executor_id=1, action="invalid")

        client.send_command.assert_not_called()
        assert "Unknown" in result


class TestSetExecutorFaderTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_fader(self, mock_get):
        from src.server import set_executor_fader

        client = _mock_client()
        mock_get.return_value = client

        result = await set_executor_fader(executor_id=1, value=75)

        client.send_command.assert_called_once_with("executor 1 at 75")
        assert "75" in result


class TestAssignToExecutorTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_assign_sequence(self, mock_get):
        from src.server import assign_to_executor

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_to_executor(sequence_id=1, executor_id=6)

        client.send_command.assert_called_once_with("assign sequence 1 at executor 6")
        assert "Sequence 1" in result
        assert "Executor 6" in result


class TestToggleBlackoutTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_toggle_blackout(self, mock_get):
        from src.server import toggle_blackout

        client = _mock_client()
        mock_get.return_value = client

        result = await toggle_blackout()

        client.send_command.assert_called_once_with("blackout")
        assert "Blackout" in result


class TestToggleHighlightTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_toggle_highlight(self, mock_get):
        from src.server import toggle_highlight

        client = _mock_client()
        mock_get.return_value = client

        result = await toggle_highlight()

        client.send_command.assert_called_once_with("highlight")
        assert "Highlight" in result


class TestLabelObjectTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_group(self, mock_get):
        from src.server import label_object

        client = _mock_client()
        mock_get.return_value = client

        result = await label_object(object_type="group", object_id=1, name="Front Wash")

        client.send_command.assert_called_once_with('label group 1 "Front Wash"')
        assert "Front Wash" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_cue(self, mock_get):
        from src.server import label_object

        client = _mock_client()
        mock_get.return_value = client

        result = await label_object(object_type="cue", object_id=5, name="Intro")

        client.send_command.assert_called_once_with('label cue 5 "Intro"')
