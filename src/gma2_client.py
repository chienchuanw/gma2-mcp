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
from src.commands import (
    appearance,
    assign,
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

            sent.append(
                await self._send(
                    assign("sequence", seq_id, "executor", exec_id)
                )
            )

            if "label" in entry:
                sent.append(
                    await self._send(label("executor", exec_id, entry["label"]))
                )

            if "fader_level" in entry:
                sent.append(
                    await self._send(executor_at(exec_id, entry["fader_level"]))
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
