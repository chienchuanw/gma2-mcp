"""
List and Info Function Keywords for grandMA2 Command Builder

This module contains functions related to list and info operations.

List is used to display show data in the command line feedback window.
Info is used to add or display user information for objects.

Included functions:
- list_objects: Generic list command
- list_cue: List cues
- list_group: List groups
- list_preset: List presets
- list_attribute: List attributes
- list_messages: List messages
- info: Generic info command
- info_group: Group info
- info_cue: Cue info
- info_preset: Preset info
"""

from ..constants import PRESET_TYPES


# ============================================================================
# LIST FUNCTION KEYWORD
# ============================================================================


def list_objects(
    object_type: str | None = None,
    object_id: int | str | None = None,
    *,
    end: int | None = None,
    filename: str | None = None,
    condition: str | None = None,
) -> str:
    """
    Construct a List command to display show data in the command line feedback window.

    List is used to display show data in the command line feedback window, such as Cues, Groups,
    Presets, Messages, etc. If no object type is specified, it displays data for the current destination.

    Args:
        object_type: Object type (e.g., "cue", "group", "preset", "attribute", "messages")
        object_id: Object ID or identifier (optional)
        end: End ID for range (uses Thru)
        filename: Output CSV filename (saved to reports folder)
        condition: Condition filter (only for Messages)

    Returns:
        str: MA List command

    Examples:
        >>> list_objects("cue")
        'list cue'
        >>> list_objects("group", end=10)
        'list group thru 10'
        >>> list_objects("attribute")
        'list attribute'
        >>> list_objects("preset", '"color"."m*"')
        'list preset "color"."m*"'
        >>> list_objects("group", filename="my_groups")
        'list group /filename=my_groups'
    """
    # Base command
    if object_type is None:
        cmd = "list"
    else:
        cmd = f"list {object_type}"

    # Handle object ID or range
    if object_id is not None:
        if end is not None:
            cmd = f"{cmd} {object_id} thru {end}"
        else:
            cmd = f"{cmd} {object_id}"
    elif end is not None:
        # Only end, means "thru N"
        cmd = f"{cmd} thru {end}"

    # Option handling
    if filename:
        cmd = f"{cmd} /filename={filename}"

    if condition:
        cmd = f"{cmd} /condition={condition}"

    return cmd


def list_cue(
    cue_id: int | str | None = None,
    *,
    end: int | None = None,
    sequence_id: int | None = None,
    filename: str | None = None,
) -> str:
    """
    Construct a List command for cues.

    List cues from the selected Executor or specified Sequence.

    Args:
        cue_id: Cue ID (optional)
        end: End cue ID for range
        sequence_id: Sequence ID (optional, specifies specific sequence)
        filename: Output CSV filename

    Returns:
        str: MA List command for cues

    Examples:
        >>> list_cue()
        'list cue'
        >>> list_cue(1, end=10)
        'list cue 1 thru 10'
        >>> list_cue(sequence_id=5)
        'list cue sequence 5'
    """
    cmd = "list cue"

    if cue_id is not None:
        if end is not None:
            cmd = f"{cmd} {cue_id} thru {end}"
        else:
            cmd = f"{cmd} {cue_id}"
    elif end is not None:
        cmd = f"{cmd} thru {end}"

    if sequence_id is not None:
        cmd = f"{cmd} sequence {sequence_id}"

    if filename:
        cmd = f"{cmd} /filename={filename}"

    return cmd


def list_group(
    group_id: int | None = None,
    *,
    end: int | None = None,
    filename: str | None = None,
) -> str:
    """
    Construct a List command for groups.

    List groups in the Group Pool.

    Args:
        group_id: Group ID (optional, specifies starting point)
        end: End group ID for range
        filename: Output CSV filename

    Returns:
        str: MA List command for groups

    Examples:
        >>> list_group()
        'list group'
        >>> list_group(end=10)
        'list group thru 10'
        >>> list_group(1, end=5)
        'list group 1 thru 5'
    """
    cmd = "list group"

    if group_id is not None:
        if end is not None:
            cmd = f"{cmd} {group_id} thru {end}"
        else:
            cmd = f"{cmd} {group_id}"
    elif end is not None:
        cmd = f"{cmd} thru {end}"

    if filename:
        cmd = f"{cmd} /filename={filename}"

    return cmd


def list_preset(
    preset_type: int | str | None = None,
    preset_id: int | str | None = None,
    *,
    end: int | None = None,
    filename: str | None = None,
) -> str:
    """
    Construct a List command for presets.

    列出 Preset Pool 中的 Presets。

    Args:
        preset_type: Preset 類型（如 "color", "position", 4 等）
        preset_id: Preset ID 或名稱模式（如 '"m*"'）
        end: 範圍結束 Preset ID
        filename: 輸出 CSV 檔案名稱

    Returns:
        str: MA List command for presets

    Examples:
        >>> list_preset()
        'list preset'
        >>> list_preset("color")
        'list preset "color"'
        >>> list_preset("color", '"m*"')
        'list preset "color"."m*"'
        >>> list_preset(4, '"m*"')
        'list preset 4."m*"'
    """
    cmd = "list preset"

    if preset_type is not None:
        # 處理文字類型名稱（加引號）或數字類型
        if isinstance(preset_type, str) and not preset_type.startswith('"'):
            type_part = f'"{preset_type}"'
        else:
            type_part = str(preset_type)

        if preset_id is not None:
            cmd = f"{cmd} {type_part}.{preset_id}"
        else:
            cmd = f"{cmd} {type_part}"
    elif preset_id is not None:
        if end is not None:
            cmd = f"{cmd} {preset_id} thru {end}"
        else:
            cmd = f"{cmd} {preset_id}"

    if filename:
        cmd = f"{cmd} /filename={filename}"

    return cmd


