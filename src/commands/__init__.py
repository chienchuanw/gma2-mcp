"""
Command Builder Module for grandMA2

This module provides high-level functions to construct grandMA2 command strings.
These functions are responsible only for generating correctly formatted commands,
not for sending them.

According to coding-standards.md, these functions are "thin wrappers" that
only construct MA commands without any Telnet logic.

=============================================================================
grandMA2 Keyword Classification
=============================================================================

The grandMA2 command line syntax follows these general rules:
- Basic syntax: [Function] [Object]
- All objects have a default function which is used if no function is given.
- Most functions have a default object or object type.
- Objects are arranged in a hierarchical tree structure.

Keywords are classified into three types:

1. HELPING KEYWORDS (Prepositions/Conjunctions)
   - Used to create relations between functions and objects
   - Examples: At, Thru, +, If, While

2. OBJECT KEYWORDS (Nouns)
   - Used to allocate objects in your show file
   - Usually used with numbers, IDs, names, and labels
   - Examples: Fixture, Channel, Group, Preset, Cue, Sequence, Executor

3. FUNCTION KEYWORDS (Verbs)
   - Perform a task or function
   - Often followed by objects to which the function applies
   - Some functions are global and don't need objects (e.g., Blackout)
   - Examples: Store, Delete, Copy, Goto, Clear, Label, SelFix

=============================================================================
"""

# Constants
from .constants import (
    PRESET_TYPES,
    STORE_BOOL_OPTIONS,
    STORE_FLAG_OPTIONS,
    STORE_VALUE_OPTIONS,
)

# Object Keywords
from .objects import (
    channel,
    cue,
    fixture,
    group,
    preset,
    sequence,
)

# Function Keywords
from .functions import (
    # At Function Keyword
    at,
    at_full,
    at_zero,
    attribute_at,
    channel_at,
    executor_at,
    fixture_at,
    group_at,
    preset_type_at,
    # Copy Function Keyword
    copy,
    copy_cue,
    # Move Function Keyword
    move,
    # Macro Placeholder
    macro_with_input_after,
    macro_with_input_before,
    # Other Function Keywords
    call_preset,
    clear,
    clear_active,
    clear_all,
    clear_selection,
    delete_group,
    go_sequence,
    goto_cue,
    label_group,
    label_preset,
    pause_sequence,
    select_fixture,
    select_group,
    store,
    store_cue,
    store_group,
    store_preset,
)

__all__ = [
    # Constants
    "PRESET_TYPES",
    "STORE_FLAG_OPTIONS",
    "STORE_BOOL_OPTIONS",
    "STORE_VALUE_OPTIONS",
    # Object Keywords
    "fixture",
    "channel",
    "group",
    "preset",
    "cue",
    "sequence",
    # At Function Keyword
    "at",
    "at_full",
    "at_zero",
    "attribute_at",
    "fixture_at",
    "channel_at",
    "group_at",
    "executor_at",
    "preset_type_at",
    # Copy Function Keyword
    "copy",
    "copy_cue",
    # Move Function Keyword
    "move",
    # Macro Placeholder (@ Character)
    "macro_with_input_after",
    "macro_with_input_before",
    # Other Function Keywords
    "store",
    "store_cue",
    "store_group",
    "store_preset",
    "select_fixture",
    "clear",
    "clear_selection",
    "clear_active",
    "clear_all",
    "label_group",
    "label_preset",
    "delete_group",
    "go_sequence",
    "pause_sequence",
    "goto_cue",
    # Backward Compatibility Aliases
    "select_group",
    "call_preset",
]
