"""
Object Keywords Tests

Tests for grandMA2 Object Keywords command generation.
Object keywords are the "nouns" of the console, used to reference objects in the show file.

Test Classes:
- TestFixtureCommands_Advanced: Tests for fixture keyword
- TestChannelCommands: Tests for channel keyword
- TestPresetCommands: Tests for preset keyword
- TestPresetTypeCommands: Tests for presettype keyword
- TestLayoutCommands: Tests for layout keyword
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

    # ---- Preset Object Keyword Extended Tests ----
    # According to grandMA2 official documentation, Preset supports multiple syntax variations

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

    # ---- Basic Syntax Tests ----

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

    # ---- Feature Syntax Tests ----

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

    # ---- Attribute Syntax Tests ----

    def test_preset_type_with_feature_and_attribute(self):
        """Test preset type with feature and attribute: PresetType 3.2.1"""
        from src.commands import preset_type

        result = preset_type(3, feature=2, attribute=1)
        assert result == "presettype 3.2.1"

    # ---- Variable Syntax Tests ----

    def test_preset_type_variable(self):
        """Test preset type variable: PresetType $preset.2"""
        from src.commands import preset_type

        result = preset_type("$preset", feature=2)
        assert result == "presettype $preset.2"

    # ---- Error Handling Tests ----

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

    Layout is an object type representing the layout of fixtures and other objects.
    The default function of Layout is Select, meaning when Layout is called,
    it selects that Layout and displays it in any Layout View with Link Selected enabled.
    """

    # ---- Basic Layout Selection ----

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

    # ---- Layout Range Selection (using thru) ----

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

    # ---- Layout Multiple Selection (using +) ----

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

    # ---- Error Handling ----

    def test_layout_no_id_raises_error(self):
        """Test that calling layout without ID raises ValueError."""
        from src.commands import layout

        with pytest.raises(ValueError, match="Must provide layout_id"):
            layout()


class TestCueCommands:
    """
    Tests for Cue keyword commands.

    Cue is an object type holding a look on stage. It is the only object type
    that accepts numerical ID as decimal fractions (0.001 to 9999.999).
    The default function is SelFix.
    """

    # ---- Basic Cue Selection ----

    def test_cue_single(self):
        """Test selecting a single cue: cue 3"""
        from src.commands import cue

        result = cue(3)
        assert result == "cue 3"

    def test_cue_decimal(self):
        """Test selecting a decimal cue: cue 3.5"""
        from src.commands import cue

        result = cue(3.5)
        assert result == "cue 3.5"

    def test_cue_precise_decimal(self):
        """Test selecting a precise decimal cue: cue 3.001"""
        from src.commands import cue

        result = cue(3.001)
        assert result == "cue 3.001"

    # ---- Cue Range Selection ----

    def test_cue_range(self):
        """Test selecting cue range: cue 1 thru 10"""
        from src.commands import cue

        result = cue(1, end=10)
        assert result == "cue 1 thru 10"

    def test_cue_range_decimal(self):
        """Test selecting decimal cue range: cue 1.5 thru 3.5"""
        from src.commands import cue

        result = cue(1.5, end=3.5)
        assert result == "cue 1.5 thru 3.5"

    def test_cue_same_start_end(self):
        """Test that same start and end selects a single cue."""
        from src.commands import cue

        result = cue(3, end=3)
        assert result == "cue 3"

    # ---- Cue Multiple Selection ----

    def test_cue_multiple(self):
        """Test selecting multiple cues: cue 1 + 3 + 5"""
        from src.commands import cue

        result = cue([1, 3, 5])
        assert result == "cue 1 + 3 + 5"

    def test_cue_multiple_decimal(self):
        """Test selecting multiple decimal cues: cue 1.5 + 3.5"""
        from src.commands import cue

        result = cue([1.5, 3.5])
        assert result == "cue 1.5 + 3.5"

    def test_cue_list_single_item(self):
        """Test that list with single element returns single cue."""
        from src.commands import cue

        result = cue([7])
        assert result == "cue 7"

    # ---- Cue with Part ----

    def test_cue_with_part(self):
        """Test selecting cue with part: cue 3 part 2"""
        from src.commands import cue

        result = cue(3, part=2)
        assert result == "cue 3 part 2"

    def test_cue_decimal_with_part(self):
        """Test selecting decimal cue with part: cue 3.5 part 1"""
        from src.commands import cue

        result = cue(3.5, part=1)
        assert result == "cue 3.5 part 1"

    # ---- Cue with Executor ----

    def test_cue_with_executor(self):
        """Test selecting cue on executor: cue 3 executor 1"""
        from src.commands import cue

        result = cue(3, executor=1)
        assert result == "cue 3 executor 1"

    def test_cue_decimal_with_executor(self):
        """Test selecting decimal cue on executor: cue 3.999 executor 1"""
        from src.commands import cue

        result = cue(3.999, executor=1)
        assert result == "cue 3.999 executor 1"

    # ---- Cue with Sequence ----

    def test_cue_with_sequence(self):
        """Test selecting cue in sequence: cue 3 sequence 5"""
        from src.commands import cue

        result = cue(3, sequence=5)
        assert result == "cue 3 sequence 5"

    # ---- Complex Cue Selection ----

    def test_cue_with_part_and_executor(self):
        """Test cue with part and executor: cue 3 part 2 executor 1"""
        from src.commands import cue

        result = cue(3, part=2, executor=1)
        assert result == "cue 3 part 2 executor 1"

    # ---- Error Handling ----

    def test_cue_no_id_raises_error(self):
        """Test that calling cue without ID raises ValueError."""
        from src.commands import cue

        with pytest.raises(ValueError, match="Must provide cue_id"):
            cue()


