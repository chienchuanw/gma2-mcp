"""
Rate and Speed Keywords Tests

Tests for grandMA2 Rate, Rate1, DoubleRate, HalfRate,
DoubleSpeed, HalfSpeed, and Speed function keyword command generation.
"""


class TestRate:
    """Tests for Rate keyword - set rate of executor."""

    def test_rate_executor(self):
        from src.commands import rate

        assert rate("executor 1") == "rate executor 1"


class TestRate1:
    """Tests for Rate1 keyword - reset rate to 1:1."""

    def test_rate1_executor(self):
        from src.commands import rate1

        assert rate1("executor 3") == "rate1 executor 3"


class TestDoubleRate:
    """Tests for DoubleRate keyword - double the rate."""

    def test_double_rate_executor(self):
        from src.commands import double_rate

        assert double_rate("executor 1") == "doublerate executor 1"


class TestHalfRate:
    """Tests for HalfRate keyword - halve the rate."""

    def test_half_rate_executor(self):
        from src.commands import half_rate

        assert half_rate("executor 1") == "halfrate executor 1"


class TestDoubleSpeed:
    """Tests for DoubleSpeed keyword - double the speed."""

    def test_double_speed_executor(self):
        from src.commands import double_speed

        assert double_speed("executor 1") == "doublespeed executor 1"


class TestHalfSpeed:
    """Tests for HalfSpeed keyword - halve the speed."""

    def test_half_speed_executor(self):
        from src.commands import half_speed

        assert half_speed("executor 1") == "halfspeed executor 1"


class TestSpeed:
    """Tests for Speed keyword - set speed of executor."""

    def test_speed_executor(self):
        from src.commands import speed

        assert speed("executor 3") == "speed executor 3"
