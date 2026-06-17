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


class TestMidiParameterized:
    def test_note_only(self):
        from src.commands.functions.midi import midi_note
        assert midi_note(60) == "midinote 60"

    def test_note_with_channel_and_velocity(self):
        from src.commands.functions.midi import midi_note
        assert midi_note(60, velocity=100, channel=2) == "midinote 2.60 100"

    def test_note_off(self):
        from src.commands.functions.midi import midi_note
        assert midi_note(60, off=True) == "midinote 60 Off"

    def test_control(self):
        from src.commands.functions.midi import midi_control
        assert midi_control(1, 64) == "midicontrol 1 64"

    def test_control_with_channel(self):
        from src.commands.functions.midi import midi_control
        assert midi_control(1, 64, channel=3) == "midicontrol 3.1 64"

    def test_program(self):
        from src.commands.functions.midi import midi_program
        assert midi_program(5) == "midiprogram 5"

    def test_program_with_channel(self):
        from src.commands.functions.midi import midi_program
        assert midi_program(5, channel=2) == "midiprogram 2.5"

    def test_bare_keywords_still_work(self):
        from src.commands.functions.midi import midi_note, midi_control, midi_program
        assert midi_note() == "midinote"
        assert midi_control() == "midicontrol"
        assert midi_program() == "midiprogram"
