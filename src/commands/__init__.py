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
    attribute,
    channel,
    cue,
    cue_part,
    dmx,
    dmx_universe,
    executor,
    # Executor Object Keywords
    fader,
    fader_page,
    button_page,
    channel_fader,
    channel_page,
    exec_button_1,
    exec_button_2,
    exec_button_3,
    all_button_executors,
    all_chase_executors,
    all_fader_executors,
    all_seq_executors,
    feature,
    fixture,
    group,
    layout,
    preset,
    preset_type,
    sequence,
    timecode,
    timecode_slot,
    timer,
)

# Function Keywords
from .functions import (
    # Assign Function Keyword
    assign,
    assign_fade,
    assign_function,
    assign_to_layout,
    empty,
    temp_fader,
    # Label Function Keyword
    label,
    # Appearance Function Keyword
    appearance,
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
    # Edit Function Keyword
    edit,
    # Cut Function Keyword
    cut,
    # Paste Function Keyword
    paste,
    # Copy Function Keyword
    copy,
    copy_cue,
    # Move Function Keyword
    move,
    # Delete Function Keyword
    delete,
    delete_cue,
    delete_fixture,
    delete_group,
    delete_messages,
    delete_preset,
    # Remove Function Keyword
    remove,
    remove_effect,
    remove_fixture,
    remove_preset_type,
    remove_selection,
    # List Function Keyword
    list_objects,
    list_attribute,
    list_cue,
    list_group,
    list_messages,
    list_preset,
    # Info Function Keyword
    info,
    info_cue,
    info_group,
    info_preset,
    # Macro Placeholder
    macro_with_input_after,
    macro_with_input_before,
    # Helping Keywords (Plus +, Minus -, And, If)
    add_to_selection,
    at_relative,
    condition_and,
    if_condition,
    page_next,
    page_previous,
    remove_from_selection,
    # Park Function Keywords
    park,
    unpark,
    # Call Function Keywords
    call,
    # Variable Function Keywords
    set_user_var,
    set_var,
    add_user_var,
    add_var,
    # Blind & Preview Function Keywords
    blind,
    blind_edit,
    preview,
    preview_edit,
    # Blackout & Global State Function Keywords
    blackout,
    black,
    freeze,
    highlight,
    full_highlight,
    solo,
    # Cue Timing Function Keywords
    delay,
    out_delay,
    fade,
    out_fade,
    # Fixture Control Function Keywords
    align,
    all_keyword,
    fix,
    locate,
    next_keyword,
    previous,
    invert,
    # Executor Control Function Keywords
    off,
    on,
    kill,
    flash,
    swop,
    stomp,
    temp,
    toggle,
    release,
    top,
    select,
    # Programmer & Show Data Function Keywords
    block,
    unblock,
    clone,
    default,
    extract,
    insert,
    record,
    replace,
    update,
    oops,
    # Intensity & Misc Function Keywords
    full,
    to_full,
    zero,
    to_zero,
    load,
    learn,
    # Crossfade Function Keywords
    crossfade,
    crossfade_a,
    crossfade_b,
    manual_xfade,
    # Rate & Speed Function Keywords
    rate,
    rate1,
    double_rate,
    half_rate,
    double_speed,
    half_speed,
    speed,
    # Step Timing Function Keywords
    snap_percent,
    step_fade,
    step_in_fade,
    step_out_fade,
    fade_path,
    # Flash/Swop Extension Function Keywords
    flash_go,
    flash_on,
    swop_go,
    swop_on,
    store_look,
    # Other Function Keywords
    call_preset,
    clear,
    clear_active,
    clear_all,
    clear_selection,
    def_go_back,
    def_go_forward,
    def_go_pause,
    go,
    go_back,
    go_back_executor,
    go_executor,
    go_fast_back,
    go_fast_forward,
    go_macro,
    go_sequence,
    goto,
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
    "attribute",
    "feature",
    "fixture",
    "channel",
    "group",
    "layout",
    "preset",
    "preset_type",
    "cue",
    "cue_part",
    "sequence",
    "executor",
    # Executor Object Keywords
    "fader",
    "fader_page",
    "button_page",
    "channel_fader",
    "channel_page",
    "exec_button_1",
    "exec_button_2",
    "exec_button_3",
    "all_button_executors",
    "all_chase_executors",
    "all_fader_executors",
    "all_seq_executors",
    "dmx",
    "dmx_universe",
    "timecode",
    "timecode_slot",
    "timer",
    # Assign Function Keyword
    "assign",
    "assign_fade",
    "assign_function",
    "assign_to_layout",
    "empty",
    "temp_fader",
    # Label Function Keyword
    "label",
    # Appearance Function Keyword
    "appearance",
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
    # Edit Function Keyword
    "edit",
    # Cut Function Keyword
    "cut",
    # Paste Function Keyword
    "paste",
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
    # Delete Function Keyword
    "delete",
    "delete_cue",
    "delete_fixture",
    "delete_group",
    "delete_messages",
    "delete_preset",
    # Remove Function Keyword
    "remove",
    "remove_effect",
    "remove_fixture",
    "remove_preset_type",
    "remove_selection",
    # List Function Keyword
    "list_objects",
    "list_attribute",
    "list_cue",
    "list_group",
    "list_messages",
    "list_preset",
    # Info Function Keyword
    "info",
    "info_cue",
    "info_group",
    "info_preset",
    # Go
    "go",
    "go_executor",
    "go_macro",
    # GoBack
    "go_back",
    "go_back_executor",
    # Goto
    "goto",
    # Go/Pause/Goto (Legacy)
    "go_sequence",
    "pause_sequence",
    "goto_cue",
    # GoFast (<<< and >>>)
    "go_fast_back",
    "go_fast_forward",
    # DefGo (Selected Executor)
    "def_go_back",
    "def_go_forward",
    "def_go_pause",
    # Helping Keywords (Plus +, Minus -, And, If)
    "at_relative",
    "add_to_selection",
    "remove_from_selection",
    "page_next",
    "page_previous",
    "condition_and",
    "if_condition",
    # Park Function Keywords
    "park",
    "unpark",
    # Call Function Keywords
    "call",
    # Variable Function Keywords
    "set_user_var",
    "set_var",
    "add_user_var",
    "add_var",
    # Blind & Preview Function Keywords
    "blind",
    "blind_edit",
    "preview",
    "preview_edit",
    # Blackout & Global State Function Keywords
    "blackout",
    "black",
    "freeze",
    "highlight",
    "full_highlight",
    "solo",
    # Cue Timing Function Keywords
    "delay",
    "out_delay",
    "fade",
    "out_fade",
    # Fixture Control Function Keywords
    "align",
    "all_keyword",
    "fix",
    "locate",
    "next_keyword",
    "previous",
    "invert",
    # Executor Control Function Keywords
    "off",
    "on",
    "kill",
    "flash",
    "swop",
    "stomp",
    "temp",
    "toggle",
    "release",
    "top",
    "select",
    # Programmer & Show Data Function Keywords
    "block",
    "unblock",
    "clone",
    "default",
    "extract",
    "insert",
    "record",
    "replace",
    "update",
    "oops",
    # Intensity & Misc Function Keywords
    "full",
    "to_full",
    "zero",
    "to_zero",
    "load",
    "learn",
    # Crossfade Function Keywords
    "crossfade",
    "crossfade_a",
    "crossfade_b",
    "manual_xfade",
    # Rate & Speed Function Keywords
    "rate",
    "rate1",
    "double_rate",
    "half_rate",
    "double_speed",
    "half_speed",
    "speed",
    # Step Timing Function Keywords
    "snap_percent",
    "step_fade",
    "step_in_fade",
    "step_out_fade",
    "fade_path",
    # Flash/Swop Extension Function Keywords
    "flash_go",
    "flash_on",
    "swop_go",
    "swop_on",
    "store_look",
    # Backward Compatibility Aliases
    "select_group",
    "call_preset",
]
