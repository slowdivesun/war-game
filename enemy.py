import pygame
from load_image import load_image
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, left, top, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy.png", -1, 0.08, angle)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.left = left
        self.top = top
        self.rect.topleft = left, top
        self.angle = angle
        self.right_facing = True

        # NOTE: drag and drop
        self.clicked = False
        self.selected = False
        self.isRandom = False

    def change_angle(self, direction):
        if (
            (self.right_facing)
            and (self.angle + 10 * direction <= 90)
            and (self.angle + 10 * direction >= -90)
        ):
            self.angle += 10 * direction
            self.image, self.rect = load_image("enemy.png", -1, 0.08, self.angle)
            self.rect.topleft = self.left, self.top
        if (
            (not self.right_facing)
            and (self.angle + 10 * direction >= 90)
            and (self.angle + 10 * direction <= 270)
        ):
            self.angle += 10 * direction
            self.image, self.rect = load_image(
                "enemy.png", -1, 0.08, (180 - self.angle)
            )
            self.angle = 180 - self.angle
            self.flip_enemy()
            self.right_facing = False
            self.rect.topleft = self.left, self.top

    def flip_enemy(self):
        self.image = self.image.copy()
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.angle = -1 * self.angle + 180
        self.right_facing = not self.right_facing
        self.rect.topleft = self.left, self.top

    def random_reorientation(self, x, y):
        print(self.left, self.top)
        print(self.rect.topleft)
        new_angle = math.atan2(self.rect.center[1] - y, x - self.rect.center[0])
        print("in radian: ", new_angle)
        new_angle = math.degrees(new_angle)
        print("in degrees: ", new_angle)

        if new_angle >= 90 and new_angle <= 180:
            self.angle = 180 - new_angle
            self.image, self.rect = load_image("enemy.png", -1, 0.08, self.angle)
            self.flip_enemy()
        if new_angle <= -90 and new_angle >= -180:
            self.angle = new_angle + 180
            self.angle *= -1
            self.image, self.rect = load_image("enemy.png", -1, 0.08, self.angle)
            self.flip_enemy()
        else:
            self.angle = new_angle
            self.image, self.rect = load_image("enemy.png", -1, 0.08, self.angle)
        self.rect.topleft = self.left, self.top

    def location(self):
        return self.rect.left, self.rect.top

    def update(self, x, y, surf):
        pygame.draw.line(
            surf, "red", (x, y), (self.rect.center[0], self.rect.center[1])
        )
        pygame.draw.line(
            surf,
            "blue",
            (self.rect.center[0], self.rect.center[1]),
            (
                self.rect.center[0] + math.cos(math.radians(self.angle)) * 900,
                self.rect.center[1] - math.sin(math.radians(self.angle)) * 900,
            ),
        )
        pass
