"""
Object Keywords for grandMA2 Command Builder

此模組包含所有 grandMA2 Object Keywords 的實作。
Object Keywords 是 grandMA2 指令語法中的「名詞」，用於指定操作的對象。

根據 grandMA2 User Manual 第 10.1.2 節的分類，Object Keywords 分為以下類別：

Fixture/Channel 相關：
- fixture: 使用 Fixture ID 存取燈具
- channel: 使用 Channel ID 存取燈具

Group/Selection 相關：
- group: 選擇燈具群組

Preset 相關：
- preset: 選擇或套用預設
- preset_type: 呼叫或選擇預設類型

Cue/Sequence 相關：
- cue: 參照 cue
- cue_part: 參照 cue part
- sequence: 參照 sequence

Executor 相關：
- executor: 參照 executor

Layout/View 相關：
- layout: 選擇 layout

DMX 相關：
- dmx: 參照 DMX 位址
- dmx_universe: 參照 DMX universe

Time 相關：
- timecode: 參照 timecode show
- timecode_slot: 參照 timecode slot
- timer: 參照 timer
"""

# Fixture/Channel 相關
from .fixtures import channel, fixture

# Group/Selection 相關
from .groups import group

# Preset 相關
from .presets import preset, preset_type

# Cue/Sequence 相關
from .cues import cue, cue_part, sequence

# Executor 相關
from .executors import executor

# Layout/View 相關
from .layouts import layout

# DMX 相關
from .dmx import dmx, dmx_universe

# Time 相關
from .time import timecode, timecode_slot, timer

__all__ = [
    # Fixture/Channel
    "fixture",
    "channel",
    # Group/Selection
    "group",
    # Preset
    "preset",
    "preset_type",
    # Cue/Sequence
    "cue",
    "cue_part",
    "sequence",
    # Executor
    "executor",
    # Layout/View
    "layout",
    # DMX
    "dmx",
    "dmx_universe",
    # Time
    "timecode",
    "timecode_slot",
    "timer",
]

