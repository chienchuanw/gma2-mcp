"""
Executor Control Keywords for grandMA2 Command Builder

Included functions:
- off: Turn off executor
- on: Turn on executor
- kill: Immediately turn off executor
- flash: Flash executor
- swop: Swop executor (solo with blackout)
- stomp: Stomp executor (assertive playback)
- temp: Temporary executor activation
- toggle: Toggle executor on/off
- release: Release executor
- top: Set executor to top priority
- select: Select objects
"""


def off(target: str | None = None, *, executor: int | None = None) -> str:
    """
    Construct an Off command to turn off an executor or object.

    Args:
        target: Object to turn off (e.g., "executor 3").
        executor: Executor number (convenience shortcut).

    Returns:
        str: MA command string

    Examples:
        >>> off()
        'off'
        >>> off("executor 3")
        'off executor 3'
        >>> off(executor=5)
        'off executor 5'
    """
    if executor is not None:
        return f"off executor {executor}"
    if target:
        return f"off {target}"
    return "off"


def on(target: str | None = None, *, executor: int | None = None) -> str:
    """
    Construct an On command to turn on an executor or object.

    Args:
        target: Object to turn on (e.g., "executor 3").
        executor: Executor number (convenience shortcut).

    Returns:
        str: MA command string

    Examples:
        >>> on()
        'on'
        >>> on("executor 3")
        'on executor 3'
    """
    if executor is not None:
        return f"on executor {executor}"
    if target:
        return f"on {target}"
    return "on"


def kill(target: str | None = None) -> str:
    """
    Construct a Kill command to immediately turn off an executor.

    Args:
        target: Object to kill (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> kill()
        'kill'
        >>> kill("executor 3")
        'kill executor 3'
    """
    if target:
        return f"kill {target}"
    return "kill"


def flash(target: str) -> str:
    """
    Construct a Flash command to flash an executor.

    Args:
        target: Object to flash (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> flash("executor 1")
        'flash executor 1'
    """
    return f"flash {target}"


def swop(target: str) -> str:
    """
    Construct a Swop command.

    Args:
        target: Object to swop (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> swop("executor 3")
        'swop executor 3'
    """
    return f"swop {target}"


def stomp(target: str) -> str:
    """
    Construct a Stomp command for assertive playback.

    Args:
        target: Object to stomp (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> stomp("executor 1")
        'stomp executor 1'
    """
    return f"stomp {target}"


def temp(target: str) -> str:
    """
    Construct a Temp command for temporary executor activation.

    Args:
        target: Object for temp activation (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> temp("executor 3")
        'temp executor 3'
    """
    return f"temp {target}"


def toggle(target: str) -> str:
    """
    Construct a Toggle command to toggle executor on/off.

    Args:
        target: Object to toggle (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> toggle("executor 1")
        'toggle executor 1'
    """
    return f"toggle {target}"


def release(target: str | None = None) -> str:
    """
    Construct a Release command to release an executor.

    Args:
        target: Object to release (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> release()
        'release'
        >>> release("executor 3")
        'release executor 3'
    """
    if target:
        return f"release {target}"
    return "release"


def top(target: str) -> str:
    """
    Construct a Top command to set executor to top priority.

    Args:
        target: Object to set to top (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> top("executor 1")
        'top executor 1'
    """
    return f"top {target}"


def select(target: str) -> str:
    """
    Construct a Select command to select objects.

    Args:
        target: Object to select (e.g., "executor 5").

    Returns:
        str: MA command string

    Examples:
        >>> select("executor 5")
        'select executor 5'
    """
    return f"select {target}"
