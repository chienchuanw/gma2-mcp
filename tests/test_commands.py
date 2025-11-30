"""
Command Builder Module Tests

Tests for various grandMA2 command construction functions to ensure
correct MA command format generation.
"""

import pytest


class TestFixtureCommands:
    """Tests for fixture-related commands."""

    # ---- 單個 fixture 選取 ----

    def test_select_fixture_single(self):
        """測試選取單一 fixture：selfix fixture 1"""
        from src.commands import select_fixture

        result = select_fixture(1)
        assert result == "selfix fixture 1"

    def test_select_fixture_single_large_id(self):
        """測試選取較大編號的單一 fixture：selfix fixture 101"""
        from src.commands import select_fixture

        result = select_fixture(101)
        assert result == "selfix fixture 101"

    # ---- 多個 fixture（列表）選取 ----

    def test_select_fixture_multiple_ids(self):
        """測試選取多個不連續的 fixtures：selfix fixture 1 + 3 + 5"""
        from src.commands import select_fixture

        result = select_fixture([1, 3, 5])
        assert result == "selfix fixture 1 + 3 + 5"

    def test_select_fixture_list_with_single_id(self):
        """測試只有一個元素的列表應該等同於選取單一 fixture"""
        from src.commands import select_fixture

        result = select_fixture([7])
        assert result == "selfix fixture 7"

    # ---- 範圍選取（使用 thru）----

    def test_select_fixture_range(self):
        """測試選取範圍：selfix fixture 1 thru 10"""
        from src.commands import select_fixture

        result = select_fixture(1, 10)
        assert result == "selfix fixture 1 thru 10"

    def test_select_fixture_with_same_start_end(self):
        """測試 start 和 end 相同時應選取單一 fixture"""
        from src.commands import select_fixture

        result = select_fixture(5, 5)
        assert result == "selfix fixture 5"

    # ---- 從頭選取到指定編號（Fixture Thru X）----

    def test_select_fixture_from_beginning(self):
        """測試從頭選取到指定編號：selfix fixture thru 10"""
        from src.commands import select_fixture

        result = select_fixture(end=10)
        assert result == "selfix fixture thru 10"

    # ---- 從指定編號選取到最後（Fixture X Thru）----

    def test_select_fixture_to_end(self):
        """測試從指定編號選取到最後：selfix fixture 5 thru"""
        from src.commands import select_fixture

        result = select_fixture(start=5, thru_all=True)
        assert result == "selfix fixture 5 thru"

    # ---- 選取全部（Fixture Thru）----

    def test_select_fixture_all(self):
        """測試選取全部 fixtures：selfix fixture thru"""
        from src.commands import select_fixture

        result = select_fixture(select_all=True)
        assert result == "selfix fixture thru"

    def test_clear_selection(self):
        """Test clearing selection."""
        from src.commands import clear_selection

        result = clear_selection()
        assert result == "clearall"


class TestGroupCommands:
    """Tests for group-related commands."""

    def test_store_group(self):
        """Test storing a group."""
        from src.commands import store_group

        result = store_group(1)
        assert result == "store group 1"

    def test_store_group_with_specific_id(self):
        """Test storing to a specific group ID."""
        from src.commands import store_group

        result = store_group(42)
        assert result == "store group 42"

    def test_label_group(self):
        """Test labeling a group."""
        from src.commands import label_group

        result = label_group(1, "Front Wash")
        assert result == 'label group 1 "Front Wash"'

    def test_label_group_with_chinese_name(self):
        """Test labeling a group with a Chinese name."""
        from src.commands import label_group

        result = label_group(1, "前區洗牆燈")
        assert result == 'label group 1 "前區洗牆燈"'

    def test_select_group(self):
        """Test selecting a group."""
        from src.commands import select_group

        result = select_group(1)
        assert result == "group 1"

    def test_delete_group(self):
        """Test deleting a group."""
        from src.commands import delete_group

        result = delete_group(1)
        assert result == "delete group 1"


class TestPresetCommands:
    """Tests for preset-related commands."""

    def test_store_preset(self):
        """Test storing a preset."""
        from src.commands import store_preset

        result = store_preset("dimmer", 1)
        assert result == "store preset 1.1"

    def test_store_preset_color(self):
        """Test storing a color preset."""
        from src.commands import store_preset

        result = store_preset("color", 5)
        assert result == "store preset 2.5"

    def test_label_preset(self):
        """Test labeling a preset."""
        from src.commands import label_preset

        result = label_preset("dimmer", 1, "Full Brightness")
        assert result == 'label preset 1.1 "Full Brightness"'

    def test_call_preset(self):
        """Test calling a preset."""
        from src.commands import call_preset

        result = call_preset("dimmer", 1)
        assert result == "preset 1.1"


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
