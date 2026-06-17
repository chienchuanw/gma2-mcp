"""
Show Introspection for grandMA2 (#57 phase 3).

grandMA2 attribute tokens are show-specific: which attributes exist (and their
names) depends on the patched fixture types. For example, on one show White is
``COLORRGB5`` (not ``COLORRGB4``), and there is no ``Red`` attribute — the red
channel's screen name is ``R``.

This module queries ``List Attribute`` once, caches it, and resolves a friendly
name (``"White"``, ``"Red"``, ``"Pan"``) to the canonical console token so tools
can validate/normalize an attribute before sending it — turning a silent failure
into either a correct command or a helpful, suggestion-bearing error.
"""

from __future__ import annotations

import difflib
from typing import Optional

from src.response_parser import strip_ansi


# Common longhand color names -> the single-letter screen names grandMA2 uses.
_COLOR_ALIASES = {
    "red": "r",
    "green": "g",
    "blue": "b",
    "white": "white",
    "amber": "amber",
    "cyan": "c",
    "magenta": "m",
    "yellow": "y",
}


def parse_attribute_table(raw: str) -> list[dict]:
    """Parse ``List Attribute`` output into [{library_name, screen_name}, ...].

    Each data row looks like ``Attribute  17 COLORRGB5  White  21: COLORRGB...``;
    the library name and screen name are the two tokens after the row number.
    """
    rows: list[dict] = []
    for line in strip_ansi(raw).split("\n"):
        tokens = line.strip().split()
        if len(tokens) >= 4 and tokens[0] == "Attribute" and tokens[1].isdigit():
            rows.append({"library_name": tokens[2], "screen_name": tokens[3]})
    return rows


def build_resolution_map(rows: list[dict]) -> dict[str, str]:
    """Build a lowercased name -> canonical library-name map from parsed rows.

    Both the library name and the screen name resolve to the library name, plus
    common color longhand aliases (red -> R -> COLORRGB1, etc.).
    """
    mapping: dict[str, str] = {}
    for row in rows:
        lib = row["library_name"]
        mapping[lib.lower()] = lib
        mapping[row["screen_name"].lower()] = lib

    for alias, screen in _COLOR_ALIASES.items():
        if screen in mapping and alias not in mapping:
            mapping[alias] = mapping[screen]

    return mapping


class AttributeResolver:
    """Resolve friendly attribute names to console tokens, with caching."""

    def __init__(self, client) -> None:
        self._client = client
        self._map: Optional[dict[str, str]] = None

    async def _ensure(self) -> dict[str, str]:
        if self._map is None:
            raw = await self._client.send_command_with_response("List Attribute")
            self._map = build_resolution_map(parse_attribute_table(raw))
        return self._map

    def invalidate(self) -> None:
        """Drop the cache (call after a patch change)."""
        self._map = None

    async def known(self) -> bool:
        """True if the attribute table was fetched and is non-empty."""
        return len(await self._ensure()) > 0

    async def resolve(self, name: str) -> Optional[str]:
        """Return the canonical attribute token for ``name``, or None if unknown."""
        mapping = await self._ensure()
        return mapping.get(name.strip().lower())

    async def suggest(self, name: str, limit: int = 5) -> list[str]:
        """Return up to ``limit`` canonical tokens close to ``name``."""
        mapping = await self._ensure()
        close = difflib.get_close_matches(
            name.strip().lower(), list(mapping.keys()), n=limit, cutoff=0.5
        )
        seen: list[str] = []
        for key in close:
            token = mapping[key]
            if token not in seen:
                seen.append(token)
        return seen
