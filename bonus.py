import pygame, sys
import os
from pygame.locals import *
import math
from load_image import load_image


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, points):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("coin.png", -1, 0.08)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.points = points
        self.rect.topleft = x, y

    def update(self):
        pass