def list_attribute(*, filename: str | None = None) -> str:
    """
    Construct a List command for attributes.

    列出 show file 中存在的所有屬性名稱。

    Args:
        filename: 輸出 CSV 檔案名稱

    Returns:
        str: MA List command for attributes

    Example:
        >>> list_attribute()
        'list attribute'
    """
    cmd = "list attribute"

    if filename:
        cmd = f"{cmd} /filename={filename}"

    return cmd


def list_messages(*, condition: str | None = None, filename: str | None = None) -> str:
    """
    Construct a List command for messages.

    列出訊息中心的訊息。

    Args:
        condition: 條件過濾
        filename: 輸出 CSV 檔案名稱

    Returns:
        str: MA List command for messages

    Examples:
        >>> list_messages()
        'list messages'
        >>> list_messages(condition="error")
        'list messages /condition=error'
    """
    cmd = "list messages"

    if condition:
        cmd = f"{cmd} /condition={condition}"

    if filename:
        cmd = f"{cmd} /filename={filename}"

    return cmd


# ============================================================================
# INFO FUNCTION KEYWORD
# ============================================================================


def info(
    object_type: str,
    object_id: int | str,
    *,
    end: int | None = None,
    text: str | None = None,
) -> str:
    """
    Construct an Info command to add or display user info to an object.

    Info 用於為物件添加或顯示用戶資訊。
    如果提供 text，則設定該資訊；否則顯示現有資訊。

    Args:
        object_type: 物件類型（如 "group", "cue", "preset"）
        object_id: 物件 ID
        end: 範圍結束 ID（使用 Thru）
        text: 要添加的資訊文字（可選，如未提供則顯示現有資訊）

    Returns:
        str: MA Info command

    Examples:
        >>> info("group", 3)
        'info group 3'
        >>> info("group", 3, text="these fixtures are in the backtruss")
        'info group 3 "these fixtures are in the backtruss"'
        >>> info("cue", 1, end=5)
        'info cue 1 thru 5'
    """
    # 構建物件部分
    if end is not None:
        object_part = f"{object_type} {object_id} thru {end}"
    else:
        object_part = f"{object_type} {object_id}"

    cmd = f"info {object_part}"

    # 如果有文字，則添加資訊
    if text is not None:
        cmd = f'{cmd} "{text}"'

    return cmd


def info_group(
    group_id: int, *, end: int | None = None, text: str | None = None
) -> str:
    """
    Construct an Info command for groups.

    為 Group 添加或顯示資訊。

    Args:
        group_id: Group ID
        end: 範圍結束 Group ID
        text: 要添加的資訊文字

    Returns:
        str: MA Info command for group

    Examples:
        >>> info_group(3)
        'info group 3'
        >>> info_group(3, text="backtruss fixtures")
        'info group 3 "backtruss fixtures"'
    """
    return info("group", group_id, end=end, text=text)


def info_cue(
    cue_id: int | str,
    *,
    sequence_id: int | None = None,
    end: int | str | None = None,
    text: str | None = None,
) -> str:
    """
    Construct an Info command for cues.

    為 Cue 添加或顯示資訊。

    Args:
        cue_id: Cue ID
        sequence_id: Sequence ID（可選）
        end: 範圍結束 Cue ID
        text: 要添加的資訊文字

    Returns:
        str: MA Info command for cue

    Examples:
        >>> info_cue(5)
        'info cue 5'
        >>> info_cue(5, sequence_id=2)
        'info cue 5 sequence 2'
        >>> info_cue(1, text="opening look")
        'info cue 1 "opening look"'
    """
    # 構建物件部分
    if end is not None:
        object_part = f"cue {cue_id} thru {end}"
    else:
        object_part = f"cue {cue_id}"

    if sequence_id is not None:
        object_part = f"{object_part} sequence {sequence_id}"

    cmd = f"info {object_part}"

    if text is not None:
        cmd = f'{cmd} "{text}"'

    return cmd


def info_preset(
    preset_type: int | str,
    preset_id: int | str,
    *,
    text: str | None = None,
) -> str:
    """
    Construct an Info command for presets.

    為 Preset 添加或顯示資訊。

    Args:
        preset_type: Preset 類型（如 "color", 4）
        preset_id: Preset ID
        text: 要添加的資訊文字

    Returns:
        str: MA Info command for preset

    Examples:
        >>> info_preset("color", 1)
        'info preset 2.1'
        >>> info_preset(4, 5, text="deep blue")
        'info preset 4.5 "deep blue"'
    """
    # 轉換 preset type
    if isinstance(preset_type, str):
        type_num = PRESET_TYPES.get(preset_type.lower(), preset_type)
    else:
        type_num = preset_type

    cmd = f"info preset {type_num}.{preset_id}"

    if text is not None:
        cmd = f'{cmd} "{text}"'

    return cmd
