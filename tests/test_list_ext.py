"""Tests for grandMA2 extended list keywords."""


class TestListExt:
    def test_list_effect_library(self):
        from src.commands import list_effect_library

        assert list_effect_library() == "listeffectlibrary"

    def test_list_fader_modules(self):
        from src.commands import list_fader_modules

        assert list_fader_modules() == "listfadermodules"

    def test_list_library(self):
        from src.commands import list_library

        assert list_library() == "listlibrary"

    def test_list_macro_library(self):
        from src.commands import list_macro_library

        assert list_macro_library() == "listmacrolibrary"

    def test_list_oops(self):
        from src.commands import list_oops

        assert list_oops() == "listoops"

    def test_list_owner(self):
        from src.commands import list_owner

        assert list_owner() == "listowner"

    def test_list_plugin_library(self):
        from src.commands import list_plugin_library

        assert list_plugin_library() == "listpluginlibrary"

    def test_list_shows(self):
        from src.commands import list_shows

        assert list_shows() == "listshows"

    def test_list_update(self):
        from src.commands import list_update

        assert list_update() == "listupdate"

    def test_list_user_var(self):
        from src.commands import list_user_var

        assert list_user_var() == "listuservar"

    def test_list_var(self):
        from src.commands import list_var

        assert list_var() == "listvar"
