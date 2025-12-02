"""
Command Builder Module Tests

Tests for various grandMA2 command construction functions to ensure
correct MA command format generation.
"""

import pytest


class TestFixtureCommands:
    """Tests for fixture-related commands."""

    # ---- Single fixture selection ----

    def test_select_fixture_single(self):
        """Test selecting a single fixture: selfix fixture 1"""
        from src.commands import select_fixture

        result = select_fixture(1)
        assert result == "selfix fixture 1"

    def test_select_fixture_single_large_id(self):
        """Test selecting a single fixture with large ID: selfix fixture 101"""
        from src.commands import select_fixture

        result = select_fixture(101)
        assert result == "selfix fixture 101"

    # ---- Multiple fixture (list) selection ----

    def test_select_fixture_multiple_ids(self):
        """Test selecting multiple non-contiguous fixtures: selfix fixture 1 + 3 + 5"""
        from src.commands import select_fixture

        result = select_fixture([1, 3, 5])
        assert result == "selfix fixture 1 + 3 + 5"

    def test_select_fixture_list_with_single_id(self):
        """Test that a list with single element equals selecting a single fixture"""
        from src.commands import select_fixture

        result = select_fixture([7])
        assert result == "selfix fixture 7"

    # ---- Range selection (using thru) ----

    def test_select_fixture_range(self):
        """Test selecting a range: selfix fixture 1 thru 10"""
        from src.commands import select_fixture

        result = select_fixture(1, 10)
        assert result == "selfix fixture 1 thru 10"

    def test_select_fixture_with_same_start_end(self):
        """Test that same start and end selects a single fixture"""
        from src.commands import select_fixture

        result = select_fixture(5, 5)
        assert result == "selfix fixture 5"

    # ---- Select from beginning to specified number (Fixture Thru X) ----

    def test_select_fixture_from_beginning(self):
        """Test selecting from beginning to specified number: selfix fixture thru 10"""
        from src.commands import select_fixture

        result = select_fixture(end=10)
        assert result == "selfix fixture thru 10"

    # ---- Select from specified number to end (Fixture X Thru) ----

    def test_select_fixture_to_end(self):
        """Test selecting from specified number to end: selfix fixture 5 thru"""
        from src.commands import select_fixture

        result = select_fixture(start=5, thru_all=True)
        assert result == "selfix fixture 5 thru"

    # ---- Select all (Fixture Thru) ----

    def test_select_fixture_all(self):
        """Test selecting all fixtures: selfix fixture thru"""
        from src.commands import select_fixture

        result = select_fixture(select_all=True)
        assert result == "selfix fixture thru"

    # ---- Clear commands ----

    def test_clear(self):
        """Test clear command - sequentially clears selection, active values, or programmer."""
        from src.commands import clear

        result = clear()
        assert result == "clear"

    def test_clear_selection(self):
        """Test clearing selection - deselects all fixtures."""
        from src.commands import clear_selection

        result = clear_selection()
        assert result == "clearselection"

    def test_clear_active(self):
        """Test clearing active values - inactivates all values in programmer."""
        from src.commands import clear_active

        result = clear_active()
        assert result == "clearactive"

    def test_clear_all(self):
        """Test clearing all - empties the entire programmer."""
        from src.commands import clear_all

        result = clear_all()
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

        result = label_group(1, "Front Wash")
        assert result == 'label group 1 "Front Wash"'

    def test_select_group(self):
        """Test selecting a group - default function is SelFix."""
        from src.commands import select_group

        result = select_group(1)
        assert result == "group 1"

    def test_select_group_with_range(self):
        """Test selecting a range of groups: group 1 thru 5"""
        from src.commands import select_group

        result = select_group(1, end=5)
        assert result == "group 1 thru 5"

    def test_select_multiple_groups(self):
        """Test selecting multiple groups: group 1 + 3 + 5"""
        from src.commands import select_group

        result = select_group([1, 3, 5])
        assert result == "group 1 + 3 + 5"

    def test_delete_group(self):
        """Test deleting a group."""
        from src.commands import delete_group

        result = delete_group(1)
        assert result == "delete group 1"


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
        import pytest

        with pytest.raises(ValueError):
            preset_type()

    def test_preset_type_attribute_without_feature_raises_error(self):
        """Test that providing attribute without feature raises ValueError."""
        from src.commands import preset_type
        import pytest

        with pytest.raises(ValueError):
            preset_type(3, attribute=1)


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


