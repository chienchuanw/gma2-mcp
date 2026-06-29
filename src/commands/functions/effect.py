"""
Effect Keywords for grandMA2 Command Builder

Included functions:
- effect: Reference/select effect
- effect_attack: Set effect attack
- effect_bpm: Set effect BPM
- effect_decay: Set effect decay
- effect_delay: Set effect delay
- effect_fade: Set effect fade
- effect_form: Set effect form/waveform
- effect_high: Set effect high value
- effect_hz: Set effect frequency in Hz
- effect_id: Set effect ID
- effect_low: Set effect low value
- effect_phase: Set effect phase
- effect_sec: Set effect speed in seconds
- effect_speed_group: Assign effect to speed group
- effect_width: Set effect width
- sync_effects: Synchronize effects
"""


def effect(effect_id: int) -> str:
    """
    Construct an Effect command to reference/select an effect.

    Args:
        effect_id: Effect number

    Returns:
        str: MA command string

    Examples:
        >>> effect(5)
        'effect 5'
    """
    return f"effect {effect_id}"


def effect_attack(value: int | float) -> str:
    """
    Construct an EffectAttack command.

    Args:
        value: Attack value (percentage)

    Returns:
        str: MA command string

    Examples:
        >>> effect_attack(50)
        'effectattack 50'
    """
    return f"effectattack {value}"


def effect_bpm(value: int | float) -> str:
    """
    Construct an EffectBPM command.

    Args:
        value: BPM value

    Returns:
        str: MA command string

    Examples:
        >>> effect_bpm(120)
        'effectbpm 120'
    """
    return f"effectbpm {value}"


def effect_decay(value: int | float) -> str:
    """
    Construct an EffectDecay command.

    Args:
        value: Decay value (percentage)

    Returns:
        str: MA command string

    Examples:
        >>> effect_decay(50)
        'effectdecay 50'
    """
    return f"effectdecay {value}"


def effect_delay(value: int | float) -> str:
    """
    Construct an EffectDelay command.

    Args:
        value: Delay value

    Returns:
        str: MA command string

    Examples:
        >>> effect_delay(30)
        'effectdelay 30'
    """
    return f"effectdelay {value}"


def effect_fade(value: int | float) -> str:
    """
    Construct an EffectFade command.

    Args:
        value: Fade value (percentage)

    Returns:
        str: MA command string

    Examples:
        >>> effect_fade(50)
        'effectfade 50'
    """
    return f"effectfade {value}"


def effect_form(value: int | str) -> str:
    """
    Construct an EffectForm command to set waveform.

    Args:
        value: Form ID (int) or form name (str, e.g., "sin")

    Returns:
        str: MA command string

    Examples:
        >>> effect_form(2)
        'effectform 2'
        >>> effect_form("sin")
        'effectform sin'
    """
    return f"effectform {value}"


def effect_high(value: int | float) -> str:
    """
    Construct an EffectHigh command.

    Args:
        value: High value

    Returns:
        str: MA command string

    Examples:
        >>> effect_high(100)
        'effecthigh 100'
    """
    return f"effecthigh {value}"


def effect_hz(value: int | float) -> str:
    """
    Construct an EffectHZ command to set frequency.

    Args:
        value: Frequency in Hz

    Returns:
        str: MA command string

    Examples:
        >>> effect_hz(1.5)
        'effecthz 1.5'
    """
    return f"effecthz {value}"


def effect_id(value: int) -> str:
    """
    Construct an EffectID command.

    Args:
        value: Effect ID number

    Returns:
        str: MA command string

    Examples:
        >>> effect_id(3)
        'effectid 3'
    """
    return f"effectid {value}"


def effect_low(value: int | float) -> str:
    """
    Construct an EffectLow command.

    Args:
        value: Low value

    Returns:
        str: MA command string

    Examples:
        >>> effect_low(0)
        'effectlow 0'
    """
    return f"effectlow {value}"


def effect_phase(value: int | float) -> str:
    """
    Construct an EffectPhase command.

    Args:
        value: Phase value in degrees

    Returns:
        str: MA command string

    Examples:
        >>> effect_phase(90)
        'effectphase 90'
    """
    return f"effectphase {value}"


def effect_sec(value: int | float) -> str:
    """
    Construct an EffectSec command to set speed in seconds.

    Args:
        value: Speed in seconds

    Returns:
        str: MA command string

    Examples:
        >>> effect_sec(2)
        'effectsec 2'
    """
    return f"effectsec {value}"


def effect_speed_group(value: int) -> str:
    """
    Construct an EffectSpeedGroup command.

    Args:
        value: Speed group number

    Returns:
        str: MA command string

    Examples:
        >>> effect_speed_group(1)
        'effectspeedgroup 1'
    """
    return f"effectspeedgroup {value}"


def effect_width(value: int | float) -> str:
    """
    Construct an EffectWidth command.

    Args:
        value: Width value (percentage)

    Returns:
        str: MA command string

    Examples:
        >>> effect_width(100)
        'effectwidth 100'
    """
    return f"effectwidth {value}"


def sync_effects() -> str:
    """
    Construct a SyncEffects command to synchronize all running effects.

    Returns:
        str: MA command string

    Examples:
        >>> sync_effects()
        'synceffects'
    """
    return "synceffects"
