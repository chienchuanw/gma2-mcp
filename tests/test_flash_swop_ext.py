"""
Flash/Swop Extension Keywords Tests

Tests for grandMA2 FlashGo, FlashOn, SwopGo, SwopOn, and StoreLook
function keyword command generation.
"""

import pytest


class TestFlashGo:
    """Tests for FlashGo keyword - flash and go."""

    def test_flash_go_executor(self):
        from src.commands import flash_go

        assert flash_go("executor 1") == "flashgo executor 1"


class TestFlashOn:
    """Tests for FlashOn keyword - flash on (latching)."""

    def test_flash_on_executor(self):
        from src.commands import flash_on

        assert flash_on("executor 1") == "flashon executor 1"


class TestSwopGo:
    """Tests for SwopGo keyword - swop and go."""

    def test_swop_go_executor(self):
        from src.commands import swop_go

        assert swop_go("executor 3") == "swopgo executor 3"


class TestSwopOn:
    """Tests for SwopOn keyword - swop on (latching)."""

    def test_swop_on_executor(self):
        from src.commands import swop_on

        assert swop_on("executor 3") == "swopon executor 3"


class TestStoreLook:
    """Tests for StoreLook keyword - store a look."""

    def test_store_look_no_args(self):
        from src.commands import store_look

        assert store_look() == "storelook"

    def test_store_look_target(self):
        from src.commands import store_look

        assert store_look("cue 3") == "storelook cue 3"
