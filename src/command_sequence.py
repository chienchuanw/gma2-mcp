"""
Command Sequence Module

Provides a builder-pattern class for composing multiple grandMA2 commands
into an ordered batch that can be previewed and executed as a unit.

CommandSequence does NOT belong in src/commands/ because it has async
execute() logic that touches the network via GMA2TelnetClient.

Example:
    >>> from src.command_sequence import CommandSequence
    >>> from src.commands import fixture_at, store_group
    >>> seq = CommandSequence()
    >>> seq.add(fixture_at(1, 50)).add(store_group(1))
    >>> seq.preview()
    ['fixture 1 at 50', 'store group 1']
    >>> await seq.execute(client)
    {'commands_sent': ['fixture 1 at 50', 'store group 1'], 'count': 2, 'success': True}
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CommandSequence:
    """
    Ordered batch of grandMA2 command strings.

    Build a sequence of commands, inspect them with preview(),
    then execute them all through a telnet client.
    """

    def __init__(self) -> None:
        self._commands: list[str] = []

    def add(self, command: str) -> CommandSequence:
        """
        Append a command string to the sequence.

        Args:
            command: A grandMA2 command string (typically from a command builder function).

        Returns:
            Self for fluent chaining.
        """
        self._commands.append(command)
        return self

    def preview(self) -> list[str]:
        """
        Return the list of commands in execution order without sending anything.

        Returns:
            Copy of the internal command list.
        """
        return list(self._commands)

    def clear(self) -> None:
        """Remove all commands from the sequence, making it reusable."""
        self._commands.clear()

    async def execute(
        self,
        client: Any,
        *,
        delay: float | None = None,
    ) -> dict[str, Any]:
        """
        Send each command in order via the telnet client.

        Args:
            client: A GMA2TelnetClient instance with an async send_command() method.
            delay: Override the per-command delay in seconds.
                   If None, uses the client's default delay.

        Returns:
            Dict with keys: commands_sent (list[str]), count (int), success (bool).
        """
        sent: list[str] = []
        for cmd in self._commands:
            if delay is not None:
                await client.send_command(cmd, delay=delay)
            else:
                await client.send_command(cmd)
            sent.append(cmd)
            logger.debug(f"CommandSequence sent: {cmd}")

        return {
            "commands_sent": sent,
            "count": len(sent),
            "success": True,
        }

    # ---- Container protocol ------------------------------------------------

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self):
        return iter(self._commands)

    # ---- String representations --------------------------------------------

    def __str__(self) -> str:
        return "\n".join(self._commands)

    def __repr__(self) -> str:
        return f"CommandSequence(commands={len(self._commands)})"
