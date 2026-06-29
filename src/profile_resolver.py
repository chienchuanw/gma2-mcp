"""
Fixture-Profile Resolver (#74)

grandMA2's Telnet interface cannot read a fixture profile's channel-function
ranges, so values like "Strobe Fast" / "Iris Open" / "Prism Rotate Slow" are
fixture-specific. That information IS in the MA2 fixture-type XML (or GDTF):
every channel's functions, percent ranges, and named DMX channel-sets.

This module parses that XML and resolves a named function ("open", "closed",
"strobe", "random", "iris", "frost", "prism") to the attribute and the ``At``
percentage to send for that fixture type — so a preset can be programmed with
the correct per-type value (and merged into one Global preset across types).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field


def _local(tag: str) -> str:
    """Strip the XML namespace from a tag name."""
    return tag.rsplit("}", 1)[-1]


def _children(elem, local: str):
    return [e for e in list(elem) if _local(e.tag) == local]


def _descendants(elem, local: str):
    return [e for e in elem.iter() if _local(e.tag) == local]


@dataclass
class ChannelSet:
    name: str
    from_dmx: int
    to_dmx: int

    @property
    def mid_percent(self) -> float:
        return (self.from_dmx + self.to_dmx) / 2 / 255 * 100


@dataclass
class ChannelFunction:
    name: str
    subattribute: str
    from_pct: float
    to_pct: float
    sets: list[ChannelSet] = field(default_factory=list)

    def at(self, position: float) -> float:
        """Percent value at ``position`` (0..1) within this function's range."""
        return self.from_pct + position * (self.to_pct - self.from_pct)


# Query -> the names/sub-strings that satisfy it (case-insensitive substring).
_ALIASES = {
    "closed": ["closed", "close"],
    "open": ["open"],
    "random": ["random", "rnd"],
    "strobe": ["strobe"],
    "prism": ["prism", "prisma"],
}
# Queries that resolve to a position WITHIN a function's range (not a fixed slot).
_BAND_QUERIES = {"strobe"}
# Shutter-slot queries are scoped to the SHUTTER feature so they don't match the
# "open"/"closed" slots that color wheels and white channels also define.
_SHUTTER_SCOPED = {"open", "closed", "strobe", "random"}


@dataclass
class FixtureProfile:
    name: str
    mode: str
    functions: dict[str, list[ChannelFunction]]
    features: dict[str, str] = field(default_factory=dict)

    def _attrs(self, feature: str | None):
        """Iterate (attribute, functions), optionally restricted to a feature."""
        for attr, funcs in self.functions.items():
            if feature is None or self.features.get(attr, "").upper() == feature:
                yield attr, funcs

    def resolve(
        self,
        query: str,
        position: float = 0.5,
        feature: str | None = None,
    ) -> tuple[str, float] | None:
        """Resolve a named function to ``(attribute, at_percent)``.

        Args:
            query: e.g. "open", "closed", "strobe", "random", "iris", "frost".
            position: 0..1 within a band query (strobe slow=0, fast=1) or within
                a single-function attribute (iris/frost amount).
            feature: restrict the search to this MA feature (e.g. "SHUTTER").
                open/closed/strobe/random default to "SHUTTER" automatically.

        Returns ``(attribute, at_percent)`` or None if not found.
        """
        q = query.strip().lower()
        needles = _ALIASES.get(q, [q])
        if feature is None and q in _SHUTTER_SCOPED:
            feature = "SHUTTER"

        # 1. Band query (strobe): position within the matching function's range,
        #    excluding random/pulse variants.
        if q in _BAND_QUERIES:
            for attr, funcs in self._attrs(feature):
                for f in funcs:
                    hay = f"{f.name} {f.subattribute}".lower()
                    if any(n in hay for n in needles) and not _is_random(hay):
                        return attr, round(f.at(position), 3)
            return None

        # 2. Named slot: a ChannelSet whose name matches (precise DMX midpoint).
        for attr, funcs in self._attrs(feature):
            for f in funcs:
                for cs in f.sets:
                    if any(n in cs.name.lower() for n in needles):
                        return attr, round(cs.mid_percent, 3)

        # 3. Fall back: attribute or function name match -> positioned in range.
        for attr, funcs in self._attrs(feature):
            if any(n in attr.lower() for n in needles) and funcs:
                return attr, round(funcs[0].at(position), 3)
            for f in funcs:
                hay = f"{f.name} {f.subattribute}".lower()
                if any(n in hay for n in needles):
                    return attr, round(f.at(position), 3)
        return None


def _is_random(hay: str) -> bool:
    return "random" in hay or "rnd" in hay


def _to_int(value: str | None) -> int:
    return int(round(float(value))) if value is not None else 0


def parse_fixture_profile(xml: str) -> FixtureProfile:
    """Parse an MA2 fixture-type XML (string or file path) into a FixtureProfile."""
    if "<" not in xml:  # treat as a file path
        with open(xml, encoding="utf-8") as fh:
            xml = fh.read()
    root = ET.fromstring(xml)

    ftype = next(iter(_descendants(root, "FixtureType")), None)
    if ftype is None:
        raise ValueError("No <FixtureType> element found")

    functions: dict[str, list[ChannelFunction]] = {}
    features: dict[str, str] = {}
    for ct in _descendants(ftype, "ChannelType"):
        attr = ct.get("attribute")
        if not attr:
            continue
        if ct.get("feature"):
            features.setdefault(attr, ct.get("feature"))
        for cf in _children(ct, "ChannelFunction"):
            if cf.get("from") is None or cf.get("to") is None:
                continue
            sets = [
                ChannelSet(
                    name=cs.get("name") or "",
                    from_dmx=_to_int(cs.get("from_dmx")),
                    to_dmx=_to_int(cs.get("to_dmx")),
                )
                for cs in _children(cf, "ChannelSet")
            ]
            functions.setdefault(attr, []).append(
                ChannelFunction(
                    name=cf.get("name") or "",
                    subattribute=cf.get("subattribute") or "",
                    from_pct=float(cf.get("from")),
                    to_pct=float(cf.get("to")),
                    sets=sets,
                )
            )

    return FixtureProfile(
        name=ftype.get("name") or "",
        mode=ftype.get("mode") or "",
        functions=functions,
        features=features,
    )


def per_type_values(
    profiles: dict[str, FixtureProfile],
    query: str,
    position: float = 0.5,
) -> dict[str, tuple[str, float]]:
    """Resolve ``query`` across multiple profiles.

    Returns ``{profile_key: (attribute, at_percent)}`` for every profile that
    supports the function (others are omitted) — exactly the per-type values
    needed to merge one logical preset across fixture types.
    """
    out: dict[str, tuple[str, float]] = {}
    for key, profile in profiles.items():
        resolved = profile.resolve(query, position=position)
        if resolved is not None:
            out[key] = resolved
    return out