class TestStoreCommands:
    """Tests for the Store keyword and its various options."""

    # ---- Basic store (default is cue) ----

    def test_store_cue_basic(self):
        """Test basic cue store: store 7"""
        from src.commands import store_cue

        result = store_cue(7)
        assert result == "store cue 7"

    def test_store_cue_with_explicit_keyword(self):
        """Test cue store with explicit cue keyword."""
        from src.commands import store_cue

        result = store_cue(1)
        assert result == "store cue 1"

    # ---- Store cue with name ----

    def test_store_cue_with_name(self):
        """Test storing cue with a name: store cue 5 "Opening"."""
        from src.commands import store_cue

        result = store_cue(5, name="Opening")
        assert result == 'store cue 5 "Opening"'

    # ---- Store cue range using Thru ----

    def test_store_cue_range(self):
        """Test storing cue range: store cue 1 thru 10"""
        from src.commands import store_cue

        result = store_cue(1, end=10)
        assert result == "store cue 1 thru 10"

    def test_store_cue_multiple_ranges(self):
        """Test storing multiple cue ranges: store cue 1 thru 10 + 20 thru 30"""
        from src.commands import store_cue

        result = store_cue(ranges=[(1, 10), (20, 30)])
        assert result == "store cue 1 thru 10 + 20 thru 30"

    # ---- Store with single options (no value) ----

    def test_store_cue_with_merge_option(self):
        """Test store with merge option: store cue 1 /merge"""
        from src.commands import store_cue

        result = store_cue(1, merge=True)
        assert result == "store cue 1 /merge"

    def test_store_cue_with_overwrite_option(self):
        """Test store with overwrite option: store cue 1 /overwrite"""
        from src.commands import store_cue

        result = store_cue(1, overwrite=True)
        assert result == "store cue 1 /overwrite"

    def test_store_cue_with_remove_option(self):
        """Test store with remove option: store cue 1 /remove"""
        from src.commands import store_cue

        result = store_cue(1, remove=True)
        assert result == "store cue 1 /remove"

    def test_store_cue_with_noconfirm_option(self):
        """Test store with noconfirm option: store cue 1 /noconfirm"""
        from src.commands import store_cue

        result = store_cue(1, noconfirm=True)
        assert result == "store cue 1 /noconfirm"

    # ---- Store with value options ----

    def test_store_cue_with_cueonly_true(self):
        """Test store with cueonly=true: store cue 1 /cueonly=true"""
        from src.commands import store_cue

        result = store_cue(1, cueonly=True)
        assert result == "store cue 1 /cueonly=true"

    def test_store_cue_with_tracking_false(self):
        """Test store with tracking=false: store cue 1 /tracking=false"""
        from src.commands import store_cue

        result = store_cue(1, tracking=False)
        assert result == "store cue 1 /tracking=false"

    def test_store_cue_with_source_option(self):
        """Test store with source option: store cue 1 /source=output"""
        from src.commands import store_cue

        result = store_cue(1, source="output")
        assert result == "store cue 1 /source=output"

    # ---- Store with multiple options ----

    def test_store_cue_with_multiple_options(self):
        """Test store with multiple options: store cue 1 /merge /noconfirm"""
        from src.commands import store_cue

        result = store_cue(1, merge=True, noconfirm=True)
        assert "/merge" in result
        assert "/noconfirm" in result
        assert result.startswith("store cue 1")

    def test_store_cue_with_mixed_options(self):
        """Test store with mixed option types."""
        from src.commands import store_cue

        result = store_cue(1, cueonly=True, merge=True)
        assert "/cueonly=true" in result
        assert "/merge" in result

    # ---- Store preset scope options ----

    def test_store_preset_with_global_option(self):
        """Test store preset with global scope: store preset 1.3 /global"""
        from src.commands import store_preset

        result = store_preset("dimmer", 3, global_scope=True)
        assert result == "store preset 1.3 /global"

    def test_store_preset_with_selective_option(self):
        """Test store preset with selective scope: store preset 1.3 /selective"""
        from src.commands import store_preset

        result = store_preset("dimmer", 3, selective=True)
        assert result == "store preset 1.3 /selective"

    def test_store_preset_with_universal_option(self):
        """Test store preset with universal scope: store preset 1.3 /universal"""
        from src.commands import store_preset

        result = store_preset("dimmer", 3, universal=True)
        assert result == "store preset 1.3 /universal"

    def test_store_preset_with_embedded_option(self):
        """Test store preset with embedded option: store preset 1.3 /embedded"""
        from src.commands import store_preset

        result = store_preset("dimmer", 3, embedded=True)
        assert result == "store preset 1.3 /embedded"

    def test_store_preset_complex_options(self):
        """Test store preset with presetfilter and keepactive options."""
        from src.commands import store_preset

        result = store_preset("dimmer", 3, presetfilter=False, keepactive=True)
        assert "/presetfilter=false" in result
        assert "/keepactive=true" in result

    # ---- General store function ----

    def test_store_generic_object(self):
        """Test storing generic object type."""
        from src.commands import store

        result = store("macro", 5)
        assert result == "store macro 5"

    def test_store_generic_with_name(self):
        """Test storing generic object with name."""
        from src.commands import store

        result = store("macro", 5, name="Reset All")
        assert result == 'store macro 5 "Reset All"'

    def test_store_generic_with_options(self):
        """Test storing generic object with options."""
        from src.commands import store

        result = store("effect", 1, noconfirm=True)
        assert result == "store effect 1 /noconfirm"


