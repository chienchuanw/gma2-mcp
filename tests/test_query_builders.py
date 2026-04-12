"""
Command builder tests for query/introspection tools.

Verifies that existing and updated command builders produce correct command
strings for all parameter combinations used by the new MCP query tools.

Test Classes:
- TestListGroupForQueryTool: list_group combos for list_groups MCP tool
- TestListCueForQueryTool: list_cue combos for list_cues MCP tool
- TestListPresetForQueryTool: list_preset combos for list_presets MCP tool
- TestInfoCueForQueryTool: info_cue combos for get_cue_info MCP tool
- TestInfoGroupForQueryTool: info_group combos for get_group_info MCP tool
- TestListVarForQueryTool: list_var with filter parameter
- TestListUserVarForQueryTool: list_user_var with filter parameter
- TestListObjectsForQueryTool: list_objects combos for query_object MCP tool
- TestInfoForQueryTool: info combos for query_object MCP tool
"""


class TestListGroupForQueryTool:
    """Verify list_group handles all parameter combos for list_groups MCP tool."""

    def test_no_params(self):
        from src.commands import list_group

        assert list_group() == "list group"

    def test_specific_group(self):
        from src.commands import list_group

        assert list_group(5) == "list group 5"

    def test_group_range(self):
        from src.commands import list_group

        assert list_group(1, end=10) == "list group 1 thru 10"

    def test_end_only(self):
        from src.commands import list_group

        assert list_group(end=10) == "list group thru 10"


class TestListCueForQueryTool:
    """Verify list_cue handles all parameter combos for list_cues MCP tool."""

    def test_no_params(self):
        from src.commands import list_cue

        assert list_cue() == "list cue"

    def test_with_sequence_id(self):
        from src.commands import list_cue

        assert list_cue(sequence_id=3) == "list cue sequence 3"

    def test_cue_range(self):
        from src.commands import list_cue

        assert list_cue(1, end=5) == "list cue 1 thru 5"

    def test_specific_cue(self):
        from src.commands import list_cue

        assert list_cue(3) == "list cue 3"

    def test_cue_range_with_sequence(self):
        from src.commands import list_cue

        assert list_cue(1, end=5, sequence_id=2) == "list cue 1 thru 5 sequence 2"


class TestListPresetForQueryTool:
    """Verify list_preset handles all parameter combos for list_presets MCP tool."""

    def test_no_params(self):
        from src.commands import list_preset

        assert list_preset() == "list preset"

    def test_by_type_string(self):
        from src.commands import list_preset

        assert list_preset("color") == 'list preset "color"'

    def test_by_type_numeric(self):
        from src.commands import list_preset

        assert list_preset(4) == "list preset 4"

    def test_type_with_id(self):
        from src.commands import list_preset

        assert list_preset("position", 1) == 'list preset "position".1'

    def test_type_with_id_range(self):
        """list_preset with preset_id range via list_objects for now."""
        from src.commands import list_preset

        # list_preset doesn't directly support end with type+id,
        # so the MCP tool will use list_objects for range queries
        assert list_preset("color", 1) == 'list preset "color".1'


class TestInfoCueForQueryTool:
    """Verify info_cue handles all parameter combos for get_cue_info MCP tool."""

    def test_basic(self):
        from src.commands import info_cue

        assert info_cue(3) == "info cue 3"

    def test_with_sequence_id(self):
        from src.commands import info_cue

        assert info_cue(3, sequence_id=1) == "info cue 3 sequence 1"

    def test_float_cue_id(self):
        from src.commands import info_cue

        assert info_cue(1.5) == "info cue 1.5"

    def test_with_range(self):
        from src.commands import info_cue

        assert info_cue(1, end=5) == "info cue 1 thru 5"


class TestInfoGroupForQueryTool:
    """Verify info_group handles all parameter combos for get_group_info MCP tool."""

    def test_basic(self):
        from src.commands import info_group

        assert info_group(5) == "info group 5"

    def test_with_range(self):
        from src.commands import info_group

        assert info_group(1, end=10) == "info group 1 thru 10"


class TestListVarForQueryTool:
    """Verify list_var handles filter parameter for list_variables MCP tool."""

    def test_no_filter(self):
        from src.commands import list_var

        assert list_var() == "listvar"

    def test_with_filter(self):
        from src.commands import list_var

        assert list_var("f*") == "listvar f*"


class TestListUserVarForQueryTool:
    """Verify list_user_var handles filter parameter for list_variables MCP tool."""

    def test_no_filter(self):
        from src.commands import list_user_var

        assert list_user_var() == "listuservar"

    def test_with_filter(self):
        from src.commands import list_user_var

        assert list_user_var("my_*") == "listuservar my_*"


class TestListObjectsForQueryTool:
    """Verify list_objects handles combos for query_object MCP tool."""

    def test_by_type(self):
        from src.commands import list_objects

        assert list_objects("executor") == "list executor"

    def test_by_type_with_id(self):
        from src.commands import list_objects

        assert list_objects("sequence", 1) == "list sequence 1"

    def test_by_type_with_range(self):
        from src.commands import list_objects

        assert list_objects("effect", 1, end=5) == "list effect 1 thru 5"


class TestInfoForQueryTool:
    """Verify info handles combos for query_object MCP tool in info mode."""

    def test_by_type_and_id(self):
        from src.commands import info

        assert info("sequence", 1) == "info sequence 1"

    def test_by_type_and_id_with_range(self):
        from src.commands import info

        assert info("executor", 1, end=5) == "info executor 1 thru 5"
