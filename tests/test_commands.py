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