class TestAtCommands:
    """Tests for At keyword commands."""

    # ---- Basic At value ----

    def test_at_value(self):
        """Test setting dimmer to value: at 75"""
        from src.commands import at

        result = at(75)
        assert result == "at 75"

    def test_at_value_float(self):
        """Test setting dimmer to float value: at 50.5"""
        from src.commands import at

        result = at(50.5)
        assert result == "at 50.5"

    def test_at_full(self):
        """Test at full: at full"""
        from src.commands import at_full

        result = at_full()
        assert result == "at full"

    def test_at_zero(self):
        """Test at zero: at 0"""
        from src.commands import at_zero

        result = at_zero()
        assert result == "at 0"

    # ---- At with Cue ----

    def test_at_cue(self):
        """Test applying cue values: at cue 3"""
        from src.commands import at

        result = at(cue=3)
        assert result == "at cue 3"

    def test_at_cue_with_sequence(self):
        """Test applying cue values with sequence: at cue 3 sequence 1"""
        from src.commands import at

        result = at(cue=3, sequence=1)
        assert result == "at cue 3 sequence 1"

    # ---- At with Fade/Delay ----

    def test_at_fade(self):
        """Test at fade time: at fade 2"""
        from src.commands import at

        result = at(fade=2)
        assert result == "at fade 2"

    def test_at_delay(self):
        """Test at delay time: at delay 2"""
        from src.commands import at

        result = at(delay=2)
        assert result == "at delay 2"

    # ---- At with Options ----

    def test_at_with_layer(self):
        """Test at with layer option."""
        from src.commands import at

        result = at(75, layer="Value")
        assert result == "at 75 /layer=Value"

    def test_at_with_ignoreselection(self):
        """Test at with ignoreselection option."""
        from src.commands import at

        result = at(50, ignoreselection=True)
        assert result == "at 50 /ignoreselection"

    def test_at_with_status(self):
        """Test at with status (tracking values)."""
        from src.commands import at

        result = at(cue=5, status=True)
        assert result == "at cue 5 /status=true"

    # ---- Attribute At ----

    def test_attribute_at_pan(self):
        """Test setting pan attribute: attribute "Pan" at 20"""
        from src.commands import attribute_at

        result = attribute_at("Pan", 20)
        assert result == 'attribute "Pan" at 20'

    def test_attribute_at_tilt(self):
        """Test setting tilt attribute: attribute "Tilt" at 50"""
        from src.commands import attribute_at

        result = attribute_at("Tilt", 50)
        assert result == 'attribute "Tilt" at 50'

    # ---- Fixture At ----

    def test_fixture_at_value(self):
        """Test fixture at value: fixture 2 at 50"""
        from src.commands import fixture_at

        result = fixture_at(2, 50)
        assert result == "fixture 2 at 50"

    def test_fixture_at_fixture(self):
        """Test fixture at fixture: fixture 2 at fixture 3"""
        from src.commands import fixture_at

        result = fixture_at(2, source_fixture=3)
        assert result == "fixture 2 at fixture 3"

    def test_fixture_at_range(self):
        """Test fixture range at value: fixture 1 thru 10 at 100"""
        from src.commands import fixture_at

        result = fixture_at(1, 100, end=10)
        assert result == "fixture 1 thru 10 at 100"

    # ---- Channel At ----

    def test_channel_at_value(self):
        """Test channel at value: channel 1 at 75"""
        from src.commands import channel_at

        result = channel_at(1, 75)
        assert result == "channel 1 at 75"

    def test_channel_at_channel(self):
        """Test channel at channel: channel 1 at channel 10"""
        from src.commands import channel_at

        result = channel_at(1, source_channel=10)
        assert result == "channel 1 at channel 10"

    def test_channel_at_range(self):
        """Test channel range at value: channel 1 thru 10 at 100"""
        from src.commands import channel_at

        result = channel_at(1, 100, end=10)
        assert result == "channel 1 thru 10 at 100"

    # ---- Group At ----

    def test_group_at(self):
        """Test group at value: group 3 at 50"""
        from src.commands import group_at

        result = group_at(3, 50)
        assert result == "group 3 at 50"

    # ---- Executor At ----

    def test_executor_at(self):
        """Test executor at value: executor 3 at 50"""
        from src.commands import executor_at

        result = executor_at(3, 50)
        assert result == "executor 3 at 50"

    # ---- PresetType At ----

    def test_preset_type_at_value(self):
        """Test preset type at value: presettype 2 at 50"""
        from src.commands import preset_type_at

        result = preset_type_at(2, 50)
        assert result == "presettype 2 at 50"

    def test_preset_type_at_range(self):
        """Test preset type range at value: presettype 2 thru 9 at 50"""
        from src.commands import preset_type_at

        result = preset_type_at(2, 50, end_type=9)
        assert result == "presettype 2 thru 9 at 50"

    def test_preset_type_at_delay(self):
        """Test preset type at delay: presettype 2 thru 9 at delay 2"""
        from src.commands import preset_type_at

        result = preset_type_at(2, 2, end_type=9, delay=2)
        assert result == "presettype 2 thru 9 at delay 2"

    def test_preset_type_at_fade(self):
        """Test preset type at fade: presettype 2 at fade 3"""
        from src.commands import preset_type_at

        result = preset_type_at(2, 3, fade=3)
        assert result == "presettype 2 at fade 3"


class TestMacroPlaceholder:
    """Tests for @ character macro placeholder."""

    def test_macro_with_input_after(self):
        """Test macro with @ at the end: Load @"""
        from src.commands import macro_with_input_after

        result = macro_with_input_after("Load")
        assert result == "Load @"

    def test_macro_with_input_after_complex(self):
        """Test macro with @ at the end for attribute: Attribute Pan At @"""
        from src.commands import macro_with_input_after

        result = macro_with_input_after("Attribute Pan At")
        assert result == "Attribute Pan At @"

    def test_macro_with_input_before(self):
        """Test macro with @ at the beginning: @ Fade 20"""
        from src.commands import macro_with_input_before

        result = macro_with_input_before("Fade 20")
        assert result == "@ Fade 20"


