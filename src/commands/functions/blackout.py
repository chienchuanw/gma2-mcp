"""
Blackout and Global State Keywords for grandMA2 Command Builder

Included functions:
- blackout: Toggle grand blackout
- black: Set output to black
- freeze: Toggle freeze mode
- highlight: Toggle highlight mode
- full_highlight: Toggle full highlight mode
- solo: Toggle solo mode
"""


def blackout() -> str:
    """
    Construct a Blackout command to toggle grand blackout.

    Returns:
        str: MA command string

    Examples:
        >>> blackout()
        'blackout'
    """
    return "blackout"


def black(target: str | None = None) -> str:
    """
    Construct a Black command to set output to black.

    Args:
        target: Object to set to black (e.g., "executor 1").
                If None, applies to current selection.

    Returns:
        str: MA command string

    Examples:
        >>> black()
        'black'
        >>> black("executor 1")
        'black executor 1'
    """
    if target:
        return f"black {target}"
    return "black"


def freeze(target: str | None = None) -> str:
    """
    Construct a Freeze command to toggle freeze mode.

    Args:
        target: Object to freeze (e.g., "executor 1").
                If None, toggles global freeze.

    Returns:
        str: MA command string

    Examples:
        >>> freeze()
        'freeze'
        >>> freeze("executor 1")
        'freeze executor 1'
    """
    if target:
        return f"freeze {target}"
    return "freeze"


def highlight() -> str:
    """
    Construct a Highlight command to toggle highlight mode.

    Returns:
        str: MA command string

    Examples:
        >>> highlight()
        'highlight'
    """
    return "highlight"


def full_highlight() -> str:
    """
    Construct a FullHighlight command to toggle full highlight mode.

    Returns:
        str: MA command string

    Examples:
        >>> full_highlight()
        'fullhighlight'
    """
    return "fullhighlight"


def solo() -> str:
    """
    Construct a Solo command to toggle solo mode.

    Returns:
        str: MA command string

    Examples:
        >>> solo()
        'solo'
    """
    return "solo"
