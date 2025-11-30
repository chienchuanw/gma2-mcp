"""
Constants for grandMA2 Command Builder

This module contains all constants used by the command builder,
including preset type mappings and store option classifications.
"""

# ============================================================================
# PRESET TYPE MAPPINGS
# ============================================================================
# grandMA2 uses numbers to distinguish preset types.
# These mappings convert human-readable names to numeric IDs.

PRESET_TYPES = {
    "dimmer": 1,
    "position": 2,
    "gobo": 3,
    "color": 2,  # color also uses preset type 2
    "beam": 4,
    "focus": 5,
    "control": 6,
    "shapers": 7,
    "video": 8,
}


# ============================================================================
# STORE OPTION CLASSIFICATIONS
# ============================================================================
# Store options are classified into three types based on their value format.

# Store options that require no value (flag-only options)
# Usage: /merge, /overwrite, /noconfirm
STORE_FLAG_OPTIONS = {
    "merge",
    "overwrite",
    "remove",
    "noconfirm",
    "global",
    "selective",
    "universal",
    "auto",
    "trackingshield",
    "embedded",
}

# Store options that require a boolean value
# Usage: /cueonly=true, /tracking=false
STORE_BOOL_OPTIONS = {
    "cueonly",
    "tracking",
    "keepactive",
    "presetfilter",
    "addnewcontent",
    "originalcontent",
    "effects",
    "values",
    "valuetimes",
}

# Store options that require a specific value
# Usage: /source=output, /screen=1
STORE_VALUE_OPTIONS = {
    "source",  # Prog, Output, DmxIn
    "useselection",  # Active, Allforselected, Activeforselected, All, Look
    "screen",  # 1..6
    "x",  # x coordinate
    "y",  # y coordinate
}

