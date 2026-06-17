"""
Fixture-profile resolver tests (#74).

Parses MA2 fixture-type XML and resolves named channel functions
(open/closed/strobe/random/iris/frost/prism) to per-type attribute values.
"""

import pytest

from src.profile_resolver import parse_fixture_profile, FixtureProfile

# Trimmed but real-structured MA2 fixture-type XML (based on the rig's profiles):
# a SHUTTER channel with closed/strobe/open/random functions, plus IRIS and FROST.
SAMPLE_XML = """<?xml version="1.0" encoding="utf-8"?>
<MA xmlns="http://schemas.malighting.de/grandma2/xml/MA">
  <FixtureType index="1" name="Test Mover" mode="34channel">
    <Modules index="0">
      <Module index="0">
        <ChannelType index="0" attribute="SHUTTER" feature="SHUTTER" preset="BEAM" coarse="1">
          <ChannelFunction index="0" from="0" to="1.562" subattribute="SHUTTER" attribute="SHUTTER">
            <ChannelSet index="0" name="closed" from_dmx="0" to_dmx="3" />
          </ChannelFunction>
          <ChannelFunction index="1" name="Strobe 1..100%" from="1.562" to="40.625" subattribute="STROBE" attribute="SHUTTER">
            <ChannelSet index="0" name="min Strobe" from_dmx="4" to_dmx="4" />
            <ChannelSet index="1" name="max Strobe" from_dmx="103" to_dmx="103" />
          </ChannelFunction>
          <ChannelFunction index="2" from="40.625" to="42.188" subattribute="SHUTTER" attribute="SHUTTER">
            <ChannelSet index="0" name="open" from_dmx="104" to_dmx="107" />
          </ChannelFunction>
          <ChannelFunction index="3" name="Rnd" from="83.203" to="98.438" subattribute="STROBE_RANDOM" attribute="SHUTTER">
            <ChannelSet index="0" name="min Rnd" from_dmx="213" to_dmx="225" />
            <ChannelSet index="1" name="max Rnd" from_dmx="239" to_dmx="251" />
          </ChannelFunction>
        </ChannelType>
        <ChannelType index="1" attribute="IRIS" feature="BEAM1" preset="BEAM" coarse="2">
          <ChannelFunction index="0" name="Iris" from="0" to="100" subattribute="IRIS" attribute="IRIS" />
        </ChannelType>
        <ChannelType index="2" attribute="FROST" feature="BEAM1" preset="BEAM" coarse="3">
          <ChannelFunction index="0" name="Frost" from="0" to="100" subattribute="FROST" attribute="FROST" />
        </ChannelType>
      </Module>
    </Modules>
  </FixtureType>
</MA>"""


class TestParse:
    def test_returns_profile_with_attributes(self):
        p = parse_fixture_profile(SAMPLE_XML)
        assert isinstance(p, FixtureProfile)
        assert p.name == "Test Mover"
        assert "SHUTTER" in p.functions
        assert "IRIS" in p.functions
        assert "FROST" in p.functions

    def test_shutter_has_four_functions(self):
        p = parse_fixture_profile(SAMPLE_XML)
        assert len(p.functions["SHUTTER"]) == 4


class TestResolveNamedSlots:
    def setup_method(self):
        self.p = parse_fixture_profile(SAMPLE_XML)

    def test_closed(self):
        attr, at = self.p.resolve("closed")
        assert attr == "SHUTTER"
        assert at < 2  # dmx 0-3 -> ~0.6%

    def test_open(self):
        attr, at = self.p.resolve("open")
        assert attr == "SHUTTER"
        assert 40 <= at <= 42  # dmx 104-107 -> ~41%

    def test_random(self):
        attr, at = self.p.resolve("random")
        assert attr == "SHUTTER"
        assert 83 <= at <= 99

    def test_unknown_returns_none(self):
        assert self.p.resolve("gobo") is None


class TestResolveStrobeBand:
    def setup_method(self):
        self.p = parse_fixture_profile(SAMPLE_XML)

    def test_strobe_slow_is_low_end(self):
        attr, at = self.p.resolve("strobe", position=0.0)
        assert attr == "SHUTTER"
        assert abs(at - 1.562) < 0.01

    def test_strobe_fast_is_high_end(self):
        _, at = self.p.resolve("strobe", position=1.0)
        assert abs(at - 40.625) < 0.01

    def test_strobe_mid(self):
        _, at = self.p.resolve("strobe", position=0.5)
        assert 20 < at < 22


class TestResolveSingleFunction:
    def setup_method(self):
        self.p = parse_fixture_profile(SAMPLE_XML)

    def test_iris_defaults_to_midpoint(self):
        attr, at = self.p.resolve("iris", position=0.5)
        assert attr == "IRIS"
        assert at == 50

    def test_frost_low(self):
        _, at = self.p.resolve("frost", position=0.0)
        assert at == 0


SIMPLE_XML = """<?xml version="1.0"?>
<MA xmlns="http://schemas.malighting.de/grandma2/xml/MA">
  <FixtureType index="2" name="Simple Par" mode="8 channel">
    <Modules index="0"><Module index="0">
      <ChannelType index="0" attribute="SHUTTER" feature="SHUTTER" preset="BEAM" coarse="6">
        <ChannelFunction index="0" from="0" to="3.125" subattribute="SHUTTER" attribute="SHUTTER">
          <ChannelSet index="0" name="open" from_dmx="0" to_dmx="7" />
        </ChannelFunction>
        <ChannelFunction index="1" name="Strobe 1..100%" from="3.125" to="96.875" subattribute="STROBE" attribute="SHUTTER" />
      </ChannelType>
    </Module></Modules>
  </FixtureType>
</MA>"""


class TestPerTypeValues:
    def test_resolves_across_profiles_and_omits_unsupported(self):
        from src.profile_resolver import per_type_values

        profiles = {
            "mover": parse_fixture_profile(SAMPLE_XML),
            "par": parse_fixture_profile(SIMPLE_XML),
        }
        # Both have strobe; values differ per profile band.
        strobe_fast = per_type_values(profiles, "strobe", position=1.0)
        assert set(strobe_fast) == {"mover", "par"}
        assert strobe_fast["mover"][0] == "SHUTTER"
        assert abs(strobe_fast["par"][1] - 96.875) < 0.01

        # Only the mover has iris; the par is omitted.
        iris = per_type_values(profiles, "iris")
        assert "mover" in iris and "par" not in iris
