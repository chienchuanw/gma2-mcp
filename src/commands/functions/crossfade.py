"""
Crossfade Keywords for grandMA2 Command Builder

Included functions:
- crossfade: Manual crossfade control
- crossfade_a: Crossfade channel A
- crossfade_b: Crossfade channel B
- manual_xfade: Manual crossfade mode
"""

from typing import Optional


def crossfade(target: Optional[str] = None) -> str:
    """
    Construct a Crossfade command for manual crossfade control.

    Args:
        target: Object to crossfade (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> crossfade()
        'crossfade'
        >>> crossfade("executor 1")
        'crossfade executor 1'
    """
    if target:
        return f"crossfade {target}"
    return "crossfade"


def crossfade_a() -> str:
    """
    Construct a CrossfadeA command for crossfade channel A.

    Returns:
        str: MA command string

    Examples:
        >>> crossfade_a()
        'crossfadea'
    """
    return "crossfadea"


def crossfade_b() -> str:
    """
    Construct a CrossfadeB command for crossfade channel B.

    Returns:
        str: MA command string

    Examples:
        >>> crossfade_b()
        'crossfadeb'
    """
    return "crossfadeb"


def manual_xfade() -> str:
    """
    Construct a ManualXFade command for manual crossfade mode.

    Returns:
        str: MA command string

    Examples:
        >>> manual_xfade()
        'manualxfade'
    """
    return "manualxfade"
