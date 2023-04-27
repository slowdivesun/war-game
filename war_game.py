import pygame, sys
import os
from pygame.locals import *
import math
from bomb import Bomb
from civilian import Civilian
from bonus import Bonus
from sliders import (
    CivilianSlider,
    BonusSlider,
    EnemySlider,
    CivilianTargetSlider,
    BonusTargetSlider,
)
import random
from load_image import load_image
from groups import explosion_group

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")
pygame.init()

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
sound_dir = os.path.join(main_dir, "sounds")
screen_shots_dir = os.path.join(main_dir, "saved_games_screen_shots")


def get_full_path(file):
    fullname = os.path.join(data_dir, file)
    return fullname


def get_full_path_ss(file):
    fullname = os.path.join(screen_shots_dir, file)
    return fullname


# Sound effects
civilian_sound = pygame.mixer.Sound("./sounds/civilian.wav")
bonus_sound = pygame.mixer.Sound("./sounds/coin.wav")
lost_sound = pygame.mixer.Sound("./sounds/gameover.wav")
won_sound = pygame.mixer.Sound("./sounds/won.wav")


# Create the Screen
disp_width = 900
disp_height = 600
DISPLAYSURF = pygame.display.set_mode((disp_width, disp_height))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


# Define Fonts
font = pygame.font.SysFont("bahnschrift", 30)  # NOTE: font size

# Define Constants
bullet_speed = 0.2
FPS = pygame.time.Clock()
begin = False


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    DISPLAYSURF.blit(img, (x, y))


e_slider = EnemySlider()
c_slider = CivilianSlider()
b_slider = BonusSlider()
ct_slider = CivilianTargetSlider()
bt_slider = BonusTargetSlider()


def draw_slider(s):
    pygame.draw.rect(DISPLAYSURF, GRAY, s.slider_rect)
    pygame.draw.circle(
        DISPLAYSURF,
        WHITE,
        (s.slider_knob_x, s.slider_knob_y),
        s.slider_knob_radius,
    )


def create_button(x, y, w, h, font, text, k, g, color=WHITE):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(DISPLAYSURF, color, button)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    DISPLAYSURF.blit(button_text, text_rect)
    return button


