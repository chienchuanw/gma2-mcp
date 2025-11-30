"""
Command Builder 模組測試

測試各種 grandMA2 指令的建構函式，確保產生正確的 MA 指令格式。
"""

import pytest


class TestFixtureCommands:
    """測試 Fixture 相關指令"""

    def test_select_fixture_single(self):
        """測試選取單一 fixture"""
        from src.commands import select_fixture

        result = select_fixture(1)
        assert result == "selfix fixture 1"

    def test_select_fixture_range(self):
        """測試選取 fixture 範圍"""
        from src.commands import select_fixture

        result = select_fixture(1, 10)
        assert result == "selfix fixture 1 thru 10"

    def test_select_fixture_with_same_start_end(self):
        """測試起始與結束相同時只選取單一 fixture"""
        from src.commands import select_fixture

        result = select_fixture(5, 5)
        assert result == "selfix fixture 5"

    def test_clear_selection(self):
        """測試清除選取"""
        from src.commands import clear_selection

        result = clear_selection()
        assert result == "clearall"


class TestGroupCommands:
    """測試 Group 相關指令"""

    def test_store_group(self):
        """測試儲存 group"""
        from src.commands import store_group

        result = store_group(1)
        assert result == "store group 1"

    def test_store_group_with_specific_id(self):
        """測試儲存到指定的 group ID"""
        from src.commands import store_group

        result = store_group(42)
        assert result == "store group 42"

    def test_label_group(self):
        """測試為 group 加上標籤"""
        from src.commands import label_group

        result = label_group(1, "Front Wash")
        assert result == 'label group 1 "Front Wash"'

    def test_label_group_with_chinese_name(self):
        """測試使用中文名稱標記 group"""
        from src.commands import label_group

        result = label_group(1, "前區洗牆燈")
        assert result == 'label group 1 "前區洗牆燈"'

    def test_select_group(self):
        """測試選取 group"""
        from src.commands import select_group

        result = select_group(1)
        assert result == "group 1"

    def test_delete_group(self):
        """測試刪除 group"""
        from src.commands import delete_group

        result = delete_group(1)
        assert result == "delete group 1"


class TestPresetCommands:
    """測試 Preset 相關指令"""

    def test_store_preset(self):
        """測試儲存 preset"""
        from src.commands import store_preset

        result = store_preset("dimmer", 1)
        assert result == "store preset 1.1"

    def test_store_preset_color(self):
        """測試儲存 color preset"""
        from src.commands import store_preset

        result = store_preset("color", 5)
        assert result == "store preset 2.5"

    def test_label_preset(self):
        """測試為 preset 加上標籤"""
        from src.commands import label_preset

        result = label_preset("dimmer", 1, "Full Brightness")
        assert result == 'label preset 1.1 "Full Brightness"'

    def test_call_preset(self):
        """測試呼叫 preset"""
        from src.commands import call_preset

        result = call_preset("dimmer", 1)
        assert result == "preset 1.1"


class TestSequenceCommands:
    """測試 Sequence 相關指令"""

    def test_go_sequence(self):
        """測試執行 sequence"""
        from src.commands import go_sequence

        result = go_sequence(1)
        assert result == "go+ sequence 1"

    def test_pause_sequence(self):
        """測試暫停 sequence"""
        from src.commands import pause_sequence

        result = pause_sequence(1)
        assert result == "pause sequence 1"

    def test_goto_cue(self):
        """測試跳轉到指定 cue"""
        from src.commands import goto_cue

        result = goto_cue(1, 5)
        assert result == "goto cue 5 sequence 1"