class TestCopyCommands:
    """Tests for Copy keyword commands."""

    # ---- Basic Copy ----

    def test_copy_single_to_target(self):
        """Test copy single object: copy group 1 at 5"""
        from src.commands import copy

        result = copy("group", 1, 5)
        assert result == "copy group 1 at 5"

    def test_copy_cue_to_target(self):
        """Test copy cue: copy cue 2 at 6"""
        from src.commands import copy

        result = copy("cue", 2, 6)
        assert result == "copy cue 2 at 6"

    def test_copy_macro_to_target(self):
        """Test copy macro: copy macro 2 at 6"""
        from src.commands import copy

        result = copy("macro", 2, 6)
        assert result == "copy macro 2 at 6"

    # ---- Copy to Clipboard ----

    def test_copy_to_clipboard(self):
        """Test copy to clipboard: copy cue 5"""
        from src.commands import copy

        result = copy("cue", 5)
        assert result == "copy cue 5"

    def test_copy_cue_to_clipboard(self):
        """Test copy_cue to clipboard: copy cue 5"""
        from src.commands import copy_cue

        result = copy_cue(5)
        assert result == "copy cue 5"

    # ---- Copy with Range (Thru) ----

    def test_copy_range_to_target(self):
        """Test copy range: copy group 1 thru 3 at 11"""
        from src.commands import copy

        result = copy("group", 1, 11, end=3)
        assert result == "copy group 1 thru 3 at 11"

    def test_copy_to_target_range(self):
        """Test copy to target range: copy group 2 at 6 thru 8"""
        from src.commands import copy

        result = copy("group", 2, 6, target_end=8)
        assert result == "copy group 2 at 6 thru 8"

    # ---- Copy with List ----

    def test_copy_list_to_target(self):
        """Test copy list: copy group 1 + 3 + 5 at 10"""
        from src.commands import copy

        result = copy("group", [1, 3, 5], 10)
        assert result == "copy group 1 + 3 + 5 at 10"

    def test_copy_to_target_list(self):
        """Test copy to target list: copy group 1 at 5 + 6 + 7"""
        from src.commands import copy

        result = copy("group", 1, [5, 6, 7])
        assert result == "copy group 1 at 5 + 6 + 7"

    # ---- Copy with Options ----

    def test_copy_with_overwrite(self):
        """Test copy with overwrite option."""
        from src.commands import copy

        result = copy("group", 1, 5, overwrite=True)
        assert result == "copy group 1 at 5 /overwrite"

    def test_copy_with_merge(self):
        """Test copy with merge option."""
        from src.commands import copy

        result = copy("cue", 1, 5, merge=True)
        assert result == "copy cue 1 at 5 /merge"

    def test_copy_with_noconfirm(self):
        """Test copy with noconfirm option."""
        from src.commands import copy

        result = copy("macro", 1, 5, noconfirm=True)
        assert result == "copy macro 1 at 5 /noconfirm"

    def test_copy_with_status(self):
        """Test copy with status option."""
        from src.commands import copy

        result = copy("cue", 1, 5, status=True)
        assert result == "copy cue 1 at 5 /status=true"

    def test_copy_with_cueonly(self):
        """Test copy with cueonly option."""
        from src.commands import copy

        result = copy("cue", 1, 5, cueonly=True)
        assert result == "copy cue 1 at 5 /cueonly=true"

    def test_copy_with_multiple_options(self):
        """Test copy with multiple options."""
        from src.commands import copy

        result = copy("cue", 1, 5, merge=True, noconfirm=True)
        assert result == "copy cue 1 at 5 /merge /noconfirm"

    # ---- copy_cue Convenience Function ----

    def test_copy_cue_basic(self):
        """Test copy_cue convenience function."""
        from src.commands import copy_cue

        result = copy_cue(2, 6)
        assert result == "copy cue 2 at 6"

    def test_copy_cue_with_range(self):
        """Test copy_cue with range."""
        from src.commands import copy_cue

        result = copy_cue(1, 10, end=5)
        assert result == "copy cue 1 thru 5 at 10"

    def test_copy_cue_with_options(self):
        """Test copy_cue with options."""
        from src.commands import copy_cue

        result = copy_cue(1, 10, overwrite=True, noconfirm=True)
        assert result == "copy cue 1 at 10 /overwrite /noconfirm"


class TestMoveCommands:
    """Tests for Move keyword commands."""

    # ---- Basic Move ----

    def test_move_single(self):
        """Test move single object: move group 5 at 9"""
        from src.commands import move

        result = move("group", 5, 9)
        assert result == "move group 5 at 9"

    def test_move_cue(self):
        """Test move cue: move cue 5 at 1"""
        from src.commands import move

        result = move("cue", 5, 1)
        assert result == "move cue 5 at 1"

    def test_move_preset(self):
        """Test move preset: move preset 3 at 10"""
        from src.commands import move

        result = move("preset", 3, 10)
        assert result == "move preset 3 at 10"

    # ---- Move with Range (Thru) ----

    def test_move_range(self):
        """Test move range: move group 1 thru 3 at 10"""
        from src.commands import move

        result = move("group", 1, 10, end=3)
        assert result == "move group 1 thru 3 at 10"

    def test_move_to_target_range(self):
        """Test move to target range: move group 1 at 10 thru 12"""
        from src.commands import move

        result = move("group", 1, 10, target_end=12)
        assert result == "move group 1 at 10 thru 12"

    # ---- Move with List ----

    def test_move_list_to_list(self):
        """Test move list to list: move preset 1 + 3 + 5 at 10 + 12 + 14"""
        from src.commands import move

        result = move("preset", [1, 3, 5], [10, 12, 14])
        assert result == "move preset 1 + 3 + 5 at 10 + 12 + 14"

    def test_move_list_to_single(self):
        """Test move list to single target: move group 1 + 2 + 3 at 10"""
        from src.commands import move

        result = move("group", [1, 2, 3], 10)
        assert result == "move group 1 + 2 + 3 at 10"


