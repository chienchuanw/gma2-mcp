"""
Programmer and Show Data Keywords Tests

Tests for grandMA2 Block, Unblock, Clone, Default, Extract, Insert,
Record, Replace, Update, and Oops function keyword command generation.
"""


class TestBlock:
    """Tests for Block keyword - blocks cue tracking."""

    def test_block_no_args(self):
        from src.commands import block

        assert block() == "block"

    def test_block_cue(self):
        from src.commands import block

        assert block("cue 5") == "block cue 5"


class TestUnblock:
    """Tests for Unblock keyword - removes tracking block."""

    def test_unblock_no_args(self):
        from src.commands import unblock

        assert unblock() == "unblock"

    def test_unblock_cue(self):
        from src.commands import unblock

        assert unblock("cue 3") == "unblock cue 3"


class TestClone:
    """Tests for Clone keyword - clones fixture programming."""

    def test_clone_fixture_to_fixture(self):
        from src.commands import clone

        assert clone("fixture 1 at fixture 5") == "clone fixture 1 at fixture 5"


class TestDefault:
    """Tests for Default keyword - resets to default values."""

    def test_default_no_args(self):
        from src.commands import default

        assert default() == "default"

    def test_default_executor(self):
        from src.commands import default

        assert default("executor 1") == "default executor 1"


class TestExtract:
    """Tests for Extract keyword - extracts values from programmer."""

    def test_extract_no_args(self):
        from src.commands import extract

        assert extract() == "extract"


class TestInsert:
    """Tests for Insert keyword - inserts cue/object."""

    def test_insert_cue(self):
        from src.commands import insert

        assert insert("cue 3") == "insert cue 3"


class TestRecord:
    """Tests for Record keyword - records show data."""

    def test_record_no_args(self):
        from src.commands import record

        assert record() == "record"


class TestReplace:
    """Tests for Replace keyword - replaces values."""

    def test_replace_no_args(self):
        from src.commands import replace

        assert replace() == "replace"

    def test_replace_cue(self):
        from src.commands import replace

        assert replace("cue 5") == "replace cue 5"


class TestUpdate:
    """Tests for Update keyword - updates stored data."""

    def test_update_no_args(self):
        from src.commands import update

        assert update() == "update"

    def test_update_cue(self):
        from src.commands import update

        assert update("cue 3") == "update cue 3"


class TestOops:
    """Tests for Oops keyword - undo last action."""

    def test_oops_no_args(self):
        from src.commands import oops

        assert oops() == "oops"
