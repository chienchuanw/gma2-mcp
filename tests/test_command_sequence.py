import pytest
from unittest.mock import AsyncMock, MagicMock

from src.command_sequence import CommandSequence


class TestCommandSequenceInit:
    def test_empty_sequence(self):
        seq = CommandSequence()
        assert len(seq) == 0
        assert seq.preview() == []

    def test_repr_empty(self):
        seq = CommandSequence()
        assert repr(seq) == "CommandSequence(commands=0)"

    def test_str_empty(self):
        seq = CommandSequence()
        assert str(seq) == ""


class TestCommandSequenceAdd:
    def test_add_single_command(self):
        seq = CommandSequence()
        seq.add("fixture 1 at 50")
        assert len(seq) == 1
        assert seq.preview() == ["fixture 1 at 50"]

    def test_add_fluent_chaining(self):
        seq = CommandSequence()
        result = seq.add("fixture 1 thru 10").add("at full").add("store group 1")
        assert result is seq
        assert len(seq) == 3
        assert seq.preview() == [
            "fixture 1 thru 10",
            "at full",
            "store group 1",
        ]

    def test_add_command_builder_output(self):
        from src.commands import fixture_at

        seq = CommandSequence()
        seq.add(fixture_at(1, 50))
        assert seq.preview() == ["fixture 1 at 50"]


class TestCommandSequencePreview:
    def test_preview_returns_copy(self):
        seq = CommandSequence()
        seq.add("cmd1").add("cmd2")
        preview = seq.preview()
        preview.append("cmd3")
        assert len(seq) == 2

    def test_preview_preserves_order(self):
        seq = CommandSequence()
        seq.add("first").add("second").add("third")
        assert seq.preview() == ["first", "second", "third"]


class TestCommandSequenceClear:
    def test_clear_removes_all(self):
        seq = CommandSequence()
        seq.add("cmd1").add("cmd2").add("cmd3")
        assert len(seq) == 3
        seq.clear()
        assert len(seq) == 0
        assert seq.preview() == []

    def test_clear_then_reuse(self):
        seq = CommandSequence()
        seq.add("old_cmd")
        seq.clear()
        seq.add("new_cmd")
        assert seq.preview() == ["new_cmd"]


class TestCommandSequenceIteration:
    def test_iterate_over_commands(self):
        seq = CommandSequence()
        seq.add("cmd1").add("cmd2").add("cmd3")
        result = list(seq)
        assert result == ["cmd1", "cmd2", "cmd3"]

    def test_iterate_empty(self):
        seq = CommandSequence()
        assert list(seq) == []


class TestCommandSequenceStringRepresentation:
    def test_str_with_commands(self):
        seq = CommandSequence()
        seq.add("fixture 1").add("at full")
        assert str(seq) == "fixture 1\nat full"

    def test_repr_with_commands(self):
        seq = CommandSequence()
        seq.add("cmd1").add("cmd2").add("cmd3")
        assert repr(seq) == "CommandSequence(commands=3)"


class TestCommandSequenceExecute:
    @pytest.mark.asyncio
    async def test_execute_sends_all_commands(self):
        mock_client = MagicMock()
        mock_client.send_command = AsyncMock()

        seq = CommandSequence()
        seq.add("fixture 1 thru 10").add("at full").add("store group 1")

        result = await seq.execute(mock_client)

        assert mock_client.send_command.call_count == 3
        calls = [c[0][0] for c in mock_client.send_command.call_args_list]
        assert calls == ["fixture 1 thru 10", "at full", "store group 1"]

    @pytest.mark.asyncio
    async def test_execute_returns_result_dict(self):
        mock_client = MagicMock()
        mock_client.send_command = AsyncMock()

        seq = CommandSequence()
        seq.add("cmd1").add("cmd2")

        result = await seq.execute(mock_client)

        assert result["commands_sent"] == ["cmd1", "cmd2"]
        assert result["count"] == 2
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_execute_empty_sequence(self):
        mock_client = MagicMock()
        mock_client.send_command = AsyncMock()

        seq = CommandSequence()
        result = await seq.execute(mock_client)

        assert result["commands_sent"] == []
        assert result["count"] == 0
        assert result["success"] is True
        mock_client.send_command.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_with_custom_delay(self):
        mock_client = MagicMock()
        mock_client.send_command = AsyncMock()

        seq = CommandSequence()
        seq.add("cmd1").add("cmd2")

        await seq.execute(mock_client, delay=0.5)

        for call in mock_client.send_command.call_args_list:
            assert call[1]["delay"] == 0.5

    @pytest.mark.asyncio
    async def test_execute_without_delay_uses_default(self):
        mock_client = MagicMock()
        mock_client.send_command = AsyncMock()

        seq = CommandSequence()
        seq.add("cmd1")

        await seq.execute(mock_client)

        mock_client.send_command.assert_called_once_with("cmd1")
