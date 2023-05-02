import pygame

disp_width = 900
disp_height = 600

top_margin = disp_height / 7
division = disp_height / 7
slider_row_height = (4 * division) / 3
slider_row_width = (2 * disp_width) / 5


class EnemySlider:
    order = 0
    slider_width = (2 * disp_width / 5) * (4 / 7)
    slider_height = 3
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    # slider_y = (disp_height / 7) + (disp_height / 14) - (slider_height / 2)
    slider_y = (
        top_margin
        + order * slider_row_height
        + (slider_row_height / 2)
        - (slider_height / 2)
    )
    slider_min = 0
    slider_max = 5
    slider_value = 1
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)
    bg_width = (2 * disp_width / 5) * (6 / 7)
    # bg_height = (disp_height / 7) * (2 / 5)
    bg_height = slider_row_height * (2 / 5)

    def __init__(self):
        pass

    def get_y(self, height):
        return (
            top_margin
            + self.order * slider_row_height
            + (slider_row_height / 2)
            - (height / 2)
        )

    def draw_text_min(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_min), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (1 / 7)) - img.get_width() / 2,
                # (disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_text_max(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_max), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (6 / 7)) - img.get_width() / 2,
                self.get_y(img.get_height()),
            ),
        )

    def draw_bg(self, surf):
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (
                (disp_width / 5) + (disp_width / 5) - self.bg_width * (1 / 2),
                # (disp_height / 7) + (disp_height / 14) - (self.bg_height * (1 / 2)),
                self.get_y(self.bg_height),
                self.bg_width,
                self.bg_height,
            ),
            border_radius=5,
        )

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        self.slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return self.slider_value


class BonusSlider:
    order = 1
    slider_width = (2 * disp_width / 5) * (4 / 7)
    slider_height = 3
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    # slider_y = (2 * disp_height / 7) + (disp_height / 14) - (slider_height / 2)
    slider_y = (
        top_margin
        + order * slider_row_height
        + (slider_row_height / 2)
        - (slider_height / 2)
    )
    slider_min = 0
    slider_max = 5
    slider_value = 1
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)
    bg_width = (2 * disp_width / 5) * (6 / 7)
    bg_height = slider_row_height * (2 / 5)

    def __init__(self):
        pass

    def get_y(self, height):
        return (
            top_margin
            + self.order * slider_row_height
            + (slider_row_height / 2)
            - (height / 2)
        )

    def draw_text_min(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_min), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (1 / 7)) - img.get_width() / 2,
                # (2 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_text_max(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_max), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (6 / 7)) - img.get_width() / 2,
                # (2 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_bg(self, surf):
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (
                (disp_width / 5) + (disp_width / 5) - self.bg_width * (1 / 2),
                # (2 * disp_height / 7) + (disp_height / 14) - (self.bg_height * (1 / 2)),
                self.get_y(self.bg_height),
                self.bg_width,
                self.bg_height,
            ),
            border_radius=5,
        )

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        self.slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return self.slider_value


