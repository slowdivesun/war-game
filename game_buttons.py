import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


def create_button_fun(x, y, w, h, font, text, k, g, color=WHITE):
    button = pygame.Rect(x, y, w, h)
    # pygame.draw.rect(DISPLAYSURF, color, button)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    # DISPLAYSURF.blit(button_text, text_rect)
    return button, button_text, text_rect


def create_button_func(
    x, y, w, h, font, text, surf, color=(0, 0, 0), back_col=(255, 255, 255)
):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surf, back_col, button)
    button_text = font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    surf.blit(button_text, text_rect)
    return button


def create_button_center(x, y, w, h, font, text, surf, color=WHITE):
    button = pygame.Rect(x - w / 2, y - h / 2, w, h)
    pygame.draw.rect(surf, color, button)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x, y))
    surf.blit(button_text, text_rect)
    return button
