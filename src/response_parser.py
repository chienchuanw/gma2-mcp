"""
Response Parser Module for grandMA2 Telnet Output

Pure functions that parse tabular text responses from grandMA2 telnet
commands (List Macro, List Cue, etc.) into structured dictionaries.

grandMA2 telnet List output is tabular text with:
- Header row with column names
- Separator line (dashes)
- Data rows with whitespace-separated columns
"""

from __future__ import annotations

import re

# CSI escape sequences, e.g. "\x1b[32m" (color) or "\x1b[K" (erase line)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from grandMA2 telnet output.

    grandMA2 wraps console output in ANSI color codes (e.g. ``\\x1b[32m``) and
    line-erase codes (``\\x1b[K``). This strips them so the text can be parsed
    or shown plainly. Trailing whitespace per line is also trimmed.
    """
    cleaned = _ANSI_RE.sub("", text)
    return "\n".join(line.rstrip() for line in cleaned.split("\n"))


# grandMA2 reports failures as "Error #NN: REASON" (after stripping ANSI).
_ERROR_RE = re.compile(r"Error\s+#(\d+):\s*(.*)")


def detect_error(raw: str) -> dict | None:
    """Detect a grandMA2 console error in a telnet response.

    grandMA2 reports failures inline as ``Error #NN: REASON`` (e.g.
    ``Error #14: OBJECT DOES NOT EXIST``). A ``WARNING, ...`` line is not an
    error and is ignored.

    Returns ``{"error_code": int, "error_text": str}`` when a numbered error is
    found, otherwise ``None``.
    """
    if not raw:
        return None
    match = _ERROR_RE.search(strip_ansi(raw))
    if not match:
        return None
    return {"error_code": int(match.group(1)), "error_text": match.group(2).strip()}


def _find_columns(header_line: str) -> list[tuple[str, int, int]]:
    """Find column names and their start/end positions from the header line.

    Returns a list of (column_name, start_index, end_index) tuples.
    end_index is -1 for the last column (extends to end of line).
    """
    columns = []
    for match in re.finditer(r"\S+", header_line):
        columns.append((match.group(), match.start(), match.end()))

    # Adjust end positions: each column extends to the start of the next column
    result = []
    for i, (name, start, _end) in enumerate(columns):
        if i + 1 < len(columns):
            next_start = columns[i + 1][1]
            result.append((name, start, next_start))
        else:
            result.append((name, start, -1))  # last column extends to EOL
    return result


def _parse_table(raw: str) -> tuple[list[tuple[str, int, int]], list[str]] | None:
    """Parse a tabular response into column definitions and data lines.

    Returns (columns, data_lines) or None if the format is not recognized.
    """
    if not raw or not raw.strip():
        return None

    lines = raw.split("\n")
    # Need at least header + separator
    if len(lines) < 2:
        return None

    header_line = lines[0]
    separator_line = lines[1]

    # Validate separator line contains dashes
    if not re.search(r"-{2,}", separator_line):
        return None

    columns = _find_columns(header_line)
    if not columns:
        return None

    # Data lines are everything after the separator, excluding empty trailing lines
    data_lines = [line for line in lines[2:] if line.strip()]

    return columns, data_lines


def _extract_column(line: str, columns: list[tuple[str, int, int]], col_name: str) -> str:
    """Extract a column value from a data line using column positions."""
    for name, start, end in columns:
        if name == col_name:
            if end == -1:
                return line[start:].strip()
            else:
                return line[start:end].strip()
    return ""


def parse_macro_lines(raw: str) -> dict:
    """Parse 'List Macro' output into structured data.

    Returns:
        {"parsed": True, "lines": [{"line_number": int, "cmd": str}, ...]}
        On failure: {"parsed": False, "lines": [], "raw_response": raw}
    """
    result = _parse_table(raw)
    if result is None:
        return {"parsed": False, "lines": [], "raw_response": raw}

    columns, data_lines = result

    parsed_lines = []
    for line in data_lines:
        no_str = _extract_column(line, columns, "No")
        cmd = _extract_column(line, columns, "CMD")
        try:
            line_number = int(no_str)
        except (ValueError, TypeError):
            continue
        parsed_lines.append({"line_number": line_number, "cmd": cmd})

    return {"parsed": True, "lines": parsed_lines}


def parse_cue_info(raw: str) -> dict:
    """Parse 'List Cue' output into structured data.

    Returns:
        {"parsed": True, "label": str, "cmd": str, "fade": str|None}
        On failure: {"parsed": False, "raw_response": raw}
    """
    result = _parse_table(raw)
    if result is None:
        return {"parsed": False, "raw_response": raw}

    columns, data_lines = result

    if not data_lines:
        return {"parsed": False, "raw_response": raw}

    # Parse the first data row (single cue info)
    line = data_lines[0]
    label = _extract_column(line, columns, "Name")
    fade = _extract_column(line, columns, "Fade") or None
    cmd = _extract_column(line, columns, "CMD")

    return {"parsed": True, "label": label, "cmd": cmd, "fade": fade}


def parse_object_label(raw: str) -> dict:
    """Parse 'List {type}' output to extract object label/name.

    Returns:
        {"parsed": True, "label": str}
        On failure: {"parsed": False, "label": None, "raw_response": raw}
    """
    result = _parse_table(raw)
    if result is None:
        return {"parsed": False, "label": None, "raw_response": raw}

    columns, data_lines = result

    if not data_lines:
        return {"parsed": False, "label": None, "raw_response": raw}

    line = data_lines[0]
    label = _extract_column(line, columns, "Name")

    return {"parsed": True, "label": label}
