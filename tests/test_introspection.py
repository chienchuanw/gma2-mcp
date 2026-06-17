"""
Show-introspection / attribute name-resolution tests (#57 phase 3).
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.introspection import (
    parse_attribute_table,
    build_resolution_map,
    AttributeResolver,
)


# Trimmed, ANSI-laden capture of `List Attribute` from a live onPC.
LIST_ATTRIBUTE_RAW = (
    "Executing : \x1b[32mList\x1b[37m \x1b[32mAttribute\x1b[37m\n\r"
    "\x1b[32m  \x1b[31mLibraryName  \x1b[32mScreenName  \x1b[37m\n\r"
    "Attribute  6 PAN                       Pan         1: POSITION\n\r"
    "Attribute 14 COLORRGB1                 R           21: COLORRGB\n\r"
    "Attribute 15 COLORRGB2                 G           21: COLORRGB\n\r"
    "Attribute 16 COLORRGB3                 B           21: COLORRGB\n\r"
    "Attribute 17 COLORRGB5                 White       21: COLORRGB\n\r"
    " [Fixture]>\x1b[K"
)


class TestParseAttributeTable:
    def test_extracts_library_and_screen_names(self):
        rows = parse_attribute_table(LIST_ATTRIBUTE_RAW)
        names = {(r["library_name"], r["screen_name"]) for r in rows}
        assert ("COLORRGB5", "White") in names
        assert ("COLORRGB1", "R") in names
        assert ("PAN", "Pan") in names


class TestResolutionMap:
    def test_library_and_screen_names_resolve(self):
        rows = parse_attribute_table(LIST_ATTRIBUTE_RAW)
        m = build_resolution_map(rows)
        assert m["white"] == "COLORRGB5"        # screen name
        assert m["colorrgb5"] == "COLORRGB5"    # library name
        assert m["pan"] == "PAN"

    def test_common_color_aliases(self):
        rows = parse_attribute_table(LIST_ATTRIBUTE_RAW)
        m = build_resolution_map(rows)
        # "red" is an alias for screen name "R"
        assert m["red"] == "COLORRGB1"
        assert m["green"] == "COLORRGB2"
        assert m["blue"] == "COLORRGB3"


class TestAttributeResolver:
    def _client(self):
        client = MagicMock()
        client.send_command_with_response = AsyncMock(
            return_value=LIST_ATTRIBUTE_RAW
        )
        return client

    @pytest.mark.asyncio
    async def test_resolves_friendly_name(self):
        resolver = AttributeResolver(self._client())
        assert await resolver.resolve("White") == "COLORRGB5"

    @pytest.mark.asyncio
    async def test_caches_after_first_fetch(self):
        client = self._client()
        resolver = AttributeResolver(client)
        await resolver.resolve("White")
        await resolver.resolve("Pan")
        assert client.send_command_with_response.await_count == 1

    @pytest.mark.asyncio
    async def test_unknown_returns_none_with_suggestions(self):
        resolver = AttributeResolver(self._client())
        assert await resolver.resolve("Reed") is None
        suggestions = await resolver.suggest("Reed")
        assert any("R" == s or "COLORRGB1" == s for s in suggestions)


class TestSetFixtureAttributeResolution:
    """set_fixture_attribute resolves friendly names and rejects unknowns (#57 p3)."""

    def _client_with_table(self):
        from src.execution import ExecutionResult

        client = MagicMock()
        client.send_command_with_response = AsyncMock(return_value=LIST_ATTRIBUTE_RAW)
        client.execute = AsyncMock(
            return_value=ExecutionResult(
                ok=True, echo="OK", error_code=None, error_text=None, raw="OK"
            )
        )
        return client

    @pytest.mark.asyncio
    async def test_white_resolves_to_token(self, monkeypatch):
        import src.server as server

        # reset the per-connection resolver cache for isolation
        server._resolver_cache["client"] = None
        client = self._client_with_table()
        monkeypatch.setattr(server, "get_client", AsyncMock(return_value=client))

        await server.set_fixture_attribute(1, "White", 0)

        calls = [c[0][0] for c in client.execute.call_args_list]
        assert 'attribute "COLORRGB5" at 0' in calls

    @pytest.mark.asyncio
    async def test_unknown_attribute_rejected_with_suggestions(self, monkeypatch):
        import src.server as server

        server._resolver_cache["client"] = None
        client = self._client_with_table()
        monkeypatch.setattr(server, "get_client", AsyncMock(return_value=client))

        result = await server.set_fixture_attribute(1, "Reed", 0)

        assert "Unknown attribute 'Reed'" in result
        client.execute.assert_not_called()
