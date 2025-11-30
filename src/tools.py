"""
MCP Tools Module

This module defines high-level tool functions that AI can call.
These tools integrate the telnet_client and commands modules,
providing a simple and easy-to-use interface for AI.

Each tool is an async function, allowing the MCP server to handle requests asynchronously.
"""

import logging
from typing import Optional, Literal

from src.commands import (
    select_fixture,
    store_group,
    label_group,
    go_sequence,
    pause_sequence,
    goto_cue,
)

logger = logging.getLogger(__name__)

# Global GMA2 client instance
# This will be initialized in server.py
_gma2_client = None


def set_gma2_client(client) -> None:
    """
    Set the global GMA2 client instance.

    Args:
        client: GMA2TelnetClient instance
    """
    global _gma2_client
    _gma2_client = client


def get_gma2_client():
    """
    Get the global GMA2 client instance.

    Returns:
        GMA2TelnetClient: Global client instance

    Raises:
        RuntimeError: Client not initialized
    """
    global _gma2_client
    if _gma2_client is None:
        raise RuntimeError("GMA2 client not initialized, call set_gma2_client() first")
    return _gma2_client


# ============================================================
# MCP Tools
# ============================================================


async def create_fixture_group(
    start_fixture: int,
    end_fixture: int,
    group_id: int,
    group_name: Optional[str] = None,
) -> str:
    """
    Create a group containing a specified range of fixtures.

    This tool performs the following steps:
    1. Select the specified range of fixtures
    2. Save the selected fixtures as a group
    3. (Optional) Add a name label to the group

    Args:
        start_fixture: Starting fixture number
        end_fixture: Ending fixture number
        group_id: Group number to save
        group_name: (Optional) Group name

    Returns:
        str: Operation result message
    """
    client = get_gma2_client()

    # Step 1: Select fixtures
    select_cmd = select_fixture(start_fixture, end_fixture)
    client.send_command(select_cmd)
    logger.info(f"Selected Fixtures {start_fixture} to {end_fixture}")

    # Step 2: Save as group
    store_cmd = store_group(group_id)
    client.send_command(store_cmd)
    logger.info(f"Saved as Group {group_id}")

    # Step 3: (Optional) Add label
    if group_name:
        label_cmd = label_group(group_id, group_name)
        client.send_command(label_cmd)
        logger.info(f'Named Group {group_id} as "{group_name}"')
        return f'Created Group {group_id} "{group_name}" containing Fixtures {start_fixture} to {end_fixture}'

    return (
        f"Created Group {group_id} containing Fixtures {start_fixture} to {end_fixture}"
    )


async def execute_sequence(
    sequence_id: int,
    action: Literal["go", "pause", "goto"],
    cue_id: Optional[int] = None,
) -> str:
    """
    Execute sequence-related operations.

    Args:
        sequence_id: Sequence number
        action: Operation type (go=execute, pause=pause, goto=jump to specific cue)
        cue_id: (Required for goto) Target cue number

    Returns:
        str: Operation result message
    """
    client = get_gma2_client()

    if action == "go":
        cmd = go_sequence(sequence_id)
        client.send_command(cmd)
        return f"Executed Sequence {sequence_id}"

    elif action == "pause":
        cmd = pause_sequence(sequence_id)
        client.send_command(cmd)
        return f"Paused Sequence {sequence_id}"

    elif action == "goto":
        if cue_id is None:
            return "Error: goto action requires cue_id to be specified"
        cmd = goto_cue(sequence_id, cue_id)
        client.send_command(cmd)
        return f"Jumped to Cue {cue_id} of Sequence {sequence_id}"

    return f"Unknown action: {action}"


async def send_raw_command(command: str) -> str:
    """
    Send a raw MA command.

    This is a low-level tool that allows sending any grandMA2 command.
    It is recommended to use other high-level tools first; use this tool only when needed.

    Args:
        command: Raw MA command to send

    Returns:
        str: Operation result message
    """
    client = get_gma2_client()
    client.send_command(command)
    logger.info(f"Sent command: {command}")
    return f"Sent command: {command}"
