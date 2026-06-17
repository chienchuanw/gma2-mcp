"""
Verified Execution Core Tests

Tests for the structured execution result built from a grandMA2 telnet reply.
Uses real captured console output (with ANSI codes) as fixtures.
"""

from src.execution import ExecutionResult, build_result


CLEAR_OK_RAW = "Executing : \x1b[32mClear\x1b[37m\n\r [Fixture]>\x1b[K"
LIST_PRESET_ERROR_RAW = (
    'Executing : \x1b[32mList\x1b[37m \x1b[32mPreset\x1b[37m "color"\n\r'
    '\x1b[31mError : List Preset "color"\x1b[37m\n\r'
    "Error #14: OBJECT DOES NOT EXIST\n\r\r [Fixture]>\x1b[K"
)


class TestBuildResult:
    def test_success_response(self):
        result = build_result("Clear", CLEAR_OK_RAW)
        assert isinstance(result, ExecutionResult)
        assert result.ok is True
        assert result.error_code is None
        assert result.error_text is None
        assert result.raw == CLEAR_OK_RAW

    def test_error_response(self):
        result = build_result('List Preset "color"', LIST_PRESET_ERROR_RAW)
        assert result.ok is False
        assert result.error_code == 14
        assert result.error_text == "OBJECT DOES NOT EXIST"
        assert result.raw == LIST_PRESET_ERROR_RAW

    def test_echo_is_ansi_stripped(self):
        result = build_result("Clear", CLEAR_OK_RAW)
        assert "\x1b" not in result.echo

    def test_summary_on_error_includes_code_and_text(self):
        result = build_result('List Preset "color"', LIST_PRESET_ERROR_RAW)
        summary = result.summary()
        assert "14" in summary
        assert "OBJECT DOES NOT EXIST" in summary

    def test_summary_on_success_is_not_an_error(self):
        result = build_result("Clear", CLEAR_OK_RAW)
        assert "Error" not in result.summary()
