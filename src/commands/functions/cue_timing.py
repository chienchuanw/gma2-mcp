"""
Cue Timing Keywords for grandMA2 Command Builder

Included functions:
- delay: Set delay time
- out_delay: Set output delay time
- fade: Set fade time
- out_fade: Set output fade time
"""

from typing import Optional, Union


def delay(value: Union[int, float], *, target: Optional[str] = None) -> str:
    """
    Construct a Delay command to set delay time.

    Args:
        value: Delay time in seconds
        target: Object to apply delay to (e.g., "cue 5").

    Returns:
        str: MA command string

    Examples:
        >>> delay(3)
        'delay 3'
        >>> delay(2, target="cue 5")
        'delay 2 cue 5'
    """
    parts = ["delay", str(value)]
    if target:
        parts.append(target)
    return " ".join(parts)


def out_delay(value: Union[int, float]) -> str:
    """
    Construct an OutDelay command to set output delay time.

    Args:
        value: Output delay time in seconds

    Returns:
        str: MA command string

    Examples:
        >>> out_delay(3)
        'outdelay 3'
    """
    return f"outdelay {value}"


def fade(value: Union[int, float], *, target: Optional[str] = None) -> str:
    """
    Construct a Fade command to set fade time.

    Args:
        value: Fade time in seconds
        target: Object to apply fade to (e.g., "cue 5").

    Returns:
        str: MA command string

    Examples:
        >>> fade(2)
        'fade 2'
        >>> fade(3, target="cue 5")
        'fade 3 cue 5'
    """
    parts = ["fade", str(value)]
    if target:
        parts.append(target)
    return " ".join(parts)


def out_fade(value: Union[int, float]) -> str:
    """
    Construct an OutFade command to set output fade time.

    Args:
        value: Output fade time in seconds

    Returns:
        str: MA command string

    Examples:
        >>> out_fade(3)
        'outfade 3'
    """
    return f"outfade {value}"
