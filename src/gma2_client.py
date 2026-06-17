"""
High-level grandMA2 client for workflow-level operations.

GMA2Client composes command builder functions and the telnet client
to provide multi-step lighting workflows as single method calls.

Example:
    >>> async with GMA2Client.create("192.168.1.100") as client:
    ...     await client.build_cue_list(1, [
    ...         {"id": 1, "name": "Preset"},
    ...         {"id": 2, "name": "Look 1", "fade": 3.0},
    ...     ])
"""

from __future__ import annotations

import logging
from typing import Any

from src.telnet_client import GMA2TelnetClient
from src.commands.functions.timecode import (
    store_timecode,
    assign_timecode_param,
)
from src.commands.functions.matricks import (
    matricks as _matricks,
    matricks_blocks,
    matricks_wings,
    matricks_groups,
    matricks_interleave,
    matricks_filter,
)
from src.commands.constants import PRESET_TYPES
# Aliased so build_color_palette can call them without its label/appearance
# bool parameters shadowing the builders.
from src.commands import appearance as appearance_cmd, label as label_cmd
from src.commands import (
    appearance,
    attribute_at,
    store_preset,
    assign,
    assign_cue_cmd,
    assign_fade,
    assign_macro_cmd,
    at,
    effect as cmd_effect,
    effect_bpm,
    effect_form as cmd_effect_form,
    effect_high,
    effect_low,
    executor_at,
    fixture_at,
    label,
    label_macro as cmd_label_macro,
    label_sequence_cue,
    preset,
    select_fixture,
    store,
    store_cue,
    store_group,
    store_macro as cmd_store_macro,
)

logger = logging.getLogger(__name__)


def _color_swatch(r: int, g: int, b: int, w: int) -> tuple[int, int, int]:
    """Derive a pool appearance swatch (0-100 RGB) from an RGBW color.

    The white channel lifts all three components toward white; a fully-off color
    gets a small floor so the pool button stays visible.
    """
    def lift(v: int) -> int:
        return min(100, round(v + w))

    sr, sg, sb = lift(r), lift(g), lift(b)
    if max(sr, sg, sb) < 8:
        sr = sg = sb = 8
    return sr, sg, sb


