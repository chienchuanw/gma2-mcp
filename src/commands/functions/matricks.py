"""
MAtricks Keywords for grandMA2 Command Builder

Included functions:
- matricks: Open/reference MAtricks
- matricks_blocks: Set MAtricks blocks value
- matricks_filter: Set MAtricks filter
- matricks_groups: Set MAtricks groups value
- matricks_interleave: Set MAtricks interleave value
- matricks_reset: Reset MAtricks settings
- matricks_wings: Set MAtricks wings value
"""


def matricks(target: str | None = None) -> str:
    """
    Construct a MAtricks command.

    Args:
        target: Object to apply MAtricks to (e.g., "fixture 1 thru 10").

    Returns:
        str: MA command string

    Examples:
        >>> matricks()
        'matricks'
        >>> matricks("fixture 1 thru 10")
        'matricks fixture 1 thru 10'
    """
    if target:
        return f"matricks {target}"
    return "matricks"


def matricks_blocks(value: int | float | None = None) -> str:
    """
    Construct a MAtricksBlocks command to set blocks value.

    Args:
        value: Number of blocks.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_blocks(4)
        'matricksblocks 4'
        >>> matricks_blocks()
        'matricksblocks'
    """
    if value is not None:
        return f"matricksblocks {value}"
    return "matricksblocks"


def matricks_filter(value: int | float) -> str:
    """
    Construct a MAtricksFilter command.

    Args:
        value: Filter value.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_filter(2)
        'matricksfilter 2'
    """
    return f"matricksfilter {value}"


def matricks_groups(value: int | float) -> str:
    """
    Construct a MAtricksGroups command.

    Args:
        value: Groups value.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_groups(3)
        'matricksgroups 3'
    """
    return f"matricksgroups {value}"


def matricks_interleave(value: int | float) -> str:
    """
    Construct a MAtricksInterleave command.

    Args:
        value: Interleave value.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_interleave(2)
        'matricksinterleave 2'
    """
    return f"matricksinterleave {value}"


def matricks_reset() -> str:
    """
    Construct a MAtricksReset command to reset all MAtricks settings.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_reset()
        'matricksreset'
    """
    return "matricksreset"


def matricks_wings(value: int | float) -> str:
    """
    Construct a MAtricksWings command.

    Args:
        value: Wings value.

    Returns:
        str: MA command string

    Examples:
        >>> matricks_wings(2)
        'matrickswings 2'
    """
    return f"matrickswings {value}"