class TestAssignCommands:
    """Tests for Assign keyword commands."""

    # ---- Basic Assign ----

    def test_assign_sequence_to_executor(self):
        """Test assign sequence to executor."""
        from src.commands import assign

        result = assign("sequence", 1, "executor", 6)
        assert result == "assign sequence 1 at executor 6"

    def test_assign_sequence_range_to_executor_range(self):
        """Test assign sequence range to executor range."""
        from src.commands import assign

        result = assign("sequence", 1, "executor", 6, source_end=5, target_end=10)
        assert result == "assign sequence 1 thru 5 at executor 6 thru 10"

    def test_assign_dmx_to_channel(self):
        """Test assign DMX address to channel."""
        from src.commands import assign

        result = assign("dmx", "2.101", "channel", 5)
        assert result == "assign dmx 2.101 at channel 5"

    def test_assign_group_to_layout(self):
        """Test assign group to layout with coordinates."""
        from src.commands import assign

        result = assign("group", 1, "layout", 1, x=5, y=2)
        assert result == "assign group 1 at layout 1 /x=5 /y=2"

    def test_assign_with_password(self):
        """Test assign user with password."""
        from src.commands import assign

        result = assign("user", "JohnDoe", password="qwerty")
        assert result == 'assign user JohnDoe /password="qwerty"'

    def test_assign_with_cue_mode(self):
        """Test assign with cue_mode option - use assign_function for this."""
        from src.commands import assign_function

        result = assign_function("go", "execbutton1", "1.1", cue_mode="xassert")
        assert result == "assign go at execbutton1 1.1 /cue_mode=xassert"

    def test_assign_with_reset(self):
        """Test assign with reset option."""
        from src.commands import assign

        result = assign("dmx", "1.1", "channel", 1, reset=True)
        assert result == "assign dmx 1.1 at channel 1 /reset"

    def test_assign_with_break(self):
        """Test assign with break option."""
        from src.commands import assign

        result = assign("dmx", "1.1", "fixture", 1, break_=2)
        assert result == "assign dmx 1.1 at fixture 1 /break=2"

    # ---- assign_function ----

    def test_assign_function_toggle(self):
        """Test assign toggle function to executor."""
        from src.commands import assign_function

        result = assign_function("Toggle", "executor", 101)
        assert result == "assign toggle at executor 101"

    def test_assign_function_go_with_cue_mode(self):
        """Test assign go function with cue_mode."""
        from src.commands import assign_function

        result = assign_function("Go", "execbutton1", "1.1", cue_mode="xassert")
        assert result == "assign go at execbutton1 1.1 /cue_mode=xassert"

    # ---- assign_fade ----

    def test_assign_fade_basic(self):
        """Test assign fade time to cue."""
        from src.commands import assign_fade

        result = assign_fade(3, 5)
        assert result == "assign fade 3 cue 5"

    def test_assign_fade_with_sequence(self):
        """Test assign fade time with sequence."""
        from src.commands import assign_fade

        result = assign_fade(2.5, 3, sequence_id=1)
        assert result == "assign fade 2.5 cue 3 sequence 1"

    # ---- assign_to_layout ----

    def test_assign_to_layout_basic(self):
        """Test assign object to layout with position."""
        from src.commands import assign_to_layout

        result = assign_to_layout("group", 1, 1, x=5, y=2)
        assert result == "assign group 1 at layout 1 /x=5 /y=2"

    def test_assign_to_layout_range(self):
        """Test assign object range to layout."""
        from src.commands import assign_to_layout

        result = assign_to_layout("macro", 1, 2, x=0, y=0, end=5)
        assert result == "assign macro 1 thru 5 at layout 2 /x=0 /y=0"


class TestLabelCommands:
    """Tests for Label keyword commands."""

    def test_label_group(self):
        """Test label group."""
        from src.commands import label

        result = label("group", 3, "All Studiocolors")
        assert result == 'label group 3 "All Studiocolors"'

    def test_label_fixture_range(self):
        """Test label fixture range with auto-enumerate."""
        from src.commands import label

        result = label("fixture", 1, "Mac700 1", end=10)
        assert result == 'label fixture 1 thru 10 "Mac700 1"'

    def test_label_preset_compound_id(self):
        """Test label preset with compound ID."""
        from src.commands import label

        result = label("preset", '"color"."Red"', "Dark Red")
        assert result == 'label preset "color"."Red" "Dark Red"'

    def test_label_with_quoted_name(self):
        """Test label with already quoted name."""
        from src.commands import label

        result = label("macro", 1, '"My Macro"')
        assert result == 'label macro 1 "My Macro"'

    def test_label_multiple_objects(self):
        """Test label multiple objects."""
        from src.commands import label

        result = label("group", [1, 2, 3], "Selected")
        assert result == 'label group 1 + 2 + 3 "Selected"'


class TestAppearanceCommands:
    """Tests for Appearance keyword commands."""

    # ---- RGB Colors ----

    def test_appearance_rgb(self):
        """Test appearance with RGB values."""
        from src.commands import appearance

        result = appearance("preset", "0.1", red=100, green=0, blue=0)
        assert result == "appearance preset 0.1 /r=100 /g=0 /b=0"

    def test_appearance_rgb_full(self):
        """Test appearance with full RGB."""
        from src.commands import appearance

        result = appearance("group", 1, red=50, green=75, blue=100)
        assert result == "appearance group 1 /r=50 /g=75 /b=100"

    # ---- HSB Colors ----

    def test_appearance_hsb(self):
        """Test appearance with HSB values."""
        from src.commands import appearance

        result = appearance("preset", "0.1", hue=0, saturation=100, brightness=50)
        assert result == "appearance preset 0.1 /h=0 /s=100 /br=50"

    def test_appearance_hue_only(self):
        """Test appearance with hue only."""
        from src.commands import appearance

        result = appearance("cue", 1, hue=180)
        assert result == "appearance cue 1 /h=180"

    # ---- Hex Color ----

    def test_appearance_hex_color(self):
        """Test appearance with hex color."""
        from src.commands import appearance

        result = appearance("group", 1, end=5, color="FF0000")
        assert result == "appearance group 1 thru 5 /color=FF0000"

    # ---- Copy from Source ----

    def test_appearance_from_source(self):
        """Test appearance copied from source object."""
        from src.commands import appearance

        result = appearance("macro", 2, source_type="macro", source_id=13)
        assert result == "appearance macro 2 at macro 13"

    def test_appearance_cue_from_group(self):
        """Test appearance cue same as group."""
        from src.commands import appearance

        result = appearance("cue", 1, source_type="group", source_id=2)
        assert result == "appearance cue 1 at group 2"

    # ---- Reset ----

    def test_appearance_reset(self):
        """Test appearance reset."""
        from src.commands import appearance

        result = appearance("preset", 1, reset=True)
        assert result == "appearance preset 1 /reset"

    # ---- Range ----

    def test_appearance_range(self):
        """Test appearance with range."""
        from src.commands import appearance

        result = appearance("group", 1, end=5, hue=240, saturation=100, brightness=75)
        assert result == "appearance group 1 thru 5 /h=240 /s=100 /br=75"

    # ---- Multiple Objects ----

    def test_appearance_multiple_objects(self):
        """Test appearance with multiple objects."""
        from src.commands import appearance

        result = appearance("macro", [1, 3, 5], color="00FF00")
        assert result == "appearance macro 1 + 3 + 5 /color=00FF00"


