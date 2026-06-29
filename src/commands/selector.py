"""
Selection-expression (selector) grammar for the grandMA2 command builder.

A selector is a grandMA2 object-range expression: integer IDs joined by the
``thru`` / ``+`` / ``-`` operators (e.g. ``"1 thru 10 + 21 - 4"``). This module
validates and normalizes such expressions in one place so every object-taking
tool can accept ranges and lists natively instead of looping one ID at a time.

Validation rejects anything that is not a well-formed numeric selection,
including command-injection attempts (``;``, letters, etc.).
"""

from __future__ import annotations

import re

_OPERATORS = {"thru", "+", "-"}
# An ID is an integer or a pool.id decimal (e.g. "4.1" for preset 1 in pool 4).
_ID_RE = re.compile(r"\d+(\.\d+)?")


def normalize_selector(spec: str | int) -> str:
    """Validate and normalize a grandMA2 selection expression.

    Args:
        spec: A selection expression string (e.g. "1 thru 10 + 21") or a bare
              integer ID.

    Returns:
        The normalized expression: single-spaced, lowercase ``thru``, with each
        operator surrounded by single spaces (e.g. "1 thru 10 + 21").

    Raises:
        ValueError: If the expression is empty or not a well-formed numeric
            selection.
    """
    if isinstance(spec, int):
        return str(spec)

    if not isinstance(spec, str) or not spec.strip():
        raise ValueError("Selector must be a non-empty expression")

    # Tokenize: split on whitespace, but also separate '+' and '-' that may be
    # written without surrounding spaces (e.g. "10+21").
    raw = spec.lower()
    for op in ("+", "-"):
        raw = raw.replace(op, f" {op} ")
    tokens = raw.split()

    if not tokens:
        raise ValueError("Selector must be a non-empty expression")

    # Grammar: NUMBER (OPERATOR NUMBER)* — must start and end on a NUMBER and
    # strictly alternate NUMBER / OPERATOR.
    expect_number = True
    for token in tokens:
        if expect_number:
            if not _ID_RE.fullmatch(token):
                raise ValueError(f"Invalid selector token: {token!r}")
        else:
            if token not in _OPERATORS:
                raise ValueError(f"Invalid selector operator: {token!r}")
        expect_number = not expect_number

    if expect_number:
        # Ended expecting a number -> trailing operator
        raise ValueError(f"Selector ends with an operator: {spec!r}")

    return " ".join(tokens)
