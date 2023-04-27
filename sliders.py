import pygame

disp_width = 900
disp_height = 600


class CivilianSlider:
    slider_width = (2 * disp_width / 5) * (4 / 5)
    slider_height = 10
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    slider_y = 350
    slider_min = 0
    slider_max = 10
    slider_value = 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)

    def __init__(self):
        pass

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return slider_value


class EnemySlider:
    slider_width = (2 * disp_width / 5) * (4 / 5)
    slider_height = 10
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    slider_y = 170
    slider_min = 0
    slider_max = 10
    slider_value = 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)

    def __init__(self):
        pass

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return slider_value


class BonusSlider:
    slider_width = (2 * disp_width / 5) * (4 / 5)
    slider_height = 10
    slider_x = (disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    slider_y = 260
    slider_min = 0
    slider_max = 10
    slider_value = 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)

    def __init__(self):
        pass

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return slider_value


class BonusTargetSlider:
    slider_width = (2 * disp_width / 5) * (4 / 5)
    slider_height = 10
    slider_x = (3 * disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    slider_y = 260
    slider_min = 0
    slider_max = 10
    slider_value = 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)

    def __init__(self):
        pass

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return slider_value


class CivilianTargetSlider:
    slider_width = (2 * disp_width / 5) * (4 / 5)
    slider_height = 10
    slider_x = (3 * disp_width / 5) + (1 * disp_width / 5) - (slider_width / 2)
    slider_y = 350
    slider_min = 0
    slider_max = 10
    slider_value = 2
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    slider_knob_radius = 8
    slider_knob_x = slider_x + int(
        (slider_value - slider_min) / (slider_max - slider_min) * slider_width
    )
    slider_knob_y = slider_y + int(slider_height / 2)

    def __init__(self):
        pass

    def find_value(self, event):
        self.slider_knob_x = min(
            max(event.pos[0], self.slider_x), self.slider_x + self.slider_width
        )
        slider_value = round(
            self.slider_min
            + (self.slider_max - self.slider_min)
            * (self.slider_knob_x - self.slider_x)
            / self.slider_width
        )

        return slider_value
