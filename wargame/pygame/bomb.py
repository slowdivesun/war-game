import pygame, sys
import os
from pygame.locals import *
import math


bomb_speed = 1

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


def calculate_new_xy_bomb(old_xy, speed, bomb_angle_radians, dt):
    new_x = old_xy[0] + (speed * math.cos(bomb_angle_radians) * dt)
    new_y = old_xy[1] + (speed * math.sin(bomb_angle_radians) * dt)
    return new_x, new_y


class Bomb(pygame.sprite.Sprite):
    def __init__(self, angle, init_x, init_y, display, lim_x, lim_y):
        self.angle = angle
        self.lim_x = lim_x
        self.lim_y = lim_y
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bomb.png", -1, 0.05)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (init_x, init_y)
        self.display = display

    def update(self, dt):
        print(self.rect.center)
        center = calculate_new_xy_bomb(self.rect.center, bomb_speed, self.angle, dt)
        print(center)
        if center[0] + 2 < self.lim_x and center[0] - 2 > self.lim_x:
            pass
        else:
            self.rect.center = center
