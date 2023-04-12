import pygame, sys
import os
from pygame.locals import *
import math


bomb_speed = 2

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def calculate_new_xy(old_xy, speed, direction, angle_in_radians, dt):
    speed_x = speed * math.cos(direction)
    speed_y = speed * math.sin(direction)
    new_x = old_xy[0] + (speed_x * math.cos(angle_in_radians) * dt)
    new_y = old_xy[1] + (
        speed_y * dt - 0.5 * 9.8 * dt * dt
    )  # second equation of motion
    return new_x, new_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, angle, init_x, init_y, display):
        self.direction = direction
        self.angle = angle
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet.png", -1, 0.02)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (init_x, init_y)
        self.display = display

    def update(self, dt):
        center = calculate_new_xy(
            self.rect.center, bomb_speed, math.radians(self.angle), dt
        )
        self.rect.center = center
        if not self.display.get_rect().contains(self.rect):
            self.kill()
