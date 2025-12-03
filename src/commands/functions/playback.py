"""
Playback Function Keywords for grandMA2 Command Builder

這個模組包含與播放控制相關的函數。

包含的函數：
- go_sequence (Go+): 執行 Sequence
- pause_sequence: 暫停 Sequence
- goto_cue: 跳轉到指定的 Cue
- go_fast_back (<<<): 快速跳到前一個步驟
- go_fast_forward (>>>): 快速跳到下一個步驟
"""

from typing import List, Optional, Union


# ============================================================================
# GO / PAUSE / GOTO FUNCTION KEYWORDS
# ============================================================================


def go_sequence(sequence_id: int) -> str:
    """
    Construct a command to execute a sequence.

    Args:
        sequence_id: Sequence number

    Returns:
        str: MA command to execute a sequence
    """
    return f"go+ sequence {sequence_id}"


def pause_sequence(sequence_id: int) -> str:
    """
    Construct a command to pause a sequence.

    Args:
        sequence_id: Sequence number

    Returns:
        str: MA command to pause a sequence
    """
    return f"pause sequence {sequence_id}"


def goto_cue(sequence_id: int, cue_id: int) -> str:
    """
    Construct a command to jump to a specific cue.

    Args:
        sequence_id: Sequence number
        cue_id: Cue number

    Returns:
        str: MA command to jump to a cue
    """
    return f"goto cue {cue_id} sequence {sequence_id}"


# ============================================================================
# <<< (GOFASTBACK) AND >>> (GOFASTFORWARD) FUNCTION KEYWORDS
# ============================================================================
# These keywords are used to quickly jump to previous/next cue step.
# The timing can be adjusted via Setup -> Show -> Playback + MIB Timing.
# ============================================================================


def go_fast_back(
    *,
    executor: Optional[Union[int, List[int]]] = None,
    sequence: Optional[int] = None,
) -> str:
    """
    Construct a GoFastBack (<<<) command to jump quickly to the previous step.

    <<< 用於快速跳轉到前一個步驟（預設不使用時間，可在 setup 中調整）。
    時間可透過 Setup -> Show -> Playback + MIB Timing 的 GoFast 屬性調整。

    Args:
        executor: Executor 編號或編號列表
        sequence: Sequence 編號

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_fast_back()
        '<<<'
        >>> go_fast_back(executor=3)
        '<<< executor 3'
        >>> go_fast_back(executor=[1, 2, 3])
        '<<< executor 1 + 2 + 3'
        >>> go_fast_back(sequence=5)
        '<<< sequence 5'
    """
    if executor is not None:
        if isinstance(executor, list):
            exec_str = " + ".join(str(e) for e in executor)
            return f"<<< executor {exec_str}"
        return f"<<< executor {executor}"

    if sequence is not None:
        return f"<<< sequence {sequence}"

    return "<<<"


def go_fast_forward(
    *,
    executor: Optional[Union[int, List[int]]] = None,
    sequence: Optional[int] = None,
) -> str:
    """
    Construct a GoFastForward (>>>) command to jump quickly to the next step.

    >>> 用於快速跳轉到下一個步驟（預設不使用時間，可在 setup 中調整）。
    時間可透過 Setup -> Show -> Playback + MIB Timing 的 GoFast 屬性調整。

    Args:
        executor: Executor 編號或編號列表
        sequence: Sequence 編號

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_fast_forward()
        '>>>'
        >>> go_fast_forward(executor=3)
        '>>> executor 3'
        >>> go_fast_forward(executor=[1, 2, 3])
        '>>> executor 1 + 2 + 3'
        >>> go_fast_forward(sequence=5)
        '>>> sequence 5'
    """
    if executor is not None:
        if isinstance(executor, list):
            exec_str = " + ".join(str(e) for e in executor)
            return f">>> executor {exec_str}"
        return f">>> executor {executor}"

    if sequence is not None:
        return f">>> sequence {sequence}"

    return ">>>"
