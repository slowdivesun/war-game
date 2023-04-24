import pygame, sys
import os
from pygame.locals import *
import math
from load_image import load_image
from explosion_group import explosion_group

bomb_speed = 1


def calculate_new_xy_bomb(old_xy, speed, bomb_angle_radians, dt):
    new_x = old_xy[0] + (speed * math.cos(bomb_angle_radians) * dt)
    new_y = old_xy[1] + (speed * math.sin(bomb_angle_radians) * dt)
    return new_x, new_y


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img, rect = load_image(f"explosions/exp{num}.png", -1, 1)
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


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
        center = calculate_new_xy_bomb(self.rect.center, bomb_speed, self.angle, dt)
        if not self.rect.collidepoint(self.lim_x, self.lim_y):
            self.rect.center = center

        else:
            new_explosion = Explosion(self.lim_x, self.lim_y)
            explosion_group.add(new_explosion)
            self.kill()