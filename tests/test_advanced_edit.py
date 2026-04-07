"""Tests for grandMA2 advanced editing keywords."""

import pytest


class TestAdvancedEdit:
    def test_align_fader_modules(self):
        from src.commands import align_fader_modules

        assert align_fader_modules() == "alignfadermodules"

    def test_all_rows(self):
        from src.commands import all_rows

        assert all_rows() == "allrows"

    def test_auto_create(self):
        from src.commands import auto_create

        assert auto_create() == "autocreate"

    def test_circular_copy(self):
        from src.commands import circular_copy

        assert circular_copy() == "circularcopy"

    def test_export_keyword(self):
        from src.commands import export_keyword

        assert export_keyword() == "export"

    def test_flip(self):
        from src.commands import flip

        assert flip() == "flip"

    def test_identify_fader_module(self):
        from src.commands import identify_fader_module

        assert identify_fader_module() == "identifyfadermodule"

    def test_import_keyword(self):
        from src.commands import import_keyword

        assert import_keyword() == "import"

    def test_interleave(self):
        from src.commands import interleave

        assert interleave() == "interleave"

    def test_remove_individuals(self):
        from src.commands import remove_individuals

        assert remove_individuals() == "removeindividuals"

    def test_shuffle_selection(self):
        from src.commands import shuffle_selection

        assert shuffle_selection() == "shuffleselection"

    def test_shuffle_values(self):
        from src.commands import shuffle_values

        assert shuffle_values() == "shufflevalues"
