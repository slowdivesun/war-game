import pygame
from load_image import load_image
from enemy import Enemy
from bonus import Bonus
from civilian import Civilian

disp_height = 600


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


def create_button_func(
    x, y, w, h, font, text, surf, color=(0, 0, 0), back_col=(255, 255, 255)
):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surf, back_col, button)
    button_text = font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    surf.blit(button_text, text_rect)
    return button


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