class TestDeleteCommands:
    """Tests for Delete keyword commands."""

    # ---- Generic Delete ----

    def test_delete_generic(self):
        """Test generic delete: delete cue 7"""
        from src.commands import delete

        result = delete("cue", 7)
        assert result == "delete cue 7"

    def test_delete_group(self):
        """Test delete group: delete group 3"""
        from src.commands import delete

        result = delete("group", 3)
        assert result == "delete group 3"

    def test_delete_fixture(self):
        """Test delete fixture (unpatch): delete fixture 4"""
        from src.commands import delete

        result = delete("fixture", 4)
        assert result == "delete fixture 4"

    def test_delete_world(self):
        """Test delete world: delete world 6"""
        from src.commands import delete

        result = delete("world", 6)
        assert result == "delete world 6"

    def test_delete_range(self):
        """Test delete range: delete cue 1 thru 5"""
        from src.commands import delete

        result = delete("cue", 1, end=5)
        assert result == "delete cue 1 thru 5"

    def test_delete_list(self):
        """Test delete list: delete group 1 + 3 + 5"""
        from src.commands import delete

        result = delete("group", [1, 3, 5])
        assert result == "delete group 1 + 3 + 5"

    def test_delete_with_noconfirm(self):
        """Test delete with noconfirm option."""
        from src.commands import delete

        result = delete("cue", 1, end=5, noconfirm=True)
        assert result == "delete cue 1 thru 5 /noconfirm"

    def test_delete_with_cueonly(self):
        """Test delete with cueonly option."""
        from src.commands import delete

        result = delete("cue", 3, cueonly=True)
        assert result == "delete cue 3 /cueonly"

    def test_delete_with_multiple_options(self):
        """Test delete with multiple options."""
        from src.commands import delete

        result = delete("cue", 1, deletevalues=True, cueonly=True, noconfirm=True)
        assert result == "delete cue 1 /deletevalues /cueonly /noconfirm"

    def test_delete_with_selection_filter(self):
        """Test delete with selection filter."""
        from src.commands import delete

        result = delete("cue", 5, selection_filter="fixture 1 thru 10")
        assert result == "delete cue 5 fixture 1 thru 10"

    # ---- Delete Cue Convenience ----

    def test_delete_cue_basic(self):
        """Test delete cue: delete cue 7"""
        from src.commands import delete_cue

        result = delete_cue(7)
        assert result == "delete cue 7"

    def test_delete_cue_with_sequence(self):
        """Test delete cue with sequence: delete cue 1 sequence 2"""
        from src.commands import delete_cue

        result = delete_cue(1, sequence_id=2)
        assert result == "delete cue 1 sequence 2"

    def test_delete_cue_range(self):
        """Test delete cue range: delete cue 1 thru 5"""
        from src.commands import delete_cue

        result = delete_cue(1, end=5)
        assert result == "delete cue 1 thru 5"

    def test_delete_cue_with_options(self):
        """Test delete cue with options."""
        from src.commands import delete_cue

        result = delete_cue(1, end=5, deletevalues=True, noconfirm=True)
        assert result == "delete cue 1 thru 5 /deletevalues /noconfirm"

    # ---- Delete Group Convenience ----

    def test_delete_group_basic(self):
        """Test delete group basic: delete group 3"""
        from src.commands import delete_group

        result = delete_group(3)
        assert result == "delete group 3"

    def test_delete_group_range(self):
        """Test delete group range: delete group 1 thru 5"""
        from src.commands import delete_group

        result = delete_group(1, end=5)
        assert result == "delete group 1 thru 5"

    def test_delete_group_with_noconfirm(self):
        """Test delete group with noconfirm."""
        from src.commands import delete_group

        result = delete_group(1, noconfirm=True)
        assert result == "delete group 1 /noconfirm"

    # ---- Delete Preset Convenience ----

    def test_delete_preset_by_name(self):
        """Test delete preset by name: delete preset 2.5 (color = presettype 2)"""
        from src.commands import delete_preset

        result = delete_preset("color", 5)
        assert result == "delete preset 2.5"

    def test_delete_preset_by_number(self):
        """Test delete preset by number: delete preset 1.1"""
        from src.commands import delete_preset

        result = delete_preset(1, 1)
        assert result == "delete preset 1.1"

    def test_delete_preset_range(self):
        """Test delete preset range: delete preset 1.1 thru 10"""
        from src.commands import delete_preset

        result = delete_preset(1, 1, end=10)
        assert result == "delete preset 1.1 thru 10"

    # ---- Delete Fixture Convenience ----

    def test_delete_fixture_basic(self):
        """Test delete fixture (unpatch): delete fixture 4"""
        from src.commands import delete_fixture

        result = delete_fixture(4)
        assert result == "delete fixture 4"

    def test_delete_fixture_range(self):
        """Test delete fixture range: delete fixture 1 thru 10"""
        from src.commands import delete_fixture

        result = delete_fixture(1, end=10)
        assert result == "delete fixture 1 thru 10"

    def test_delete_fixture_list(self):
        """Test delete fixture list: delete fixture 1 + 5 + 10"""
        from src.commands import delete_fixture

        result = delete_fixture([1, 5, 10])
        assert result == "delete fixture 1 + 5 + 10"

    # ---- Delete Messages ----

    def test_delete_messages(self):
        """Test delete messages: delete messages"""
        from src.commands import delete_messages

        result = delete_messages()
        assert result == "delete messages"


