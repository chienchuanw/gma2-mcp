"""
Fixture Control Keywords Tests

Tests for grandMA2 Align, All, Fix, Locate, Next, Previous, and Invert
function keyword command generation.
"""


class TestAlign:
    """Tests for Align keyword - distributes values across fixtures."""

    def test_align_no_args(self):
        from src.commands import align

        assert align() == "align"

    def test_align_with_mode(self):
        from src.commands import align

        assert align("<") == "align <"


class TestAllKeyword:
    """Tests for All keyword - selects all in context."""

    def test_all_no_args(self):
        from src.commands import all_keyword

        assert all_keyword() == "all"


class TestFix:
    """Tests for Fix keyword - fixes attribute values."""

    def test_fix_no_args(self):
        from src.commands import fix

        assert fix() == "fix"

    def test_fix_executor(self):
        from src.commands import fix

        assert fix("executor 3") == "fix executor 3"


class TestLocate:
    """Tests for Locate keyword - locates fixtures to default position."""

    def test_locate_no_args(self):
        from src.commands import locate

        assert locate() == "locate"


class TestNextKeyword:
    """Tests for Next keyword - selects next fixture."""

    def test_next_no_args(self):
        from src.commands import next_keyword

        assert next_keyword() == "next"


class TestPrevious:
    """Tests for Previous keyword - selects previous fixture."""

    def test_previous_no_args(self):
        from src.commands import previous

        assert previous() == "previous"


class TestInvert:
    """Tests for Invert keyword - inverts selection."""

    def test_invert_no_args(self):
        from src.commands import invert

        assert invert() == "invert"
