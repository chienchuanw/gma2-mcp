"""
Flash/Swop Extension Keywords for grandMA2 Command Builder

Included functions:
- flash_go: Flash and go
- flash_on: Flash on (latching)
- swop_go: Swop and go
- swop_on: Swop on (latching)
- store_look: Store a look
"""


def flash_go(target: str) -> str:
    """
    Construct a FlashGo command to flash and go.

    Args:
        target: Object to flash-go (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> flash_go("executor 1")
        'flashgo executor 1'
    """
    return f"flashgo {target}"


def flash_on(target: str) -> str:
    """
    Construct a FlashOn command for latching flash.

    Args:
        target: Object to flash-on (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> flash_on("executor 1")
        'flashon executor 1'
    """
    return f"flashon {target}"


def swop_go(target: str) -> str:
    """
    Construct a SwopGo command to swop and go.

    Args:
        target: Object to swop-go (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> swop_go("executor 3")
        'swopgo executor 3'
    """
    return f"swopgo {target}"


def swop_on(target: str) -> str:
    """
    Construct a SwopOn command for latching swop.

    Args:
        target: Object to swop-on (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> swop_on("executor 3")
        'swopon executor 3'
    """
    return f"swopon {target}"


def store_look(target: str | None = None) -> str:
    """
    Construct a StoreLook command to store a look.

    Args:
        target: Object to store look to (e.g., "cue 3").

    Returns:
        str: MA command string

    Examples:
        >>> store_look()
        'storelook'
        >>> store_look("cue 3")
        'storelook cue 3'
    """
    if target:
        return f"storelook {target}"
    return "storelook"
