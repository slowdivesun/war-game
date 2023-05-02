import pygame
from pygame.locals import *
import random
from load_image import load_image
from groups import bonus_animation_group
from constants import DISPLAYSURF


class ParticleStar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.particles = []
        self.image, self.rect = load_image("star.png", -1, 0.3)
        pygame.sprite.Sprite.__init__(self)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.area = DISPLAYSURF.get_rect()
        self.rect.topleft = x, y
        self.counter = 0
        self.len = 10
        self.index = 0

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x += particle[1]
                particle[0].y += particle[2]
                particle[3] -= 0.2
                DISPLAYSURF.blit(self.image, particle[0])

    def add_particles(self):
        pos_x = self.x
        pos_y = self.y
        direction_x = random.randint(-2, 2)
        direction_y = random.randint(-2, 2)
        lifetime = random.randint(4, 10)
        particle_rect = pygame.Rect(int(pos_x), int(pos_y), self.width, self.height)
        self.particles.append([particle_rect, direction_x, direction_y, lifetime])

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[3] > 0]
        self.particles = particle_copy

    def update(self):
        speed = 4
        self.counter += 1
        if self.counter >= speed and self.index < self.len - 1:
            self.counter = 0
            self.index += 1
            self.add_particles()

        if self.index >= self.len - 1 and self.counter >= speed:
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, points):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("coin.png", -1, 0.08)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.points = points
        self.rect.topleft = x, y
        self.top = y
        self.left = x
        self.clicked = False

    def collected(self):
        bonus_animation_group.add(ParticleStar(self.left, self.top))
        self.kill()
