from game_buttons import create_button_center, create_button_func
from constants import *


def ext_begin_button_gray():
    return create_button_center(
        begin_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Begin",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_back_button():
    return create_button_center(
        back_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        pygame.font.SysFont("segoeuisymbol", 30),
        "\U00002B05",
        DISPLAYSURF,
        (199, 95, 95),
    )


def ext_info_button():
    return create_button_center(
        info_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        pygame.font.SysFont("segoeuisymbol", 30),
        "\U00002139",
        DISPLAYSURF,
        (63, 60, 230),
    )


def ext_rotate_left_button_gray():
    return create_button_center(
        rotatel_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        emoji_font,
        "🔄️",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_rotate_right_button_gray():
    return create_button_center(
        rotater_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        emoji_font,
        "🔃",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_flip_button_gray():
    return create_button_center(
        flip_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Flip",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_rotate_left_button_green():
    return create_button_center(
        rotatel_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        emoji_font,
        "🔄️",
        DISPLAYSURF,
        BTN_GREEN,
    )


def ext_rotate_right_button_green():
    return create_button_center(
        rotater_btn_order * (btn_col_width) + (small_btn_col_width / 2),
        btn_y,
        small_btn_width,
        settings_btn_height,
        emoji_font,
        "🔃",
        DISPLAYSURF,
        BTN_GREEN,
    )


def ext_flip_button_green():
    return create_button_center(
        flip_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Flip",
        DISPLAYSURF,
        BTN_GREEN,
    )


def ext_random_button_gray():
    return create_button_center(
        random_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Random",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_random_button_green():
    return create_button_center(
        random_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Random",
        DISPLAYSURF,
        BTN_GREEN,
    )


def ext_restart_button():
    return create_button_center(
        restart_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Restart",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_menu_button():
    return create_button_center(
        menu_btn_order * (btn_col_width) + (btn_col_width / 2),
        btn_y,
        settings_btn_width,
        settings_btn_height,
        font,
        "Menu",
        DISPLAYSURF,
        BTN_GRAY,
    )


def ext_start_button():
    return create_button_func(
        2 * disp_width / 3,
        disp_height / 2,
        topbar_btn_width,
        35,
        pygame.font.SysFont("Arial", 23),
        "START",
        DISPLAYSURF,
        (255, 255, 255),
        "#ed5e3e",
    )


def ext_start_button_hover():
    return create_button_func(
        2 * disp_width / 3,
        disp_height / 2,
        topbar_btn_width,
        35,
        pygame.font.SysFont("Arial", 23),
        "START",
        DISPLAYSURF,
        (255, 255, 255),
        "#f9430a",
    )


def ext_settings_button():
    return create_button_func(
        disp_width / 2 + topbar_btn_width,
        0,
        topbar_btn_width,
        upper_strip,
        pygame.font.SysFont("BOLD", 25),
        "SETTINGS",
        DISPLAYSURF,
        (255, 255, 255),
        (0, 0, 0),
    )


def ext_settings_button_hover():
    return create_button_func(
        disp_width / 2 + topbar_btn_width,
        0,
        topbar_btn_width,
        upper_strip,
        pygame.font.SysFont("BOLD", 25),
        "SETTINGS",
        DISPLAYSURF,
        (255, 255, 255),
        "#232023",
    )


def ext_about_button():
    return create_button_func(
        disp_width / 2 + 2 * topbar_btn_width,
        0,
        topbar_btn_width,
        upper_strip,
        pygame.font.SysFont("BOLD", 25),
        "ABOUT",
        DISPLAYSURF,
        (255, 255, 255),
        (0, 0, 0),
    )


def ext_about_button_hover():
    return create_button_func(
        disp_width / 2 + 2 * topbar_btn_width,
        0,
        topbar_btn_width,
        upper_strip,
        pygame.font.SysFont("BOLD", 25),
        "ABOUT",
        DISPLAYSURF,
        (255, 255, 255),
        "#232023",
    )
