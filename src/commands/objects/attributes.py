"""
Attribute and Feature Object Keywords for grandMA2 Command Builder

This module contains Attribute and Feature object keywords.

Attribute:
- Object type used as reference to fixture attributes
- Can be called by name (string) or number
- Organized by Features, which are organized by PresetType
- Shortcut: Att

Feature:
- Container for related attributes
- Can use dot notation to access specific attribute
- Organized under PresetType

Included functions:
- attribute: Reference fixture attributes by name or number
- feature: Reference feature groups with optional attribute
"""

from typing import Optional, Union


def attribute(attr_id: Union[int, str]) -> str:
    """
    Construct an Attribute command to reference fixture attributes.

    Attribute is an object type used as reference to fixture attributes.
    The default function is Call - calling attributes will bring them to
    the encoder and select them in the fixture sheet (blue column header).

    Note: Press Preset twice on the console to enter Attribute keyword.
    Note: Attribute numbers may change when fixtures are added.
          Use unique attribute library names in macros for stability.
    Tip: Type "List Attribute" to see all attributes with names and numbers.

    Args:
        attr_id: Attribute name (string) or number (integer).
                 String names are automatically quoted.

    Returns:
        str: MA command to reference the attribute

    Examples:
        >>> attribute("pan")
        'attribute "pan"'
        >>> attribute("tilt")
        'attribute "tilt"'
        >>> attribute(1)
        'attribute 1'
        >>> attribute(5)
        'attribute 5'
    """
    if isinstance(attr_id, str):
        return f'attribute "{attr_id}"'
    return f"attribute {attr_id}"


def feature(
    feature_id: Union[int, str],
    attr_num: Optional[int] = None,
) -> str:
    """
    Construct a Feature command to reference feature groups.

    Feature is a container for related attributes. Attributes are
    organized by Features, which in turn are organized by PresetType.
    You can use dot notation to access specific attributes within a feature.

    Args:
        feature_id: Feature number or variable (e.g., "$feature")
        attr_num: Optional attribute number within the feature.
                  If provided, uses dot notation (e.g., "feature 3.1")

    Returns:
        str: MA command to reference the feature (with optional attribute)

    Examples:
        >>> feature(3)
        'feature 3'
        >>> feature(3, 1)
        'feature 3.1'
        >>> feature(2, 5)
        'feature 2.5'
        >>> feature("$feature", 1)
        'feature $feature.1'
    """
    if attr_num is not None:
        return f"feature {feature_id}.{attr_num}"
    return f"feature {feature_id}"

