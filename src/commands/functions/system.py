"""System management keywords for grandMA2 Command Builder."""

from typing import Optional, Union


def backup() -> str:
    return "backup"


def black_screen() -> str:
    return "blackscreen"


def cmd_delay(value: Union[int, float]) -> str:
    return f"cmddelay {value}"


def cmd_help() -> str:
    return "cmdhelp"


def delete_show(name: str) -> str:
    return f"deleteshow {name}"


def escape() -> str:
    return "escape"


def exit_keyword() -> str:
    return "exit"


def help_keyword() -> str:
    return "help"


def load_show(name: str, *, noconfirm: bool = False) -> str:
    cmd = f'loadshow "{name}"'
    if noconfirm:
        cmd = f"{cmd} /noconfirm"
    return cmd


def lock() -> str:
    return "lock"


def login() -> str:
    return "login"


def logout() -> str:
    return "logout"


def new_show(name: str | None = None, *, noconfirm: bool = False) -> str:
    cmd = "newshow"
    if name:
        cmd = f'{cmd} "{name}"'
    if noconfirm:
        cmd = f"{cmd} /noconfirm"
    return cmd


def normal() -> str:
    return "normal"


def reboot() -> str:
    return "reboot"


def reload_plugins() -> str:
    return "reloadplugins"


def restart() -> str:
    return "restart"


def save_show(name: str | None = None, *, noconfirm: bool = False) -> str:
    cmd = "saveshow"
    if name:
        cmd = f'{cmd} "{name}"'
    if noconfirm:
        cmd = f"{cmd} /noconfirm"
    return cmd


def select_drive() -> str:
    return "selectdrive"


def set_hostname(name: str) -> str:
    return f"sethostname {name}"


def set_ip(address: str) -> str:
    return f"setip {address}"


def set_network_speed(value: str) -> str:
    return f"setnetworkspeed {value}"


def setup() -> str:
    return "setup"


def shutdown() -> str:
    return "shutdown"


def tools() -> str:
    return "tools"


def unlock() -> str:
    return "unlock"


def version() -> str:
    return "version"
