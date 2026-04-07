"""Tests for grandMA2 network/session keywords."""

import pytest


class TestNetworkNoArgs:
    def test_change_dest(self):
        from src.commands import change_dest

        assert change_dest() == "changedest"

    def test_chat(self):
        from src.commands import chat

        assert chat() == "chat"

    def test_disconnect_station(self):
        from src.commands import disconnect_station

        assert disconnect_station() == "disconnectstation"

    def test_drop_control(self):
        from src.commands import drop_control

        assert drop_control() == "dropcontrol"

    def test_end_session(self):
        from src.commands import end_session

        assert end_session() == "endsession"

    def test_invite_station(self):
        from src.commands import invite_station

        assert invite_station() == "invitestation"

    def test_join_session(self):
        from src.commands import join_session

        assert join_session() == "joinsession"

    def test_leave_session(self):
        from src.commands import leave_session

        assert leave_session() == "leavesession"

    def test_network_info(self):
        from src.commands import network_info

        assert network_info() == "networkinfo"

    def test_network_node_info(self):
        from src.commands import network_node_info

        assert network_node_info() == "networknodeinfo"

    def test_network_node_update(self):
        from src.commands import network_node_update

        assert network_node_update() == "networknodeupdate"

    def test_network_speed_test(self):
        from src.commands import network_speed_test

        assert network_speed_test() == "networkspeedtest"

    def test_take_control(self):
        from src.commands import take_control

        assert take_control() == "takecontrol"

    def test_web_remote_prog_only(self):
        from src.commands import web_remote_prog_only

        assert web_remote_prog_only() == "webremoteprogonly"


class TestNetworkWithArgs:
    def test_remote(self):
        from src.commands import remote

        assert remote("192.168.0.5") == "remote 192.168.0.5"

    def test_remote_command(self):
        from src.commands import remote_command

        assert remote_command("go executor 1") == "remotecommand go executor 1"

    def test_telnet(self):
        from src.commands import telnet

        assert telnet("192.168.0.1") == "telnet 192.168.0.1"
