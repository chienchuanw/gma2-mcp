"""
Object Keywords for grandMA2 Command Builder

This module contains implementations of all grandMA2 Object Keywords.
Object Keywords are "nouns" in grandMA2 command syntax used to specify the objects to operate on.

According to the classification in grandMA2 User Manual section 10.1.2, Object Keywords are divided into:

Fixture/Channel related:
- fixture: Access fixtures using Fixture ID
- channel: Access fixtures using Channel ID

Group/Selection related:
- group: Select fixture groups

Preset related:
- preset: Select or apply presets
- preset_type: Call or select preset types

Cue/Sequence related:
- cue: Reference cues
- cue_part: Reference cue parts
- sequence: Reference sequences

Executor related:
- executor: Reference executors

Layout/View related:
- layout: Select layouts

DMX related:
- dmx: Reference DMX addresses
- dmx_universe: Reference DMX universes

Time related:
- timecode: Reference timecode shows
- timecode_slot: Reference timecode slots
- timer: Reference timers
"""

# Fixture/Channel related
from .fixtures import channel, fixture

# Group/Selection related
from .groups import group

# Preset related
from .presets import preset, preset_type

# Attribute/Feature related
from .attributes import attribute, feature

# Cue/Sequence related
from .cues import cue, cue_part, sequence

# Executor related
from .executors import executor

# Executor Object Keywords
from .executor_objects import (
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
)

# Misc Object Keywords
from .misc_objects import (
    camera,
    channel_link,
    filter_keyword,
    fixture_type,
    form,
    gel,
    image,
    item_3d,
    layer,
    macro,
    mask,
    master,
    master_fade,
    media_server,
    menu,
    message,
    messages,
    model,
    plugin,
    pm_area,
    profile,
    protocol,
    root,
    screen,
    search_result,
    selection,
    special_master,
    surface,
    user,
    user_profile,
    value_keyword,
    view,
    view_button,
    view_page,
    world,
)

# Layout/View related
from .layouts import layout

# DMX related
from .dmx import dmx, dmx_universe

# Time related
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
    # Attribute/Feature
    "attribute",
    "feature",
    # Cue/Sequence
    "cue",
    "cue_part",
    "sequence",
    # Executor
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
    # Misc Object Keywords
    "camera",
    "channel_link",
    "filter_keyword",
    "fixture_type",
    "form",
    "gel",
    "image",
    "item_3d",
    "layer",
    "macro",
    "mask",
    "master",
    "master_fade",
    "media_server",
    "menu",
    "message",
    "messages",
    "model",
    "plugin",
    "pm_area",
    "profile",
    "protocol",
    "root",
    "screen",
    "search_result",
    "selection",
    "special_master",
    "surface",
    "user",
    "user_profile",
    "value_keyword",
    "view",
    "view_button",
    "view_page",
    "world",
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