class GMA2Client:
    """Orchestration layer over GMA2TelnetClient + command builders."""

    def __init__(self, telnet_client: GMA2TelnetClient) -> None:
        self._client = telnet_client

    @classmethod
    async def create(
        cls,
        host: str,
        port: int = 30000,
        user: str = "administrator",
        password: str = "admin",
    ) -> GMA2Client:
        """Create a connected GMA2Client instance."""
        telnet = GMA2TelnetClient(host=host, port=port, user=user, password=password)
        await telnet.connect()
        await telnet.login()
        return cls(telnet)

    async def __aenter__(self) -> GMA2Client:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._client.disconnect()

    async def _send(self, cmd: str) -> str:
        await self._client.send_command(cmd)
        return cmd

    async def build_cue_list(
        self,
        sequence_id: int,
        cues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Create a sequence of cues from cue definitions.

        Each cue dict may contain:
            id (int): Cue number (required)
            name (str): Optional cue label
            fade (float): Optional fade time in seconds

        Args:
            sequence_id: Sequence to store cues into
            cues: List of cue definition dicts

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for cue_def in cues:
            cue_id = cue_def["id"]
            name = cue_def.get("name")
            sent.append(await self._send(store_cue(cue_id, name=name)))

            if "fade" in cue_def:
                sent.append(await self._send(assign_fade(cue_def["fade"], cue_id)))

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Built {len(cues)} cues in Sequence {sequence_id}",
        }

    async def setup_group_with_preset(
        self,
        fixtures: tuple[int, int],
        group_id: int,
        group_name: str,
        preset_type: str,
        preset_id: int,
    ) -> dict[str, Any]:
        """
        Select fixtures, store as named group, and apply a preset.

        Args:
            fixtures: (start, end) fixture range
            group_id: Group number to store
            group_name: Label for the group
            preset_type: Preset type (dimmer, color, position, etc.)
            preset_id: Preset number to apply

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        start, end = fixtures
        sent: list[str] = []

        sent.append(await self._send(select_fixture(start, end)))
        sent.append(await self._send(store_group(group_id, name=group_name)))
        sent.append(await self._send(preset(preset_type, preset_id)))

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f'Created Group {group_id} "{group_name}" (Fixtures {start}-{end}) with {preset_type} preset {preset_id}',
        }

    async def quick_look(
        self,
        fixtures: tuple[int, int],
        value: int,
        store_as_cue: int | None = None,
    ) -> dict[str, Any]:
        """
        Select fixtures, set to a value, and optionally store as a cue.

        Args:
            fixtures: (start, end) fixture range
            value: Dimmer value (0-100)
            store_as_cue: If provided, store the look as this cue number

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        start, end = fixtures
        sent: list[str] = []

        sent.append(await self._send(select_fixture(start, end)))
        sent.append(await self._send(at(value)))

        if store_as_cue is not None:
            sent.append(await self._send(store_cue(store_as_cue)))

        summary = f"Fixtures {start}-{end} at {value}%"
        if store_as_cue is not None:
            summary += f", stored as Cue {store_as_cue}"

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": summary,
        }

    async def assign_sequences_to_executors(
        self,
        assignments: list[tuple[int, int]],
    ) -> dict[str, Any]:
        """
        Assign multiple sequences to executors.

        Args:
            assignments: List of (sequence_id, executor_id) pairs

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for seq_id, exec_id in assignments:
            sent.append(
                await self._send(assign("sequence", seq_id, "executor", exec_id))
            )

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Assigned {len(assignments)} sequences to executors",
        }

    async def store_cue_across_sequences(
        self,
        cue_id: int | float,
        sequence_start: int,
        sequence_end: int,
        cue_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Store a cue across a range of sequences.

        Args:
            cue_id: Cue number to store
            sequence_start: First sequence number
            sequence_end: Last sequence number (inclusive)
            cue_name: Optional name for the cue

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for seq in range(sequence_start, sequence_end + 1):
            cmd = store("sequence", f"{seq} cue {cue_id}", name=cue_name)
            sent.append(await self._send(cmd))

        count = sequence_end - sequence_start + 1
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Stored cue {cue_id} across {count} sequences ({sequence_start}-{sequence_end})",
        }

    async def label_cue_across_sequences(
        self,
        cue_id: int | float,
        sequence_start: int,
        sequence_end: int,
        label: str,
    ) -> dict[str, Any]:
        """
        Label a cue across a range of sequences.

        Args:
            cue_id: Cue number to label
            sequence_start: First sequence number
            sequence_end: Last sequence number (inclusive)
            label: Label to assign

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for seq in range(sequence_start, sequence_end + 1):
            cmd = label_sequence_cue(seq, cue_id, label)
            sent.append(await self._send(cmd))

        count = sequence_end - sequence_start + 1
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Labeled cue {cue_id} across {count} sequences ({sequence_start}-{sequence_end})",
        }

    async def appearance_cue_across_sequences(
        self,
        cue_id: int | float,
        sequence_start: int,
        sequence_end: int,
        **color_kwargs: Any,
    ) -> dict[str, Any]:
        """
        Set appearance on a cue across a range of sequences.

        Args:
            cue_id: Cue number
            sequence_start: First sequence number
            sequence_end: Last sequence number (inclusive)
            **color_kwargs: Color arguments passed to appearance builder
                (red, green, blue, hue, saturation, brightness, color)

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for seq in range(sequence_start, sequence_end + 1):
            cmd = appearance(
                f"sequence {seq} cue", str(cue_id), **color_kwargs
            )
            sent.append(await self._send(cmd))

        count = sequence_end - sequence_start + 1
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Set appearance on cue {cue_id} across {count} sequences ({sequence_start}-{sequence_end})",
        }

    async def clone_fixtures(
        self,
        source_fixture: int,
        target_fixture: int,
        source_end: int | None = None,
        target_end: int | None = None,
        mode: str = "default",
    ) -> dict[str, Any]:
        """
        Clone programming from one fixture (range) to another.

        Args:
            source_fixture: Source fixture ID (or start of range)
            target_fixture: Target fixture ID (or start of range)
            source_end: End of source fixture range (optional)
            target_end: End of target fixture range (optional)
            mode: Clone mode — "default", "overwrite", or "merge"

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        source = f"fixture {source_fixture}"
        if source_end is not None:
            source += f" thru {source_end}"

        target = f"fixture {target_fixture}"
        if target_end is not None:
            target += f" thru {target_end}"

        cmd = f"clone {source} at {target}"
        if mode == "overwrite":
            cmd += " /overwrite"
        elif mode == "merge":
            cmd += " /merge"
        cmd += " /noconfirm"

        sent.append(await self._send(cmd))

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Cloned {source} to {target} (mode: {mode})",
        }

    async def setup_effect_on_group(
        self,
        group_id: int,
        effect_id: int,
        bpm: int | float | None = None,
        form: str | int | None = None,
        high: int | float | None = None,
        low: int | float | None = None,
    ) -> dict[str, Any]:
        """
        Select a group and apply an effect with optional parameters.

        Args:
            group_id: Group to select
            effect_id: Effect to apply from the effect pool
            bpm: Optional effect speed in BPM
            form: Optional waveform (name or number)
            high: Optional effect high value
            low: Optional effect low value

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        sent.append(await self._send(f"group {group_id}"))
        sent.append(await self._send(cmd_effect(effect_id)))

        if bpm is not None:
            sent.append(await self._send(effect_bpm(bpm)))
        if form is not None:
            sent.append(await self._send(cmd_effect_form(form)))
        if high is not None:
            sent.append(await self._send(effect_high(high)))
        if low is not None:
            sent.append(await self._send(effect_low(low)))

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Applied Effect {effect_id} to Group {group_id}",
        }

    async def setup_executor_page(
        self,
        page: int,
        assignments: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Set up a full executor page with sequences, labels, and fader levels.

        Each assignment dict may contain:
            executor_id (int): Executor number (required)
            sequence_id (int): Sequence to assign (required)
            label (str): Optional label for the executor
            fader_level (int): Optional fader level (0-100)

        Args:
            page: Executor page number
            assignments: List of assignment dicts

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for entry in assignments:
            exec_id = entry["executor_id"]
            seq_id = entry["sequence_id"]
            # Use page-qualified executor addressing: Executor [Page].[ID]
            page_exec = f"{page}.{exec_id}"

            sent.append(
                await self._send(
                    assign("sequence", seq_id, "executor", page_exec)
                )
            )

            if "label" in entry:
                sent.append(
                    await self._send(label("executor", page_exec, entry["label"]))
                )

            if "fader_level" in entry:
                sent.append(
                    await self._send(executor_at(page_exec, entry["fader_level"]))
                )

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Set up {len(assignments)} executors on Page {page}",
        }

    async def batch_label(
        self,
        object_type: str,
        labels: dict[int, str],
    ) -> dict[str, Any]:
        """
        Label multiple objects of the same type.

        Args:
            object_type: Object type (e.g., "group", "cue", "sequence")
            labels: Dict mapping object IDs to label names

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        for obj_id, name in labels.items():
            sent.append(await self._send(label(object_type, obj_id, name)))

        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Labeled {len(labels)} {object_type}(s)",
        }

    async def create_and_run_macro(
        self,
        macro_id: int,
        commands: list[str],
        name: str | None = None,
        pool: int = 1,
        run: bool = False,
    ) -> dict[str, Any]:
        """
        Create a macro with command lines and optionally execute it.

        Args:
            macro_id: Macro number to create
            commands: List of command strings for each macro line
            name: Optional label for the macro
            pool: Macro pool number (default: 1)
            run: Whether to execute the macro after creation

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []

        sent.append(await self._send(cmd_store_macro(macro_id)))

        for i, command in enumerate(commands, start=1):
            sent.append(
                await self._send(assign_macro_cmd(macro_id, i, command, pool=pool))
            )

        if name is not None:
            sent.append(await self._send(cmd_label_macro(macro_id, name)))

        if run:
            sent.append(await self._send(f"go+ macro {pool}.{macro_id}"))

        action = "Created and executed" if run else "Created"
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"{action} Macro {macro_id} with {len(commands)} lines",
        }

    async def create_song_objects(
        self,
        song_id: int,
        song_name: str,
    ) -> dict[str, Any]:
        """
        Create and label a Sequence + Page pair for a song.

        Args:
            song_id: ID for both the sequence and page
            song_name: Name to assign to both objects

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []
        sent.append(await self._send(store("sequence", song_id, name=song_name)))
        sent.append(await self._send(store("page", song_id, name=song_name)))
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f'Created Sequence {song_id} and Page {song_id} "{song_name}"',
        }

    async def setup_timecode(
        self,
        tc_id: int,
        name: str | None = None,
        slot: int | None = None,
    ) -> dict[str, Any]:
        """
        Create a timecode show and optionally name it and assign a slot.

        Common SMPTE setup pattern: store the timecode pool object, label it,
        and bind it to a timecode slot for cue triggering.

        Args:
            tc_id: Timecode show ID
            name: Optional display name
            slot: Optional timecode slot to assign

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []
        sent.append(await self._send(store_timecode(tc_id)))
        if name is not None:
            sent.append(await self._send(assign_timecode_param(tc_id, "name", name)))
        if slot is not None:
            sent.append(await self._send(assign_timecode_param(tc_id, "slot", slot)))
        name_part = f' "{name}"' if name else ""
        slot_part = f" on slot {slot}" if slot is not None else ""
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Created Timecode {tc_id}{name_part}{slot_part}",
        }

    async def setup_fan_effect(
        self,
        blocks: int | None = None,
        wings: int | None = None,
        groups: int | None = None,
        interleave: int | None = None,
        filter: int | None = None,
    ) -> dict[str, Any]:
        """
        Configure MAtricks for a fan effect on the current selection.

        Sends the MAtricks reference followed by each provided parameter.

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        params = [
            (blocks, matricks_blocks),
            (wings, matricks_wings),
            (groups, matricks_groups),
            (interleave, matricks_interleave),
            (filter, matricks_filter),
        ]
        sent: list[str] = [await self._send(_matricks())]
        for val, fn in params:
            if val is not None:
                sent.append(await self._send(fn(val)))
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f"Configured MAtricks fan effect ({len(sent) - 1} params)",
        }

    async def build_color_palette(
        self,
        target: str,
        colors: list[dict[str, Any]],
        *,
        preset_type: str = "color",
        scope: str = "global",
        merge: bool = False,
        label: bool = True,
        appearance: bool = True,
    ) -> dict[str, Any]:
        """
        Program a list of colors into presets for a target fixture selection.

        For each color: select ``target``, set R/G/B/W (COLORRGB1/2/3/5), store the
        preset (with ``scope`` and optional ``merge``), and optionally label it and
        set its pool appearance swatch.

        Use ``merge=True`` to extend an existing palette to a new fixture group
        without disturbing values already stored for other fixture types.

        Args:
            target: A grandMA2 selection command (e.g. "Group 3", "Group 1 Thru 5").
            colors: List of dicts: {id, name?, r, g, b, w?} with r/g/b/w in 0-100.
            preset_type: Preset pool type (default "color").
            scope: "global", "selective", or "universal".
            merge: Merge into existing presets instead of replacing them.
            label: Apply the color's name as the preset label.
            appearance: Set each preset's pool appearance swatch from its color.

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        pool = PRESET_TYPES.get(preset_type.lower(), 4)
        scope_kwargs: dict[str, Any] = {"noconfirm": True}
        if scope == "global":
            scope_kwargs["global_scope"] = True
        elif scope == "selective":
            scope_kwargs["selective"] = True
        elif scope == "universal":
            scope_kwargs["universal"] = True
        if merge:
            scope_kwargs["merge"] = True

        sent: list[str] = []
        for color in colors:
            cid = color["id"]
            r = color.get("r", 0)
            g = color.get("g", 0)
            b = color.get("b", 0)
            w = color.get("w", 0)
            sent.append(await self._send(target))
            sent.append(await self._send(attribute_at("COLORRGB1", r)))
            sent.append(await self._send(attribute_at("COLORRGB2", g)))
            sent.append(await self._send(attribute_at("COLORRGB3", b)))
            sent.append(await self._send(attribute_at("COLORRGB5", w)))
            sent.append(
                await self._send(store_preset(preset_type, cid, **scope_kwargs))
            )
            if label and color.get("name"):
                sent.append(
                    await self._send(label_cmd("preset", f"{pool}.{cid}", color["name"]))
                )
            if appearance:
                sr, sg, sb = _color_swatch(r, g, b, w)
                sent.append(
                    await self._send(
                        appearance_cmd("preset", f"{pool}.{cid}", red=sr, green=sg, blue=sb)
                    )
                )

        mode = " (merged)" if merge else ""
        return {
            "commands_sent": sent,
            "count": len(colors),
            "summary": f"Programmed {len(colors)} {preset_type} preset(s) into {target}{mode}",
        }

    async def build_preset_palette(
        self,
        preset_type: str,
        presets: list[dict[str, Any]],
        *,
        scope: str = "global",
        merge: bool = False,
        label: bool = True,
    ) -> dict[str, Any]:
        """
        Build a preset palette of any type from per-fixture-type value sets.

        Generalizes the color/beam/focus build pattern: for each preset, for each
        target (a selection string), select the target, set its attributes, and
        store the preset. The first target uses ``scope``; subsequent targets of
        the same preset always merge (per-type accumulation into one preset).

        Args:
            preset_type: "color"/"beam"/"focus"/... (mapped to a pool number).
            presets: list of ``{id, name?, by_target: [{target, attrs}]}`` where
                ``target`` is a selection command and ``attrs`` is a list of
                ``(attribute, value)`` pairs.
            scope: "global", "selective", or "universal".
            merge: if True, the FIRST target also merges (extend an existing
                preset instead of replacing it).
            label: apply each preset's name as its label.

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        pool = PRESET_TYPES.get(preset_type.lower(), 1)

        def _scope_kwargs(do_merge: bool) -> dict[str, Any]:
            kw: dict[str, Any] = {"noconfirm": True}
            if scope == "global":
                kw["global_scope"] = True
            elif scope == "selective":
                kw["selective"] = True
            elif scope == "universal":
                kw["universal"] = True
            if do_merge:
                kw["merge"] = True
            return kw

        sent: list[str] = []
        for preset in presets:
            pid = preset["id"]
            for j, tgt in enumerate(preset.get("by_target", [])):
                do_merge = merge if j == 0 else True
                sent.append(await self._send("Clear"))
                sent.append(await self._send(tgt["target"]))
                for attr, val in tgt.get("attrs", []):
                    sent.append(await self._send(attribute_at(attr, val)))
                sent.append(
                    await self._send(
                        store_preset(preset_type, pid, **_scope_kwargs(do_merge))
                    )
                )
            if label and preset.get("name"):
                sent.append(
                    await self._send(
                        label_cmd("preset", f"{pool}.{pid}", preset["name"])
                    )
                )

        return {
            "commands_sent": sent,
            "count": len(presets),
            "summary": f"Built {len(presets)} {preset_type} preset(s)",
        }

    async def setup_song_macro(
        self,
        macro_id: int,
        song_name: str,
        var_name: str = "$song",
    ) -> dict[str, Any]:
        """
        Create a macro with a SetVar command on line 1.

        Args:
            macro_id: Macro number to create
            song_name: Song name used for label and variable value
            var_name: Variable name for the SetVar command (default: "$song")

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []
        sent.append(await self._send(cmd_store_macro(macro_id)))
        sent.append(await self._send(cmd_label_macro(macro_id, song_name)))
        setvar_cmd = f"SetVar {var_name}='{song_name}'"
        sent.append(await self._send(assign_macro_cmd(macro_id, 1, setvar_cmd)))
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f'Created Macro {macro_id} "{song_name}" with {var_name} assignment',
        }

    async def build_set_list(
        self,
        sequence_id: int,
        sequence_name: str,
        songs: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Create a set-list sequence with cue-to-macro links.

        Each song dict must contain:
            cue_id (int): Cue number in the set-list sequence
            macro_id (int): Macro to trigger via cue CMD
            name (str): Name for the cue

        Args:
            sequence_id: Sequence number for the set list
            sequence_name: Label for the set-list sequence
            songs: List of song definition dicts

        Returns:
            Result dict with commands_sent, count, and summary.
        """
        sent: list[str] = []
        sent.append(await self._send(store("sequence", sequence_id, name=sequence_name)))
        for song in songs:
            cue_id = song["cue_id"]
            macro_id = song["macro_id"]
            name = song["name"]
            sent.append(
                await self._send(
                    store("sequence", f"{sequence_id} cue {cue_id}", name=name)
                )
            )
            sent.append(
                await self._send(assign_cue_cmd(cue_id, sequence_id, f"Macro {macro_id}"))
            )
        return {
            "commands_sent": sent,
            "count": len(sent),
            "summary": f'Built set list "{sequence_name}" with {len(songs)} songs',
        }
