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
from draw_functions import *
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
BTN_GRAY = (17, 125, 28)
BTN_GREEN = (96, 102, 97)


# Define Fonts
font = pygame.font.SysFont("bahnschrift", 30)  # NOTE: font size
emoji_font = pygame.font.SysFont("segoeuisymbol", 30)

# Define Constants
bullet_speed = 0.2
FPS = pygame.time.Clock()
begin = False
checked = True

# Button Parameters
settings_btn_width = 150
settings_btn_height = 40
small_btn_width = 75
flip_btn_order = 0
rotater_btn_order = 1
rotatel_btn_order = 1.5
begin_btn_order = 2
back_btn_order = 3
info_btn_order = 3.5
small_btn_col_width = disp_width / 10
btn_col_width = disp_width / 5
btn_row_height = disp_height / 8
btn_row_top_margin = 7 * btn_row_height
btn_y = btn_row_top_margin + btn_row_height / 2


# def draw_text(text, font, text_color, x, y):
#     img = font.render(text, True, text_color)
#     DISPLAYSURF.blit(img, (x - img.get_width() / 2, y))


e_slider = EnemySlider()
c_slider = CivilianSlider()
b_slider = BonusSlider()
ct_slider = CivilianTargetSlider(c_slider)
bt_slider = BonusTargetSlider(b_slider)
all_sliders = [e_slider, c_slider, b_slider, ct_slider, bt_slider]


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


def create_button_new(
    x, y, w, h, font, text, k, g, color=(0, 0, 0), back_col=(255, 255, 255)
):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(DISPLAYSURF, back_col, button)
    button_text = font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    DISPLAYSURF.blit(button_text, text_rect)
    return button


def create_button_center(x, y, w, h, font, text, k, g, color=WHITE):
    button = pygame.Rect(x - w / 2, y - h / 2, w, h)
    pygame.draw.rect(DISPLAYSURF, color, button)
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x, y))
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
        print("in radian: ", new_angle)
        new_angle = math.degrees(new_angle)
        print("in degrees: ", new_angle)

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
        self.rect.topleft = 350, 300
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
    top = (3 * disp_height / 4) - 10 - load_image("civilian.png")[0].get_height() * 0.05
    img_width = load_image("civilian.png")[0].get_width() * 0.05

    for i in range(count):
        civilians.append(Civilian(left + (img_width + 40) * i, top))

    return civilians


