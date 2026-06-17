"""
Verified Execution Core for grandMA2 Commands

grandMA2 reports command failures inline in the telnet reply
(``Error #NN: REASON``) rather than via a status code. This module turns a raw
telnet reply into a structured :class:`ExecutionResult` so tools can report the
console's actual outcome instead of fabricating success.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.response_parser import detect_error, strip_ansi


@dataclass(frozen=True)
class ExecutionResult:
    """Structured outcome of a single grandMA2 command.

    Attributes:
        ok: True when the console reported no error.
        echo: ANSI-stripped, human-readable console output.
        error_code: grandMA2 error number (e.g. 14), or None on success.
        error_text: grandMA2 error reason, or None on success.
        raw: the original, unmodified telnet reply.
    """

    ok: bool
    echo: str
    error_code: int | None
    error_text: str | None
    raw: str

    def summary(self) -> str:
        """A concise, truthful one-line summary for an MCP tool to return."""
        if self.ok:
            return self.echo.strip() or "OK"
        return f"Error #{self.error_code}: {self.error_text}"


def build_result(command: str, raw: str) -> ExecutionResult:
    """Build an :class:`ExecutionResult` from a command and its telnet reply.

    Pure function (no network) so it is fully unit-testable.
    """
    error = detect_error(raw)
    if error is None:
        return ExecutionResult(
            ok=True,
            echo=strip_ansi(raw).strip(),
            error_code=None,
            error_text=None,
            raw=raw,
        )
    return ExecutionResult(
        ok=False,
        echo=strip_ansi(raw).strip(),
        error_code=error["error_code"],
        error_text=error["error_text"],
        raw=raw,
    )
