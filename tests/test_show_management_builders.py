"""
Command builder tests for show file management tools (Issue #5).

Verifies that existing and updated command builders produce correct command
strings for all parameter combinations used by the new MCP show management tools.
"""


class TestSaveShowBuilder:
    def test_no_params(self):
        from src.commands import save_show

        assert save_show() == "saveshow"

    def test_with_name(self):
        from src.commands import save_show

        assert save_show("MyShow") == 'saveshow "MyShow"'

    def test_with_noconfirm(self):
        from src.commands import save_show

        assert save_show(noconfirm=True) == "saveshow /noconfirm"

    def test_with_name_and_noconfirm(self):
        from src.commands import save_show

        assert save_show("MyShow", noconfirm=True) == 'saveshow "MyShow" /noconfirm'


class TestLoadShowBuilder:
    def test_basic(self):
        from src.commands import load_show

        assert load_show("Macbeth") == 'loadshow "Macbeth"'

    def test_with_noconfirm(self):
        from src.commands import load_show

        assert load_show("Macbeth", noconfirm=True) == 'loadshow "Macbeth" /noconfirm'


class TestNewShowBuilder:
    def test_no_params(self):
        from src.commands import new_show

        assert new_show() == "newshow"

    def test_with_name(self):
        from src.commands import new_show

        assert new_show("NewProject") == 'newshow "NewProject"'

    def test_with_name_and_noconfirm(self):
        from src.commands import new_show

        assert new_show("NewProject", noconfirm=True) == 'newshow "NewProject" /noconfirm'

    def test_noconfirm_only(self):
        from src.commands import new_show

        assert new_show(noconfirm=True) == "newshow /noconfirm"


class TestListShowsBuilder:
    def test_no_params(self):
        from src.commands import list_shows

        assert list_shows() == "listshows"

    def test_with_filter(self):
        from src.commands import list_shows

        assert list_shows("Mac*") == "listshows Mac*"
