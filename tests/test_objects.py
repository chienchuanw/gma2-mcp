"""
Object Keywords Tests

測試 grandMA2 Object Keywords 的命令生成。
Object keywords 是控制台的「名詞」，用於參照 show file 中的物件。

測試類別：
- TestFixtureCommands_Advanced: fixture keyword 測試
- TestChannelCommands: channel keyword 測試
- TestPresetCommands: preset keyword 測試
- TestPresetTypeCommands: presettype keyword 測試
- TestLayoutCommands: layout keyword 測試
"""

import pytest


class TestFixtureCommands_Advanced:
    """Tests for fixture keyword (direct fixture access)."""

    def test_fixture_single(self):
        """Test selecting a single fixture by ID: fixture 34"""
        from src.commands import fixture

        result = fixture(34)
        assert result == "fixture 34"

    def test_fixture_with_subfixture(self):
        """Test selecting a subfixture: fixture 11.5"""
        from src.commands import fixture

        result = fixture(11, sub_id=5)
        assert result == "fixture 11.5"

    def test_fixture_range(self):
        """Test selecting fixture range: fixture 1 thru 10"""
        from src.commands import fixture

        result = fixture(1, end=10)
        assert result == "fixture 1 thru 10"

    def test_fixture_multiple(self):
        """Test selecting multiple fixtures: fixture 1 + 5 + 10"""
        from src.commands import fixture

        result = fixture([1, 5, 10])
        assert result == "fixture 1 + 5 + 10"

    def test_fixture_all(self):
        """Test selecting all fixtures: fixture thru"""
        from src.commands import fixture

        result = fixture(select_all=True)
        assert result == "fixture thru"


class TestChannelCommands:
    """Tests for channel keyword (access fixtures by Channel ID)."""

    def test_channel_single(self):
        """Test selecting a single channel: channel 34"""
        from src.commands import channel

        result = channel(34)
        assert result == "channel 34"

    def test_channel_with_subfixture(self):
        """Test selecting a channel subfixture: channel 11.5"""
        from src.commands import channel

        result = channel(11, sub_id=5)
        assert result == "channel 11.5"

    def test_channel_range(self):
        """Test selecting channel range: channel 1 thru 10"""
        from src.commands import channel

        result = channel(1, end=10)
        assert result == "channel 1 thru 10"

    def test_channel_multiple(self):
        """Test selecting multiple channels: channel 1 + 5 + 10"""
        from src.commands import channel

        result = channel([1, 5, 10])
        assert result == "channel 1 + 5 + 10"

    def test_channel_all(self):
        """Test selecting all channels: channel thru"""
        from src.commands import channel

        result = channel(select_all=True)
        assert result == "channel thru"


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

    # ---- Preset Object Keyword 擴充測試 ----
    # 根據 grandMA2 官方文件，Preset 支援多種語法

    def test_preset_with_type_and_id(self):
        """Test preset with type name and ID: preset 3.2 (gobo type)"""
        from src.commands import preset

        result = preset("gobo", 2)
        assert result == "preset 3.2"

    def test_preset_id_only(self):
        """Test preset with ID only: preset 5"""
        from src.commands import preset

        result = preset(5)
        assert result == "preset 5"

    def test_preset_type_number_and_id(self):
        """Test preset with type number and ID: preset 3.2"""
        from src.commands import preset

        result = preset(3, 2)
        assert result == "preset 3.2"

    def test_preset_by_name(self):
        """Test preset by name: preset "DarkRed" """
        from src.commands import preset

        result = preset(name="DarkRed")
        assert result == 'preset "DarkRed"'

    def test_preset_wildcard_with_name(self):
        """Test preset with wildcard and name: preset *."DarkRed" """
        from src.commands import preset

        result = preset(name="DarkRed", wildcard=True)
        assert result == 'preset *."DarkRed"'

    def test_preset_type_with_name(self):
        """Test preset type with name: preset "color"."Red" """
        from src.commands import preset

        result = preset("color", name="Red")
        assert result == 'preset "color"."Red"'

    def test_preset_range(self):
        """Test preset range: preset 1.1 thru 5"""
        from src.commands import preset

        result = preset(1, 1, end=5)
        assert result == "preset 1.1 thru 5"

    def test_preset_multiple(self):
        """Test selecting multiple presets: preset 1.1 + 1.3 + 1.5"""
        from src.commands import preset

        result = preset(1, [1, 3, 5])
        assert result == "preset 1.1 + 1.3 + 1.5"