class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("target.png", -1, 0.1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 445, 210
        # NOTE: Draw border around rect
        # pygame.draw.rect(self.image, "red", self.image.get_rect(), 2)

        # NOTE: Color the rect
        # colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        # colorImage.fill("#848787")
        # self.image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def location(self):
        return self.rect.left, self.rect.top


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

    def location(self):
        return self.rect.left, self.rect.top


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

    def update(self, dt):
        center = calculate_new_xy(
            self.rect.center, bullet_speed, math.radians(self.angle), dt
        )
        self.rect.center = center
        # print(self.rect.center)
        # NOTE: Bullet leaves the screen
        if not DISPLAYSURF.get_rect().contains(self.rect):
            self.kill()


def calculate_new_xy(old_xy, speed, angle_in_radians, dt):
    new_x = old_xy[0] + (speed * math.cos(angle_in_radians) * dt)
    new_y = old_xy[1] - (speed * math.sin(angle_in_radians) * dt)
    return new_x, new_y


class Soldier(pygame.sprite.Sprite):
    def __init__(self, soldier_x=10, soldier_y=90):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("soldier.png", -1, 0.035)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.right_facing = True

    def restart(self):
        self.rect.topleft = 10, 90

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

    def location(self):
        return self.rect.left, self.rect.top


def draw_enemies(count):
    enemies = []
    left = 5
    top = 5
    img_width = load_image("enemy.png")[0].get_width() * 0.08

    for i in range(count):
        enemies.append(Enemy(left + (img_width + 2) * i, top))

    return enemies


def draw_civilians(count):
    civilians = []
    left = 5
    top = disp_height - 10 - load_image("enemy.png")[0].get_height() * 0.08
    img_width = load_image("civilian.png")[0].get_width() * 0.05

    for i in range(count):
        civilians.append(Civilian(left + (img_width + 40) * i, top))

    return civilians


def check_collision(new_x, new_y, ew, eh, targ):
    if new_x + ew > targ.rect.left - 2 and new_x + ew < targ.rect.right + 2:
        if new_y + eh > targ.rect.top - 2 and new_y + eh < targ.rect.bottom + 2:
            return True
        if new_y > targ.rect.top - 2 and new_y < targ.rect.bottom + 2:
            return True

    if new_x > targ.rect.left - 2 and new_x < targ.rect.right + 2:
        if new_y + eh > targ.rect.top - 2 and new_y + eh < targ.rect.bottom + 2:
            return True
        if new_y > targ.rect.top - 2 and new_y < targ.rect.bottom + 2:
            return True
    return False


def generate_bomb_coordinates():
    side = random.randint(1, 4)
    side = 1
    coordinate_x = 0
    coordinate_y = 0
    # top, right, bottom, left
    if side == 1:
        coordinate_x = random.randint(0, 900)
    if side == 2:
        coordinate_x = 900
        coordinate_y = random.randint(0, 600)
    if side == 3:
        coordinate_y = 600
        coordinate_x = random.randint(0, 900)
    if side == 4:
        coordinate_y = random.randint(0, 600)
    return coordinate_x, coordinate_y


def start():
    # Bullet Event
    milliseconds_delay = 2000  # 0.5 seconds
    bullet_event = pygame.USEREVENT + 1
    pygame.time.set_timer(bullet_event, milliseconds_delay)

    # Bomb Event
    bomb_delay = 3000
    bomb_event = pygame.USEREVENT + 2
    pygame.time.set_timer(bomb_event, bomb_delay)

    # Bomb Detonate Event
    detonate_event = pygame.USEREVENT + 3

    # Display parameters
    pygame.display.set_caption("War")
    pygame.mouse.set_visible(True)
    DISPLAYSURF.fill("#aaeebb")

    # Create The Background
    background = pygame.Surface(DISPLAYSURF.get_size())
    background.fill("#aaeebb")

    # Add bushes
    bush_img = pygame.image.load(get_full_path("bush.png"))
    # bush_img.convert_alpha() # bush_img.convert()
    bush_img = bush_img.copy()
    alpha = 128
    bush_img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    bush_img = pygame.transform.scale(bush_img, (60, 40))
    for y in range(0, 600, 40):
        for x in range(0, 900, 60):
            background.blit(bush_img, (x, y))
    pygame.display.flip()

    # Display The Background
    DISPLAYSURF.blit(background, (0, 0))
    pygame.display.flip()

    soldier = Soldier()
    target = Target()
    enemies = draw_enemies(e_slider.slider_value)
    civilians = draw_civilians(c_slider.slider_value)
    allsprites = pygame.sprite.RenderPlain((soldier, target))
    enemy_group = pygame.sprite.Group(tuple(enemies))
    civilian_group = pygame.sprite.Group(tuple(civilians))
    bullet_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()

    # create_button(550, 10, 120, 50, font, "Quit", 580, 15)

    game = True
    won = False
    killed = False
    is_selected = False
    selected_enemy = None
    direction = -1
    global begin
    begin_button = None
    restart_button = None
    rotate_left_button = None
    rotate_right_button = None
    menu_button = None
    flip_button = None

    while game:
        direction = -1
        # Game Won
        if soldier.rect.colliderect(target.rect):
            won = True
        if len(pygame.sprite.spritecollide(soldier, bullet_group, True)) > 0:
            killed = True
        if explosion_group.sprite != None:
            killed = True
        for event in pygame.event.get():
            # Make new bullets
            if (event.type == bullet_event) and begin and (not won) and (not killed):
                for enemy in enemy_group:
                    bullet = Bullet(enemy)
                    bullet_group.add(bullet)
            # Make new bombs
            if (event.type == bomb_event) and begin and (not won) and (not killed):
                coordinate_x, coordinate_y = generate_bomb_coordinates()
                sold_y = soldier.rect.center[1]
                sold_x = soldier.rect.center[0]
                bomb_angle = math.atan2(
                    sold_y - coordinate_y,
                    sold_x - coordinate_x,
                )
                bomb = Bomb(
                    bomb_angle,
                    coordinate_x,
                    coordinate_y,
                    DISPLAYSURF,
                    sold_x,
                    sold_y,
                )
                bomb_group.add(bomb)
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.K_ESCAPE:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 0
                elif event.key == pygame.K_DOWN:
                    direction = 1
                elif event.key == pygame.K_LEFT:
                    direction = 2
                elif event.key == pygame.K_RIGHT:
                    direction = 3
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                if event.button == 1:
                    for enemy in enemy_group:
                        if enemy.rect.collidepoint(pos):
                            enemy.clicked = True
                            enemy.selected = not enemy.selected
                            is_selected = enemy.selected
                            if is_selected:
                                selected_enemy = enemy
                            else:
                                selected_enemy = None
                        else:
                            enemy.selected = False
                if (begin_button != None) and (
                    begin_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = True
                    begin_button = None
                if (restart_button != None) and (
                    restart_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = True
                    won = False
                    killed = False
                    soldier.restart()
                    bomb_group.empty()
                    explosion_group.empty()
                    bullet_group.empty()
                    restart_button = None
                if (
                    (rotate_left_button != None)
                    and is_selected
                    and rotate_left_button.collidepoint(pygame.mouse.get_pos())
                ):
                    selected_enemy.change_angle(1)
                if (
                    (rotate_right_button != None)
                    and is_selected
                    and rotate_right_button.collidepoint(pygame.mouse.get_pos())
                ):
                    selected_enemy.change_angle(-1)
                if (
                    (flip_button != None)
                    and is_selected
                    and flip_button.collidepoint(pygame.mouse.get_pos())
                ):
                    selected_enemy.flip_enemy()
                if (menu_button != None) and (
                    menu_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = False
                    won = False
                    killed = False
                    bomb_group.empty()
                    explosion_group.empty()
                    bullet_group.empty()
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONUP:
                for enemy in enemy_group:
                    enemy.clicked = False

        # Move the enemy to desired position
        if not begin:
            for enemy in enemy_group:
                if enemy.clicked:
                    pos = pygame.mouse.get_pos()
                    new_x = pos[0] - (enemy.rect.width / 2)
                    new_y = pos[1] - (enemy.rect.height / 2)
                    ew = enemy.rect.width
                    eh = enemy.rect.height

                    if not check_collision(new_x, new_y, ew, eh, target):
                        enemy.left = pos[0] - (enemy.rect.width / 2)
                        enemy.top = pos[1] - (enemy.rect.height / 2)
                        enemy.rect.topleft = pos[0] - (enemy.rect.width / 2), pos[1] - (
                            enemy.rect.height / 2
                        )
        # update bomb target coordinates
        for b in bomb_group:
            b.lim_x = soldier.rect.center[0]
            b.lim_y = soldier.rect.center[1]

        # Time Elapsed
        dt = FPS.tick(60)

        # Draw Everything
        DISPLAYSURF.blit(background, (0, 0))
        allsprites.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        civilian_group.draw(DISPLAYSURF)
        bullet_group.draw(DISPLAYSURF)
        bomb_group.draw(DISPLAYSURF)
        explosion_group.draw(DISPLAYSURF)

        # Call Update Function of all Sprites
        # Don't draw buttons if game has begun
        if (begin) and (not won) and (not killed):
            allsprites.update(direction)
            bullet_group.update(dt)
            bomb_group.update(dt)
            explosion_group.update()

        # Buttons to start the game and change parameters
        if not begin:
            begin_button = create_button(
                650, 500, 100, 40, font, "Begin", 680, 505, (17, 125, 28)
            )
            if is_selected:
                rotate_left_button = create_button(
                    450, 500, 150, 40, font, "Rotate(L)", 680, 505, (17, 125, 28)
                )
                rotate_right_button = create_button(
                    250, 500, 150, 40, font, "Rotate(R)", 680, 505, (17, 125, 28)
                )
                flip_button = create_button(
                    50, 500, 100, 40, font, "Flip", 680, 505, (17, 125, 28)
                )
            else:
                rotate_left_button = create_button(
                    450, 500, 150, 40, font, "Rotate(L)", 680, 505, (96, 102, 97)
                )
                rotate_right_button = create_button(
                    250, 500, 150, 40, font, "Rotate(R)", 680, 505, (96, 102, 97)
                )
                flip_button = create_button(
                    50, 500, 100, 40, font, "Flip", 680, 505, (96, 102, 97)
                )

        # Display restart button if game has ended
        if won or killed:
            restart_button = create_button(
                650, 500, 120, 40, font, "Restart", 680, 505, (17, 125, 28)
            )
            menu_button = create_button(
                450, 500, 120, 40, font, "Menu", 680, 505, (17, 125, 28)
            )

        if won:
            pass

        if killed:
            pass

        pygame.display.flip()

    pygame.quit()


def main_menu():
    pygame.display.set_caption("Settings")
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill("#aaeebb")

    # Display The Background
    DISPLAYSURF.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        DISPLAYSURF.blit(background, (0, 0))
        draw_slider(e_slider)
        draw_slider(c_slider)
        draw_slider(b_slider)
        draw_slider(ct_slider)
        draw_slider(bt_slider)
        button1 = create_button(
            380, 500, 120, 50, pygame.font.SysFont("Arial", 30), "START", 410, 505
        )
        menu_btn_width = 150
        create_button(
            disp_width / 10 - menu_btn_width / 2,
            150,
            menu_btn_width,
            50,
            font,
            "Obstacles",
            114.5,
            155,
        )
        create_button(
            disp_width / 10 - menu_btn_width / 2,
            240,
            menu_btn_width,
            50,
            font,
            "Bonus",
            114.5,
            155,
        )
        create_button(
            disp_width / 10 - menu_btn_width / 2,
            330,
            menu_btn_width,
            50,
            font,
            "Civilians",
            114.5,
            155,
        )
        buttons = [button1]  # NOTE: removed button3,button4 from list
        draw_text("Choose parameters", font, (255, 255, 255), 340, 10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:  # if left button is pressed
                    if e_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        e_slider.slider_value = e_slider.find_value(event)
                    if b_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        b_slider.slider_value = b_slider.find_value(event)
                    if c_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        c_slider.slider_value = c_slider.find_value(event)

            elif event.type == MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.collidepoint(pygame.mouse.get_pos()):
                        if btn == button1:
                            start()
                        # elif btn == button3:
                        # elif btn == button4:

        draw_text(
            str(e_slider.slider_value),
            font,
            WHITE,
            e_slider.slider_knob_x - 10,
            e_slider.slider_y - 40,
        )
        draw_text(
            str(b_slider.slider_value),
            font,
            WHITE,
            b_slider.slider_knob_x - 10,
            b_slider.slider_y - 40,
        )
        draw_text(
            str(c_slider.slider_value),
            font,
            WHITE,
            c_slider.slider_knob_x - 10,
            c_slider.slider_y - 40,
        )
        pygame.display.update()


main_menu()
