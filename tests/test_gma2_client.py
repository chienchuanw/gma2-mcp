import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.gma2_client import GMA2Client


def _mock_telnet():
    client = MagicMock()
    client.send_command = AsyncMock()
    client.connect = AsyncMock()
    client.login = AsyncMock()
    client.disconnect = AsyncMock()
    return client


class TestGMA2ClientInit:
    def test_init_with_telnet_client(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)
        assert client._client is telnet


class TestGMA2ClientContextManager:
    @pytest.mark.asyncio
    async def test_context_manager_disconnects(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        async with client:
            pass

        telnet.disconnect.assert_called_once()


class TestBuildCueList:
    @pytest.mark.asyncio
    async def test_simple_cues(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.build_cue_list(
            1,
            [
                {"id": 1, "name": "Preset"},
                {"id": 2, "name": "Look 1"},
                {"id": 3, "name": "Blackout"},
            ],
        )

        assert result["count"] == 3  # 3 store with inline name
        cmds = result["commands_sent"]
        assert cmds[0] == 'store cue 1 "Preset"'
        assert cmds[1] == 'store cue 2 "Look 1"'
        assert cmds[2] == 'store cue 3 "Blackout"'
        assert "3 cues" in result["summary"]

    @pytest.mark.asyncio
    async def test_cues_with_fade(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.build_cue_list(
            1,
            [
                {"id": 1, "name": "Intro", "fade": 3.0},
            ],
        )

        cmds = result["commands_sent"]
        assert cmds[0] == 'store cue 1 "Intro"'
        assert cmds[1] == "assign fade 3.0 cue 1"
        assert result["count"] == 2

    @pytest.mark.asyncio
    async def test_cue_without_name_or_fade(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.build_cue_list(1, [{"id": 5}])

        assert result["count"] == 1
        assert result["commands_sent"] == ["store cue 5"]


class TestSetupGroupWithPreset:
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_group_with_preset(
            fixtures=(1, 10),
            group_id=1,
            group_name="Front Wash",
            preset_type="color",
            preset_id=3,
        )

        cmds = result["commands_sent"]
        assert cmds[0] == "selfix fixture 1 thru 10"
        assert cmds[1] == 'store group 1 "Front Wash"'
        assert cmds[2] == "preset 4.3"
        assert result["count"] == 3
        assert "Front Wash" in result["summary"]


class TestQuickLook:
    @pytest.mark.asyncio
    async def test_quick_look_without_store(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.quick_look(fixtures=(1, 20), value=50)

        cmds = result["commands_sent"]
        assert cmds[0] == "selfix fixture 1 thru 20"
        assert cmds[1] == "at 50"
        assert result["count"] == 2

    @pytest.mark.asyncio
    async def test_quick_look_stored_as_cue(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.quick_look(fixtures=(1, 20), value=100, store_as_cue=5)

        cmds = result["commands_sent"]
        assert cmds[2] == "store cue 5"
        assert result["count"] == 3
        assert "Cue 5" in result["summary"]


class TestAssignSequencesToExecutors:
    @pytest.mark.asyncio
    async def test_batch_assignment(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.assign_sequences_to_executors(
            [
                (1, 1),
                (2, 2),
                (3, 3),
            ]
        )

        cmds = result["commands_sent"]
        assert cmds[0] == "assign sequence 1 at executor 1"
        assert cmds[1] == "assign sequence 2 at executor 2"
        assert cmds[2] == "assign sequence 3 at executor 3"
        assert result["count"] == 3
        assert "3 sequences" in result["summary"]


class TestStoreCueAcrossSequences:
    @pytest.mark.asyncio
    async def test_range_with_name(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.store_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=125,
            cue_name="((LOADING SONG))",
        )

        cmds = result["commands_sent"]
        assert result["count"] == 25
        assert cmds[0] == 'store sequence 101 cue 0.5 "((LOADING SONG))"'
        assert cmds[24] == 'store sequence 125 cue 0.5 "((LOADING SONG))"'
        assert "25" in result["summary"]

    @pytest.mark.asyncio
    async def test_single_sequence(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.store_cue_across_sequences(
            cue_id=1,
            sequence_start=101,
            sequence_end=101,
        )

        cmds = result["commands_sent"]
        assert result["count"] == 1
        assert cmds[0] == "store sequence 101 cue 1"

    @pytest.mark.asyncio
    async def test_without_name(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.store_cue_across_sequences(
            cue_id=3,
            sequence_start=1,
            sequence_end=3,
        )

        cmds = result["commands_sent"]
        assert result["count"] == 3
        assert cmds[0] == "store sequence 1 cue 3"
        assert cmds[1] == "store sequence 2 cue 3"
        assert cmds[2] == "store sequence 3 cue 3"


class TestLabelCueAcrossSequences:
    @pytest.mark.asyncio
    async def test_range(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.label_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=125,
            label="((LOADING SONG))",
        )

        cmds = result["commands_sent"]
        assert result["count"] == 25
        assert cmds[0] == 'label sequence 101 cue 0.5 "((LOADING SONG))"'
        assert cmds[24] == 'label sequence 125 cue 0.5 "((LOADING SONG))"'

    @pytest.mark.asyncio
    async def test_single_sequence(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.label_cue_across_sequences(
            cue_id=1,
            sequence_start=50,
            sequence_end=50,
            label="Intro",
        )

        cmds = result["commands_sent"]
        assert result["count"] == 1
        assert cmds[0] == 'label sequence 50 cue 1 "Intro"'


class TestAppearanceCueAcrossSequences:
    @pytest.mark.asyncio
    async def test_rgb_range(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.appearance_cue_across_sequences(
            cue_id=0.5,
            sequence_start=101,
            sequence_end=103,
            red=0,
            green=0,
            blue=0,
        )

        cmds = result["commands_sent"]
        assert result["count"] == 3
        assert cmds[0] == "appearance sequence 101 cue 0.5 /r=0 /g=0 /b=0"
        assert cmds[1] == "appearance sequence 102 cue 0.5 /r=0 /g=0 /b=0"
        assert cmds[2] == "appearance sequence 103 cue 0.5 /r=0 /g=0 /b=0"

    @pytest.mark.asyncio
    async def test_hex_variant(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.appearance_cue_across_sequences(
            cue_id=1,
            sequence_start=101,
            sequence_end=102,
            color="FF0000",
        )

        cmds = result["commands_sent"]
        assert result["count"] == 2
        assert cmds[0] == "appearance sequence 101 cue 1 /color=FF0000"
        assert cmds[1] == "appearance sequence 102 cue 1 /color=FF0000"


class TestCloneFixtures:
    @pytest.mark.asyncio
    async def test_single_fixture_clone(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.clone_fixtures(source_fixture=1, target_fixture=5)

        cmds = result["commands_sent"]
        assert result["count"] == 1
        assert cmds[0] == "clone fixture 1 at fixture 5 /noconfirm"

    @pytest.mark.asyncio
    async def test_fixture_range_clone(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.clone_fixtures(
            source_fixture=1, target_fixture=11, source_end=5, target_end=15
        )

        cmds = result["commands_sent"]
        assert cmds[0] == "clone fixture 1 thru 5 at fixture 11 thru 15 /noconfirm"

    @pytest.mark.asyncio
    async def test_clone_with_overwrite(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.clone_fixtures(
            source_fixture=1, target_fixture=5, mode="overwrite"
        )

        cmds = result["commands_sent"]
        assert cmds[0] == "clone fixture 1 at fixture 5 /overwrite /noconfirm"

    @pytest.mark.asyncio
    async def test_clone_with_merge(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.clone_fixtures(
            source_fixture=1, target_fixture=5, mode="merge"
        )

        cmds = result["commands_sent"]
        assert cmds[0] == "clone fixture 1 at fixture 5 /merge /noconfirm"


class TestSetupEffectOnGroup:
    @pytest.mark.asyncio
    async def test_basic_effect_on_group(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_effect_on_group(group_id=1, effect_id=5)

        cmds = result["commands_sent"]
        assert result["count"] == 2
        assert "group 1" in cmds[0]
        assert "effect 5" in cmds[1]

    @pytest.mark.asyncio
    async def test_effect_with_full_params(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_effect_on_group(
            group_id=1, effect_id=5, bpm=120, form="sin", high=100, low=0
        )

        assert result["count"] == 6


class TestSetupExecutorPage:
    @pytest.mark.asyncio
    async def test_two_executors_with_labels(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_executor_page(
            page=1,
            assignments=[
                {"executor_id": 1, "sequence_id": 1, "label": "Wash"},
                {"executor_id": 2, "sequence_id": 2, "label": "Spots"},
            ],
        )

        cmds = result["commands_sent"]
        # 2 assigns + 2 labels = 4 commands
        assert result["count"] == 4
        assert "page 1" in result["summary"].lower()
        # Verify page-qualified executor addressing
        assert "executor 1.1" in cmds[0]
        assert "executor 1.2" in cmds[2]

    @pytest.mark.asyncio
    async def test_executor_with_fader_level(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_executor_page(
            page=2,
            assignments=[
                {"executor_id": 1, "sequence_id": 1, "fader_level": 80},
            ],
        )

        cmds = result["commands_sent"]
        # 1 assign + 1 fader = 2 commands
        assert result["count"] == 2
        # Verify page-qualified addressing
        assert "executor 2.1" in cmds[0]
        assert "executor 2.1 at 80" in cmds[1]

    @pytest.mark.asyncio
    async def test_executor_page3_addressing(self):
        """Verify page parameter is used in all executor commands."""
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_executor_page(
            page=3,
            assignments=[
                {"executor_id": 5, "sequence_id": 10, "label": "FX", "fader_level": 100},
            ],
        )

        cmds = result["commands_sent"]
        assert result["count"] == 3  # assign + label + fader
        assert "executor 3.5" in cmds[0]  # assign
        assert 'label executor 3.5 "FX"' == cmds[1]  # label
        assert "executor 3.5 at 100" == cmds[2]  # fader


class TestBatchLabel:
    @pytest.mark.asyncio
    async def test_label_multiple_groups(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.batch_label(
            object_type="group", labels={1: "Wash", 2: "Spots", 3: "Beams"}
        )

        assert result["count"] == 3
        assert "3" in result["summary"]
        assert "group" in result["summary"].lower()


class TestCreateAndRunMacro:
    @pytest.mark.asyncio
    async def test_create_without_running(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.create_and_run_macro(
            macro_id=10,
            commands=["Go Sequence 1", "Go Sequence 2"],
            name="Two Seqs",
        )

        cmds = result["commands_sent"]
        # store + 2 assigns + label = 4
        assert result["count"] == 4
        assert cmds[0] == "store macro 10"

    @pytest.mark.asyncio
    async def test_create_and_run(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.create_and_run_macro(
            macro_id=10, commands=["Go Sequence 1"], run=True
        )

        cmds = result["commands_sent"]
        # store + 1 assign + go+ = 3
        assert result["count"] == 3
        assert cmds[-1] == "go+ macro 1.10"
        assert "executed" in result["summary"].lower()


class TestCreateSongObjects:
    @pytest.mark.asyncio
    async def test_creates_sequence_and_page(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.create_song_objects(song_id=101, song_name="Opening+Childhood")

        cmds = result["commands_sent"]
        assert cmds[0] == 'store sequence 101 "Opening+Childhood"'
        assert cmds[1] == 'store page 101 "Opening+Childhood"'
        assert result["count"] == 2
        assert "Sequence 101" in result["summary"]
        assert "Page 101" in result["summary"]
        assert "Opening+Childhood" in result["summary"]

    @pytest.mark.asyncio
    async def test_sends_two_commands(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        await client.create_song_objects(song_id=5, song_name="Finale")

        assert telnet.send_command.call_count == 2


class TestSetupSongMacro:
    @pytest.mark.asyncio
    async def test_creates_macro_with_setvar(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_song_macro(macro_id=101, song_name="Opening+Childhood")

        cmds = result["commands_sent"]
        assert cmds[0] == "store macro 101"
        assert cmds[1] == 'label macro 101 "Opening+Childhood"'
        assert "SetVar $song='Opening+Childhood'" in cmds[2]
        assert result["count"] == 3
        assert "Macro 101" in result["summary"]
        assert "$song" in result["summary"]

    @pytest.mark.asyncio
    async def test_custom_var_name(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.setup_song_macro(
            macro_id=10, song_name="Test", var_name="$current"
        )

        cmds = result["commands_sent"]
        assert "SetVar $current='Test'" in cmds[2]
        assert "$current" in result["summary"]


class TestBuildSetList:
    @pytest.mark.asyncio
    async def test_builds_set_list_with_songs(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        songs = [
            {"cue_id": 1, "macro_id": 101, "name": "Opening"},
            {"cue_id": 2, "macro_id": 102, "name": "Finale"},
        ]
        result = await client.build_set_list(
            sequence_id=100, sequence_name="Main Set", songs=songs
        )

        cmds = result["commands_sent"]
        # First command: store the set-list sequence
        assert cmds[0] == 'store sequence 100 "Main Set"'
        # Song 1: store cue + assign cmd
        assert cmds[1] == 'store sequence 100 cue 1 "Opening"'
        assert cmds[2] == 'assign cue 1 sequence 100 /cmd="Macro 101"'
        # Song 2: store cue + assign cmd
        assert cmds[3] == 'store sequence 100 cue 2 "Finale"'
        assert cmds[4] == 'assign cue 2 sequence 100 /cmd="Macro 102"'
        # 1 store seq + 2 * (store cue + assign) = 5
        assert result["count"] == 5
        assert "Main Set" in result["summary"]
        assert "2 songs" in result["summary"]

    @pytest.mark.asyncio
    async def test_empty_songs_list(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.build_set_list(
            sequence_id=100, sequence_name="Empty Set", songs=[]
        )

        cmds = result["commands_sent"]
        assert len(cmds) == 1
        assert cmds[0] == 'store sequence 100 "Empty Set"'
        assert result["count"] == 1
        assert "0 songs" in result["summary"]


class TestGMA2ClientResultStructure:
    @pytest.mark.asyncio
    async def test_result_has_required_keys(self):
        telnet = _mock_telnet()
        client = GMA2Client(telnet)

        result = await client.build_cue_list(1, [{"id": 1}])

        assert "commands_sent" in result
        assert "count" in result
        assert "summary" in result
        assert isinstance(result["commands_sent"], list)
        assert isinstance(result["count"], int)
        assert isinstance(result["summary"], str)
