"""
Step Timing Keywords Tests

Tests for grandMA2 SnapPercent, StepFade, StepInFade, StepOutFade,
and FadePath function keyword command generation.
"""


class TestSnapPercent:
    """Tests for SnapPercent keyword - set snap percentage."""

    def test_snap_percent_value(self):
        from src.commands import snap_percent

        assert snap_percent(50) == "snappercent 50"


class TestStepFade:
    """Tests for StepFade keyword - set step fade time."""

    def test_step_fade_value(self):
        from src.commands import step_fade

        assert step_fade(2) == "stepfade 2"


class TestStepInFade:
    """Tests for StepInFade keyword - set step in-fade time."""

    def test_step_in_fade_value(self):
        from src.commands import step_in_fade

        assert step_in_fade(3) == "stepinfade 3"


class TestStepOutFade:
    """Tests for StepOutFade keyword - set step out-fade time."""

    def test_step_out_fade_value(self):
        from src.commands import step_out_fade

        assert step_out_fade(1) == "stepoutfade 1"


class TestFadePath:
    """Tests for FadePath keyword - set fade path."""

    def test_fade_path_value(self):
        from src.commands import fade_path

        assert fade_path(2) == "fadepath 2"
