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
