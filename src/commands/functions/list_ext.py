"""Extended list keywords for grandMA2 Command Builder."""


def list_effect_library() -> str:
    return "listeffectlibrary"


def list_fader_modules() -> str:
    return "listfadermodules"


def list_library() -> str:
    return "listlibrary"


def list_macro_library() -> str:
    return "listmacrolibrary"


def list_oops() -> str:
    return "listoops"


def list_owner() -> str:
    return "listowner"


def list_plugin_library() -> str:
    return "listpluginlibrary"


def list_shows(filter: str | None = None) -> str:
    cmd = "listshows"
    if filter:
        cmd = f"{cmd} {filter}"
    return cmd


def list_update() -> str:
    return "listupdate"


def list_user_var(filter: str | None = None) -> str:
    cmd = "listuservar"
    if filter:
        cmd = f"{cmd} {filter}"
    return cmd


def list_var(filter: str | None = None) -> str:
    cmd = "listvar"
    if filter:
        cmd = f"{cmd} {filter}"
    return cmd