class TestRemoveCommands:
    """Tests for Remove keyword commands."""

    # ---- Generic Remove ----

    def test_remove_basic(self):
        """Test basic remove: remove"""
        from src.commands import remove

        result = remove()
        assert result == "remove"

    def test_remove_selection(self):
        """Test remove selection: remove selection"""
        from src.commands import remove

        result = remove("selection")
        assert result == "remove selection"

    def test_remove_fixture_with_id(self):
        """Test remove fixture: remove fixture 1"""
        from src.commands import remove

        result = remove("fixture", 1)
        assert result == "remove fixture 1"

    def test_remove_with_range(self):
        """Test remove with range: remove fixture 1 thru 10"""
        from src.commands import remove

        result = remove("fixture", 1, end=10)
        assert result == "remove fixture 1 thru 10"

    def test_remove_with_if_filter(self):
        """Test remove with if filter: remove fixture 1 if PresetType 1"""
        from src.commands import remove

        result = remove("fixture", 1, if_filter="PresetType 1")
        assert result == "remove fixture 1 if PresetType 1"

    def test_remove_presettype_quoted(self):
        """Test remove presettype: remove presettype "position" """
        from src.commands import remove

        result = remove("presettype", '"position"')
        assert result == 'remove presettype "position"'

    # ---- Remove Selection Convenience ----

    def test_remove_selection_convenience(self):
        """Test remove selection convenience: remove selection"""
        from src.commands import remove_selection

        result = remove_selection()
        assert result == "remove selection"

    # ---- Remove Preset Type Convenience ----

    def test_remove_preset_type_by_name(self):
        """Test remove preset type by name: remove presettype "position" """
        from src.commands import remove_preset_type

        result = remove_preset_type("position")
        assert result == 'remove presettype "position"'

    def test_remove_preset_type_by_number(self):
        """Test remove preset type by number: remove presettype 1"""
        from src.commands import remove_preset_type

        result = remove_preset_type(1)
        assert result == "remove presettype 1"

    def test_remove_preset_type_with_filter(self):
        """Test remove preset type with filter."""
        from src.commands import remove_preset_type

        result = remove_preset_type("color", if_filter="fixture 1 thru 10")
        assert result == 'remove presettype "color" if fixture 1 thru 10'

    # ---- Remove Fixture Convenience ----

    def test_remove_fixture_basic(self):
        """Test remove fixture: remove fixture 1"""
        from src.commands import remove_fixture

        result = remove_fixture(1)
        assert result == "remove fixture 1"

    def test_remove_fixture_range(self):
        """Test remove fixture range: remove fixture 1 thru 10"""
        from src.commands import remove_fixture

        result = remove_fixture(1, end=10)
        assert result == "remove fixture 1 thru 10"

    def test_remove_fixture_list(self):
        """Test remove fixture list: remove fixture 1 + 5 + 10"""
        from src.commands import remove_fixture

        result = remove_fixture([1, 5, 10])
        assert result == "remove fixture 1 + 5 + 10"

    def test_remove_fixture_with_if_filter(self):
        """Test remove fixture with if filter."""
        from src.commands import remove_fixture

        result = remove_fixture(1, if_filter="PresetType 1")
        assert result == "remove fixture 1 if PresetType 1"

    # ---- Remove Effect Convenience ----

    def test_remove_effect_basic(self):
        """Test remove effect: remove effect 1"""
        from src.commands import remove_effect

        result = remove_effect(1)
        assert result == "remove effect 1"

    def test_remove_effect_range(self):
        """Test remove effect range: remove effect 1 thru 5"""
        from src.commands import remove_effect

        result = remove_effect(1, end=5)
        assert result == "remove effect 1 thru 5"


