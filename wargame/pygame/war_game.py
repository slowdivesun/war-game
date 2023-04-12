import pygame, sys
import os
from pygame.locals import *
import math
from bomb import Bomb
import random

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")
pygame.init()

disp_width = 900
disp_height = 600
DISPLAYSURF = pygame.display.set_mode((disp_width, disp_height))

# Define Terrain
terrain = "Desert"
desert_img = pygame.image.load("desert.png")
desert_img = pygame.transform.scale(desert_img, (250, 240))
mountain_img = pygame.image.load("mountain.png")
mountain_img = pygame.transform.scale(mountain_img, (250, 240))
snow_img = pygame.image.load("snow.png")
snow_img = pygame.transform.scale(snow_img, (250, 240))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define slider
slider_width = 300
slider_height = 10
slider_x = (disp_width / 2) - (slider_width / 2)
slider_y = 170
slider_min = 0
slider_max = 10
slider_value = 5
slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
slider_knob_radius = 8
slider_knob_x = slider_x + int(
    (slider_value - slider_min) / (slider_max - slider_min) * slider_width
)
slider_knob_y = slider_y + int(slider_height / 2)

font = pygame.font.SysFont("Arial", 30)  # NOTE: font size
bullet_speed = 1
FPS = pygame.time.Clock()


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    DISPLAYSURF.blit(img, (x, y))


def draw_slider():
    pygame.draw.rect(DISPLAYSURF, GRAY, slider_rect)
    pygame.draw.circle(
        DISPLAYSURF, WHITE, (slider_knob_x, slider_knob_y), slider_knob_radius
    )


def create_buttons(x, y, w, h, font, text, k, g, color="black"):
    button = pygame.Rect(x, y, w, h)
    pygame.draw.rect(DISPLAYSURF, (255, 255, 255), button)
    button_text = font.render(text, True, color)
    text_rect = button_text.get_rect(center=(x + (w / 2), y + (h / 2)))
    DISPLAYSURF.blit(button_text, text_rect)
    return button


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1, angle=0):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


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
    def __init__(self, left, top, angle=30):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy.png", -1, 0.08, angle)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = left, top
        self.angle = angle

        # NOTE: drag and drop
        self.clicked = False

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
                newpos = self.rect.move((0, -5))
        elif direction == 1:  # DOWN
            if self.rect.bottom != self.area.bottom:
                newpos = self.rect.move((0, 5))
        elif direction == 2:
            if self.rect.left != self.area.left:
                newpos = self.rect.move((-5, 0))
        else:
            if self.rect.right != self.area.right:
                print("hello")
                newpos = self.rect.move((5, 0))

        self.rect = newpos

    def location(self):
        return self.rect.left, self.rect.top


