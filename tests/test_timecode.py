"""
Timecode command builder tests (Issue #39).

Verified against grandMA2 manual command-line syntax:
Store/Go/Pause/Off/Top/Record Timecode N, Assign Timecode N /Slot = S.
"""

from src.commands.functions.timecode import (
    store_timecode,
    go_timecode,
    pause_timecode,
    off_timecode,
    top_timecode,
    record_timecode,
    assign_timecode_param,
)


class TestTimecodeBuilders:
    def test_store(self):
        assert store_timecode(2) == "store timecode 2"

    def test_go(self):
        assert go_timecode(2) == "go timecode 2"

    def test_pause(self):
        assert pause_timecode(2) == "pause timecode 2"

    def test_off(self):
        assert off_timecode(2) == "off timecode 2"

    def test_top(self):
        assert top_timecode(2) == "top timecode 2"

    def test_record(self):
        assert record_timecode(2) == "record timecode 2"


class TestAssignTimecodeParam:
    def test_slot(self):
        assert assign_timecode_param(1, "slot", 3) == "assign timecode 1 /slot = 3"

    def test_length(self):
        assert (
            assign_timecode_param(1, "length", "1h30m0s")
            == "assign timecode 1 /length = 1h30m0s"
        )

    def test_name_is_quoted(self):
        assert (
            assign_timecode_param(1, "name", "MyShow")
            == 'assign timecode 1 /name = "MyShow"'
        )
