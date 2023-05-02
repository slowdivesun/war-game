import pygame
from load_image import load_image
import math
from constants import WHITE

bullet_speed = 0.2


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
        new_angle = math.atan2(self.rect.center[1] - y, x - self.rect.center[0])
        new_angle = math.degrees(new_angle)

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
        # pygame.draw.line(
        #     surf, "red", (x, y), (self.rect.center[0], self.rect.center[1])
        # )
        # pygame.draw.line(
        #     surf,
        #     "blue",
        #     (self.rect.center[0], self.rect.center[1]),
        #     (
        #         self.rect.center[0] + math.cos(math.radians(self.angle)) * 900,
        #         self.rect.center[1] - math.sin(math.radians(self.angle)) * 900,
        #     ),
        # )
        pass

    def killed(self):
        self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        enemy,
    ):
        self.enemy = enemy
        self.angle = self.enemy.angle
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bullet.png", -1, 0.02, self.angle)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = (
            self.enemy.rect.center[0]
            + (self.enemy.rect.width / 2) * math.cos(math.radians(self.angle)),
            self.enemy.rect.center[1]
            - (self.enemy.rect.height / 2) * math.sin(math.radians(self.angle))
            - (self.rect.height / 2) * math.sin(math.radians(self.angle)),
        )
        self.isRandom = enemy.isRandom
        self.positionx = self.rect.center[0]
        self.positiony = self.rect.center[1]

    def update(self, dt, x, y, surf):
        # original
        # center = calculate_new_xy(
        #     self.rect.center, bullet_speed, math.radians(self.angle), dt
        # )
        # self.rect.center = center
        # pygame.draw.line(
        #     surf, WHITE, (self.rect.center[0], self.rect.center[1]), (x, y)
        # )
        center = calculate_new_xy(
            (self.positionx, self.positiony), bullet_speed, math.radians(self.angle), dt
        )
        self.positionx = center[0]
        self.positiony = center[1]
        self.rect.center = (round(self.positionx), round(self.positiony))
        # print(self.rect.center)
        # NOTE: Bullet leaves the screen
        if not surf.get_rect().contains(self.rect):
            self.kill()


def calculate_new_xy(old_xy, speed, angle_in_radians, dt):
    new_x = old_xy[0] + (speed * math.cos(angle_in_radians) * dt)
    new_y = old_xy[1] - (speed * math.sin(angle_in_radians) * dt)
    return new_x, new_y
