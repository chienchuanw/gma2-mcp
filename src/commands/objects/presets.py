"""
Preset Object Keywords for grandMA2 Command Builder

包含與預設相關的 Object Keywords：
- preset: 選擇或套用預設
- preset_type: 呼叫或選擇預設類型

Preset Types 的對應關係：
- dimmer=1, color=2, gobo=3, beam=4, focus=5, control=6, shapers=7, video=8
"""

from typing import List, Optional, Union

from ..constants import PRESET_TYPES


def preset(
    preset_type_or_id: Optional[Union[int, str]] = None,
    preset_id: Optional[Union[int, List[int]]] = None,
    *,
    name: Optional[str] = None,
    end: Optional[int] = None,
    wildcard: bool = False,
) -> str:
    """
    建構 Preset 指令以選擇或套用預設。

    Preset 可用於：
    - 選擇儲存在預設中的燈具
    - 將預設套用到目前選擇的燈具或頻道

    如果沒有選擇燈具/頻道，預設函式是 SelFix。
    如果已選擇燈具/頻道，預設函式是 At。

    Args:
        preset_type_or_id: 預設類型（字串如 "dimmer"）或類型編號（整數）
                           或當只提供一個參數時為預設 ID
        preset_id: 預設編號或編號列表（用於多重選擇）
        name: 預設名稱（按名稱選擇時使用）
        end: 結束編號（用於範圍選擇）
        wildcard: 是否使用萬用字元 *（與 name 一起使用）

    Returns:
        str: MA 指令字串

    Examples:
        >>> preset(5)
        'preset 5'
        >>> preset("dimmer", 1)
        'preset 1.1'
        >>> preset(3, 2)
        'preset 3.2'
        >>> preset(name="DarkRed")
        'preset "DarkRed"'
        >>> preset(name="DarkRed", wildcard=True)
        'preset *."DarkRed"'
        >>> preset("color", name="Red")
        'preset "color"."Red"'
        >>> preset(1, 1, end=5)
        'preset 1.1 thru 5'
        >>> preset(1, [1, 3, 5])
        'preset 1.1 + 1.3 + 1.5'
    """
    # Case 1: 僅名稱（可選萬用字元）
    if name is not None and preset_type_or_id is None:
        if wildcard:
            return f'preset *."{name}"'
        return f'preset "{name}"'

    # Case 2: 類型 + 名稱（例如：preset "color"."Red"）
    if name is not None and preset_type_or_id is not None:
        if isinstance(preset_type_or_id, str):
            type_str = f'"{preset_type_or_id}"'
        else:
            type_str = str(preset_type_or_id)
        return f'preset {type_str}."{name}"'

    # Case 3: 僅預設 ID（例如：preset 5）
    if preset_type_or_id is not None and preset_id is None:
        return f"preset {preset_type_or_id}"

    # Case 4: 類型 + ID（例如：preset 3.2 或 preset "dimmer".1）
    if preset_type_or_id is not None and preset_id is not None:
        # 取得類型編號
        if isinstance(preset_type_or_id, str):
            type_num = PRESET_TYPES.get(preset_type_or_id.lower(), 1)
        else:
            type_num = preset_type_or_id

        # 處理多重選擇（列表）
        if isinstance(preset_id, list):
            if len(preset_id) == 1:
                return f"preset {type_num}.{preset_id[0]}"
            presets_str = " + ".join(f"{type_num}.{pid}" for pid in preset_id)
            return f"preset {presets_str}"

        # 處理範圍選擇
        if end is not None:
            return f"preset {type_num}.{preset_id} thru {end}"

        # 單一選擇
        return f"preset {type_num}.{preset_id}"

    raise ValueError("Must provide preset_type_or_id, preset_id, or name")


def preset_type(
    type_id: Optional[Union[int, str]] = None,
    *,
    name: Optional[str] = None,
    feature: Optional[int] = None,
    attribute: Optional[int] = None,
) -> str:
    """
    建構 PresetType 指令以呼叫或選擇預設類型。

    PresetType 可用於：
    - 在燈具表和預設類型欄中呼叫 PresetType
    - 選擇 PresetType 中的 Features 和 Attributes
    - 為選擇的燈具啟用 PresetType

    預設類型包含 features 和 attributes，可以使用點分隔的數字來呼叫。

    Args:
        type_id: PresetType 編號（整數）或變數（例如："$preset"）
        name: PresetType 名稱（例如："Dimmer"、"Color"）
        feature: Feature 編號（可選）
        attribute: Attribute 編號（可選，需要 feature）

    Returns:
        str: MA 指令字串

    Raises:
        ValueError: 當既沒有提供 type_id 也沒有提供 name 時
        ValueError: 當提供 attribute 但沒有提供 feature 時

    Examples:
        >>> preset_type(3)
        'presettype 3'
        >>> preset_type(name="Dimmer")
        'presettype "Dimmer"'
        >>> preset_type(3, feature=1)
        'presettype 3.1'
        >>> preset_type(name="Color", feature=2)
        'presettype "Color".2'
        >>> preset_type(3, feature=2, attribute=1)
        'presettype 3.2.1'
        >>> preset_type("$preset", feature=2)
        'presettype $preset.2'
    """
    # 驗證：不能有 attribute 而沒有 feature
    if attribute is not None and feature is None:
        raise ValueError("Cannot specify attribute without feature")

    # 驗證：必須提供 type_id 或 name
    if type_id is None and name is None:
        raise ValueError("Must provide type_id or name")

    # Case 1: 使用名稱
    if name is not None:
        base = f'presettype "{name}"'
        if feature is not None:
            base = f"{base}.{feature}"
            if attribute is not None:
                base = f"{base}.{attribute}"
        return base

    # Case 2: 使用數字或變數
    base = f"presettype {type_id}"
    if feature is not None:
        base = f"{base}.{feature}"
        if attribute is not None:
            base = f"{base}.{attribute}"
    return base
