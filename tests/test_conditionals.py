"""Tests for grandMA2 conditional/flow keywords."""


class TestConditionals:
    def test_end_if(self):
        from src.commands import end_if

        assert end_if() == "endif"

    def test_if_active(self):
        from src.commands import if_active

        assert if_active() == "ifactive"

    def test_if_output(self):
        from src.commands import if_output

        assert if_output() == "ifoutput"

    def test_if_prog(self):
        from src.commands import if_prog

        assert if_prog() == "ifprog"

    def test_or_keyword(self):
        from src.commands import or_keyword

        assert or_keyword() == "or"

    def test_with_keyword(self):
        from src.commands import with_keyword

        assert with_keyword() == "with"
