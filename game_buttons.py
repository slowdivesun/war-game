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


class GameButton:
    def __init__(self, x, y, w, h, font, text, color=WHITE):
        self.button = pygame.Rect(x, y, w, h)
        self.text = font.render(text, True, BLACK)
        self.text_rect = self.text.get_rect(center=(x + (w / 2), y + (h / 2)))
        self.visible = True

    def toggle_disability(self):
        pass

    def render_button(self, surface, color):
        pygame.draw.rect(surface, color, self.button)
        surface.blit(self.text, self.text_rect)
