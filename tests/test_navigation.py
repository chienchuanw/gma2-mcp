"""Tests for grandMA2 navigation keywords."""

import pytest


class TestNavigation:
    def test_agenda(self):
        from src.commands import agenda

        assert agenda() == "agenda"

    def test_alert(self):
        from src.commands import alert

        assert alert() == "alert"

    def test_down(self):
        from src.commands import down

        assert down() == "down"

    def test_load_next(self):
        from src.commands import load_next

        assert load_next() == "loadnext"

    def test_load_prev(self):
        from src.commands import load_prev

        assert load_prev() == "loadprev"

    def test_move_3d(self):
        from src.commands import move_3d

        assert move_3d() == "move3d"

    def test_next_row(self):
        from src.commands import next_row

        assert next_row() == "nextrow"

    def test_preview_executor(self):
        from src.commands import preview_executor

        assert preview_executor() == "previewexecutor"

    def test_prev_row(self):
        from src.commands import prev_row

        assert prev_row() == "prevrow"

    def test_rotate_3d(self):
        from src.commands import rotate_3d

        assert rotate_3d() == "rotate3d"

    def test_search(self):
        from src.commands import search

        assert search() == "search"

    def test_up(self):
        from src.commands import up

        assert up() == "up"
