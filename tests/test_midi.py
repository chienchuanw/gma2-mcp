"""Tests for grandMA2 MIDI keywords."""

import pytest


class TestMidi:
    def test_midi_control(self):
        from src.commands import midi_control

        assert midi_control() == "midicontrol"

    def test_midi_note(self):
        from src.commands import midi_note

        assert midi_note() == "midinote"

    def test_midi_program(self):
        from src.commands import midi_program

        assert midi_program() == "midiprogram"
