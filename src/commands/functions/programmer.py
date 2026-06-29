"""
Programmer and Show Data Keywords for grandMA2 Command Builder

Included functions:
- block: Block cue tracking
- unblock: Remove tracking block
- clone: Clone fixture programming
- default: Reset to default values
- extract: Extract values from programmer
- insert: Insert cue/object
- record: Record show data
- replace: Replace values
- update: Update stored data
- oops: Undo last action
"""


def block(target: str | None = None) -> str:
    """
    Construct a Block command to block cue tracking.

    Args:
        target: Object to block (e.g., "cue 5").

    Returns:
        str: MA command string

    Examples:
        >>> block()
        'block'
        >>> block("cue 5")
        'block cue 5'
    """
    if target:
        return f"block {target}"
    return "block"


def unblock(target: str | None = None) -> str:
    """
    Construct an Unblock command to remove tracking block.

    Args:
        target: Object to unblock (e.g., "cue 3").

    Returns:
        str: MA command string

    Examples:
        >>> unblock()
        'unblock'
        >>> unblock("cue 3")
        'unblock cue 3'
    """
    if target:
        return f"unblock {target}"
    return "unblock"


def clone(target: str) -> str:
    """
    Construct a Clone command to clone fixture programming.

    Args:
        target: Clone expression (e.g., "fixture 1 at fixture 5").

    Returns:
        str: MA command string

    Examples:
        >>> clone("fixture 1 at fixture 5")
        'clone fixture 1 at fixture 5'
    """
    return f"clone {target}"


def default(target: str | None = None) -> str:
    """
    Construct a Default command to reset to default values.

    Args:
        target: Object to reset (e.g., "executor 1").

    Returns:
        str: MA command string

    Examples:
        >>> default()
        'default'
        >>> default("executor 1")
        'default executor 1'
    """
    if target:
        return f"default {target}"
    return "default"


def extract(target: str | None = None) -> str:
    """
    Construct an Extract command to extract values from programmer.

    Args:
        target: Object to extract from.

    Returns:
        str: MA command string

    Examples:
        >>> extract()
        'extract'
    """
    if target:
        return f"extract {target}"
    return "extract"


def insert(target: str) -> str:
    """
    Construct an Insert command to insert a cue or object.

    Args:
        target: Object to insert (e.g., "cue 3").

    Returns:
        str: MA command string

    Examples:
        >>> insert("cue 3")
        'insert cue 3'
    """
    return f"insert {target}"


def record(target: str | None = None) -> str:
    """
    Construct a Record command to record show data.

    Args:
        target: Object to record.

    Returns:
        str: MA command string

    Examples:
        >>> record()
        'record'
    """
    if target:
        return f"record {target}"
    return "record"


def replace(target: str | None = None) -> str:
    """
    Construct a Replace command to replace values.

    Args:
        target: Object to replace (e.g., "cue 5").

    Returns:
        str: MA command string

    Examples:
        >>> replace()
        'replace'
        >>> replace("cue 5")
        'replace cue 5'
    """
    if target:
        return f"replace {target}"
    return "replace"


def update(target: str | None = None) -> str:
    """
    Construct an Update command to update stored data.

    Args:
        target: Object to update (e.g., "cue 3").

    Returns:
        str: MA command string

    Examples:
        >>> update()
        'update'
        >>> update("cue 3")
        'update cue 3'
    """
    if target:
        return f"update {target}"
    return "update"


def oops() -> str:
    """
    Construct an Oops command to undo the last action.

    Returns:
        str: MA command string

    Examples:
        >>> oops()
        'oops'
    """
    return "oops"
