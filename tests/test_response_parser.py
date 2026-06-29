"""
Response Parser Tests

Tests for grandMA2 telnet response parsing functions.
Uses sample telnet output strings as fixtures.
"""

from src.response_parser import (
    detect_error,
    parse_cue_info,
    parse_macro_lines,
    parse_object_label,
    strip_ansi,
)

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
    "No   Name           CMD\n---  ----           ---\n 1   MyLine         Blackout\n"
)

MACRO_LIST_EMPTY_CMD = "No   Name           CMD\n---  ----           ---\n 1   Placeholder    \n"

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

OBJECT_LABEL_OUTPUT = "No   Name\n---  ----\n 1   Front Wash\n"

OBJECT_LABEL_EMPTY_NAME = "No   Name\n---  ----\n 1   \n"


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


# ============================================================================
# strip_ansi - remove ANSI escape sequences and carriage returns
# ============================================================================

# Real captured grandMA2 telnet output (with ANSI color codes + \r)
CLEAR_OK_RAW = "Executing : \x1b[32mClear\x1b[37m\n\r [Fixture]>\x1b[K"
LIST_PRESET_ERROR_RAW = (
    'Executing : \x1b[32mList\x1b[37m \x1b[32mPreset\x1b[37m "color"\n\r'
    '\x1b[31mError : List Preset "color"\x1b[37m\n\r'
    "Error #14: OBJECT DOES NOT EXIST\n\r\r [Fixture]>\x1b[K"
)


class TestStripAnsi:
    def test_removes_color_codes(self):
        assert strip_ansi("\x1b[32mClear\x1b[37m") == "Clear"

    def test_removes_clear_line_code(self):
        assert strip_ansi("[Fixture]>\x1b[K") == "[Fixture]>"

    def test_preserves_plain_text(self):
        assert strip_ansi("Error #14: OBJECT DOES NOT EXIST") == (
            "Error #14: OBJECT DOES NOT EXIST"
        )

    def test_strips_real_clear_output(self):
        assert "\x1b" not in strip_ansi(CLEAR_OK_RAW)


# ============================================================================
# detect_error - identify grandMA2 console errors in a response
# ============================================================================


class TestDetectError:
    def test_numbered_error_returns_code_and_text(self):
        err = detect_error(LIST_PRESET_ERROR_RAW)
        assert err is not None
        assert err["error_code"] == 14
        assert err["error_text"] == "OBJECT DOES NOT EXIST"

    def test_clean_response_returns_none(self):
        assert detect_error(CLEAR_OK_RAW) is None

    def test_empty_response_returns_none(self):
        assert detect_error("") is None

    def test_warning_is_not_an_error(self):
        raw = (
            "Executing : \x1b[32mList\x1b[37m \x1b[32mPreset\x1b[37m 4\n\r"
            "\x1b[31mWARNING, NO OBJECTS FOUND FOR LIST\x1b[37m\n\r [Fixture]>\x1b[K"
        )
        assert detect_error(raw) is None


class TestDetectErrorBareForm:
    def test_unnumbered_error_is_detected(self):
        raw = (
            "Executing : \x1b[32mSomeCmd\x1b[37m\n\r"
            "\x1b[31mError : illegal object\x1b[37m\n\r [Fixture]>\x1b[K"
        )
        err = detect_error(raw)
        assert err is not None
        assert err["error_code"] is None
        assert "illegal object" in err["error_text"]

    def test_numbered_error_still_takes_precedence(self):
        err = detect_error(LIST_PRESET_ERROR_RAW)
        assert err["error_code"] == 14
