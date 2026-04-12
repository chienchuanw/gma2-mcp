"""
Response Parser Tests

Tests for grandMA2 telnet response parsing functions.
Uses sample telnet output strings as fixtures.
"""

import pytest

from src.response_parser import parse_macro_lines, parse_cue_info, parse_object_label


# ============================================================================
# Fixtures - sample telnet output
# ============================================================================

MACRO_LIST_OUTPUT = (
    "No   Name           CMD\n"
    "---  ----           ---\n"
    " 1                  SetVar $song='Opening+Childhood'\n"
    " 2                  Go Sequence 101\n"
)

MACRO_LIST_SINGLE_LINE = (
    "No   Name           CMD\n"
    "---  ----           ---\n"
    " 1   MyLine         Blackout\n"
)

MACRO_LIST_EMPTY_CMD = (
    "No   Name           CMD\n"
    "---  ----           ---\n"
    " 1   Placeholder    \n"
)

CUE_LIST_OUTPUT = (
    "No       Name        Fade   OutFade  Delay  OutDelay  CMD\n"
    "------   ----        ----   -------  -----  --------  ---\n"
    " 1       Opening     2.0                               Go Macro 5\n"
)

CUE_LIST_NO_CMD = (
    "No       Name        Fade   OutFade  Delay  OutDelay  CMD\n"
    "------   ----        ----   -------  -----  --------  ---\n"
    " 1       Blackout    0.5                               \n"
)

CUE_LIST_MINIMAL = (
    "No       Name        Fade   CMD\n"
    "------   ----        ----   ---\n"
    " 1       Scene1      3.0    \n"
)

OBJECT_LABEL_OUTPUT = (
    "No   Name\n"
    "---  ----\n"
    " 1   Front Wash\n"
)

OBJECT_LABEL_EMPTY_NAME = (
    "No   Name\n"
    "---  ----\n"
    " 1   \n"
)


# ============================================================================
# TestParseMacroLines
# ============================================================================


class TestParseMacroLines:
    """Tests for parse_macro_lines."""

    def test_parse_multiple_lines(self):
        result = parse_macro_lines(MACRO_LIST_OUTPUT)
        assert result["parsed"] is True
        assert len(result["lines"]) == 2
        assert result["lines"][0]["line_number"] == 1
        assert result["lines"][0]["cmd"] == "SetVar $song='Opening+Childhood'"
        assert result["lines"][1]["line_number"] == 2
        assert result["lines"][1]["cmd"] == "Go Sequence 101"

    def test_parse_single_line_with_name(self):
        result = parse_macro_lines(MACRO_LIST_SINGLE_LINE)
        assert result["parsed"] is True
        assert len(result["lines"]) == 1
        assert result["lines"][0]["line_number"] == 1
        assert result["lines"][0]["cmd"] == "Blackout"

    def test_parse_empty_cmd(self):
        result = parse_macro_lines(MACRO_LIST_EMPTY_CMD)
        assert result["parsed"] is True
        assert len(result["lines"]) == 1
        assert result["lines"][0]["cmd"] == ""

    def test_parse_empty_response(self):
        result = parse_macro_lines("")
        assert result["parsed"] is False
        assert result["lines"] == []
        assert result["raw_response"] == ""

    def test_parse_garbage_input(self):
        result = parse_macro_lines("this is not tabular data")
        assert result["parsed"] is False
        assert result["lines"] == []

    def test_parse_header_only(self):
        raw = "No   Name           CMD\n---  ----           ---\n"
        result = parse_macro_lines(raw)
        assert result["parsed"] is True
        assert result["lines"] == []


# ============================================================================
# TestParseCueInfo
# ============================================================================


class TestParseCueInfo:
    """Tests for parse_cue_info."""

    def test_parse_cue_with_cmd(self):
        result = parse_cue_info(CUE_LIST_OUTPUT)
        assert result["parsed"] is True
        assert result["label"] == "Opening"
        assert result["fade"] == "2.0"
        assert result["cmd"] == "Go Macro 5"

    def test_parse_cue_no_cmd(self):
        result = parse_cue_info(CUE_LIST_NO_CMD)
        assert result["parsed"] is True
        assert result["label"] == "Blackout"
        assert result["fade"] == "0.5"
        assert result["cmd"] == ""

    def test_parse_cue_minimal_columns(self):
        result = parse_cue_info(CUE_LIST_MINIMAL)
        assert result["parsed"] is True
        assert result["label"] == "Scene1"
        assert result["fade"] == "3.0"

    def test_parse_empty_response(self):
        result = parse_cue_info("")
        assert result["parsed"] is False
        assert result["raw_response"] == ""

    def test_parse_garbage_input(self):
        result = parse_cue_info("random text without structure")
        assert result["parsed"] is False


# ============================================================================
# TestParseObjectLabel
# ============================================================================


class TestParseObjectLabel:
    """Tests for parse_object_label."""

    def test_parse_label(self):
        result = parse_object_label(OBJECT_LABEL_OUTPUT)
        assert result["parsed"] is True
        assert result["label"] == "Front Wash"

    def test_parse_empty_name(self):
        result = parse_object_label(OBJECT_LABEL_EMPTY_NAME)
        assert result["parsed"] is True
        assert result["label"] == ""

    def test_parse_empty_response(self):
        result = parse_object_label("")
        assert result["parsed"] is False
        assert result["label"] is None
        assert result["raw_response"] == ""

    def test_parse_garbage_input(self):
        result = parse_object_label("no table here")
        assert result["parsed"] is False
        assert result["label"] is None
