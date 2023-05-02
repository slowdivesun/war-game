import pygame
import math
from constants import DISPLAYSURF, disp_height, explosion_sound
from groups import projectile_group, enemy_explosion_group
from bomb import Explosion
from load_image import load_image

projectile_angle = 45
projectile_velocity = 50
g = -9.8


class Projectile(pygame.sprite.Sprite):
    def __init__(self, soldier, start_time, vel):
        pygame.sprite.Sprite.__init__(self)
        self.soldier = soldier
        self.image, self.rect = load_image("bomb.png", -1, 0.03)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = soldier.rect.center[0], soldier.rect.center[1]
        self.velocity = vel
        self.right_facing = soldier.right_facing
        self.originx = soldier.rect.center[0]
        self.originy = soldier.rect.center[1]
        self.posx = self.originx
        self.posy = self.originy
        self.start_time = start_time
        self.angle = projectile_angle

    def update(self, now, dt):
        if not self.right_facing:
            self.angle = 135
        time_change = now - self.start_time
        # print("time_change = ", time_change, ", dt = ", dt)
        time_change /= 150.0

        if time_change > 0:
            new_pos = calculate_new_xy_projectile(
                self.velocity, math.radians(self.angle), time_change
            )
            self.posx = self.originx + new_pos[0]
            self.posy = self.originy - new_pos[1]
            self.rect.center = (round(self.posx), round(self.posy))
        if self.rect.y >= self.originy:
            self.rect.y = self.originy - self.rect.height
            self.velocity = 0
            self.kill()
        if not DISPLAYSURF.get_rect().contains(self.rect):
            self.kill()

    def enemy_explosion(self, x, y):
        pygame.mixer.Sound.play(explosion_sound)
        new_explosion = Explosion(x, y)
        enemy_explosion_group.add(new_explosion)
        self.kill()


def calculate_new_xy_projectile(vel, angle_radians, time_change):
    grav_time_square = g * time_change * time_change / 2.0
    displacement_x = vel * math.cos(angle_radians) * time_change
    displacement_y = vel * math.sin(angle_radians) * time_change + grav_time_square
    # print("displacements: ", displacement_x, displacement_y)
    return displacement_x, displacement_y


class Soldier(pygame.sprite.Sprite):
    def __init__(self, civ_target=0, bon_target=0, soldier_x=10, soldier_y=90):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("soldier.png", -1, 0.035)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 350, 300
        self.max_health = 10
        self.health = self.max_health
        self.civ_target = civ_target
        self.bon_target = bon_target
        self.bonus = 0
        self.civilians = 0
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

    def add_bonus(self):
        self.bonus += 1

    def add_civlian(self):
        self.civilians += 1

    def throw(self, start_time, vel=projectile_velocity):
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
            50,
            5,
        ),
    )
    pygame.draw.rect(
        DISPLAYSURF,
        (0, 128, 0),
        (
            sold.rect.center[0] - 3 * 15 / 2,
            sold.rect.topleft[1] - 10,
            ((50 / sold.max_health) * (sold.health)),
            5,
        ),
    )
