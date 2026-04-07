"""Network/session keywords for grandMA2 Command Builder."""


def change_dest() -> str:
    return "changedest"


def chat() -> str:
    return "chat"


def disconnect_station() -> str:
    return "disconnectstation"


def drop_control() -> str:
    return "dropcontrol"


def end_session() -> str:
    return "endsession"


def invite_station() -> str:
    return "invitestation"


def join_session() -> str:
    return "joinsession"


def leave_session() -> str:
    return "leavesession"


def network_info() -> str:
    return "networkinfo"


def network_node_info() -> str:
    return "networknodeinfo"


def network_node_update() -> str:
    return "networknodeupdate"


def network_speed_test() -> str:
    return "networkspeedtest"


def remote(target: str) -> str:
    return f"remote {target}"


def remote_command(command: str) -> str:
    return f"remotecommand {command}"


def take_control() -> str:
    return "takecontrol"


def telnet(target: str) -> str:
    return f"telnet {target}"


def web_remote_prog_only() -> str:
    return "webremoteprogonly"
