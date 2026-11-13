"""
Preset Object Keywords for grandMA2 Command Builder

Contains Object Keywords related to presets:
- preset: Select presets (bare ``preset x.y``)
- at_preset: Apply a preset to the selection (``at preset x.y``)
- preset_type: Call or select preset types

Preset Types mapping:
- dimmer=1, color=2, gobo=3, beam=4, focus=5, control=6, shapers=7, video=8
"""

from ..constants import PRESET_TYPES


def preset(
    preset_type_or_id: int | str | None = None,
    preset_id: int | list[int] | None = None,
    *,
    name: str | None = None,
    end: int | None = None,
    wildcard: bool = False,
) -> str:
    """
    Construct a Preset command to select or apply presets.

    Preset can be used to:
    - Select fixtures stored in a preset
    - Apply a preset to currently selected fixtures or channels

    The manual says the default function is SelFix with no selection and At
    with a selection. Over telnet on 3.9.60 the bare form does NOT apply the
    preset to a selection -- it fails silently (#92). To apply a preset, use
    ``at_preset()``.

    Args:
        preset_type_or_id: Preset type (string like "dimmer") or type number (integer)
                           or preset ID when only one parameter is provided
        preset_id: Preset number or list of numbers (for multiple selection)
        name: Preset name (used when selecting by name)
        end: End number (for range selection)
        wildcard: Whether to use wildcard * (used with name)

    Returns:
        str: MA command string

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
    # Case 1: Name only (optional wildcard)
    if name is not None and preset_type_or_id is None:
        if wildcard:
            return f'preset *."{name}"'
        return f'preset "{name}"'

    # Case 2: Type + Name (e.g., preset "color"."Red")
    if name is not None and preset_type_or_id is not None:
        if isinstance(preset_type_or_id, str):
            type_str = f'"{preset_type_or_id}"'
        else:
            type_str = str(preset_type_or_id)
        return f'preset {type_str}."{name}"'

    # Case 3: Preset ID only (e.g., preset 5)
    if preset_type_or_id is not None and preset_id is None:
        return f"preset {preset_type_or_id}"

    # Case 4: Type + ID (e.g., preset 3.2 or preset "dimmer".1)
    if preset_type_or_id is not None and preset_id is not None:
        # Get type number
        if isinstance(preset_type_or_id, str):
            type_num = PRESET_TYPES.get(preset_type_or_id.lower(), 1)
        else:
            type_num = preset_type_or_id

        # Handle multiple selection (list)
        if isinstance(preset_id, list):
            if len(preset_id) == 1:
                return f"preset {type_num}.{preset_id[0]}"
            presets_str = " + ".join(f"{type_num}.{pid}" for pid in preset_id)
            return f"preset {presets_str}"

        # Handle range selection
        if end is not None:
            return f"preset {type_num}.{preset_id} thru {end}"

        # Single selection
        return f"preset {type_num}.{preset_id}"

    raise ValueError("Must provide preset_type_or_id, preset_id, or name")


def at_preset(preset_type: int | str, preset_id: int) -> str:
    """
    Construct an At Preset command to apply a preset to the current selection.

    Always use this (not the bare ``preset()``) to apply: the bare form fails
    silently over telnet on 3.9.60 (#92). ``At Preset 3.2`` is also the
    manual's own example for applying a preset.

    Args:
        preset_type: Preset type name (e.g. "color") or type number
        preset_id: Preset number

    Returns:
        str: MA command string

    Examples:
        >>> at_preset("color", 3)
        'at preset 4.3'
        >>> at_preset(2, 11)
        'at preset 2.11'
    """
    return f"at {preset(preset_type, preset_id)}"


def preset_type(
    type_id: int | str | None = None,
    *,
    name: str | None = None,
    feature: int | None = None,
    attribute: int | None = None,
) -> str:
    """
    Construct a PresetType command to call or select preset types.

    PresetType can be used to:
    - Call PresetType in fixture sheet and preset type columns
    - Select Features and Attributes in PresetType
    - Enable PresetType for selected fixtures

    Preset types contain features and attributes, which can be called using dot-separated numbers.

    Args:
        type_id: PresetType number (integer) or variable (e.g., "$preset")
        name: PresetType name (e.g., "Dimmer", "Color")
        feature: Feature number (optional)
        attribute: Attribute number (optional, requires feature)

    Returns:
        str: MA command string

    Raises:
        ValueError: When neither type_id nor name is provided
        ValueError: When attribute is provided without feature

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
    # Validation: cannot have attribute without feature
    if attribute is not None and feature is None:
        raise ValueError("Cannot specify attribute without feature")

    # Validation: must provide type_id or name
    if type_id is None and name is None:
        raise ValueError("Must provide type_id or name")

    # Case 1: Using name
    if name is not None:
        base = f'presettype "{name}"'
        if feature is not None:
            base = f"{base}.{feature}"
            if attribute is not None:
                base = f"{base}.{attribute}"
        return base

    # Case 2: Using number or variable
    base = f"presettype {type_id}"
    if feature is not None:
        base = f"{base}.{feature}"
        if attribute is not None:
            base = f"{base}.{attribute}"
    return base
