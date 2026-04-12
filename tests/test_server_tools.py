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


class TestCreateFixtureGroupTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_create_fixture_group_with_name(self, mock_get):
        from src.server import create_fixture_group

        client = _mock_client()
        mock_get.return_value = client

        result = await create_fixture_group(
            start_fixture=1, end_fixture=10, group_id=1, group_name="Front Wash"
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert len(calls) == 2
        assert calls[0] == "selfix fixture 1 thru 10"
        assert calls[1] == 'store group 1 "Front Wash"'
        assert "Front Wash" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_create_fixture_group_without_name(self, mock_get):
        from src.server import create_fixture_group

        client = _mock_client()
        mock_get.return_value = client

        result = await create_fixture_group(
            start_fixture=1, end_fixture=10, group_id=1
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert len(calls) == 2
        assert calls[0] == "selfix fixture 1 thru 10"
        assert calls[1] == "store group 1"
        assert "Group 1" in result


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

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_cue_includes_warnings(self, mock_get):
        from src.server import delete_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_cue(cue_id=1)

        assert "⚠ Warnings:" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_cue_warnings_mention_executor_handles(self, mock_get):
        from src.server import delete_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_cue(cue_id=1)

        assert "executor" in result.lower()
        assert "missing cue" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_cue_warnings_mention_lost_programming(self, mock_get):
        from src.server import delete_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_cue(cue_id=1)

        assert "permanently lost" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_cue_still_sends_command(self, mock_get):
        from src.server import delete_cue

        client = _mock_client()
        mock_get.return_value = client

        await delete_cue(cue_id=5)

        client.send_command.assert_called_once_with("delete cue 5")


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


class TestAssignAppearanceTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_rgb(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="group", object_id=1, red=100, green=0, blue=0
        )

        client.send_command.assert_called_once_with(
            "appearance group 1 /r=100 /g=0 /b=0"
        )
        assert "group" in result
        assert "1" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_hex_color(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="preset", object_id="0.1", color="FF0000"
        )

        client.send_command.assert_called_once_with(
            "appearance preset 0.1 /color=FF0000"
        )
        assert "preset" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_hsb(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="cue",
            object_id=5,
            hue=240,
            saturation=100,
            brightness=50,
        )

        client.send_command.assert_called_once_with(
            "appearance cue 5 /h=240 /s=100 /br=50"
        )
        assert "cue" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_range(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="group", object_id=1, end=5, red=0, green=100, blue=0
        )

        client.send_command.assert_called_once_with(
            "appearance group 1 thru 5 /r=0 /g=100 /b=0"
        )
        assert "group" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_source_copy(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="macro",
            object_id=2,
            source_type="macro",
            source_id=13,
        )

        client.send_command.assert_called_once_with(
            "appearance macro 2 at macro 13"
        )
        assert "macro" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_reset(self, mock_get):
        from src.server import assign_appearance

        client = _mock_client()
        mock_get.return_value = client

        result = await assign_appearance(
            object_type="group", object_id=1, reset=True
        )

        client.send_command.assert_called_once_with(
            "appearance group 1 /reset"
        )
        assert "group" in result


class TestSetMacroLineTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_macro_line_basic(self, mock_get):
        from src.server import set_macro_line

        client = _mock_client()
        mock_get.return_value = client

        result = await set_macro_line(macro_id=101, line=1, command="SetVar $song='Opening+Childhood'")

        client.send_command.assert_called_once_with('assign macro 1.101.1 /cmd="SetVar $song=\'Opening+Childhood\'"')
        assert "Line 1" in result
        assert "Macro 101" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_macro_line_custom_pool(self, mock_get):
        from src.server import set_macro_line

        client = _mock_client()
        mock_get.return_value = client

        result = await set_macro_line(macro_id=50, line=3, command="Go Sequence 5", pool=2)

        client.send_command.assert_called_once_with('assign macro 2.50.3 /cmd="Go Sequence 5"')
        assert "50" in result


class TestLabelSequenceCueTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_sequence_cue_named(self, mock_get):
        from src.server import label_sequence_cue as label_sequence_cue_tool
        client = _mock_client()
        mock_get.return_value = client
        result = await label_sequence_cue_tool(sequence="Set List", cue_id=1, name="Opening+Childhood")
        client.send_command.assert_called_once_with('label sequence "Set List" cue 1 "Opening+Childhood"')
        assert "Opening+Childhood" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_sequence_cue_numbered(self, mock_get):
        from src.server import label_sequence_cue as label_sequence_cue_tool
        client = _mock_client()
        mock_get.return_value = client
        result = await label_sequence_cue_tool(sequence="100", cue_id=1, name="Opening+Childhood")
        client.send_command.assert_called_once_with('label sequence 100 cue 1 "Opening+Childhood"')
        assert "Opening+Childhood" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_sequence_cue_with_end_cue(self, mock_get):
        from src.server import label_sequence_cue as label_sequence_cue_tool
        client = _mock_client()
        mock_get.return_value = client
        result = await label_sequence_cue_tool(sequence="Set List", cue_id=1, name="Act 1", end_cue=5)
        client.send_command.assert_called_once_with('label sequence "Set List" cue 1 thru 5 "Act 1"')
        assert "thru 5" in result


class TestStoreCueAcrossSequencesTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_cue_across_sequences(self, mock_get):
        from src.server import store_cue_across_sequences

        client = _mock_client()
        mock_get.return_value = client

        result = await store_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=103,
            cue_name="((LOADING SONG))",
        )

        assert result["count"] == 3
        assert result["commands_sent"][0] == 'store sequence 101 cue 0.5 "((LOADING SONG))"'
        assert result["commands_sent"][2] == 'store sequence 103 cue 0.5 "((LOADING SONG))"'
        assert "3" in result["summary"]

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_store_cue_across_sequences_without_name(self, mock_get):
        from src.server import store_cue_across_sequences

        client = _mock_client()
        mock_get.return_value = client

        result = await store_cue_across_sequences(
            cue_id=1,
            sequence_start=101,
            sequence_end=101,
        )

        assert result["count"] == 1
        assert result["commands_sent"][0] == "store sequence 101 cue 1"


class TestLabelCueAcrossSequencesTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_cue_across_sequences(self, mock_get):
        from src.server import label_cue_across_sequences

        client = _mock_client()
        mock_get.return_value = client

        result = await label_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=103,
            label="((LOADING SONG))",
        )

        assert result["count"] == 3
        assert result["commands_sent"][0] == 'label sequence 101 cue 0.5 "((LOADING SONG))"'


class TestAppearanceCueAcrossSequencesTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_cue_across_sequences_rgb(self, mock_get):
        from src.server import appearance_cue_across_sequences

        client = _mock_client()
        mock_get.return_value = client

        result = await appearance_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=102,
            red=0,
            green=0,
            blue=0,
        )

        assert result["count"] == 2
        assert result["commands_sent"][0] == "appearance sequence 101 cue 0.5 /r=0 /g=0 /b=0"

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_appearance_cue_across_sequences_hex(self, mock_get):
        from src.server import appearance_cue_across_sequences

        client = _mock_client()
        mock_get.return_value = client

        result = await appearance_cue_across_sequences(
            cue_id=1,
            sequence_start=101,
            sequence_end=101,
            color="FF0000",
        )

        assert result["count"] == 1
        assert result["commands_sent"][0] == "appearance sequence 101 cue 1 /color=FF0000"


class TestSetCueCmdTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_cue_cmd_macro(self, mock_get):
        from src.server import set_cue_cmd

        client = _mock_client()
        mock_get.return_value = client

        result = await set_cue_cmd(cue_id=1, sequence_id=100, command="Macro 101")

        client.send_command.assert_called_once_with(
            'assign cue 1 sequence 100 /cmd="Macro 101"'
        )
        assert "Cue 1" in result
        assert "Sequence 100" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_cue_cmd_go(self, mock_get):
        from src.server import set_cue_cmd

        client = _mock_client()
        mock_get.return_value = client

        result = await set_cue_cmd(cue_id=5, sequence_id=200, command="Go Sequence 10")

        client.send_command.assert_called_once_with(
            'assign cue 5 sequence 200 /cmd="Go Sequence 10"'
        )
        assert "Cue 5" in result


class TestRunMacroTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_run_macro_default_pool(self, mock_get):
        from src.server import run_macro

        client = _mock_client()
        mock_get.return_value = client

        result = await run_macro(macro_id=5)

        client.send_command.assert_called_once_with("go+ macro 1.5")
        assert "Macro 5" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_run_macro_custom_pool(self, mock_get):
        from src.server import run_macro

        client = _mock_client()
        mock_get.return_value = client

        result = await run_macro(macro_id=10, pool=2)

        client.send_command.assert_called_once_with("go+ macro 2.10")
        assert "10" in result


class TestCreateMacroTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_create_macro_with_commands(self, mock_get):
        from src.server import create_macro

        client = _mock_client()
        mock_get.return_value = client

        result = await create_macro(
            macro_id=10, commands=["Go Sequence 1", "Go Sequence 2"]
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "store macro 10"
        assert calls[1] == 'assign macro 1.10.1 /cmd="Go Sequence 1"'
        assert calls[2] == 'assign macro 1.10.2 /cmd="Go Sequence 2"'
        assert "2 lines" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_create_macro_with_name(self, mock_get):
        from src.server import create_macro

        client = _mock_client()
        mock_get.return_value = client

        result = await create_macro(
            macro_id=10, commands=["Go Sequence 1"], name="Start Show"
        )

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert calls[0] == "store macro 10"
        assert calls[1] == 'assign macro 1.10.1 /cmd="Go Sequence 1"'
        assert calls[2] == 'label macro 10 "Start Show"'
        assert "Start Show" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_create_macro_empty_commands(self, mock_get):
        from src.server import create_macro

        client = _mock_client()
        mock_get.return_value = client

        result = await create_macro(macro_id=10, commands=[])

        client.send_command.assert_not_called()
        assert "at least one command" in result.lower()


class TestLabelMacroTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_label_macro(self, mock_get):
        from src.server import label_macro_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await label_macro_tool(macro_id=5, name="Blackout All")

        client.send_command.assert_called_once_with('label macro 5 "Blackout All"')
        assert "Macro 5" in result
        assert "Blackout All" in result


class TestListMacrosTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_list_macros(self, mock_get):
        from src.server import list_macros

        client = _mock_client()
        client.send_command_with_response = AsyncMock(return_value="Macro 1: Test")
        mock_get.return_value = client

        result = await list_macros()

        client.send_command_with_response.assert_called_once()
        assert "Macro 1: Test" in result


class TestDeleteMacroTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_macro(self, mock_get):
        from src.server import delete_macro_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_macro_tool(macro_id=5)

        client.send_command.assert_called_once_with("delete macro 1.5 /noconfirm")
        assert "Macro 5" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_delete_macro_includes_warnings(self, mock_get):
        from src.server import delete_macro_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await delete_macro_tool(macro_id=5)

        assert "⚠ Warnings:" in result


class TestApplyEffectTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_apply_effect(self, mock_get):
        from src.server import apply_effect

        client = _mock_client()
        mock_get.return_value = client

        result = await apply_effect(effect_id=5)

        client.send_command.assert_called_once_with("effect 5")
        assert "Effect 5" in result


class TestSetEffectSpeedTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_speed_bpm(self, mock_get):
        from src.server import set_effect_speed

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_speed(value=120, unit="bpm")

        client.send_command.assert_called_once_with("effectbpm 120")
        assert "120" in result
        assert "BPM" in result

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_speed_hz(self, mock_get):
        from src.server import set_effect_speed

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_speed(value=2.5, unit="hz")

        client.send_command.assert_called_once_with("effecthz 2.5")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_speed_invalid_unit(self, mock_get):
        from src.server import set_effect_speed

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_speed(value=120, unit="mph")

        client.send_command.assert_not_called()
        assert "bpm" in result.lower()
        assert "hz" in result.lower()


class TestSetEffectFormTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_form_string(self, mock_get):
        from src.server import set_effect_form

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_form(form="sin")

        client.send_command.assert_called_once_with("effectform sin")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_form_number(self, mock_get):
        from src.server import set_effect_form

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_form(form="6")

        client.send_command.assert_called_once_with("effectform 6")


class TestSetEffectRangeTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_both_high_and_low(self, mock_get):
        from src.server import set_effect_range

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_range(high=100, low=0)

        calls = [c[0][0] for c in client.send_command.call_args_list]
        assert "effecthigh 100" in calls
        assert "effectlow 0" in calls

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_only_high(self, mock_get):
        from src.server import set_effect_range

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_range(high=80)

        client.send_command.assert_called_once_with("effecthigh 80")

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_neither_provided(self, mock_get):
        from src.server import set_effect_range

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_range()

        client.send_command.assert_not_called()
        assert "at least one" in result.lower()


class TestSetEffectPhaseTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_phase(self, mock_get):
        from src.server import set_effect_phase

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_phase(phase=180)

        client.send_command.assert_called_once_with("effectphase 180")


class TestSetEffectWidthTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_set_width(self, mock_get):
        from src.server import set_effect_width

        client = _mock_client()
        mock_get.return_value = client

        result = await set_effect_width(width=50)

        client.send_command.assert_called_once_with("effectwidth 50")


class TestStopEffectsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_stop_effects(self, mock_get):
        from src.server import stop_effects

        client = _mock_client()
        mock_get.return_value = client

        result = await stop_effects()

        client.send_command.assert_called_once_with("off effect")
        assert "stop" in result.lower() or "off" in result.lower()


class TestSyncEffectsTool:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_sync_effects(self, mock_get):
        from src.server import sync_effects_tool

        client = _mock_client()
        mock_get.return_value = client

        result = await sync_effects_tool()

        client.send_command.assert_called_once_with("synceffects")
        assert "sync" in result.lower()


class TestGracefulShutdown:
    @pytest.mark.asyncio
    async def test_lifespan_disconnects_on_exit(self):
        """Server lifespan should call disconnect() on shutdown."""
        from src.server import server_lifespan
        import src.server as server_module

        mock_client = MagicMock()
        mock_client.disconnect = AsyncMock()

        original_client = server_module._client
        server_module._client = mock_client
        try:
            async with server_lifespan(None):
                pass  # simulate server running
            mock_client.disconnect.assert_called_once()
        finally:
            server_module._client = original_client


class TestConnectionErrorHandling:
    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_tool_returns_error_on_connection_lost(self, mock_get):
        from src.server import store_cue

        client = _mock_client()
        client.send_command = AsyncMock(
            side_effect=ConnectionError(
                "failed to reconnect after 3 attempts to 127.0.0.1:30000"
            )
        )
        mock_get.return_value = client

        result = await store_cue(cue_id=1)
        assert "connection lost" in result.lower() or "failed to reconnect" in result.lower()

    @pytest.mark.asyncio
    @patch("src.server.get_client")
    async def test_tool_returns_normal_on_success(self, mock_get):
        from src.server import store_cue

        client = _mock_client()
        mock_get.return_value = client

        result = await store_cue(cue_id=1)
        assert "Cue 1" in result
        assert "connection" not in result.lower()
