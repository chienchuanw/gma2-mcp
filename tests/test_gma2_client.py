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
