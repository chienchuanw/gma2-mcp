"""
Blackout and Global State Keywords Tests

Tests for grandMA2 Blackout, Black, Freeze, Highlight, FullHighlight,
and Solo function keyword command generation.
"""


class TestBlackout:
    """Tests for Blackout keyword - toggles grand blackout."""

    def test_blackout_no_args(self):
        from src.commands import blackout

        assert blackout() == "blackout"


class TestBlack:
    """Tests for Black keyword - sets output to black."""

    def test_black_no_args(self):
        from src.commands import black

        assert black() == "black"

    def test_black_executor(self):
        from src.commands import black

        assert black("executor 1") == "black executor 1"


class TestFreeze:
    """Tests for Freeze keyword - toggles freeze mode."""

    def test_freeze_no_args(self):
        from src.commands import freeze

        assert freeze() == "freeze"

    def test_freeze_executor(self):
        from src.commands import freeze

        assert freeze("executor 1") == "freeze executor 1"


class TestHighlight:
    """Tests for Highlight keyword - toggles highlight mode."""

    def test_highlight_no_args(self):
        from src.commands import highlight

        assert highlight() == "highlight"


class TestFullHighlight:
    """Tests for FullHighlight keyword - toggles full highlight mode."""

    def test_full_highlight_no_args(self):
        from src.commands import full_highlight

        assert full_highlight() == "fullhighlight"


class TestSolo:
    """Tests for Solo keyword - toggles solo mode."""

    def test_solo_no_args(self):
        from src.commands import solo

        assert solo() == "solo"
