"""
Playback Function Keywords for grandMA2 Command Builder

這個模組包含與播放控制相關的函數。

包含的函數：
- go: 執行物件的下一個步驟（支援 Executor、Macro、Sequence 等）
- go_back: 執行物件的前一個步驟
- goto: 跳轉到指定的 Cue
- go_sequence (Go+): 執行 Sequence（簡化版）
- pause_sequence: 暫停 Sequence
- goto_cue: 跳轉到指定的 Cue（簡化版）
- go_fast_back (<<<): 快速跳到前一個步驟
- go_fast_forward (>>>): 快速跳到下一個步驟
- def_go_back: 選定 Executor 的前一個 Cue
- def_go_forward: 選定 Executor 的下一個 Cue
- def_go_pause: 暫停選定 Executor
"""

from typing import List, Literal, Optional, Union

# Cue Mode 類型定義
CueMode = Literal["normal", "assert", "xassert", "release"]


# ============================================================================
# GO FUNCTION KEYWORD
# ============================================================================
# Go is a function keyword to activate the next step of an executing object.
# If the target object has steps, it will go to the next step.
# If the object is step-less, it will start running forward.
# ============================================================================


def go(
    object_type: Optional[str] = None,
    object_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    cue_mode: Optional[CueMode] = None,
    userprofile: Optional[str] = None,
) -> str:
    """
    Construct a Go command to activate the next step of an executing object.

    Go 用於啟動執行物件的下一個步驟。如果目標物件有步驟，會跳到下一步。
    如果物件沒有步驟，會開始向前執行。

    Args:
        object_type: 物件類型 (executor, macro, sequence 等)
        object_id: 物件 ID 或 ID 列表
        end: 範圍結束 ID（用於 thru）
        cue_mode: Cue 模式 (normal, assert, xassert, release)
        userprofile: 使用者設定檔名稱

    Returns:
        str: MA 指令字串

    Examples:
        >>> go("executor", 3)
        'go executor 3'
        >>> go("macro", 2)
        'go macro 2'
        >>> go("executor", 1, end=5)
        'go executor 1 thru 5'
        >>> go("executor", 3, cue_mode="assert")
        'go executor 3 /cue_mode=assert'
        >>> go("executor", 3, userprofile="Klaus")
        'go executor 3 /userprofile="Klaus"'
    """
    parts = ["go"]

    # 物件類型和 ID
    if object_type:
        parts.append(object_type)
        if object_id is not None:
            if isinstance(object_id, list):
                id_str = " + ".join(str(i) for i in object_id)
                parts.append(id_str)
            else:
                parts.append(str(object_id))
                if end is not None:
                    parts.append(f"thru {end}")

    # 選項
    if cue_mode:
        parts.append(f"/cue_mode={cue_mode}")
    if userprofile:
        parts.append(f'/userprofile="{userprofile}"')

    return " ".join(parts)


def go_executor(
    executor_id: Union[int, List[int]],
    *,
    end: Optional[int] = None,
    cue_mode: Optional[CueMode] = None,
    userprofile: Optional[str] = None,
) -> str:
    """
    Construct a Go command for an executor.

    便利函式，用於執行指定 Executor 的下一個步驟。

    Args:
        executor_id: Executor ID 或 ID 列表
        end: 範圍結束 ID
        cue_mode: Cue 模式
        userprofile: 使用者設定檔名稱

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_executor(3)
        'go executor 3'
        >>> go_executor([1, 2, 3])
        'go executor 1 + 2 + 3'
    """
    return go(
        "executor", executor_id, end=end, cue_mode=cue_mode, userprofile=userprofile
    )


def go_macro(macro_id: int) -> str:
    """
    Construct a Go command to start a macro.

    便利函式，用於啟動指定的 Macro。

    Args:
        macro_id: Macro ID

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_macro(2)
        'go macro 2'
    """
    return go("macro", macro_id)


# ============================================================================
# GOBACK FUNCTION KEYWORD
# ============================================================================
# GoBack is a function keyword to activate the previous step of an object.
# Set the default fade time in Setup -> Show -> Playback & MIB Timing -> GoBack.
# ============================================================================


def go_back(
    object_type: Optional[str] = None,
    object_id: Optional[Union[int, List[int]]] = None,
    *,
    end: Optional[int] = None,
    cue_mode: Optional[CueMode] = None,
    userprofile: Optional[str] = None,
) -> str:
    """
    Construct a GoBack command to activate the previous step of an object.

    GoBack 用於啟動執行物件的前一個步驟。如果目標物件有步驟，會跳到前一步。
    如果物件沒有步驟，會開始向後執行。
    預設 fade 時間可在 Setup -> Show -> Playback & MIB Timing -> GoBack 中設定。

    Args:
        object_type: 物件類型 (executor, sequence 等)
        object_id: 物件 ID 或 ID 列表
        end: 範圍結束 ID（用於 thru）
        cue_mode: Cue 模式 (normal, assert, xassert, release)
        userprofile: 使用者設定檔名稱

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_back("executor", 3)
        'goback executor 3'
        >>> go_back("executor", 3, cue_mode="assert")
        'goback executor 3 /cue_mode=assert'
    """
    parts = ["goback"]

    # 物件類型和 ID
    if object_type:
        parts.append(object_type)
        if object_id is not None:
            if isinstance(object_id, list):
                id_str = " + ".join(str(i) for i in object_id)
                parts.append(id_str)
            else:
                parts.append(str(object_id))
                if end is not None:
                    parts.append(f"thru {end}")

    # 選項
    if cue_mode:
        parts.append(f"/cue_mode={cue_mode}")
    if userprofile:
        parts.append(f'/userprofile="{userprofile}"')

    return " ".join(parts)