class TestListCommands:
    """Tests for List keyword commands."""

    # ---- Generic List ----

    def test_list_objects_cue(self):
        """Test list cue: list cue"""
        from src.commands import list_objects

        result = list_objects("cue")
        assert result == "list cue"

    def test_list_objects_group_range(self):
        """Test list group range: list group thru 10"""
        from src.commands import list_objects

        result = list_objects("group", end=10)
        assert result == "list group thru 10"

    def test_list_objects_attribute(self):
        """Test list attribute: list attribute"""
        from src.commands import list_objects

        result = list_objects("attribute")
        assert result == "list attribute"

    def test_list_objects_with_filename(self):
        """Test list with filename option."""
        from src.commands import list_objects

        result = list_objects("group", filename="my_groups")
        assert result == "list group /filename=my_groups"

    def test_list_objects_empty(self):
        """Test list without object type: list"""
        from src.commands import list_objects

        result = list_objects()
        assert result == "list"

    # ---- List Cue Convenience ----

    def test_list_cue_basic(self):
        """Test list cue: list cue"""
        from src.commands import list_cue

        result = list_cue()
        assert result == "list cue"

    def test_list_cue_range(self):
        """Test list cue range: list cue 1 thru 10"""
        from src.commands import list_cue

        result = list_cue(1, end=10)
        assert result == "list cue 1 thru 10"

    def test_list_cue_with_sequence(self):
        """Test list cue with sequence: list cue sequence 5"""
        from src.commands import list_cue

        result = list_cue(sequence_id=5)
        assert result == "list cue sequence 5"

    def test_list_cue_with_filename(self):
        """Test list cue with filename."""
        from src.commands import list_cue

        result = list_cue(filename="cue_list")
        assert result == "list cue /filename=cue_list"

    # ---- List Group Convenience ----

    def test_list_group_basic(self):
        """Test list group: list group"""
        from src.commands import list_group

        result = list_group()
        assert result == "list group"

    def test_list_group_range(self):
        """Test list group range: list group thru 10"""
        from src.commands import list_group

        result = list_group(end=10)
        assert result == "list group thru 10"

    def test_list_group_specific_range(self):
        """Test list group specific range: list group 1 thru 5"""
        from src.commands import list_group

        result = list_group(1, end=5)
        assert result == "list group 1 thru 5"

    # ---- List Preset Convenience ----

    def test_list_preset_basic(self):
        """Test list preset: list preset"""
        from src.commands import list_preset

        result = list_preset()
        assert result == "list preset"

    def test_list_preset_by_type(self):
        """Test list preset by type: list preset "color" """
        from src.commands import list_preset

        result = list_preset("color")
        assert result == 'list preset "color"'

    def test_list_preset_with_wildcard(self):
        """Test list preset with wildcard: list preset "color"."m*" """
        from src.commands import list_preset

        result = list_preset("color", '"m*"')
        assert result == 'list preset "color"."m*"'

    def test_list_preset_numeric_type_with_wildcard(self):
        """Test list preset with numeric type: list preset 4."m*" """
        from src.commands import list_preset

        result = list_preset(4, '"m*"')
        assert result == 'list preset 4."m*"'

    # ---- List Attribute Convenience ----

    def test_list_attribute_basic(self):
        """Test list attribute: list attribute"""
        from src.commands import list_attribute

        result = list_attribute()
        assert result == "list attribute"

    def test_list_attribute_with_filename(self):
        """Test list attribute with filename."""
        from src.commands import list_attribute

        result = list_attribute(filename="attrs")
        assert result == "list attribute /filename=attrs"

    # ---- List Messages Convenience ----

    def test_list_messages_basic(self):
        """Test list messages: list messages"""
        from src.commands import list_messages

        result = list_messages()
        assert result == "list messages"

    def test_list_messages_with_condition(self):
        """Test list messages with condition."""
        from src.commands import list_messages

        result = list_messages(condition="error")
        assert result == "list messages /condition=error"


class TestInfoCommands:
    """Tests for Info keyword commands."""

    # ---- Generic Info ----

    def test_info_display(self):
        """Test info display: info group 3"""
        from src.commands import info

        result = info("group", 3)
        assert result == "info group 3"

    def test_info_add_text(self):
        """Test info add text: info group 3 "some text" """
        from src.commands import info

        result = info("group", 3, text="these fixtures are in the back truss")
        assert result == 'info group 3 "these fixtures are in the back truss"'

    def test_info_range(self):
        """Test info range: info cue 1 thru 5"""
        from src.commands import info

        result = info("cue", 1, end=5)
        assert result == "info cue 1 thru 5"

    # ---- Info Group Convenience ----

    def test_info_group_display(self):
        """Test info group display: info group 3"""
        from src.commands import info_group

        result = info_group(3)
        assert result == "info group 3"

    def test_info_group_add_text(self):
        """Test info group add text."""
        from src.commands import info_group

        result = info_group(3, text="main stage fixtures")
        assert result == 'info group 3 "main stage fixtures"'

    def test_info_group_range(self):
        """Test info group range: info group 1 thru 5"""
        from src.commands import info_group

        result = info_group(1, end=5)
        assert result == "info group 1 thru 5"

    # ---- Info Cue Convenience ----

    def test_info_cue_display(self):
        """Test info cue display: info cue 5"""
        from src.commands import info_cue

        result = info_cue(5)
        assert result == "info cue 5"

    def test_info_cue_with_sequence(self):
        """Test info cue with sequence: info cue 5 sequence 2"""
        from src.commands import info_cue

        result = info_cue(5, sequence_id=2)
        assert result == "info cue 5 sequence 2"

    def test_info_cue_add_text(self):
        """Test info cue add text."""
        from src.commands import info_cue

        result = info_cue(1, text="opening look")
        assert result == 'info cue 1 "opening look"'

    def test_info_cue_range(self):
        """Test info cue range: info cue 1 thru 10"""
        from src.commands import info_cue

        result = info_cue(1, end=10)
        assert result == "info cue 1 thru 10"

    # ---- Info Preset Convenience ----

    def test_info_preset_display(self):
        """Test info preset display: info preset 4.5"""
        from src.commands import info_preset

        result = info_preset(4, 5)
        assert result == "info preset 4.5"

    def test_info_preset_by_name(self):
        """Test info preset by name: info preset 2.1 (color=2)"""
        from src.commands import info_preset

        result = info_preset("color", 1)
        assert result == "info preset 2.1"

    def test_info_preset_add_text(self):
        """Test info preset add text."""
        from src.commands import info_preset

        result = info_preset(4, 5, text="deep blue")
        assert result == 'info preset 4.5 "deep blue"'


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

        import pytest

        with pytest.raises(ValueError, match="Must provide layout_id"):
            layout()
