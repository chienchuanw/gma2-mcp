"""
Macro Function Keywords for grandMA2 Command Builder

Includes:
- store_macro: Store/create a macro in the macro pool
- label_macro: Label a macro
- delete_macro: Delete a macro from the pool
- macro_with_input_after: Add user input placeholder at the end of command
- macro_with_input_before: Add user input placeholder at the beginning of command

The "@" character is used in macros as a placeholder for user input.
This is completely different from the "At" keyword.

- @ at the end: User input will come after the command
- @ at the beginning: User input will come before the command (CLI must be disabled)
"""

from typing import Optional


def store_macro(macro_id: int, name: Optional[str] = None) -> str:
    """
    Construct a Store Macro command.

    Args:
        macro_id: Macro number to store
        name: Optional name for the macro

    Returns:
        str: MA command string

    Examples:
        >>> store_macro(5)
        'store macro 5'
        >>> store_macro(5, name="My Macro")
        'store macro 5 "My Macro"'
    """
    cmd = f"store macro {macro_id}"
    if name is not None:
        cmd += f' "{name}"'
    return cmd


def label_macro(macro_id: int, name: str) -> str:
    """
    Construct a Label Macro command.

    Args:
        macro_id: Macro number to label
        name: Label text for the macro

    Returns:
        str: MA command string

    Examples:
        >>> label_macro(5, "Dimmer Chase")
        'label macro 5 "Dimmer Chase"'
    """
    return f'label macro {macro_id} "{name}"'


def delete_macro(macro_id: int, pool: int = 1) -> str:
    """
    Construct a Delete Macro command.

    Args:
        macro_id: Macro number to delete
        pool: Macro pool number (default: 1)

    Returns:
        str: MA command string

    Examples:
        >>> delete_macro(5)
        'delete macro 1.5'
        >>> delete_macro(5, pool=2)
        'delete macro 2.5'
    """
    return f"delete macro {pool}.{macro_id}"


def macro_with_input_after(command: str) -> str:
    """
    Create a macro line with user input placeholder at the end.

    The @ at the end means the user will provide input after
    executing the macro.

    Args:
        command: The command prefix before user input

    Returns:
        str: Macro line with @ placeholder at the end

    Examples:
        >>> macro_with_input_after("Load")
        'Load @'
        >>> macro_with_input_after("Attribute Pan At")
        'Attribute Pan At @'
    """
    return f"{command} @"


def macro_with_input_before(command: str) -> str:
    """
    Create a macro line with user input placeholder at the beginning.

    The @ at the beginning means the user's previous command line
    input will be prepended. Note: CLI must be disabled for this to work.

    Args:
        command: The command suffix after user input

    Returns:
        str: Macro line with @ placeholder at the beginning

    Examples:
        >>> macro_with_input_before("Fade 20")
        '@ Fade 20'
    """
    return f"@ {command}"
