"""
Playback Commands Tests

測試 grandMA2 播放控制相關命令的生成。
包含 Go、Pause、Goto、GoFast 系列命令。

測試類別：
- TestSequenceCommands: go_sequence, pause_sequence, goto_cue 測試
- TestGoFastCommands: go_fast_back, go_fast_forward 測試
"""

import pytest


class TestSequenceCommands:
    """Tests for sequence-related commands."""

    def test_go_sequence(self):
        """Test executing a sequence."""
        from src.commands import go_sequence

        result = go_sequence(1)
        assert result == "go+ sequence 1"

    def test_pause_sequence(self):
        """Test pausing a sequence."""
        from src.commands import pause_sequence

        result = pause_sequence(1)
        assert result == "pause sequence 1"

    def test_goto_cue(self):
        """Test jumping to a specific cue."""
        from src.commands import goto_cue

        result = goto_cue(1, 5)
        assert result == "goto cue 5 sequence 1"


class TestGoFastCommands:
    """Tests for <<< (GoFastBack) and >>> (GoFastForward) keywords."""

    # ---- GoFastBack (<<<) 測試 ----

    def test_go_fast_back_executor(self):
        """Test <<< Executor 3 - jumps to previous cue on executor 3."""
        from src.commands import go_fast_back

        result = go_fast_back(executor=3)
        assert result == "<<< executor 3"

    def test_go_fast_back_executor_list(self):
        """Test <<< with multiple executors."""
        from src.commands import go_fast_back

        result = go_fast_back(executor=[1, 2, 3])
        assert result == "<<< executor 1 + 2 + 3"

    def test_go_fast_back_sequence(self):
        """Test <<< Sequence 5 - jumps to previous cue on sequence 5."""
        from src.commands import go_fast_back

        result = go_fast_back(sequence=5)
        assert result == "<<< sequence 5"

    def test_go_fast_back_no_target(self):
        """Test <<< without target - applies to current executor/sequence."""
        from src.commands import go_fast_back

        result = go_fast_back()
        assert result == "<<<"

    # ---- GoFastForward (>>>) 測試 ----

    def test_go_fast_forward_executor(self):
        """Test >>> Executor 3 - jumps to next cue on executor 3."""
        from src.commands import go_fast_forward

        result = go_fast_forward(executor=3)
        assert result == ">>> executor 3"

    def test_go_fast_forward_executor_list(self):
        """Test >>> with multiple executors."""
        from src.commands import go_fast_forward

        result = go_fast_forward(executor=[1, 2, 3])
        assert result == ">>> executor 1 + 2 + 3"

    def test_go_fast_forward_sequence(self):
        """Test >>> Sequence 5 - jumps to next cue on sequence 5."""
        from src.commands import go_fast_forward

        result = go_fast_forward(sequence=5)
        assert result == ">>> sequence 5"

    def test_go_fast_forward_no_target(self):
        """Test >>> without target - applies to current executor/sequence."""
        from src.commands import go_fast_forward

        result = go_fast_forward()
        assert result == ">>>"


class TestDefGoCommands:
    """Tests for DefGoBack, DefGoForward, DefGoPause keywords.

    這些指令作用於選定的 Executor（預設 Executor），
    等同於按下控台上的實體 Go-、Go+、Pause 按鈕。
    """

    def test_def_go_back(self):
        """Test DefGoBack - calls previous cue in selected executor."""
        from src.commands import def_go_back

        result = def_go_back()
        assert result == "defgoback"

    def test_def_go_forward(self):
        """Test DefGoForward - calls next cue in selected executor."""
        from src.commands import def_go_forward

        result = def_go_forward()
        assert result == "defgoforward"

    def test_def_go_pause(self):
        """Test DefGoPause - pauses current fade in selected executor."""
        from src.commands import def_go_pause

        result = def_go_pause()
        assert result == "defgopause"
