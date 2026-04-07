"""
Blind and Preview Keywords for grandMA2 Command Builder

This module contains Blind, BlindEdit, Preview, and PreviewEdit function keywords.

Blind:
- Toggles blind mode where edits are not visible on stage output
- Can be applied to specific executors

Preview:
- Toggles preview mode to visualize executor output without affecting stage
- Can be applied to specific executors

Included functions:
- blind: Toggle blind editing mode
- blind_edit: Toggle blind edit mode
- preview: Toggle preview mode
- preview_edit: Toggle preview edit mode
"""

from typing import Optional


def blind(target: Optional[str] = None) -> str:
    """
    Construct a Blind command to toggle blind editing mode.

    Blind mode allows editing without affecting stage output.
    Changes made in blind mode are only visible in the programmer.

    Args:
        target: Object to apply blind to (e.g., "executor 3").
                If None, toggles global blind mode.

    Returns:
        str: MA command string

    Examples:
        >>> blind()
        'blind'
        >>> blind("executor 3")
        'blind executor 3'
    """
    if target:
        return f"blind {target}"
    return "blind"


def blind_edit() -> str:
    """
    Construct a BlindEdit command to toggle blind edit mode.

    BlindEdit allows editing in blind mode with additional options.

    Returns:
        str: MA command string

    Examples:
        >>> blind_edit()
        'blindedit'
    """
    return "blindedit"


def preview(target: Optional[str] = None) -> str:
    """
    Construct a Preview command to toggle preview mode.

    Preview mode visualizes executor output without affecting stage output.
    Useful for checking cue content before going live.

    Args:
        target: Object to preview (e.g., "executor 5").
                If None, toggles global preview mode.

    Returns:
        str: MA command string

    Examples:
        >>> preview()
        'preview'
        >>> preview("executor 5")
        'preview executor 5'
    """
    if target:
        return f"preview {target}"
    return "preview"


def preview_edit() -> str:
    """
    Construct a PreviewEdit command to toggle preview edit mode.

    PreviewEdit combines preview and edit modes.

    Returns:
        str: MA command string

    Examples:
        >>> preview_edit()
        'previewedit'
    """
    return "previewedit"
