"""
Fixture Control Keywords for grandMA2 Command Builder

Included functions:
- align: Distribute values across selected fixtures
- all_keyword: Select all in context (named to avoid shadowing built-in)
- fix: Fix attribute values
- locate: Locate fixtures to default position
- next_keyword: Select next fixture (named to avoid shadowing built-in)
- previous: Select previous fixture
- invert: Invert selection
"""

from typing import Optional


def align(target: Optional[str] = None) -> str:
    """
    Construct an Align command to distribute values across selected fixtures.

    Args:
        target: Align mode or target (e.g., "<", ">", "><").
                If None, applies default align.

    Returns:
        str: MA command string

    Examples:
        >>> align()
        'align'
        >>> align("<")
        'align <'
    """
    if target:
        return f"align {target}"
    return "align"


def all_keyword() -> str:
    """
    Construct an All command to select all in context.

    Named ``all_keyword`` to avoid shadowing Python's built-in ``all()``.

    Returns:
        str: MA command string

    Examples:
        >>> all_keyword()
        'all'
    """
    return "all"


def fix(target: Optional[str] = None) -> str:
    """
    Construct a Fix command to fix attribute values.

    Args:
        target: Object to fix (e.g., "executor 3").
                If None, fixes current selection.

    Returns:
        str: MA command string

    Examples:
        >>> fix()
        'fix'
        >>> fix("executor 3")
        'fix executor 3'
    """
    if target:
        return f"fix {target}"
    return "fix"


def locate() -> str:
    """
    Construct a Locate command to reset fixtures to default position with open dimmer.

    Returns:
        str: MA command string

    Examples:
        >>> locate()
        'locate'
    """
    return "locate"


def next_keyword() -> str:
    """
    Construct a Next command to select the next fixture.

    Named ``next_keyword`` to avoid shadowing Python's built-in ``next()``.

    Returns:
        str: MA command string

    Examples:
        >>> next_keyword()
        'next'
    """
    return "next"


def previous() -> str:
    """
    Construct a Previous command to select the previous fixture.

    Returns:
        str: MA command string

    Examples:
        >>> previous()
        'previous'
    """
    return "previous"


def invert() -> str:
    """
    Construct an Invert command to invert the current selection.

    Returns:
        str: MA command string

    Examples:
        >>> invert()
        'invert'
    """
    return "invert"