class CivilianSlider:
    order = 2
    slider_width = (2 * disp_width / 5) * (4 / 7)
    slider_height = 3
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    # slider_y = (3 * disp_height / 7) + (disp_height / 14) - (slider_height / 2)
    slider_y = (
        top_margin
        + order * slider_row_height
        + (slider_row_height / 2)
        - (slider_height / 2)
    )
    slider_min = 0
    slider_max = 5
    slider_value = 0
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)
    bg_width = (2 * disp_width / 5) * (6 / 7)
    # bg_height = (disp_height / 7) * (2 / 5)
    bg_height = slider_row_height * (2 / 5)

    def __init__(self):
        pass

    def get_y(self, height):
        return (
            top_margin
            + self.order * slider_row_height
            + (slider_row_height / 2)
            - (height / 2)
        )

    def draw_text_min(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_min), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (1 / 7)) - img.get_width() / 2,
                # (3 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_text_max(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_max), True, text_color)
        surf.blit(
            img,
            (
                disp_width / 5 + ((2 * disp_width / 5) * (6 / 7)) - img.get_width() / 2,
                # (3 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_bg(self, surf):
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (
                (disp_width / 5) + (disp_width / 5) - self.bg_width * (1 / 2),
                # (3 * disp_height / 7) + (disp_height / 14) - (self.bg_height * (1 / 2)),
                self.get_y(self.bg_height),
                self.bg_width,
                self.bg_height,
            ),
            border_radius=5,
        )

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        self.slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return self.slider_value


class BonusTargetSlider:
    order = 1
    slider_width = (2 * disp_width / 5) * (4 / 7)
    slider_height = 3
    slider_x = (3 * disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    # slider_y = (2 * disp_height / 7) + (disp_height / 14) - (slider_height / 2)
    slider_y = (
        top_margin
        + order * slider_row_height
        + (slider_row_height / 2)
        - (slider_height / 2)
    )
    slider_min = 0
    slider_max = 5
    slider_value = 0
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x
    slider_knob_y = slider_y + int(slider_height / 2)
    bg_width = (2 * disp_width / 5) * (6 / 7)
    # bg_height = (disp_height / 7) * (2 / 5)
    bg_height = slider_row_height * (2 / 5)

    def __init__(self, parent):
        self.parent = parent
        self.slider_max = parent.slider_value
        self.slider_knob_x = self.slider_x

    def get_y(self, height):
        return (
            top_margin
            + self.order * slider_row_height
            + (slider_row_height / 2)
            - (height / 2)
        )

    def draw_text_min(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_min), True, text_color)
        surf.blit(
            img,
            (
                3 * disp_width / 5
                + ((2 * disp_width / 5) * (1 / 7))
                - img.get_width() / 2,
                # (2 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_text_max(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_max), True, text_color)
        surf.blit(
            img,
            (
                3 * disp_width / 5
                + ((2 * disp_width / 5) * (6 / 7))
                - img.get_width() / 2,
                # (2 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_bg(self, surf):
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (
                (3 * disp_width / 5) + (disp_width / 5) - self.bg_width * (1 / 2),
                # (2 * disp_height / 7) + (disp_height / 14) - (self.bg_height * (1 / 2)),
                self.get_y(self.bg_height),
                self.bg_width,
                self.bg_height,
            ),
            border_radius=5,
        )

    def update(self):
        self.slider_value = 0
        self.slider_max = self.parent.slider_value
        if self.slider_max != 0:
            self.slider_knob_x = self.slider_x + int(
                (self.slider_value - self.slider_min)
                / (self.slider_max - self.slider_min)
                * self.slider_width
            )
        else:
            self.slider_knob_x = self.slider_x

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        if self.slider_max != 0:
            self.slider_value = round(
                self.slider_min
                + (self.slider_max - self.slider_min)
                * (self.slider_knob_x - self.slider_x)
                / self.slider_width
            )
        else:
            self.slider_value = 0

        return self.slider_value


class CivilianTargetSlider:
    order = 2
    slider_width = (2 * disp_width / 5) * (4 / 7)
    slider_height = 3
    slider_x = (3 * disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    # slider_y = (3 * disp_height / 7) + (disp_height / 14) - (slider_height / 2)
    slider_y = (
        top_margin
        + order * slider_row_height
        + (slider_row_height / 2)
        - (slider_height / 2)
    )
    slider_min = 0
    slider_max = 5
    slider_value = 0
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x
    slider_knob_y = slider_y + int(slider_height / 2)
    bg_width = (2 * disp_width / 5) * (6 / 7)
    # bg_height = (disp_height / 7) * (2 / 5)
    bg_height = slider_row_height * (2 / 5)

    def __init__(self, parent):
        self.parent = parent
        self.slider_max = parent.slider_value
        self.slider_knob_x = self.slider_x
        pass

    def get_y(self, height):
        return (
            top_margin
            + self.order * slider_row_height
            + (slider_row_height / 2)
            - (height / 2)
        )

    def update(self):
        self.slider_value = 0
        self.slider_max = self.parent.slider_value
        if self.slider_max != 0:
            self.slider_knob_x = self.slider_x + int(
                (self.slider_value - self.slider_min)
                / (self.slider_max - self.slider_min)
                * self.slider_width
            )
        else:
            self.slider_knob_x = self.slider_x

    def draw_text_min(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_min), True, text_color)
        surf.blit(
            img,
            (
                3 * disp_width / 5
                + ((2 * disp_width / 5) * (1 / 7))
                - img.get_width() / 2,
                # (3 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_text_max(self, surf, font, text_color=(128, 128, 128)):
        img = font.render(str(self.slider_max), True, text_color)
        surf.blit(
            img,
            (
                3 * disp_width / 5
                + ((2 * disp_width / 5) * (6 / 7))
                - img.get_width() / 2,
                # (3 * disp_height / 7) + (disp_height / 14) - (img.get_height() / 2),
                self.get_y(img.get_height()),
            ),
        )

    def draw_bg(self, surf):
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (
                (3 * disp_width / 5) + (disp_width / 5) - self.bg_width * (1 / 2),
                # (3 * disp_height / 7) + (disp_height / 14) - (self.bg_height * (1 / 2)),
                self.get_y(self.bg_height),
                self.bg_width,
                self.bg_height,
            ),
            border_radius=5,
        )

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        if self.slider_max != 0:
            self.slider_value = round(
                self.slider_min
                + (self.slider_max - self.slider_min)
                * (self.slider_knob_x - self.slider_x)
                / self.slider_width
            )
        else:
            self.slider_value = 0

        return self.slider_value
