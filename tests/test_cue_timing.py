"""
Cue Timing Keywords Tests

Tests for grandMA2 Delay, OutDelay, Fade, and OutFade
function keyword command generation.
"""

import pytest


class TestDelay:
    """Tests for Delay keyword - sets delay time."""

    def test_delay_value(self):
        from src.commands import delay

        assert delay(3) == "delay 3"

    def test_delay_with_target(self):
        from src.commands import delay

        assert delay(2, target="cue 5") == "delay 2 cue 5"


class TestOutDelay:
    """Tests for OutDelay keyword - sets output delay time."""

    def test_out_delay_value(self):
        from src.commands import out_delay

        assert out_delay(3) == "outdelay 3"


class TestFade:
    """Tests for Fade keyword - sets fade time."""

    def test_fade_value(self):
        from src.commands import fade

        assert fade(2) == "fade 2"

    def test_fade_with_target(self):
        from src.commands import fade

        assert fade(3, target="cue 5") == "fade 3 cue 5"


class TestOutFade:
    """Tests for OutFade keyword - sets output fade time."""

    def test_out_fade_value(self):
        from src.commands import out_fade

        assert out_fade(3) == "outfade 3"
