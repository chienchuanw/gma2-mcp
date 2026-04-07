"""
Executor Control Keywords Tests

Tests for grandMA2 Off, On, Kill, Flash, Swop, Stomp, Temp, Toggle,
Release, Top, and Select function keyword command generation.
"""

import pytest


class TestOff:
    """Tests for Off keyword - turns off executor."""

    def test_off_no_args(self):
        from src.commands import off

        assert off() == "off"

    def test_off_target(self):
        from src.commands import off

        assert off("executor 3") == "off executor 3"

    def test_off_executor_kwarg(self):
        from src.commands import off

        assert off(executor=5) == "off executor 5"


class TestOn:
    """Tests for On keyword - turns on executor."""

    def test_on_no_args(self):
        from src.commands import on

        assert on() == "on"

    def test_on_target(self):
        from src.commands import on

        assert on("executor 3") == "on executor 3"


class TestKill:
    """Tests for Kill keyword - immediately turns off executor."""

    def test_kill_no_args(self):
        from src.commands import kill

        assert kill() == "kill"

    def test_kill_target(self):
        from src.commands import kill

        assert kill("executor 3") == "kill executor 3"


class TestFlash:
    """Tests for Flash keyword - flashes executor."""

    def test_flash_target(self):
        from src.commands import flash

        assert flash("executor 1") == "flash executor 1"


class TestSwop:
    """Tests for Swop keyword - swops executor."""

    def test_swop_target(self):
        from src.commands import swop

        assert swop("executor 3") == "swop executor 3"


class TestStomp:
    """Tests for Stomp keyword - stomps executor."""

    def test_stomp_target(self):
        from src.commands import stomp

        assert stomp("executor 1") == "stomp executor 1"


class TestTemp:
    """Tests for Temp keyword - temporary executor activation."""

    def test_temp_target(self):
        from src.commands import temp

        assert temp("executor 3") == "temp executor 3"


class TestToggle:
    """Tests for Toggle keyword - toggles executor on/off."""

    def test_toggle_target(self):
        from src.commands import toggle

        assert toggle("executor 1") == "toggle executor 1"


class TestRelease:
    """Tests for Release keyword - releases executor."""

    def test_release_no_args(self):
        from src.commands import release

        assert release() == "release"

    def test_release_target(self):
        from src.commands import release

        assert release("executor 3") == "release executor 3"


class TestTop:
    """Tests for Top keyword - sets executor to top priority."""

    def test_top_target(self):
        from src.commands import top

        assert top("executor 1") == "top executor 1"


class TestSelect:
    """Tests for Select keyword - selects objects."""

    def test_select_target(self):
        from src.commands import select

        assert select("executor 5") == "select executor 5"
