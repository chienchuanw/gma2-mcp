"""Tests for grandMA2 system management keywords."""


class TestSystemNoArgs:
    def test_backup(self):
        from src.commands import backup

        assert backup() == "backup"

    def test_black_screen(self):
        from src.commands import black_screen

        assert black_screen() == "blackscreen"

    def test_cmd_help(self):
        from src.commands import cmd_help

        assert cmd_help() == "cmdhelp"

    def test_escape(self):
        from src.commands import escape

        assert escape() == "escape"

    def test_exit_keyword(self):
        from src.commands import exit_keyword

        assert exit_keyword() == "exit"

    def test_help_keyword(self):
        from src.commands import help_keyword

        assert help_keyword() == "help"

    def test_lock(self):
        from src.commands import lock

        assert lock() == "lock"

    def test_login(self):
        from src.commands import login

        assert login() == "login"

    def test_logout(self):
        from src.commands import logout

        assert logout() == "logout"

    def test_new_show(self):
        from src.commands import new_show

        assert new_show() == "newshow"

    def test_normal(self):
        from src.commands import normal

        assert normal() == "normal"

    def test_reboot(self):
        from src.commands import reboot

        assert reboot() == "reboot"

    def test_reload_plugins(self):
        from src.commands import reload_plugins

        assert reload_plugins() == "reloadplugins"

    def test_restart(self):
        from src.commands import restart

        assert restart() == "restart"

    def test_save_show(self):
        from src.commands import save_show

        assert save_show() == "saveshow"

    def test_select_drive(self):
        from src.commands import select_drive

        assert select_drive() == "selectdrive"

    def test_setup(self):
        from src.commands import setup

        assert setup() == "setup"

    def test_shutdown(self):
        from src.commands import shutdown

        assert shutdown() == "shutdown"

    def test_tools(self):
        from src.commands import tools

        assert tools() == "tools"

    def test_unlock(self):
        from src.commands import unlock

        assert unlock() == "unlock"

    def test_version(self):
        from src.commands import version

        assert version() == "version"


class TestSystemWithArgs:
    def test_cmd_delay(self):
        from src.commands import cmd_delay

        assert cmd_delay(3) == "cmddelay 3"

    def test_delete_show(self):
        from src.commands import delete_show

        assert delete_show("myshow") == "deleteshow myshow"

    def test_load_show(self):
        from src.commands import load_show

        assert load_show("myshow") == 'loadshow "myshow"'

    def test_set_hostname(self):
        from src.commands import set_hostname

        assert set_hostname("console1") == "sethostname console1"

    def test_set_ip(self):
        from src.commands import set_ip

        assert set_ip("192.168.0.1") == "setip 192.168.0.1"

    def test_set_network_speed(self):
        from src.commands import set_network_speed

        assert set_network_speed("100") == "setnetworkspeed 100"
