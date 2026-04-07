"""
Executor Object Keywords Tests

Tests for grandMA2 Fader, FaderPage, ButtonPage, ChannelFader, ChannelPage,
ExecButton1/2/3, and All*Executors object keyword command generation.
"""

import pytest


class TestFader:
    """Tests for Fader object keyword."""

    def test_fader_with_id(self):
        from src.commands import fader

        assert fader(1) == "fader 1"


class TestFaderPage:
    """Tests for FaderPage object keyword."""

    def test_fader_page_with_id(self):
        from src.commands import fader_page

        assert fader_page(3) == "faderpage 3"


class TestButtonPage:
    """Tests for ButtonPage object keyword."""

    def test_button_page_with_id(self):
        from src.commands import button_page

        assert button_page(2) == "buttonpage 2"


class TestChannelFader:
    """Tests for ChannelFader object keyword."""

    def test_channel_fader_with_id(self):
        from src.commands import channel_fader

        assert channel_fader(5) == "channelfader 5"


class TestChannelPage:
    """Tests for ChannelPage object keyword."""

    def test_channel_page_with_id(self):
        from src.commands import channel_page

        assert channel_page(1) == "channelpage 1"


class TestExecButton1:
    """Tests for ExecButton1 object keyword."""

    def test_exec_button_1_with_id(self):
        from src.commands import exec_button_1

        assert exec_button_1(3) == "execbutton1 3"


class TestExecButton2:
    """Tests for ExecButton2 object keyword."""

    def test_exec_button_2_with_id(self):
        from src.commands import exec_button_2

        assert exec_button_2(3) == "execbutton2 3"


class TestExecButton3:
    """Tests for ExecButton3 object keyword."""

    def test_exec_button_3_with_id(self):
        from src.commands import exec_button_3

        assert exec_button_3(3) == "execbutton3 3"


class TestAllButtonExecutors:
    """Tests for AllButtonExecutors selector."""

    def test_all_button_executors(self):
        from src.commands import all_button_executors

        assert all_button_executors() == "allbuttonexecutors"


class TestAllChaseExecutors:
    """Tests for AllChaseExecutors selector."""

    def test_all_chase_executors(self):
        from src.commands import all_chase_executors

        assert all_chase_executors() == "allchaseexecutors"


class TestAllFaderExecutors:
    """Tests for AllFaderExecutors selector."""

    def test_all_fader_executors(self):
        from src.commands import all_fader_executors

        assert all_fader_executors() == "allfaderexecutors"


class TestAllSequExecutors:
    """Tests for AllSequExecutors selector."""

    def test_all_seq_executors(self):
        from src.commands import all_seq_executors

        assert all_seq_executors() == "allsequexecutors"
