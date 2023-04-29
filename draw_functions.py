import pygame


def draw_text(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x, y))


def draw_text_middle(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))


def draw_text_right_align(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width(), y - img.get_height() / 2))


def create_button_func(
    x, y, w, h, font, text, surf, color=(0, 0, 0), back_col=(255, 255, 255)
):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surf, back_col, button)
    button_text = font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    surf.blit(button_text, text_rect)
    return button
