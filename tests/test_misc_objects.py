"""
Misc Object Keywords Tests

Tests for grandMA2 remaining object keywords: Camera, ChannelLink, Filter,
FixtureType, Form, Gel, Image, Item3D, Layer, Macro, Mask, Master, MasterFade,
MediaServer, Menu, Message, Messages, Model, Plugin, PMArea, Profile, Protocol,
Root, Screen, SearchResult, Selection, SpecialMaster, Surface, User, UserProfile,
Value, View, ViewButton, ViewPage, World.
"""


class TestObjectsWithId:
    """Tests for object keywords that accept an integer ID."""

    def test_camera(self):
        from src.commands import camera

        assert camera(1) == "camera 1"

    def test_channel_link(self):
        from src.commands import channel_link

        assert channel_link(3) == "channellink 3"

    def test_fixture_type(self):
        from src.commands import fixture_type

        assert fixture_type(2) == "fixturetype 2"

    def test_form(self):
        from src.commands import form

        assert form(1) == "form 1"

    def test_gel(self):
        from src.commands import gel

        assert gel(5) == "gel 5"

    def test_image(self):
        from src.commands import image

        assert image(3) == "image 3"

    def test_item_3d(self):
        from src.commands import item_3d

        assert item_3d(1) == "item3d 1"

    def test_layer(self):
        from src.commands import layer

        assert layer(2) == "layer 2"

    def test_macro(self):
        from src.commands import macro

        assert macro(5) == "macro 5"

    def test_mask(self):
        from src.commands import mask

        assert mask(1) == "mask 1"

    def test_master(self):
        from src.commands import master

        assert master(3) == "master 3"

    def test_master_fade(self):
        from src.commands import master_fade

        assert master_fade(1) == "masterfade 1"

    def test_media_server(self):
        from src.commands import media_server

        assert media_server(1) == "mediaserver 1"

    def test_menu(self):
        from src.commands import menu

        assert menu(2) == "menu 2"

    def test_model(self):
        from src.commands import model

        assert model(1) == "model 1"

    def test_plugin(self):
        from src.commands import plugin

        assert plugin(3) == "plugin 3"

    def test_pm_area(self):
        from src.commands import pm_area

        assert pm_area(1) == "pmarea 1"

    def test_profile(self):
        from src.commands import profile

        assert profile(2) == "profile 2"

    def test_protocol(self):
        from src.commands import protocol

        assert protocol(1) == "protocol 1"

    def test_screen(self):
        from src.commands import screen

        assert screen(3) == "screen 3"

    def test_special_master(self):
        from src.commands import special_master

        assert special_master(1) == "specialmaster 1"

    def test_surface(self):
        from src.commands import surface

        assert surface(2) == "surface 2"

    def test_user(self):
        from src.commands import user

        assert user(1) == "user 1"

    def test_user_profile(self):
        from src.commands import user_profile

        assert user_profile(3) == "userprofile 3"

    def test_view(self):
        from src.commands import view

        assert view(3) == "view 3"

    def test_view_button(self):
        from src.commands import view_button

        assert view_button(1) == "viewbutton 1"

    def test_view_page(self):
        from src.commands import view_page

        assert view_page(2) == "viewpage 2"

    def test_world(self):
        from src.commands import world

        assert world(1) == "world 1"


class TestObjectsWithoutId:
    """Tests for object keywords that return static strings."""

    def test_filter_keyword(self):
        from src.commands import filter_keyword

        assert filter_keyword() == "filter"

    def test_message(self):
        from src.commands import message

        assert message() == "message"

    def test_messages(self):
        from src.commands import messages

        assert messages() == "messages"

    def test_root(self):
        from src.commands import root

        assert root() == "root"

    def test_search_result(self):
        from src.commands import search_result

        assert search_result() == "searchresult"

    def test_selection(self):
        from src.commands import selection

        assert selection() == "selection"

    def test_value_keyword(self):
        from src.commands import value_keyword

        assert value_keyword() == "value"
