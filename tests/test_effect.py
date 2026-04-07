"""
Effect Keywords Tests

Tests for grandMA2 Effect, EffectAttack, EffectBPM, EffectDecay, EffectDelay,
EffectFade, EffectForm, EffectHigh, EffectHZ, EffectID, EffectLow, EffectPhase,
EffectSec, EffectSpeedGroup, EffectWidth, and SyncEffects function keyword
command generation.
"""

import pytest


class TestEffect:
    """Tests for Effect keyword."""

    def test_effect_with_id(self):
        from src.commands import effect

        assert effect(5) == "effect 5"


class TestEffectAttack:
    """Tests for EffectAttack keyword."""

    def test_effect_attack_value(self):
        from src.commands import effect_attack

        assert effect_attack(50) == "effectattack 50"


class TestEffectBPM:
    """Tests for EffectBPM keyword."""

    def test_effect_bpm_value(self):
        from src.commands import effect_bpm

        assert effect_bpm(120) == "effectbpm 120"


class TestEffectDecay:
    """Tests for EffectDecay keyword."""

    def test_effect_decay_value(self):
        from src.commands import effect_decay

        assert effect_decay(50) == "effectdecay 50"


class TestEffectDelay:
    """Tests for EffectDelay keyword."""

    def test_effect_delay_value(self):
        from src.commands import effect_delay

        assert effect_delay(30) == "effectdelay 30"


class TestEffectFade:
    """Tests for EffectFade keyword."""

    def test_effect_fade_value(self):
        from src.commands import effect_fade

        assert effect_fade(50) == "effectfade 50"


class TestEffectForm:
    """Tests for EffectForm keyword."""

    def test_effect_form_numeric(self):
        from src.commands import effect_form

        assert effect_form(2) == "effectform 2"

    def test_effect_form_string(self):
        from src.commands import effect_form

        assert effect_form("sin") == "effectform sin"


class TestEffectHigh:
    """Tests for EffectHigh keyword."""

    def test_effect_high_value(self):
        from src.commands import effect_high

        assert effect_high(100) == "effecthigh 100"


class TestEffectHZ:
    """Tests for EffectHZ keyword."""

    def test_effect_hz_value(self):
        from src.commands import effect_hz

        assert effect_hz(1.5) == "effecthz 1.5"


class TestEffectID:
    """Tests for EffectID keyword."""

    def test_effect_id_value(self):
        from src.commands import effect_id

        assert effect_id(3) == "effectid 3"


class TestEffectLow:
    """Tests for EffectLow keyword."""

    def test_effect_low_value(self):
        from src.commands import effect_low

        assert effect_low(0) == "effectlow 0"


class TestEffectPhase:
    """Tests for EffectPhase keyword."""

    def test_effect_phase_value(self):
        from src.commands import effect_phase

        assert effect_phase(90) == "effectphase 90"


class TestEffectSec:
    """Tests for EffectSec keyword."""

    def test_effect_sec_value(self):
        from src.commands import effect_sec

        assert effect_sec(2) == "effectsec 2"


class TestEffectSpeedGroup:
    """Tests for EffectSpeedGroup keyword."""

    def test_effect_speed_group_value(self):
        from src.commands import effect_speed_group

        assert effect_speed_group(1) == "effectspeedgroup 1"


class TestEffectWidth:
    """Tests for EffectWidth keyword."""

    def test_effect_width_value(self):
        from src.commands import effect_width

        assert effect_width(100) == "effectwidth 100"


class TestSyncEffects:
    """Tests for SyncEffects keyword."""

    def test_sync_effects(self):
        from src.commands import sync_effects

        assert sync_effects() == "synceffects"