def draw_bonuses(count):
    bonuses = []
    left = 5
    top = (
        (3 * disp_height / 4)
        - 20
        - load_image("civilian.png")[0].get_height() * 0.05
        - load_image("coin.png")[0].get_height() * 0.08
    )
    img_width = load_image("coin.png")[0].get_width() * 0.08

    for i in range(count):
        bonuses.append(Bonus(left + (img_width + 30) * i, top, 5))

    return bonuses


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
    # side = 1
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
    bonuses = draw_bonuses(b_slider.slider_value)
    civilian_target = ct_slider.slider_value
    bonus_target = bt_slider.slider_value
    soldier_group = pygame.sprite.Group((soldier))
    target_group = pygame.sprite.Group((target))
    enemy_group = pygame.sprite.Group(tuple(enemies))
    civilian_group = pygame.sprite.Group(tuple(civilians))
    bonus_group = pygame.sprite.Group(tuple(bonuses))
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
    back_button = None
    info_button = None

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
                sold_y = soldier.rect.center[1]
                sold_x = soldier.rect.center[0]
                for enemy in enemy_group:
                    enemy.random_reorientation(sold_x, sold_y)
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
                # bomb_group.add(bomb)
            if event.type == pygame.QUIT:
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
                elif event.key == pygame.K_r:
                    for civ in civilian_group:
                        if civ.incident:
                            civ.rescued()
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
                    for civ in civilian_group:
                        if civ.rect.collidepoint(pos):
                            civ.clicked = True
                if (begin_button != None) and (
                    begin_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = True
                    begin_button = None
                    restart_button = None
                    rotate_left_button = None
                    rotate_right_button = None
                    menu_button = None
                    flip_button = None
                    back_button = None
                    info_button = None
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
                    new_main_menu()
                if (back_button != None) and (
                    back_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = False
                    won = False
                    killed = False
                    bomb_group.empty()
                    explosion_group.empty()
                    bullet_group.empty()
                if (info_button != None) and (
                    info_button.collidepoint(pygame.mouse.get_pos())
                ):
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                for enemy in enemy_group:
                    enemy.clicked = False
                for civ in civilian_group:
                    civ.clicked = False

        # Move the enemies, civilians and bonuses to desired position
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
            for civ in civilian_group:
                if civ.clicked:
                    pos = pygame.mouse.get_pos()
                    new_x = pos[0] - (civ.rect.width / 2)
                    new_y = pos[1] - (civ.rect.height / 2)
                    ew = civ.rect.width
                    eh = civ.rect.height
                    if not check_collision(new_x, new_y, ew, eh, target):
                        civ.left = pos[0] - (civ.rect.width / 2)
                        civ.top = pos[1] - (civ.rect.height / 2)
                        civ.rect.topleft = pos[0] - (civ.rect.width / 2), pos[1] - (
                            civ.rect.height / 2
                        )

        # update bomb target coordinates
        for b in bomb_group:
            b.lim_x = soldier.rect.center[0]
            b.lim_y = soldier.rect.center[1]

        # Time Elapsed
        dt = FPS.tick(60)

        # Draw Everything
        DISPLAYSURF.blit(background, (0, 0))
        if not killed:
            soldier_group.draw(DISPLAYSURF)
        target_group.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        bonus_group.draw(DISPLAYSURF)
        civilian_group.draw(DISPLAYSURF)
        bullet_group.draw(DISPLAYSURF)
        bomb_group.draw(DISPLAYSURF)
        explosion_group.draw(DISPLAYSURF)

        # Call Update Function of all Sprites
        # Don't draw buttons if game has begun
        if (begin) and (not won) and (not killed):
            soldier_group.update(direction)
            bullet_group.update(dt)
            bomb_group.update(dt)
            for civ in civilian_group:
                if civ.rect.colliderect(soldier.rect):
                    civ.incident = True
                else:
                    civ.incident = False
        if begin and (not won):
            explosion_group.update()

        # Buttons to start the game and change parameters
        if not begin:
            begin_button = create_button_center(
                begin_btn_order * (btn_col_width) + (btn_col_width / 2),
                btn_y,
                settings_btn_width,
                settings_btn_height,
                font,
                "Begin",
                680,
                505,
                BTN_GRAY,
            )
            back_button = create_button_center(
                back_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                btn_y,
                small_btn_width,
                settings_btn_height,
                pygame.font.SysFont("segoeuisymbol", 30),
                "\U00002B05",
                680,
                505,
                (199, 95, 95),
            )
            info_button = create_button_center(
                info_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                btn_y,
                small_btn_width,
                settings_btn_height,
                pygame.font.SysFont("segoeuisymbol", 30),
                "\U00002139",
                680,
                505,
                (63, 60, 230),
            )
            if is_selected:
                rotate_left_button = create_button_center(
                    rotatel_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                    btn_y,
                    small_btn_width,
                    settings_btn_height,
                    emoji_font,
                    "\U000021AA",
                    680,
                    505,
                    BTN_GRAY,
                )
                rotate_right_button = create_button_center(
                    rotater_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                    btn_y,
                    small_btn_width,
                    settings_btn_height,
                    emoji_font,
                    "\U000021A9",
                    680,
                    505,
                    BTN_GRAY,
                )
                flip_button = create_button_center(
                    flip_btn_order * (btn_col_width) + (btn_col_width / 2),
                    btn_y,
                    settings_btn_width,
                    settings_btn_height,
                    font,
                    "Flip",
                    680,
                    505,
                    BTN_GRAY,
                )
            else:
                rotate_left_button = create_button_center(
                    rotatel_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                    btn_y,
                    small_btn_width,
                    settings_btn_height,
                    emoji_font,
                    "\U000021AA",
                    680,
                    505,
                    BTN_GREEN,
                )
                rotate_right_button = create_button_center(
                    rotater_btn_order * (btn_col_width) + (small_btn_col_width / 2),
                    btn_y,
                    small_btn_width,
                    settings_btn_height,
                    emoji_font,
                    "\U000021A9",
                    680,
                    505,
                    BTN_GREEN,
                )
                flip_button = create_button_center(
                    flip_btn_order * (btn_col_width) + (btn_col_width / 2),
                    btn_y,
                    settings_btn_width,
                    settings_btn_height,
                    font,
                    "Flip",
                    680,
                    505,
                    BTN_GREEN,
                )

        # Display restart button if game has ended
        if won or killed:
            restart_button = create_button(
                650, 500, 120, 40, font, "Restart", 680, 505, BTN_GRAY
            )
            menu_button = create_button(
                450, 500, 120, 40, font, "Menu", 680, 505, BTN_GRAY
            )

        if won:
            pass

        if killed:
            pass

        pygame.display.flip()

    pygame.quit()


# def main_menu():
#     pygame.display.set_caption("Settings")
#     background = pygame.Surface(DISPLAYSURF.get_size())
#     background = background.convert()
#     background.fill("#aaeebb")

#     # Display The Background
#     DISPLAYSURF.blit(background, (0, 0))
#     pygame.display.flip()

#     while True:
#         DISPLAYSURF.blit(background, (0, 0))
#         draw_slider(e_slider)
#         draw_slider(c_slider)
#         draw_slider(b_slider)
#         draw_slider(ct_slider)
#         draw_slider(bt_slider)
#         button1 = create_button(
#             380, 500, 120, 50, pygame.font.SysFont("Arial", 30), "START", 410, 505
#         )
#         menu_btn_width = 150
#         create_button(
#             disp_width / 10 - menu_btn_width / 2,
#             150,
#             menu_btn_width,
#             50,
#             font,
#             "Obstacles",
#             114.5,
#             155,
#         )
#         create_button(
#             disp_width / 10 - menu_btn_width / 2,
#             240,
#             menu_btn_width,
#             50,
#             font,
#             "Bonus",
#             114.5,
#             155,
#         )
#         create_button(
#             disp_width / 10 - menu_btn_width / 2,
#             330,
#             menu_btn_width,
#             50,
#             font,
#             "Civilians",
#             114.5,
#             155,
#         )
#         buttons = [button1]  # NOTE: removed button3,button4 from list
#         draw_text("Choose parameters", font, (255, 255, 255), disp_width / 2, 10)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()

#             elif event.type == pygame.MOUSEMOTION:
#                 if event.buttons[0] == 1:  # if left button is pressed
#                     if e_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
#                         e_slider.slider_value = e_slider.find_value(event)
#                     if b_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
#                         b_slider.slider_value = b_slider.find_value(event)
#                         bt_slider.update()
#                     if c_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
#                         c_slider.slider_value = c_slider.find_value(event)
#                         ct_slider.update()
#                     if ct_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
#                         ct_slider.slider_value = ct_slider.find_value(event)
#                     if bt_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
#                         bt_slider.slider_value = bt_slider.find_value(event)

#             elif event.type == MOUSEBUTTONDOWN:
#                 for btn in buttons:
#                     if btn.collidepoint(pygame.mouse.get_pos()):
#                         if btn == button1:
#                             start()
#                         # elif btn == button3:
#                         # elif btn == button4:

#         draw_text(
#             str(e_slider.slider_value),
#             font,
#             WHITE,
#             e_slider.slider_knob_x,
#             e_slider.slider_y - 40,
#         )
#         draw_text(
#             str(b_slider.slider_value),
#             font,
#             WHITE,
#             b_slider.slider_knob_x,
#             b_slider.slider_y - 40,
#         )
#         draw_text(
#             str(c_slider.slider_value),
#             font,
#             WHITE,
#             c_slider.slider_knob_x,
#             c_slider.slider_y - 40,
#         )
#         draw_text(
#             str(ct_slider.slider_value),
#             font,
#             WHITE,
#             ct_slider.slider_knob_x,
#             ct_slider.slider_y - 40,
#         )
#         draw_text(
#             str(bt_slider.slider_value),
#             font,
#             WHITE,
#             bt_slider.slider_knob_x,
#             bt_slider.slider_y - 40,
#         )
#         pygame.display.update()


def go_settings():
    pygame.display.set_caption("Settings")

    global checked

    # Load the background image
    background_image = pygame.image.load(get_full_path("backl.jpg"))
    background_image.set_alpha(150)
    background_image = pygame.transform.scale(background_image, (900, 600))
    # Create a surface for the background image
    background = pygame.Surface(DISPLAYSURF.get_size())
    # Draw the background image onto the surface
    background.blit(background_image, (0, 0))

    # Define the rectangle
    rect = pygame.Rect(0, disp_height / 7, disp_width, 5 * disp_height / 7)
    rect_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    apply = pygame.Rect(
        disp_width / 8 - 75, (5 * disp_height / 7 + disp_height / 14) - 20, 150, 40
    )
    apply_surf = pygame.Surface((apply.width, apply.height), pygame.SRCALPHA)
    cancel = pygame.Rect(
        3 * disp_width / 8 - 75, (5 * disp_height / 7 + disp_height / 14) - 20, 150, 40
    )
    cancel_surf = pygame.Surface((cancel.width, cancel.height), pygame.SRCALPHA)
    apply_text = font.render("APPLY", True, (255, 255, 255))
    apply_text_rect = apply_text.get_rect(center=(apply.width // 2, apply.height // 2))
    cancel_text = font.render("CANCEL", True, (255, 255, 255))
    cancel_text_rect = cancel_text.get_rect(
        center=(cancel.width // 2, cancel.height // 2)
    )
    checkbox_rect = pygame.Rect(
        15 * disp_width / 16 - 15,
        (5 * disp_height / 7) + (disp_height / 14) - 15,
        30,
        30,
    )

    # Define the checkbox colors
    unchecked_color = (255, 255, 255)
    checked_color = (0, 255, 0)
    border_color = (0, 0, 0)

    # Set the initial checkbox state to unchecked
    running = True
    temp_checked = checked
    menu_btn_width = 150

    # CONSTANTS
    top_margin = disp_height / 7
    division = disp_height / 7
    slider_row_height = (4 * division) / 3
    slider_row_width = (2 * disp_width) / 5

    while running:
        DISPLAYSURF.blit(background, (0, 0))
        draw_slider(e_slider)
        draw_slider(c_slider)
        draw_slider(b_slider)
        draw_slider(ct_slider)
        draw_slider(bt_slider)
        pygame.draw.line(
            DISPLAYSURF,
            "white",
            (0, 5 * disp_height / 7),
            (disp_width, 5 * disp_height / 7),
        )  # DEBUG

        DISPLAYSURF.blit(
            rect_surf, (0, disp_height / 7)
        )  # this is the light background

        draw_text_middle(
            "OBSTACLES :",
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            disp_width / 10,
            top_margin + 0 * slider_row_height + slider_row_height / 2,
            DISPLAYSURF,
        )
        draw_text_middle(
            "BONUS :",
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            disp_width / 10,
            top_margin + 1 * slider_row_height + slider_row_height / 2,
            DISPLAYSURF,
        )
        draw_text_middle(
            "CIVILIANS :",
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            disp_width / 10,
            top_margin + 2 * slider_row_height + slider_row_height / 2,
            DISPLAYSURF,
        )
        pygame.draw.rect(
            rect_surf,
            (51, 51, 51, 180),
            pygame.Rect(0, 0, rect_surf.get_width(), rect_surf.get_height()),
        )
        pygame.draw.rect(
            apply_surf,
            (51, 51, 51, 220),
            pygame.Rect(0, 0, apply_surf.get_width(), apply_surf.get_height()),
        )
        pygame.draw.rect(
            cancel_surf,
            (51, 51, 51, 220),
            pygame.Rect(0, 0, cancel_surf.get_width(), cancel_surf.get_height()),
        )
        draw_text_middle(
            "SETTINGS",
            pygame.font.SysFont("Arial", 25),
            "#ffffff",
            disp_width / 2,
            disp_height / 14,
            DISPLAYSURF,
        )

        for s in all_sliders:
            draw_slider(s)
            s.draw_text_min(
                DISPLAYSURF,
                pygame.font.SysFont("BOLD", 30),
                GRAY,
            )
            s.draw_text_max(
                DISPLAYSURF,
                pygame.font.SysFont("BOLD", 30),
                GRAY,
            )
            pygame.draw.circle(
                DISPLAYSURF,
                (255, 255, 255),
                (
                    s.slider_knob_x,
                    s.slider_knob_y - 20 - 1 - slider_row_height * (2 / 5) * (1 / 2),
                ),
                20,
                4,
            )
            draw_text_middle(
                str(s.slider_value),
                pygame.font.SysFont("Arial", 20),
                WHITE,
                s.slider_knob_x,
                s.slider_knob_y - 20 - 1 - slider_row_height * (2 / 5) * (1 / 2),
                DISPLAYSURF,
            )

        draw_text_right_align(
            "Show Tutorial",
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            (7 * disp_width / 8),
            (5 * disp_height / 7 + disp_height / 14),
            DISPLAYSURF,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:  # if left button is pressed
                    # move slider knob
                    if e_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        e_slider.slider_value = e_slider.find_value(event)
                    if b_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        b_slider.slider_value = b_slider.find_value(event)
                        bt_slider.update()
                    if c_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        c_slider.slider_value = c_slider.find_value(event)
                        ct_slider.update()
                    if ct_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        ct_slider.slider_value = ct_slider.find_value(event)
                    if bt_slider.slider_rect.collidepoint(pygame.mouse.get_pos()):
                        bt_slider.slider_value = bt_slider.find_value(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse click was inside the checkbox
                if checkbox_rect.collidepoint(event.pos):
                    temp_checked = not checked
                if apply.collidepoint(event.pos):
                    checked = temp_checked
                    new_main_menu()
                if cancel.collidepoint(event.pos):
                    #   slider_value=temp_value
                    new_main_menu()

        # Draw the checkbox
        if temp_checked:
            pygame.draw.rect(DISPLAYSURF, checked_color, checkbox_rect)
            pygame.draw.line(
                DISPLAYSURF,
                border_color,
                (checkbox_rect.left + 10, checkbox_rect.centery),
                (checkbox_rect.centerx, checkbox_rect.bottom - 10),
                3,
            )
            pygame.draw.line(
                DISPLAYSURF,
                border_color,
                (checkbox_rect.centerx, checkbox_rect.bottom - 10),
                (checkbox_rect.right - 10, checkbox_rect.top + 10),
                3,
            )
        else:
            pygame.draw.rect(DISPLAYSURF, unchecked_color, checkbox_rect)
        pygame.draw.rect(DISPLAYSURF, border_color, checkbox_rect, 3)

        cancel_surf.blit(cancel_text, cancel_text_rect)
        DISPLAYSURF.blit(
            cancel_surf,
            (3 * disp_width / 8 - 75, (5 * disp_height / 7 + disp_height / 14) - 20),
        )
        apply_surf.blit(apply_text, apply_text_rect)
        DISPLAYSURF.blit(
            apply_surf,
            (disp_width / 8 - 75, (5 * disp_height / 7 + disp_height / 14) - 20),
        )
        pygame.display.update()

    pygame.quit()


def intermediate():
    # Set up the screen
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Get Ready to War!")
    text = "Commander : Welcome Soldier!Here is your mission, you have to reach the target which is located at (,) and you are at (,).Reach the target and escape from the enemy base at the same time.The target is surrounded by the red rectance in the picture."
    intro_img = pygame.image.load(get_full_path("intro.png"))
    intro_img = pygame.transform.scale(intro_img, (400, 480))

    # Split the text into lines based on screen width
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if font.size(line + " " + word)[0] > screen.get_width() - 430:
            lines.append(line.strip())
            line = ""
        line += " " + word
    lines.append(line.strip())
    clock = pygame.time.Clock()
    index = 0
    j = 0
    surfaces = []
    y = 0
    while True:
        screen.fill("#889988")
        clock.tick(50)
        Play = create_button(
            400,
            525,
            120,
            50,
            pygame.font.SysFont(None, 36),
            "Play!",
            410,
            530,
            screen,
            WHITE,
            "#964F4CFF",
        )
        if Play.collidepoint(pygame.mouse.get_pos()):
            Play = create_button(
                400,
                525,
                120,
                50,
                pygame.font.SysFont(None, 38),
                "Play",
                410,
                530,
                screen,
                "#696667FF",
                WHITE,
            )
        else:
            Play = create_button(
                400,
                525,
                120,
                50,
                pygame.font.SysFont(None, 36),
                "Play",
                410,
                530,
                screen,
                WHITE,
                "#964F4CFF",
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Play.collidepoint(pygame.mouse.get_pos()):
                    # Start the game
                    start()

        # Draw the text surface to the screen

        # Update the text surface
        index += 1
        screen.blit(intro_img, (500, 0))
        if j < len(lines):
            if index > len(lines[j]):
                index = 0
                j += 1
            if j < len(lines):
                text_surface = font.render(lines[j][:index], True, (0, 0, 0))

        if len(surfaces) > 0:
            for k in range(len(surfaces)):
                screen.blit(surfaces[k], (30, 40 + 40 * k))
                y = k + 1
        if j < len(lines):
            if index + 1 > len(lines[j]):
                surfaces += [text_surface]
        if j < len(lines):
            screen.blit(text_surface, (30, 40 + 40 * y))

        pygame.display.update()


def new_main_menu():
    global checked
    global slider_value
    pygame.display.set_caption("Main Page")
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    # Display The Background
    DISPLAYSURF.blit(background, (0, 0))
    home_img = pygame.image.load(get_full_path("soldier_home.png"))
    home_img = pygame.transform.scale(home_img, (450, 400))
    icon_img = pygame.image.load(get_full_path("icon.png"))
    icon_img = pygame.transform.scale(icon_img, (130, 80))
    background1 = pygame.Surface((900, 520))
    background1.fill("#333333")
    while True:  # main game loop
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(background1, (0, 80))
        background1.blit(home_img, (25, 10))
        DISPLAYSURF.blit(icon_img, (10, 0))
        starts = create_button_new(
            600,
            330,
            140,
            35,
            pygame.font.SysFont("Arial", 23),
            "START",
            630,
            335,
            (255, 255, 255),
            "#ed5e3e",
        )
        if starts.collidepoint(pygame.mouse.get_pos()):
            starts = create_button_new(
                600,
                330,
                140,
                35,
                pygame.font.SysFont("Arial", 23),
                "START",
                630,
                335,
                (255, 255, 255),
                "#f9430a",
            )
        else:
            starts = create_button_new(
                600,
                330,
                140,
                35,
                pygame.font.SysFont("Arial", 23),
                "START",
                630,
                335,
                (255, 255, 255),
                "#ed5e3e",
            )
        settings = create_button_new(
            620,
            0,
            130,
            80,
            pygame.font.SysFont("BOLD", 25),
            "SETTINGS",
            630,
            30,
            (255, 255, 255),
            (0, 0, 0),
        )
        if settings.collidepoint(pygame.mouse.get_pos()):
            settings = create_button_new(
                620,
                0,
                130,
                80,
                pygame.font.SysFont("BOLD", 25),
                "SETTINGS",
                630,
                30,
                (255, 255, 255),
                "#232023",
            )
        else:
            settings = create_button_new(
                620,
                0,
                130,
                80,
                pygame.font.SysFont("BOLD", 25),
                "SETTINGS",
                630,
                30,
                (255, 255, 255),
                (0, 0, 0),
            )
        about = create_button_new(
            750,
            0,
            130,
            80,
            pygame.font.SysFont("BOLD", 25),
            "ABOUT",
            780,
            30,
            (255, 255, 255),
            (0, 0, 0),
        )
        if about.collidepoint(pygame.mouse.get_pos()):
            about = create_button_new(
                750,
                0,
                130,
                80,
                pygame.font.SysFont("BOLD", 25),
                "ABOUT",
                780,
                30,
                (255, 255, 255),
                "#232023",
            )
        else:
            about = create_button_new(
                750,
                0,
                130,
                80,
                pygame.font.SysFont("BOLD", 25),
                "ABOUT",
                780,
                30,
                (255, 255, 255),
                (0, 0, 0),
            )
        games = create_button_new(
            430, 460, 160, 32, pygame.font.SysFont("Arial", 23), "Saved Games", 450, 465
        )

        buttons = [starts, games, settings, about]
        draw_text(
            "HOME", pygame.font.SysFont("BOLD", 25), "#f9430a", 530, 30, DISPLAYSURF
        )
        draw_text(
            "UNLEASH YOUR",
            pygame.font.SysFont("impact", 35),
            (255, 255, 255),
            590,
            180,
            DISPLAYSURF,
        )
        draw_text(
            "INNER",
            pygame.font.SysFont("impact", 35),
            (255, 255, 255),
            590,
            230,
            DISPLAYSURF,
        )
        draw_text(
            "WARRIOR",
            pygame.font.SysFont("impact", 35),
            "#f9430a",
            680,
            230,
            DISPLAYSURF,
        )
        draw_text(
            "OBSTACLES :",
            pygame.font.SysFont("BOLD", 30),
            "#f9430a",
            300,
            330,
            DISPLAYSURF,
        )
        draw_text(
            str(e_slider.slider_value),
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            440,
            330,
            DISPLAYSURF,
        )
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.collidepoint(pygame.mouse.get_pos()):
                        if btn == starts:
                            if checked:
                                intermediate()
                            else:
                                start()
                        elif btn == about:
                            # about_us()
                            pass
                            pygame.display.set_caption("Main Page")
                        elif btn == games:
                            # go_saved_games(saved_games)
                            pass
                            pygame.display.set_caption("Main Page")
                        elif btn == settings:
                            go_settings()
                            pygame.display.set_caption("Main Page")

        pygame.display.update()


new_main_menu()
