"""
Macro Commands Tests

Tests for grandMA2 macro placeholder command generation.
The @ character is used as a placeholder for user input in macros.

Test Classes:
- TestMacroPlaceholder: Tests for macro_with_input_after, macro_with_input_before
"""

import pytest


class TestMacroPlaceholder:
    """Tests for @ character macro placeholder."""

    def test_macro_with_input_after(self):
        """Test macro with @ at the end: Load @"""
        from src.commands import macro_with_input_after

        result = macro_with_input_after("Load")
        assert result == "Load @"

    def test_macro_with_input_after_complex(self):
        """Test macro with @ at the end for attribute: Attribute Pan At @"""
        from src.commands import macro_with_input_after

        result = macro_with_input_after("Attribute Pan At")
        assert result == "Attribute Pan At @"

    def test_macro_with_input_before(self):
        """Test macro with @ at the beginning: @ Fade 20"""
        from src.commands import macro_with_input_before

        result = macro_with_input_before("Fade 20")
        assert result == "@ Fade 20"


class TestStoreMacro:
    """Tests for store_macro command builder."""

    def test_store_macro_without_name(self):
        from src.commands import store_macro

        result = store_macro(macro_id=5)
        assert result == "store macro 5"

    def test_store_macro_with_name(self):
        from src.commands import store_macro

        result = store_macro(macro_id=5, name="My Macro")
        assert result == 'store macro 5 "My Macro"'


class TestLabelMacro:
    """Tests for label_macro command builder."""

    def test_label_macro(self):
        from src.commands import label_macro

        result = label_macro(macro_id=5, name="Dimmer Chase")
        assert result == 'label macro 5 "Dimmer Chase"'


class TestDeleteMacro:
    """Tests for delete_macro command builder."""

    def test_delete_macro_default_pool(self):
        from src.commands import delete_macro

        result = delete_macro(macro_id=5)
        assert result == "delete macro 1.5"

    def test_delete_macro_custom_pool(self):
        from src.commands import delete_macro

        result = delete_macro(macro_id=5, pool=2)
        assert result == "delete macro 2.5"
