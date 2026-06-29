"""
Intensity and Misc Keywords for grandMA2 Command Builder

Included functions:
- full: Set to full intensity
- to_full: Fade executor to full
- zero: Set to zero
- to_zero: Fade executor to zero
- load: Load cue into executor
- learn: Learn speed from taps
"""


def full() -> str:
    """
    Construct a Full command to set to full intensity.

    Returns:
        str: MA command string

    Examples:
        >>> full()
        'full'
    """
    return "full"


def to_full(target: str) -> str:
    """
    Construct a ToFull command to fade executor to full.

    Args:
        target: Object to fade to full (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> to_full("executor 1")
        'tofull executor 1'
    """
    return f"tofull {target}"


def zero() -> str:
    """
    Construct a Zero command to set to zero.

    Returns:
        str: MA command string

    Examples:
        >>> zero()
        'zero'
    """
    return "zero"


def to_zero(target: str) -> str:
    """
    Construct a ToZero command to fade executor to zero.

    Args:
        target: Object to fade to zero (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> to_zero("executor 1")
        'tozero executor 1'
    """
    return f"tozero {target}"


def load(target: str) -> str:
    """
    Construct a Load command to load a cue into an executor.

    Args:
        target: Load expression (e.g., "cue 5 executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> load("cue 5 executor 1")
        'load cue 5 executor 1'
    """
    return f"load {target}"


def learn() -> str:
    """
    Construct a Learn command to learn speed from taps.

    Returns:
        str: MA command string

    Examples:
        >>> learn()
        'learn'
    """
    return "learn"