def draw_enemies(count):
    enemies = []
    left = 5
    top = 5
    img_width = pygame.image.load("./wargame/pygame/data/enemy.png").get_width() * 0.08

    for i in range(count):
        enemies.append(Enemy(left + (img_width + 2) * i, top))

    return enemies


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

    # Display parameters
    pygame.display.set_caption("War")
    pygame.mouse.set_visible(True)
    DISPLAYSURF.fill("#aaeebb")

    # Create The Background
    background = pygame.Surface(DISPLAYSURF.get_size())
    background.fill("#aaeebb")

    # Add bushes
    bush_img = pygame.image.load("./wargame/pygame/data/bush.png")
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
    enemies = draw_enemies(slider_value)
    allsprites = pygame.sprite.RenderPlain((soldier, target))
    enemy_group = pygame.sprite.Group(tuple(enemies))
    bullet_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()

    create_buttons(550, 10, 120, 50, font, "Quit", 580, 15)

    going = True
    direction = -1

    clock = pygame.time.Clock()

    while going:
        direction = -1
        if soldier.location() == target.location():
            going = False
        for event in pygame.event.get():
            if event.type == bullet_event:
                for enemy in enemy_group:
                    bullet = Bullet(enemy)
                    bullet_group.add(bullet)
            if event.type == bomb_event:
                coordinate_x, coordinate_y = generate_bomb_coordinates()

                bomb_angle = math.atan2(
                    soldier.rect.center[1] - coordinate_y,
                    soldier.rect.center[0] - coordinate_x,
                )
                print("bomb-angle: ", bomb_angle)
                bomb = Bomb(
                    bomb_angle,
                    coordinate_x,
                    coordinate_y,
                    DISPLAYSURF,
                    10,
                    90,
                )
                bomb_group.add(bomb)
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.K_ESCAPE:
                going = False
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
            elif event.type == pygame.MOUSEBUTTONUP:
                for enemy in enemy_group:
                    enemy.clicked = False

        for enemy in enemy_group:
            if enemy.clicked == True:
                pos = pygame.mouse.get_pos()
                new_x = pos[0] - (enemy.rect.width / 2)
                new_y = pos[1] - (enemy.rect.height / 2)
                ew = enemy.rect.width
                eh = enemy.rect.height

                if not check_collision(new_x, new_y, ew, eh, target):
                    enemy.rect.topleft = pos[0] - (enemy.rect.width / 2), pos[1] - (
                        enemy.rect.height / 2
                    )

        dt = FPS.tick(60)

        # Draw Everything
        DISPLAYSURF.blit(background, (0, 0))
        allsprites.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        bullet_group.draw(DISPLAYSURF)
        bomb_group.draw(DISPLAYSURF)

        allsprites.update(direction)
        bullet_group.update(dt)
        bomb_group.update(dt)

        pygame.display.flip()

    pygame.quit()


def terrain_select():
    global terrain
    global desert_img
    pygame.display.set_caption("Terrain")
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display The Background
    DISPLAYSURF.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(desert_img, (325, 80))
        DISPLAYSURF.blit(mountain_img, (25, 80))
        DISPLAYSURF.blit(snow_img, (625, 80))
        button1 = create_buttons(80, 340, 120, 50, font, "Mountains", 81, 345)
        button2 = create_buttons(390, 340, 120, 50, font, "Desert", 410, 345)
        button3 = create_buttons(700, 340, 120, 50, font, "Snow", 730, 345)
        button4 = create_buttons(380, 500, 120, 50, font, "Save", 410, 505)
        buttons = [button1, button3, button2, button4]

        draw_text("Choose Terrain", font, (255, 255, 255), 340, 10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.collidepoint(pygame.mouse.get_pos()):
                        if btn == button1:
                            terrain = "Mountains"
                        elif btn == button2:
                            terrain = "Desert"
                        elif btn == button3:
                            terrain = "Snow"
                        else:
                            return

        pygame.display.update()


def main_menu():
    global slider_value
    global slider_knob_x
    global slider_knob_y
    pygame.display.set_caption("Settings")
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill("#aaeebb")

    # Display The Background
    DISPLAYSURF.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        DISPLAYSURF.blit(background, (0, 0))
        draw_slider()
        button1 = create_buttons(
            380,
            500,
            120,
            50,
            pygame.font.SysFont("Arial", 30),
            "START",
            410,
            505,
            "black",
        )
        create_buttons(110, 150, 130, 50, font, "Obstacles", 114.5, 155)
        button3 = create_buttons(380, 300, 120, 50, font, "Terrain", 400, 305)
        # button4 = create_buttons(640, 150, 120, 50, font, "Enemy", 658, 155)
        buttons = [button1, button3]  # NOTE: removed button4 from list
        draw_text("Choose parameters", font, (255, 255, 255), 340, 10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:  # if left button is pressed
                    # move slider knob
                    slider_knob_x = min(
                        max(event.pos[0], slider_x), slider_x + slider_width
                    )
                    slider_value = round(
                        slider_min
                        + (slider_max - slider_min)
                        * (slider_knob_x - slider_x)
                        / slider_width
                    )
            elif event.type == MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.collidepoint(pygame.mouse.get_pos()):
                        if btn == button1:
                            start()
                        elif btn == button3:
                            terrain_select()
                            pygame.display.set_caption("Main Page")
                        # elif btn == button4:

        draw_text(str(slider_value), font, WHITE, slider_knob_x - 10, slider_y - 40)
        pygame.display.update()


main_menu()
