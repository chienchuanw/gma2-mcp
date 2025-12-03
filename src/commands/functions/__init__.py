"""
Function Keywords for grandMA2 Command Builder

此模組將 Function Keywords 按照功能分類拆解為多個子模組：
- store.py: Store 相關函數
- selection.py: 選擇與清除相關函數
- playback.py: 播放控制相關函數
- edit.py: 編輯操作（Copy, Move, Delete, Remove）
- assignment.py: 指派相關函數
- labeling.py: 標籤與外觀相關函數
- values.py: 數值設定相關函數（At keyword）
- info.py: 資訊查詢相關函數（List, Info）
- macro.py: 巨集佔位符相關函數

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

# Playback Function Keywords (Go, Pause, Goto, GoFast)
from .playback import (
    go_sequence,
    pause_sequence,
    goto_cue,
    go_fast_back,
    go_fast_forward,
)

# Edit Function Keywords (Copy, Move, Delete, Remove)
from .edit import (
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
    # Go/Pause/Goto
    "go_sequence",
    "pause_sequence",
    "goto_cue",
    # GoFast
    "go_fast_back",
    "go_fast_forward",
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
    # Backward Compatibility Aliases
    "select_group",
    "call_preset",
]
