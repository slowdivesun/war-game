import pygame, sys
import os
from pygame.locals import *
import math
from load_image import load_image


class Civilian(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("civilian.png", -1, 0.05)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = x, y

    def rescued(self):
        self.kill()

    def update(self):
        pass
