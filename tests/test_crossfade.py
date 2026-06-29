"""
Crossfade Keywords Tests

Tests for grandMA2 Crossfade, CrossfadeA, CrossfadeB, and ManualXFade
function keyword command generation.
"""


class TestCrossfade:
    """Tests for Crossfade keyword - manual crossfade control."""

    def test_crossfade_no_args(self):
        from src.commands import crossfade

        assert crossfade() == "crossfade"

    def test_crossfade_executor(self):
        from src.commands import crossfade

        assert crossfade("executor 1") == "crossfade executor 1"


class TestCrossfadeA:
    """Tests for CrossfadeA keyword - crossfade channel A."""

    def test_crossfade_a_no_args(self):
        from src.commands import crossfade_a

        assert crossfade_a() == "crossfadea"


class TestCrossfadeB:
    """Tests for CrossfadeB keyword - crossfade channel B."""

    def test_crossfade_b_no_args(self):
        from src.commands import crossfade_b

        assert crossfade_b() == "crossfadeb"


class TestManualXFade:
    """Tests for ManualXFade keyword - manual crossfade mode."""

    def test_manual_xfade_no_args(self):
        from src.commands import manual_xfade

        assert manual_xfade() == "manualxfade"
