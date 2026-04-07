"""
Function Keywords for grandMA2 Command Builder

This module organizes Function Keywords by functionality into multiple submodules:
- store.py: Store-related functions
- selection.py: Selection and clear-related functions
- playback.py: Playback control-related functions
- edit.py: Edit operations (Copy, Move, Delete, Remove)
- assignment.py: Assignment-related functions
- labeling.py: Label and appearance-related functions
- values.py: Value setting functions (At keyword)
- info.py: Information query functions (List, Info)
- macro.py: Macro placeholder-related functions

Function keywords are the "verbs" of the console. They perform a task or
function and are often followed by objects to which the function applies.
Some functions are global and do not need to be followed by objects.

Examples: Store, Delete, Copy, Goto, Clear, Label, SelFix, Go, Pause
"""

# Store Function Keywords
from .store import (
    store,
    store_cue,
    store_group,
    store_preset,
)

# Selection Function Keywords (SelFix, Clear)
from .selection import (
    select_fixture,
    clear,
    clear_selection,
    clear_active,
    clear_all,
)

# Playback Function Keywords (Go, Pause, Goto, GoFast, DefGo)
from .playback import (
    go,
    go_executor,
    go_macro,
    go_back,
    go_back_executor,
    goto,
    go_sequence,
    pause_sequence,
    goto_cue,
    go_fast_back,
    go_fast_forward,
    def_go_back,
    def_go_forward,
    def_go_pause,
)

# Edit Function Keywords (Edit, Cut, Paste, Copy, Move, Delete, Remove)
from .edit import (
    edit,
    cut,
    paste,
    copy,
    copy_cue,
    move,
    delete,
    delete_cue,
    delete_group,
    delete_preset,
    delete_fixture,
    delete_messages,
    remove,
    remove_selection,
    remove_preset_type,
    remove_fixture,
    remove_effect,
)

# Assignment Function Keywords
from .assignment import (
    assign,
    assign_function,
    assign_fade,
    assign_to_layout,
    empty,
    temp_fader,
)

# Labeling Function Keywords (Label, Appearance)
from .labeling import (
    label,
    label_group,
    label_preset,
    appearance,
)

# Values Function Keywords (At)
from .values import (
    at,
    at_full,
    at_zero,
    fixture_at,
    channel_at,
    group_at,
    executor_at,
    preset_type_at,
    attribute_at,
)

# Info Function Keywords (List, Info)
from .info import (
    list_objects,
    list_cue,
    list_group,
    list_preset,
    list_attribute,
    list_messages,
    info,
    info_group,
    info_cue,
    info_preset,
)

# Macro Placeholder Function Keywords
from .macro import (
    macro_with_input_after,
    macro_with_input_before,
)

# Helping Keywords (Plus +, Minus -, And, If)
from .helping import (
    at_relative,
    add_to_selection,
    remove_from_selection,
    page_next,
    page_previous,
    condition_and,
    if_condition,
)

# Park Function Keywords (Park, Unpark)
from .park import (
    park,
    unpark,
)

# Blind & Preview Function Keywords
from .blind import (
    blind,
    blind_edit,
    preview,
    preview_edit,
)

# Blackout & Global State Function Keywords
from .blackout import (
    blackout,
    black,
    freeze,
    highlight,
    full_highlight,
    solo,
)

# Cue Timing Function Keywords
from .cue_timing import (
    delay,
    out_delay,
    fade,
    out_fade,
)

# Fixture Control Function Keywords
from .fixture_control import (
    align,
    all_keyword,
    fix,
    locate,
    next_keyword,
    previous,
    invert,
)

# Executor Control Function Keywords
from .executor_control import (
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
)

# Programmer & Show Data Function Keywords
from .programmer import (
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
)

# Crossfade Function Keywords
from .crossfade import (
    crossfade,
    crossfade_a,
    crossfade_b,
    manual_xfade,
)

# Step Timing Function Keywords
from .step_timing import (
    snap_percent,
    step_fade,
    step_in_fade,
    step_out_fade,
    fade_path,
)

# Flash/Swop Extension Function Keywords
from .flash_swop_ext import (
    flash_go,
    flash_on,
    swop_go,
    swop_on,
    store_look,
)

# Rate & Speed Function Keywords
from .rate_speed import (
    rate,
    rate1,
    double_rate,
    half_rate,
    double_speed,
    half_speed,
    speed,
)

# Intensity & Misc Function Keywords
from .intensity import (
    full,
    to_full,
    zero,
    to_zero,
    load,
    learn,
)

# Call Function Keywords
from .call import (
    call,
)

# Variable Function Keywords
from .variables import (
    set_user_var,
    set_var,
    add_user_var,
    add_var,
)

# Backward Compatibility Aliases
# select_group -> group (from objects.py)
# call_preset -> preset (from objects.py)
from ..objects import group as select_group
from ..objects import preset as call_preset

__all__ = [
    # Store
    "store",
    "store_cue",
    "store_group",
    "store_preset",
    # SelFix
    "select_fixture",
    # Clear
    "clear",
    "clear_selection",
    "clear_active",
    "clear_all",
    # Label
    "label",
    "label_group",
    "label_preset",
    # Delete
    "delete",
    "delete_cue",
    "delete_group",
    "delete_preset",
    "delete_fixture",
    "delete_messages",
    # Remove
    "remove",
    "remove_selection",
    "remove_preset_type",
    "remove_fixture",
    "remove_effect",
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
    # GoFast
    "go_fast_back",
    "go_fast_forward",
    # DefGo (Selected Executor)
    "def_go_back",
    "def_go_forward",
    "def_go_pause",
    # Edit
    "edit",
    # Cut
    "cut",
    # Paste
    "paste",
    # Copy
    "copy",
    "copy_cue",
    # Move
    "move",
    # Assign
    "assign",
    "assign_function",
    "assign_fade",
    "assign_to_layout",
    "empty",
    "temp_fader",
    # Appearance
    "appearance",
    # At
    "at",
    "at_full",
    "at_zero",
    "fixture_at",
    "channel_at",
    "group_at",
    "executor_at",
    "preset_type_at",
    "attribute_at",
    # List
    "list_objects",
    "list_cue",
    "list_group",
    "list_preset",
    "list_attribute",
    "list_messages",
    # Info
    "info",
    "info_group",
    "info_cue",
    "info_preset",
    # Macro Placeholder
    "macro_with_input_after",
    "macro_with_input_before",
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
    # Backward Compatibility Aliases
    "select_group",
    "call_preset",
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
]
