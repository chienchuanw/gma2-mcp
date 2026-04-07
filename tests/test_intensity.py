"""
Intensity and Misc Keywords Tests

Tests for grandMA2 Full, ToFull, Zero, ToZero, Load, and Learn
function keyword command generation.
"""

import pytest


class TestFull:
    """Tests for Full keyword - sets to full intensity."""

    def test_full_no_args(self):
        from src.commands import full

        assert full() == "full"


class TestToFull:
    """Tests for ToFull keyword - fades executor to full."""

    def test_to_full_target(self):
        from src.commands import to_full

        assert to_full("executor 1") == "tofull executor 1"


class TestZero:
    """Tests for Zero keyword - sets to zero."""

    def test_zero_no_args(self):
        from src.commands import zero

        assert zero() == "zero"


class TestToZero:
    """Tests for ToZero keyword - fades executor to zero."""

    def test_to_zero_target(self):
        from src.commands import to_zero

        assert to_zero("executor 1") == "tozero executor 1"


class TestLoad:
    """Tests for Load keyword - loads cue into executor."""

    def test_load_target(self):
        from src.commands import load

        assert load("cue 5 executor 1") == "load cue 5 executor 1"


class TestLearn:
    """Tests for Learn keyword - learns speed from taps."""

    def test_learn_no_args(self):
        from src.commands import learn

        assert learn() == "learn"
