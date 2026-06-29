"""
MIDI output keywords for grandMA2 Command Builder.

Verified against the grandMA2 manual command-line syntax:
- MidiNote [channel.]note [velocity] | MidiNote note Off
- MidiControl [channel.]controller value
- MidiProgram [channel.]program

If no MIDI channel is given, the channel configured in Setup -> MIDI Show
Control is used. Calling a builder with no arguments returns the bare keyword.
"""

from __future__ import annotations


def _addressed(channel: int | None, number: int) -> str:
    """Render an optional ``channel.number`` address (or just ``number``)."""
    if channel is not None:
        return f"{channel}.{number}"
    return str(number)


def midi_note(
    note: int | None = None,
    *,
    velocity: int | None = None,
    channel: int | None = None,
    off: bool = False,
) -> str:
    """Send a MIDI note message via the MIDI Out port.

    Args:
        note: MIDI note number (0-127). If None, returns the bare keyword.
        velocity: Note velocity (0-127). Defaults to full (127) on the console
                  when omitted.
        channel: MIDI channel (uses the Setup default when omitted).
        off: If True, send a note-off (``MidiNote note Off``).

    Examples:
        >>> midi_note(60)
        'midinote 60'
        >>> midi_note(60, velocity=100, channel=2)
        'midinote 2.60 100'
        >>> midi_note(60, off=True)
        'midinote 60 Off'
    """
    if note is None:
        return "midinote"
    cmd = f"midinote {_addressed(channel, note)}"
    if off:
        return f"{cmd} Off"
    if velocity is not None:
        return f"{cmd} {velocity}"
    return cmd


def midi_control(
    controller: int | None = None,
    value: int | None = None,
    *,
    channel: int | None = None,
) -> str:
    """Send a MIDI control-change message via the MIDI Out port.

    Args:
        controller: Controller number. If None, returns the bare keyword.
        value: Control value (0-127).
        channel: MIDI channel (uses the Setup default when omitted).

    Examples:
        >>> midi_control(1, 64)
        'midicontrol 1 64'
        >>> midi_control(1, 64, channel=3)
        'midicontrol 3.1 64'
    """
    if controller is None:
        return "midicontrol"
    return f"midicontrol {_addressed(channel, controller)} {value}"


def midi_program(
    program: int | None = None,
    *,
    channel: int | None = None,
) -> str:
    """Send a MIDI program-change message via the MIDI Out port.

    Args:
        program: Program number. If None, returns the bare keyword.
        channel: MIDI channel (uses the Setup default when omitted).

    Examples:
        >>> midi_program(5)
        'midiprogram 5'
        >>> midi_program(5, channel=2)
        'midiprogram 2.5'
    """
    if program is None:
        return "midiprogram"
    return f"midiprogram {_addressed(channel, program)}"
