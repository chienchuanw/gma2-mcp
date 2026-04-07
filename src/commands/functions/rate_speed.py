"""
Rate and Speed Keywords for grandMA2 Command Builder

Included functions:
- rate: Set rate of executor
- rate1: Reset rate to 1:1
- double_rate: Double the rate
- half_rate: Halve the rate
- double_speed: Double the speed
- half_speed: Halve the speed
- speed: Set speed of executor
"""

from typing import Optional


def rate(target: Optional[str] = None) -> str:
    """
    Construct a Rate command to set rate of executor.

    Args:
        target: Object to set rate for (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> rate("executor 1")
        'rate executor 1'
    """
    if target:
        return f"rate {target}"
    return "rate"


def rate1(target: Optional[str] = None) -> str:
    """
    Construct a Rate1 command to reset rate to 1:1.

    Args:
        target: Object to reset rate for (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> rate1("executor 3")
        'rate1 executor 3'
    """
    if target:
        return f"rate1 {target}"
    return "rate1"


def double_rate(target: Optional[str] = None) -> str:
    """
    Construct a DoubleRate command to double the rate.

    Args:
        target: Object to double rate for (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> double_rate("executor 1")
        'doublerate executor 1'
    """
    if target:
        return f"doublerate {target}"
    return "doublerate"


def half_rate(target: Optional[str] = None) -> str:
    """
    Construct a HalfRate command to halve the rate.

    Args:
        target: Object to halve rate for (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> half_rate("executor 1")
        'halfrate executor 1'
    """
    if target:
        return f"halfrate {target}"
    return "halfrate"


def double_speed(target: Optional[str] = None) -> str:
    """
    Construct a DoubleSpeed command to double the speed.

    Args:
        target: Object to double speed for (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> double_speed("executor 1")
        'doublespeed executor 1'
    """
    if target:
        return f"doublespeed {target}"
    return "doublespeed"


def half_speed(target: Optional[str] = None) -> str:
    """
    Construct a HalfSpeed command to halve the speed.

    Args:
        target: Object to halve speed for (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> half_speed("executor 1")
        'halfspeed executor 1'
    """
    if target:
        return f"halfspeed {target}"
    return "halfspeed"


def speed(target: Optional[str] = None) -> str:
    """
    Construct a Speed command to set speed of executor.

    Args:
        target: Object to set speed for (e.g., "executor 3").

    Returns:
        str: MA command string

    Examples:
        >>> speed("executor 3")
        'speed executor 3'
    """
    if target:
        return f"speed {target}"
    return "speed"
