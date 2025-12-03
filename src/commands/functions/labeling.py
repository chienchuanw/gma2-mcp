"""
Label and Appearance Function Keywords for grandMA2 Command Builder

這個模組包含與標籤和外觀相關的函數。

Label 用於給物件命名。
Appearance 用於改變 Pool 物件的框架顏色和 Cue 的背景顏色。

包含的函數：
- label: 通用的標籤命令
- label_group: 標籤 Group
- label_preset: 標籤 Preset
- appearance: 改變物件外觀
"""

from typing import List, Optional, Union

from ..constants import PRESET_TYPES


# ============================================================================
# LABEL FUNCTION KEYWORD
# ============================================================================


def label_group(group_id: int, name: str) -> str:
    """
    Construct a command to label a group.

    Args:
        group_id: Group number
        name: Group name

    Returns:
        str: MA command to label a group
    """
    return f'label group {group_id} "{name}"'


def label_preset(preset_type: str, preset_id: int, name: str) -> str:
    """
    Construct a command to label a preset.

    Args:
        preset_type: Preset type
        preset_id: Preset number
        name: Preset name

    Returns:
        str: MA command to label a preset
    """
    type_num = PRESET_TYPES.get(preset_type.lower(), 1)
    return f'label preset {type_num}.{preset_id} "{name}"'


def label(
    object_type: str,
    object_id: Union[int, str, List[int]],
    name: str,
    *,
    end: Optional[int] = None,
) -> str:
    """
    Construct a Label command to give names to objects.

    If multiple objects are labeled and the name contains a number,
    the number will be automatically enumerated for each object.

    Args:
        object_type: Type of object (e.g., "fixture", "group", "preset")
        object_id: Object ID (can be compound like '"color"."Red"')
        name: Name to assign (in quotes)
        end: End ID for range labeling

    Returns:
        str: MA command to label object(s)

    Examples:
        >>> label("group", 3, "All Studiocolors")
        'label group 3 "All Studiocolors"'
        >>> label("fixture", 1, "Mac700 1", end=10)
        'label fixture 1 thru 10 "Mac700 1"'
        >>> label("preset", '"color"."Red"', "Dark Red")
        'label preset "color"."Red" "Dark Red"'
    """
    # 建立物件參照
    if isinstance(object_id, list):
        obj_str = " + ".join(str(i) for i in object_id)
        cmd = f"label {object_type} {obj_str}"
    elif end is not None:
        cmd = f"label {object_type} {object_id} thru {end}"
    else:
        cmd = f"label {object_type} {object_id}"

    # 加入名稱（確保有引號）
    if name.startswith('"') and name.endswith('"'):
        cmd += f" {name}"
    else:
        cmd += f' "{name}"'

    return cmd


# ============================================================================
# APPEARANCE FUNCTION KEYWORD
# ============================================================================
# Appearance changes frame colors of pool objects and background colors of cues.
# Can set colors via RGB (0-100), HSB (hue 0-360, sat/bright 0-100), or hex.
# Can also copy appearance from a source object.
# ============================================================================


def appearance(
    object_type: str,
    object_id: Union[int, str, List[int]],
    *,
    end: Optional[int] = None,
    source_type: Optional[str] = None,
    source_id: Optional[Union[int, str]] = None,
    reset: bool = False,
    color: Optional[str] = None,
    red: Optional[int] = None,
    green: Optional[int] = None,
    blue: Optional[int] = None,
    hue: Optional[int] = None,
    saturation: Optional[int] = None,
    brightness: Optional[int] = None,
) -> str:
    """
    Construct an Appearance command to change frame/background colors.

    Colors can be set via RGB (0-100), HSB (hue 0-360, sat/bright 0-100),
    hex color code, or by copying from a source object.

    Args:
        object_type: Type of object (e.g., "preset", "group", "cue", "macro")
        object_id: Object ID (can be compound like "0.1" for preset pool)
        end: End ID for range
        source_type: Source object type (for copying appearance)
        source_id: Source object ID (for copying appearance)
        reset: Reset appearance to default
        color: Hex color (000000-FFFFFF) or gel name
        red: Red component (0-100)
        green: Green component (0-100)
        blue: Blue component (0-100)
        hue: Hue (0-360)
        saturation: Saturation (0-100)
        brightness: Brightness (0-100)

    Returns:
        str: MA command for appearance

    Examples:
        >>> appearance("preset", "0.1", red=100, green=0, blue=0)
        'appearance preset 0.1 /r=100 /g=0 /b=0'
        >>> appearance("preset", "0.1", hue=0, saturation=100, brightness=50)
        'appearance preset 0.1 /h=0 /s=100 /br=50'
        >>> appearance("macro", 2, source_type="macro", source_id=13)
        'appearance macro 2 at macro 13'
        >>> appearance("group", 1, end=5, color="FF0000")
        'appearance group 1 thru 5 /color=FF0000'
    """
    # 建立物件參照
    if isinstance(object_id, list):
        obj_str = " + ".join(str(i) for i in object_id)
        cmd = f"appearance {object_type} {obj_str}"
    elif end is not None:
        cmd = f"appearance {object_type} {object_id} thru {end}"
    else:
        cmd = f"appearance {object_type} {object_id}"

    # 從來源物件複製外觀
    if source_type is not None and source_id is not None:
        cmd += f" at {source_type} {source_id}"
        return cmd

    # 建立選項
    options = []
    if reset:
        options.append("/reset")
    if color is not None:
        options.append(f"/color={color}")
    if red is not None:
        options.append(f"/r={red}")
    if green is not None:
        options.append(f"/g={green}")
    if blue is not None:
        options.append(f"/b={blue}")
    if hue is not None:
        options.append(f"/h={hue}")
    if saturation is not None:
        options.append(f"/s={saturation}")
    if brightness is not None:
        options.append(f"/br={brightness}")

    if options:
        cmd += " " + " ".join(options)

    return cmd
