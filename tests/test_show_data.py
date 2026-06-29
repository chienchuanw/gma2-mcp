"""Tests for grandMA2 show data management keywords."""


class TestShowData:
    def test_crash_log_copy(self):
        from src.commands import crash_log_copy

        assert crash_log_copy() == "crashlogcopy"

    def test_crash_log_delete(self):
        from src.commands import crash_log_delete

        assert crash_log_delete() == "crashlogdelete"

    def test_crash_log_list(self):
        from src.commands import crash_log_list

        assert crash_log_list() == "crashloglist"

    def test_lua(self):
        from src.commands import lua

        assert lua() == "lua"

    def test_psr(self):
        from src.commands import psr

        assert psr() == "psr"

    def test_psr_list(self):
        from src.commands import psr_list

        assert psr_list() == "psrlist"

    def test_psr_prepare(self):
        from src.commands import psr_prepare

        assert psr_prepare() == "psrprepare"

    def test_reset_dmx_selection(self):
        from src.commands import reset_dmx_selection

        assert reset_dmx_selection() == "resetdmxselection"

    def test_reset_guid(self):
        from src.commands import reset_guid

        assert reset_guid() == "resetguid"

    def test_thru(self):
        from src.commands import thru

        assert thru() == "thru"

    def test_update_firmware(self):
        from src.commands import update_firmware

        assert update_firmware() == "updatefirmware"

    def test_update_software(self):
        from src.commands import update_software

        assert update_software() == "updatesoftware"

    def test_update_thumbnails(self):
        from src.commands import update_thumbnails

        assert update_thumbnails() == "updatethumbnails"
