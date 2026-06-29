"""
MAtricks Keywords Tests

Tests for grandMA2 MAtricks, MAtricksBlocks, MAtricksFilter, MAtricksGroups,
MAtricksInterleave, MAtricksReset, and MAtricksWings function keyword command generation.
"""


class TestMAtricks:
    """Tests for MAtricks keyword."""

    def test_matricks_no_args(self):
        from src.commands import matricks

        assert matricks() == "matricks"

    def test_matricks_with_target(self):
        from src.commands import matricks

        assert matricks("fixture 1 thru 10") == "matricks fixture 1 thru 10"


class TestMAtricksBlocks:
    """Tests for MAtricksBlocks keyword."""

    def test_matricks_blocks_value(self):
        from src.commands import matricks_blocks

        assert matricks_blocks(4) == "matricksblocks 4"

    def test_matricks_blocks_no_args(self):
        from src.commands import matricks_blocks

        assert matricks_blocks() == "matricksblocks"


class TestMAtricksFilter:
    """Tests for MAtricksFilter keyword."""

    def test_matricks_filter_value(self):
        from src.commands import matricks_filter

        assert matricks_filter(2) == "matricksfilter 2"


class TestMAtricksGroups:
    """Tests for MAtricksGroups keyword."""

    def test_matricks_groups_value(self):
        from src.commands import matricks_groups

        assert matricks_groups(3) == "matricksgroups 3"


class TestMAtricksInterleave:
    """Tests for MAtricksInterleave keyword."""

    def test_matricks_interleave_value(self):
        from src.commands import matricks_interleave

        assert matricks_interleave(2) == "matricksinterleave 2"


class TestMAtricksReset:
    """Tests for MAtricksReset keyword."""

    def test_matricks_reset(self):
        from src.commands import matricks_reset

        assert matricks_reset() == "matricksreset"


class TestMAtricksWings:
    """Tests for MAtricksWings keyword."""

    def test_matricks_wings_value(self):
        from src.commands import matricks_wings

        assert matricks_wings(2) == "matrickswings 2"
