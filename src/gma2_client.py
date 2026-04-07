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
    assign,
    assign_fade,
    at,
    fixture_at,
    label,
    preset,
    select_fixture,
    store_cue,
    store_group,
    label_group,
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
            sent.append(await self._send(store_cue(cue_id)))

            if "name" in cue_def:
                sent.append(await self._send(label("cue", cue_id, cue_def["name"])))

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
        sent.append(await self._send(store_group(group_id)))
        sent.append(await self._send(label_group(group_id, group_name)))
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
