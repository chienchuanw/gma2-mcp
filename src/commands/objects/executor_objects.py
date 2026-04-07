"""
Executor Object Keywords for grandMA2 Command Builder

Included functions:
- fader: Reference fader object
- fader_page: Reference fader page
- button_page: Reference button page
- channel_fader: Reference channel fader
- channel_page: Reference channel page
- exec_button_1: Reference executor button 1
- exec_button_2: Reference executor button 2
- exec_button_3: Reference executor button 3
- all_button_executors: Select all button executors
- all_chase_executors: Select all chase executors
- all_fader_executors: Select all fader executors
- all_seq_executors: Select all sequence executors
"""


def fader(fader_id: int) -> str:
    """
    Construct a Fader object reference.

    Args:
        fader_id: Fader number

    Returns:
        str: MA command string

    Examples:
        >>> fader(1)
        'fader 1'
    """
    return f"fader {fader_id}"


def fader_page(page_id: int) -> str:
    """
    Construct a FaderPage object reference.

    Args:
        page_id: Fader page number

    Returns:
        str: MA command string

    Examples:
        >>> fader_page(3)
        'faderpage 3'
    """
    return f"faderpage {page_id}"


def button_page(page_id: int) -> str:
    """
    Construct a ButtonPage object reference.

    Args:
        page_id: Button page number

    Returns:
        str: MA command string

    Examples:
        >>> button_page(2)
        'buttonpage 2'
    """
    return f"buttonpage {page_id}"


def channel_fader(fader_id: int) -> str:
    """
    Construct a ChannelFader object reference.

    Args:
        fader_id: Channel fader number

    Returns:
        str: MA command string

    Examples:
        >>> channel_fader(5)
        'channelfader 5'
    """
    return f"channelfader {fader_id}"


def channel_page(page_id: int) -> str:
    """
    Construct a ChannelPage object reference.

    Args:
        page_id: Channel page number

    Returns:
        str: MA command string

    Examples:
        >>> channel_page(1)
        'channelpage 1'
    """
    return f"channelpage {page_id}"


def exec_button_1(button_id: int) -> str:
    """
    Construct an ExecButton1 object reference.

    Args:
        button_id: Executor button 1 number

    Returns:
        str: MA command string

    Examples:
        >>> exec_button_1(3)
        'execbutton1 3'
    """
    return f"execbutton1 {button_id}"


def exec_button_2(button_id: int) -> str:
    """
    Construct an ExecButton2 object reference.

    Args:
        button_id: Executor button 2 number

    Returns:
        str: MA command string

    Examples:
        >>> exec_button_2(3)
        'execbutton2 3'
    """
    return f"execbutton2 {button_id}"


def exec_button_3(button_id: int) -> str:
    """
    Construct an ExecButton3 object reference.

    Args:
        button_id: Executor button 3 number

    Returns:
        str: MA command string

    Examples:
        >>> exec_button_3(3)
        'execbutton3 3'
    """
    return f"execbutton3 {button_id}"


def all_button_executors() -> str:
    """
    Construct an AllButtonExecutors selector to select all button executors.

    Returns:
        str: MA command string

    Examples:
        >>> all_button_executors()
        'allbuttonexecutors'
    """
    return "allbuttonexecutors"


def all_chase_executors() -> str:
    """
    Construct an AllChaseExecutors selector to select all chase executors.

    Returns:
        str: MA command string

    Examples:
        >>> all_chase_executors()
        'allchaseexecutors'
    """
    return "allchaseexecutors"


def all_fader_executors() -> str:
    """
    Construct an AllFaderExecutors selector to select all fader executors.

    Returns:
        str: MA command string

    Examples:
        >>> all_fader_executors()
        'allfaderexecutors'
    """
    return "allfaderexecutors"


def all_seq_executors() -> str:
    """
    Construct an AllSequExecutors selector to select all sequence executors.

    Returns:
        str: MA command string

    Examples:
        >>> all_seq_executors()
        'allsequexecutors'
    """
    return "allsequexecutors"
