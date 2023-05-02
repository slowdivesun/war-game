import pygame
from load_image import load_image
from enemy import Enemy
from bonus import Bonus
from civilian import Civilian
from constants import (
    disp_height,
    disp_width,
    DISPLAYSURF,
    WHITE,
    topbar_btn_width,
    upper_strip,
)


def draw_text(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x, y))


def draw_text_middle(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))


def draw_text_right_align(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width(), y - img.get_height() / 2))


def draw_text_left_align(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x, y - img.get_height() / 2))


def draw_enemies(count):
    enemies = []
    left = 5
    top = 5
    img_width = load_image("enemy.png")[0].get_width() * 0.08

    for i in range(count):
        enemies.append(Enemy(left + (img_width + 2) * i, top))

    return enemies


def draw_civilians(count):
    civilians = []
    left = 5
    top = (3 * disp_height / 4) - 10 - load_image("civilian.png")[0].get_height() * 0.05
    img_width = load_image("civilian.png")[0].get_width() * 0.05

    for i in range(count):
        civilians.append(Civilian(left + (img_width + 40) * i, top))

    return civilians


def draw_bonuses(count):
    bonuses = []
    left = 5
    top = (
        (3 * disp_height / 4)
        - 20
        - load_image("civilian.png")[0].get_height() * 0.05
        - load_image("coin.png")[0].get_height() * 0.08
    )
    img_width = load_image("coin.png")[0].get_width() * 0.08

    for i in range(count):
        bonuses.append(Bonus(left + (img_width + 30) * i, top, 5))

    return bonuses


def main_menu_ui():
    draw_text_middle(
        "HOME",
        pygame.font.SysFont("BOLD", 25),
        "#f9430a",
        disp_width / 2 + topbar_btn_width / 2,
        upper_strip / 2,
        DISPLAYSURF,
    )
    draw_text(
        "UNLEASH YOUR",
        pygame.font.SysFont("impact", 35),
        (255, 255, 255),
        2 * disp_width / 3,
        disp_height / 4,
        DISPLAYSURF,
    )
    draw_text(
        "INNER",
        pygame.font.SysFont("impact", 35),
        (255, 255, 255),
        2 * disp_width / 3,
        disp_height / 4 + 40,
        DISPLAYSURF,
    )
    draw_text(
        "WARRIOR",
        pygame.font.SysFont("impact", 35),
        "#f9430a",
        2 * disp_width / 3
        + pygame.font.SysFont("impact", 35)
        .render("INNER ", True, (255, 255, 255))
        .get_width(),
        disp_height / 4 + 40,
        DISPLAYSURF,
    )
    draw_text_left_align(
        "OBSTACLES :",
        pygame.font.SysFont("BOLD", 30),
        "#f9430a",
        disp_width / 3,
        disp_height / 2 + 35 / 2,
        DISPLAYSURF,
    )


def settings_ui(top_margin, slider_row_height, rect_surf, apply_surf, cancel_surf):
    draw_text_middle(
        "OBSTACLES :",
        pygame.font.SysFont("BOLD", 30),
        "#ffffff",
        disp_width / 10,
        top_margin + 0 * slider_row_height + slider_row_height / 2,
        DISPLAYSURF,
    )
    draw_text_middle(
        "BONUS :",
        pygame.font.SysFont("BOLD", 30),
        "#ffffff",
        disp_width / 10,
        top_margin + 1 * slider_row_height + slider_row_height / 2,
        DISPLAYSURF,
    )
    draw_text_middle(
        "CIVILIANS :",
        pygame.font.SysFont("BOLD", 30),
        "#ffffff",
        disp_width / 10,
        top_margin + 2 * slider_row_height + slider_row_height / 2,
        DISPLAYSURF,
    )
    pygame.draw.rect(
        rect_surf,
        (51, 51, 51, 120),
        pygame.Rect(0, 0, rect_surf.get_width(), rect_surf.get_height()),
    )
    pygame.draw.rect(
        apply_surf,
        (51, 51, 51, 220),
        pygame.Rect(0, 0, apply_surf.get_width(), apply_surf.get_height()),
    )
    pygame.draw.rect(
        cancel_surf,
        (51, 51, 51, 220),
        pygame.Rect(0, 0, cancel_surf.get_width(), cancel_surf.get_height()),
    )
    draw_text_middle(
        "SETTINGS",
        pygame.font.SysFont("Arial", 25),
        "#ffffff",
        disp_width / 2,
        disp_height / 14,
        DISPLAYSURF,
    )
