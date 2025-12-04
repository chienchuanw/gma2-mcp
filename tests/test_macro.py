"""
Macro Commands Tests

測試 grandMA2 巨集佔位符相關命令的生成。
@ 字元在巨集中用作使用者輸入的佔位符。

測試類別：
- TestMacroPlaceholder: macro_with_input_after, macro_with_input_before 測試
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

