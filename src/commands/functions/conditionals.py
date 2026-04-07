"""Conditional/flow keywords for grandMA2 Command Builder."""


def end_if() -> str:
    return "endif"


def if_active() -> str:
    return "ifactive"


def if_output() -> str:
    return "ifoutput"


def if_prog() -> str:
    return "ifprog"


def or_keyword() -> str:
    return "or"


def with_keyword() -> str:
    return "with"