class TestPresetTypeCommands:
    """Tests for PresetType Object Keyword."""

    # ---- 基本語法測試 ----

    def test_preset_type_by_number(self):
        """Test calling preset type by number: PresetType 3"""
        from src.commands import preset_type

        result = preset_type(3)
        assert result == "presettype 3"

    def test_preset_type_by_name(self):
        """Test calling preset type by name: PresetType "Dimmer" """
        from src.commands import preset_type

        result = preset_type(name="Dimmer")
        assert result == 'presettype "Dimmer"'

    def test_preset_type_by_name_color(self):
        """Test calling preset type by name: PresetType "Color" """
        from src.commands import preset_type

        result = preset_type(name="Color")
        assert result == 'presettype "Color"'

    # ---- Feature 語法測試 ----

    def test_preset_type_with_feature(self):
        """Test preset type with feature: PresetType 3.1"""
        from src.commands import preset_type

        result = preset_type(3, feature=1)
        assert result == "presettype 3.1"

    def test_preset_type_name_with_feature(self):
        """Test preset type name with feature: PresetType "Color".2"""
        from src.commands import preset_type

        result = preset_type(name="Color", feature=2)
        assert result == 'presettype "Color".2'

    # ---- Attribute 語法測試 ----

    def test_preset_type_with_feature_and_attribute(self):
        """Test preset type with feature and attribute: PresetType 3.2.1"""
        from src.commands import preset_type

        result = preset_type(3, feature=2, attribute=1)
        assert result == "presettype 3.2.1"

    # ---- 變數語法測試 ----

    def test_preset_type_variable(self):
        """Test preset type variable: PresetType $preset.2"""
        from src.commands import preset_type

        result = preset_type("$preset", feature=2)
        assert result == "presettype $preset.2"

    # ---- 錯誤處理測試 ----

    def test_preset_type_no_args_raises_error(self):
        """Test that calling preset_type() without args raises ValueError."""
        from src.commands import preset_type

        with pytest.raises(ValueError):
            preset_type()

    def test_preset_type_attribute_without_feature_raises_error(self):
        """Test that providing attribute without feature raises ValueError."""
        from src.commands import preset_type

        with pytest.raises(ValueError):
            preset_type(3, attribute=1)


class TestLayoutCommands:
    """
    Tests for Layout keyword commands.

    Layout 是一個物件類型，代表 fixtures 和其他物件的佈局。
    Layout 的預設功能是 Select，表示呼叫 Layout 時會選擇該 Layout，
    並在任何啟用 Link Selected 的 Layout View 中顯示。
    """

    # ---- 基本 Layout 選擇 ----

    def test_layout_single(self):
        """Test selecting a single layout: layout 3"""
        from src.commands import layout

        result = layout(3)
        assert result == "layout 3"

    def test_layout_with_large_id(self):
        """Test selecting layout with large ID: layout 101"""
        from src.commands import layout

        result = layout(101)
        assert result == "layout 101"

    # ---- Layout 範圍選擇 (使用 thru) ----

    def test_layout_range(self):
        """Test selecting layout range: layout 1 thru 5"""
        from src.commands import layout

        result = layout(1, end=5)
        assert result == "layout 1 thru 5"

    def test_layout_same_start_end(self):
        """Test that same start and end selects a single layout."""
        from src.commands import layout

        result = layout(3, end=3)
        assert result == "layout 3"

    # ---- Layout 多選 (使用 +) ----

    def test_layout_multiple(self):
        """Test selecting multiple layouts: layout 1 + 3 + 5"""
        from src.commands import layout

        result = layout([1, 3, 5])
        assert result == "layout 1 + 3 + 5"

    def test_layout_list_single_item(self):
        """Test that list with single element equals selecting a single layout."""
        from src.commands import layout

        result = layout([7])
        assert result == "layout 7"

    # ---- 錯誤處理 ----

    def test_layout_no_id_raises_error(self):
        """Test that calling layout without ID raises ValueError."""
        from src.commands import layout

        with pytest.raises(ValueError, match="Must provide layout_id"):
            layout()
