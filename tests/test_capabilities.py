"""Unit tests for the capabilities serializer (issue #85).

The capabilities tool exposes the MCP's version, tool list, and the show-profile
schema version it targets, so gma2-workflow can run a startup contract self-check.
"""

import pytest


class TestBuildCapabilities:
    def test_returns_version_tools_and_schema_version(self):
        from src.capabilities import build_capabilities

        caps = build_capabilities(
            version="0.1.0",
            tool_names=["toggle_blackout", "store_cue"],
            profile_schema_version=1,
        )

        assert caps["version"] == "0.1.0"
        assert caps["profile_schema_version"] == 1
        assert "toggle_blackout" in caps["tools"]
        assert "store_cue" in caps["tools"]

    def test_tools_are_sorted(self):
        from src.capabilities import build_capabilities

        caps = build_capabilities(
            version="0.1.0",
            tool_names=["store_cue", "apply_preset", "toggle_blackout"],
            profile_schema_version=1,
        )

        assert caps["tools"] == ["apply_preset", "store_cue", "toggle_blackout"]

    def test_tool_count_matches_list_length(self):
        from src.capabilities import build_capabilities

        caps = build_capabilities(
            version="0.1.0",
            tool_names=["a", "b", "c"],
            profile_schema_version=1,
        )

        assert caps["tool_count"] == 3
        assert caps["tool_count"] == len(caps["tools"])

    def test_empty_tool_list_is_valid(self):
        from src.capabilities import build_capabilities

        caps = build_capabilities(
            version="0.1.0",
            tool_names=[],
            profile_schema_version=1,
        )

        assert caps["tools"] == []
        assert caps["tool_count"] == 0

    def test_shape_is_stable(self):
        from src.capabilities import build_capabilities

        caps = build_capabilities(
            version="9.9.9",
            tool_names=["x"],
            profile_schema_version=2,
        )

        assert set(caps.keys()) == {
            "version",
            "tools",
            "tool_count",
            "profile_schema_version",
        }


class TestCapabilitiesTool:
    @pytest.mark.asyncio
    async def test_reports_real_version_tools_and_schema(self):
        from src import __version__
        from src.capabilities import PROFILE_SCHEMA_VERSION
        from src.server import capabilities

        caps = await capabilities()

        assert caps["version"] == __version__
        assert caps["profile_schema_version"] == PROFILE_SCHEMA_VERSION
        # a known registered tool appears in the list
        assert "toggle_blackout" in caps["tools"]
        assert caps["tool_count"] == len(caps["tools"])

    @pytest.mark.asyncio
    async def test_does_not_require_a_console_connection(self):
        # The capabilities tool is pure metadata: it must not touch the telnet
        # client. If it called get_client(), this patched failure would raise.
        from unittest.mock import patch

        from src.server import capabilities

        with patch(
            "src.server.get_client",
            side_effect=AssertionError("capabilities must not connect"),
        ):
            caps = await capabilities()

        assert caps["tool_count"] > 0
