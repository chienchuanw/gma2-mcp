"""
Misc Object Keywords for grandMA2 Command Builder

Remaining object keywords not covered by dedicated modules.
"""


def camera(camera_id: int) -> str:
    return f"camera {camera_id}"


def channel_link(link_id: int) -> str:
    return f"channellink {link_id}"


def filter_keyword() -> str:
    return "filter"


def fixture_type(type_id: int) -> str:
    return f"fixturetype {type_id}"


def form(form_id: int) -> str:
    return f"form {form_id}"


def gel(gel_id: int) -> str:
    return f"gel {gel_id}"


def image(image_id: int) -> str:
    return f"image {image_id}"


def item_3d(item_id: int) -> str:
    return f"item3d {item_id}"


def layer(layer_id: int) -> str:
    return f"layer {layer_id}"


def macro(macro_id: int) -> str:
    return f"macro {macro_id}"


def mask(mask_id: int) -> str:
    return f"mask {mask_id}"


def master(master_id: int) -> str:
    return f"master {master_id}"


def master_fade(master_id: int) -> str:
    return f"masterfade {master_id}"


def media_server(server_id: int) -> str:
    return f"mediaserver {server_id}"


def menu(menu_id: int) -> str:
    return f"menu {menu_id}"


def message() -> str:
    return "message"


def messages() -> str:
    return "messages"


def model(model_id: int) -> str:
    return f"model {model_id}"


def plugin(plugin_id: int) -> str:
    return f"plugin {plugin_id}"


def pm_area(area_id: int) -> str:
    return f"pmarea {area_id}"


def profile(profile_id: int) -> str:
    return f"profile {profile_id}"


def protocol(protocol_id: int) -> str:
    return f"protocol {protocol_id}"


def root() -> str:
    return "root"


def screen(screen_id: int) -> str:
    return f"screen {screen_id}"


def search_result() -> str:
    return "searchresult"


def selection() -> str:
    return "selection"


def special_master(master_id: int) -> str:
    return f"specialmaster {master_id}"


def surface(surface_id: int) -> str:
    return f"surface {surface_id}"


def user(user_id: int) -> str:
    return f"user {user_id}"


def user_profile(profile_id: int) -> str:
    return f"userprofile {profile_id}"


def value_keyword() -> str:
    return "value"


def view(view_id: int) -> str:
    return f"view {view_id}"


def view_button(button_id: int) -> str:
    return f"viewbutton {button_id}"


def view_page(page_id: int) -> str:
    return f"viewpage {page_id}"


def world(world_id: int) -> str:
    return f"world {world_id}"
