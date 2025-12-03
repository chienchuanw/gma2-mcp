"""
Macro Placeholder Function Keywords for grandMA2 Command Builder

「@」字元用於 Macro 中作為使用者輸入的佔位符。
這與「At」keyword 完全不同。

- @ 在結尾：使用者輸入會在命令之後
- @ 在開頭：使用者輸入會在命令之前（CLI 必須被禁用）

包含的函數：
- macro_with_input_after: 在命令結尾加入使用者輸入佔位符
- macro_with_input_before: 在命令開頭加入使用者輸入佔位符
"""


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
