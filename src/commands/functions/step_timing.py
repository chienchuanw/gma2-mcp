"""
Step Timing Keywords for grandMA2 Command Builder

Included functions:
- snap_percent: Set snap percentage
- step_fade: Set step fade time
- step_in_fade: Set step in-fade time
- step_out_fade: Set step out-fade time
- fade_path: Set fade path
"""

from typing import Union


def snap_percent(value: Union[int, float]) -> str:
    """
    Construct a SnapPercent command to set snap percentage.

    Args:
        value: Snap percentage value

    Returns:
        str: MA command string

    Examples:
        >>> snap_percent(50)
        'snappercent 50'
    """
    return f"snappercent {value}"


def step_fade(value: Union[int, float]) -> str:
    """
    Construct a StepFade command to set step fade time.

    Args:
        value: Step fade time in seconds

    Returns:
        str: MA command string

    Examples:
        >>> step_fade(2)
        'stepfade 2'
    """
    return f"stepfade {value}"


def step_in_fade(value: Union[int, float]) -> str:
    """
    Construct a StepInFade command to set step in-fade time.

    Args:
        value: Step in-fade time in seconds

    Returns:
        str: MA command string

    Examples:
        >>> step_in_fade(3)
        'stepinfade 3'
    """
    return f"stepinfade {value}"


def step_out_fade(value: Union[int, float]) -> str:
    """
    Construct a StepOutFade command to set step out-fade time.

    Args:
        value: Step out-fade time in seconds

    Returns:
        str: MA command string

    Examples:
        >>> step_out_fade(1)
        'stepoutfade 1'
    """
    return f"stepoutfade {value}"


def fade_path(value: Union[int, float]) -> str:
    """
    Construct a FadePath command to set fade path.

    Args:
        value: Fade path number

    Returns:
        str: MA command string

    Examples:
        >>> fade_path(2)
        'fadepath 2'
    """
    return f"fadepath {value}"
