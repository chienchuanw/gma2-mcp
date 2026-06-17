"""
Selector grammar tests (#57 phase 2).

normalize_selector validates and normalizes a grandMA2 selection expression
made of integers joined by thru / + / - operators.
"""

import pytest

from src.commands.selector import normalize_selector


class TestNormalizeSelector:
    def test_single_id(self):
        assert normalize_selector("5") == "5"

    def test_thru_range(self):
        assert normalize_selector("1 thru 10") == "1 thru 10"

    def test_plus_list(self):
        assert normalize_selector("1 + 3 + 5") == "1 + 3 + 5"

    def test_minus(self):
        assert normalize_selector("1 thru 10 - 4") == "1 thru 10 - 4"

    def test_normalizes_spacing_and_case(self):
        assert normalize_selector("1  THRU  10+21") == "1 thru 10 + 21"

    def test_accepts_int(self):
        assert normalize_selector(21) == "21"

    def test_accepts_dotted_pool_id(self):
        # Presets/macros use pool.id addressing, e.g. 4.1
        assert normalize_selector("4.1 thru 4.5") == "4.1 thru 4.5"

    def test_rejects_empty(self):
        with pytest.raises(ValueError):
            normalize_selector("")

    def test_rejects_letters(self):
        with pytest.raises(ValueError):
            normalize_selector("group abc")

    def test_rejects_trailing_operator(self):
        with pytest.raises(ValueError):
            normalize_selector("1 thru")

    def test_rejects_injection(self):
        with pytest.raises(ValueError):
            normalize_selector("1; delete group 1")