class TestCuePartCommands:
    """
    Tests for cue_part convenience function.

    Parts segment cues to assign different timings for groups of fixture parameters.
    """

    def test_cue_part_basic(self):
        """Test basic cue part: cue 3 part 2"""
        from src.commands import cue_part

        result = cue_part(3, 2)
        assert result == "cue 3 part 2"

    def test_cue_part_decimal_cue(self):
        """Test cue part with decimal cue: cue 2.5 part 1"""
        from src.commands import cue_part

        result = cue_part(2.5, 1)
        assert result == "cue 2.5 part 1"

    def test_cue_part_with_executor(self):
        """Test cue part with executor: cue 3 part 2 executor 1"""
        from src.commands import cue_part

        result = cue_part(3, 2, executor=1)
        assert result == "cue 3 part 2 executor 1"

    def test_cue_part_with_sequence(self):
        """Test cue part with sequence: cue 3 part 2 sequence 5"""
        from src.commands import cue_part

        result = cue_part(3, 2, sequence=5)
        assert result == "cue 3 part 2 sequence 5"


class TestSequenceCommands:
    """
    Tests for Sequence keyword commands.

    Sequence is an object type containing cues. The default function is SelFix.
    """

    # ---- Basic Sequence Selection ----

    def test_sequence_single(self):
        """Test selecting a single sequence: sequence 3"""
        from src.commands import sequence

        result = sequence(3)
        assert result == "sequence 3"

    # ---- Sequence Range Selection ----

    def test_sequence_range(self):
        """Test selecting sequence range: sequence 1 thru 5"""
        from src.commands import sequence

        result = sequence(1, end=5)
        assert result == "sequence 1 thru 5"

    def test_sequence_same_start_end(self):
        """Test that same start and end selects a single sequence."""
        from src.commands import sequence

        result = sequence(3, end=3)
        assert result == "sequence 3"

    # ---- Sequence Multiple Selection ----

    def test_sequence_multiple(self):
        """Test selecting multiple sequences: sequence 1 + 3 + 5"""
        from src.commands import sequence

        result = sequence([1, 3, 5])
        assert result == "sequence 1 + 3 + 5"

    def test_sequence_list_single_item(self):
        """Test that list with single element returns single sequence."""
        from src.commands import sequence

        result = sequence([7])
        assert result == "sequence 7"

    # ---- Sequence with Pool ----

    def test_sequence_with_pool(self):
        """Test selecting sequence in pool: sequence 2.5"""
        from src.commands import sequence

        result = sequence(5, pool=2)
        assert result == "sequence 2.5"

    # ---- Error Handling ----

    def test_sequence_no_id_raises_error(self):
        """Test that calling sequence without ID raises ValueError."""
        from src.commands import sequence

        with pytest.raises(ValueError, match="Must provide sequence_id"):
            sequence()

    def test_sequence_pool_with_list_raises_error(self):
        """Test that using pool with list raises ValueError."""
        from src.commands import sequence

        with pytest.raises(ValueError, match="Cannot use pool with multiple"):
            sequence([1, 2], pool=2)


class TestExecutorCommands:
    """
    Tests for Executor keyword commands.

    Executor is an object type that can hold sequences, chasers, or other objects.
    """

    # ---- Basic Executor Selection ----

    def test_executor_single(self):
        """Test selecting a single executor: executor 3"""
        from src.commands import executor

        result = executor(3)
        assert result == "executor 3"

    # ---- Executor Range Selection ----

    def test_executor_range(self):
        """Test selecting executor range: executor 1 thru 5"""
        from src.commands import executor

        result = executor(1, end=5)
        assert result == "executor 1 thru 5"

    def test_executor_same_start_end(self):
        """Test that same start and end selects a single executor."""
        from src.commands import executor

        result = executor(3, end=3)
        assert result == "executor 3"

    # ---- Executor Multiple Selection ----

    def test_executor_multiple(self):
        """Test selecting multiple executors: executor 1 + 3 + 5"""
        from src.commands import executor

        result = executor([1, 3, 5])
        assert result == "executor 1 + 3 + 5"

    def test_executor_list_single_item(self):
        """Test that list with single element returns single executor."""
        from src.commands import executor

        result = executor([7])
        assert result == "executor 7"

    # ---- Executor with Page ----

    def test_executor_with_page(self):
        """Test selecting executor on page: executor 2.5"""
        from src.commands import executor

        result = executor(5, page=2)
        assert result == "executor 2.5"

    # ---- Error Handling ----

    def test_executor_no_id_raises_error(self):
        """Test that calling executor without ID raises ValueError."""
        from src.commands import executor

        with pytest.raises(ValueError, match="Must provide executor_id"):
            executor()

    def test_executor_page_with_list_raises_error(self):
        """Test that using page with list raises ValueError."""
        from src.commands import executor

        with pytest.raises(ValueError, match="Cannot use page with multiple"):
            executor([1, 2], page=2)
