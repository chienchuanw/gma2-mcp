"""Capabilities serializer for the workflow dependency contract (issue #85).

`gma2-workflow` depends on this server across a repo boundary with no shared CI.
The `capabilities` MCP tool exposes a machine-readable surface — version, tool
list, and the show-profile schema version this server targets — so the workflow's
`connect` skill can self-check against a profile's ``meta.capabilities_min`` during
prep instead of discovering drift at show time.
"""

# The show-profile schema version this server is compatible with
# (see gma2-workflow/profiles/SCHEMA.md). Bump when the profile contract changes.
PROFILE_SCHEMA_VERSION = 1


def build_capabilities(
    version: str,
    tool_names: list[str],
    profile_schema_version: int,
) -> dict:
    """Build the capabilities descriptor.

    Pure function (no I/O) so it is trivially unit-testable.

    Args:
        version: This server's version (``src.__version__``).
        tool_names: Names of the registered MCP tools.
        profile_schema_version: The show-profile schema version this server targets.

    Returns:
        dict: ``{version, tools (sorted), tool_count, profile_schema_version}``.
    """
    tools = sorted(tool_names)
    return {
        "version": version,
        "tools": tools,
        "tool_count": len(tools),
        "profile_schema_version": profile_schema_version,
    }
