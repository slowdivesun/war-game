import pygame
from pygame.locals import *
import math
from load_image import load_image
from groups import explosion_group
import random
from constants import disp_width, disp_height, explosion_sound, DISPLAYSURF

bomb_speed = 0.4
disp_width = 900
disp_height = 600


def calculate_new_xy_bomb(old_xy, speed, bomb_angle_radians, dt):
    new_x = old_xy[0] + (speed * math.cos(bomb_angle_radians) * dt)
    new_y = old_xy[1] + (speed * math.sin(bomb_angle_radians) * dt)
    return new_x, new_y


class Explosion(pygame.sprite.Sprite):
    def __init__(self, tx, ty, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img, rect = load_image(f"explosions/exp{num}.png", -1, 1)
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [tx, ty]
        self.counter = 0
        self.sold_coordinates = (x, y)
        self.damage_done = False
        self.type = type  # soldier can get hurt

    def calculate_damage(self, soldier, curr_soldier_coordinates):
        if not self.damage_done:
            distance = math.sqrt(
                (self.rect.center[0] - curr_soldier_coordinates[0]) ** 2
                + (self.rect.center[1] - curr_soldier_coordinates[1]) ** 2
            )
            distance = math.floor(distance)
            # print("dist: ", distance)
            if distance > 40:
                damage = 0
            else:
                damage = 10 - (distance * 10 / 40)
            # print("damage: ", damage)
            soldier.decrease_health(damage)
            self.damage_done = True

    def update(self, soldier, soldier_cood):
        if self.type == 1:
            self.calculate_damage(soldier, soldier_cood)
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
    def __init__(self, init_x, init_y, display, lim_x, lim_y):
        self.lim_x = lim_x
        self.lim_y = lim_y
        self.init_x = init_x
        self.init_y = init_y
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bomb.png", -1, 0.05)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (init_x, init_y)
        self.display = display
        self.margin = 40
        self.target_coordinates = random_point_in_circle(
            (self.lim_x, self.lim_y), self.margin
        )
        self.angle = math.atan2(
            self.target_coordinates[1] - init_y,
            self.target_coordinates[0] - init_x,
        )

    def update(self, dt):
        # pygame.draw.line(
        #     DISPLAYSURF,
        #     "blue",
        #     (self.init_x, self.init_y),
        #     (
        #         self.target_coordinates[0],
        #         self.target_coordinates[1],
        #     ),
        # )
        center = calculate_new_xy_bomb(self.rect.center, bomb_speed, self.angle, dt)
        self.rect.center = round(center[0]), round(center[1])
        if self.rect.collidepoint(
            self.target_coordinates[0], self.target_coordinates[1]
        ):
            pygame.mixer.Sound.play(explosion_sound)
            new_explosion = Explosion(
                self.target_coordinates[0],
                self.target_coordinates[1],
                self.lim_x,
                self.lim_y,
                1,
            )
            explosion_group.add(new_explosion)
            self.kill()


def generate_bomb_coordinates():
    side = random.randint(1, 4)
    # side = 1
    coordinate_x = 0
    coordinate_y = 0
    # top, right, bottom, left
    if side == 1:
        coordinate_x = random.randint(0, disp_width)
    if side == 2:
        coordinate_x = disp_width
        coordinate_y = random.randint(0, disp_height)
    if side == 3:
        coordinate_y = disp_height
        coordinate_x = random.randint(0, disp_width)
    if side == 4:
        coordinate_y = random.randint(0, disp_height)
    return coordinate_x, coordinate_y


def random_point_in_circle(center, radius):
    print("center: ", center)
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(0, radius)
    x = math.floor(center[0] + r * math.cos(angle))
    y = math.floor(center[1] + r * math.sin(angle))
    print("x: ", x, ", y: ", y)
    return (x, y)