def go_back_executor(
    executor_id: Union[int, List[int]],
    *,
    end: Optional[int] = None,
    cue_mode: Optional[CueMode] = None,
    userprofile: Optional[str] = None,
) -> str:
    """
    Construct a GoBack command for an executor.

    便利函式，用於執行指定 Executor 的前一個步驟。

    Args:
        executor_id: Executor ID 或 ID 列表
        end: 範圍結束 ID
        cue_mode: Cue 模式
        userprofile: 使用者設定檔名稱

    Returns:
        str: MA 指令字串

    Examples:
        >>> go_back_executor(3)
        'goback executor 3'
    """
    return go_back(
        "executor", executor_id, end=end, cue_mode=cue_mode, userprofile=userprofile
    )


# ============================================================================
# GOTO FUNCTION KEYWORD
# ============================================================================
# Goto is a function keyword to jump to a specific cue in a list.
# Set the fade time in Setup -> Show -> Playback & MIB Timing -> Goto.
# ============================================================================


def goto(
    cue_id: Union[int, float],
    *,
    executor: Optional[int] = None,
    sequence: Optional[int] = None,
    cue_mode: Optional[CueMode] = None,
    userprofile: Optional[str] = None,
) -> str:
    """
    Construct a Goto command to jump to a specific cue.

    Goto 用於跳轉到指定的 Cue。
    預設 fade 時間可在 Setup -> Show -> Playback & MIB Timing -> Goto 中設定。

    Args:
        cue_id: Cue 編號
        executor: Executor 編號（可選）
        sequence: Sequence 編號（可選）
        cue_mode: Cue 模式 (normal, assert, xassert, release)
        userprofile: 使用者設定檔名稱

    Returns:
        str: MA 指令字串

    Examples:
        >>> goto(3)
        'goto cue 3'
        >>> goto(5, executor=4)
        'goto cue 5 executor 4'
        >>> goto(3, sequence=1)
        'goto cue 3 sequence 1'
        >>> goto(3, cue_mode="assert")
        'goto cue 3 /cue_mode=assert'
    """
    parts = ["goto", "cue", str(cue_id)]

    # Executor 或 Sequence
    if executor is not None:
        parts.append(f"executor {executor}")
    elif sequence is not None:
        parts.append(f"sequence {sequence}")

    # 選項
    if cue_mode:
        parts.append(f"/cue_mode={cue_mode}")
    if userprofile:
        parts.append(f'/userprofile="{userprofile}"')

    return " ".join(parts)


# ============================================================================
# LEGACY CONVENIENCE FUNCTIONS (保持向後相容)
# ============================================================================


def go_sequence(sequence_id: int) -> str:
    """
    Construct a command to execute a sequence (legacy).

    這是舊版便利函式，建議使用 go("sequence", id) 代替。

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
    Construct a command to jump to a specific cue (legacy).

    這是舊版便利函式，建議使用 goto(cue_id, sequence=sequence_id) 代替。

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


# ============================================================================
# DEFGOBACK / DEFGOFORWARD / DEFGOPAUSE FUNCTION KEYWORDS
# ============================================================================
# These keywords operate on the **selected executor** (default executor).
# They are equivalent to pressing the physical Go-, Go+, and Pause buttons.
# ============================================================================


def def_go_back() -> str:
    """
    Construct a DefGoBack command to call the previous cue in the selected executor.

    DefGoBack 用於在選定的 Executor 上呼叫前一個 Cue。
    等同於按下控台上的大型 Go- 按鈕。

    Returns:
        str: MA 指令字串

    Examples:
        >>> def_go_back()
        'defgoback'
    """
    return "defgoback"


def def_go_forward() -> str:
    """
    Construct a DefGoForward command to call the next cue in the selected executor.

    DefGoForward 用於在選定的 Executor 上呼叫下一個 Cue。
    等同於按下控台上的大型 Go+ 按鈕。

    Returns:
        str: MA 指令字串

    Examples:
        >>> def_go_forward()
        'defgoforward'
    """
    return "defgoforward"


def def_go_pause() -> str:
    """
    Construct a DefGoPause command to pause the current fade in the selected executor.

    DefGoPause 用於暫停選定 Executor 上當前的 fade 和 effect。
    如果 assign menu 中的 "Link effect to rate" 選項開啟，也會暫停 effects。
    等同於按下控台上的大型 Pause 按鈕。

    Returns:
        str: MA 指令字串

    Examples:
        >>> def_go_pause()
        'defgopause'
    """
    return "defgopause"
