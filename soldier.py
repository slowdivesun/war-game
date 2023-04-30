import pygame
import math
from constants import DISPLAYSURF
from groups import projectile_group
from load_image import load_image

projectile_angle = 45


class Projectile(pygame.sprite.Sprite):
    def __init__(self, soldier, start_time, vel):
        pygame.sprite.Sprite.__init__(self)
        self.soldier = soldier
        self.image, self.rect = load_image("bomb.png", -1, 0.03)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = soldier.rect.topleft[0], soldier.rect.topleft[1]
        self.velocity = vel
        self.right_facing = soldier.right_facing
        self.posx = self.rect.center[0]
        self.posy = self.rect.center[1]
        self.start_time = start_time

    def update(self, now):
        angle = 45
        if not self.right_facing:
            angle = 135
        time_change = now - self.start_time
        if time_change > 0:
            time_change /= 100
            new_pos = calculate_new_xy_projectile(
                self.velocity, math.radians(angle), time_change
            )
            self.posx += new_pos[0]
            self.posy -= new_pos[1]
            self.rect.center = (round(self.posx), round(self.posy))
        if not DISPLAYSURF.get_rect().contains(self.rect):
            self.kill()


def calculate_new_xy_projectile(speed, angle_radians, dt):
    print("Speed: ", speed, speed * math.cos(angle_radians))
    displacement_x = speed * math.cos(angle_radians) * dt
    displacement_y = speed * math.sin(angle_radians) * dt - 0.5 * 9.8 * dt * dt
    print("displacements: ", displacement_x, displacement_y)
    return displacement_x, displacement_y


class Soldier(pygame.sprite.Sprite):
    def __init__(self, soldier_x=10, soldier_y=90):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("soldier.png", -1, 0.035)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 350, 300
        self.health = 3
        self.move = 18
        self.right_facing = True

    def restart(self):
        self.rect.topleft = 350, 300
        self.health = 3

    def update(self, direction):
        if direction == 2 and self.right_facing == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.right_facing = False
        if direction == 3 and self.right_facing == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.right_facing = True
        if direction != -1:
            self._walk(direction)

    def _walk(self, direction):
        newpos = self.rect.move((0, 0))
        if direction == 0:  # UP
            if self.rect.top != self.area.top:
                newpos = self.rect.move((0, -10))
        elif direction == 1:  # DOWN
            if self.rect.bottom != self.area.bottom:
                newpos = self.rect.move((0, 10))
        elif direction == 2:
            if self.rect.left != self.area.left:
                newpos = self.rect.move((-10, 0))
        else:
            if self.rect.right != self.area.right:
                newpos = self.rect.move((10, 0))

        self.rect = newpos

    def throw(self, start_time, vel=15):
        new_proj = Projectile(self, start_time, vel)
        projectile_group.add(new_proj)

    def location(self):
        return self.rect.left, self.rect.top


def display_health(sold):
    pygame.draw.rect(
        DISPLAYSURF,
        (255, 0, 0),
        pygame.Rect(
            sold.rect.center[0] - 3 * 15 / 2,
            sold.rect.topleft[1] - 10,
            3 * 15,
            5,
        ),
    )
    pygame.draw.rect(
        DISPLAYSURF,
        (0, 128, 0),
        (
            sold.rect.center[0] - 3 * 15 / 2,
            sold.rect.topleft[1] - 10,
            (15 * (sold.health)),
            5,
        ),
    )
