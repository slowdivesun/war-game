import pygame, sys
import os
from pygame.locals import *
import math
from constants import *
from bomb import Bomb, generate_bomb_coordinates
from civilian import Civilian
from bonus import Bonus
from enemy import Enemy, Bullet
from soldier import *
from sliders import (
    CivilianSlider,
    BonusSlider,
    EnemySlider,
    CivilianTargetSlider,
    BonusTargetSlider,
)
from draw_functions import *
from game_buttons import create_button_func, create_button_center
from buttons import *
from load_image import load_image
from groups import explosion_group, projectile_group

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


# Define Constants
FPS = pygame.time.Clock()
begin = False
checked = True


e_slider = EnemySlider()
c_slider = CivilianSlider()
b_slider = BonusSlider()
ct_slider = CivilianTargetSlider(c_slider)
bt_slider = BonusTargetSlider(b_slider)
all_sliders = [e_slider, c_slider, b_slider, ct_slider, bt_slider]


def draw_slider(s):
    s.draw_bg(DISPLAYSURF)
    pygame.draw.rect(DISPLAYSURF, GRAY, s.slider_rect)
    pygame.draw.circle(
        DISPLAYSURF,
        "#f9430a",
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

        number_of_strikes = 0
        if (
            number_of_strikes := len(
                pygame.sprite.spritecollide(soldier, bullet_group, True)
            )
        ) > 0:
            soldier.health -= number_of_strikes
            if soldier.health <= 0:
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
                elif event.key == pygame.K_SPACE:
                    if projectile_group.sprite == None:
                        soldier.throw(pygame.time.get_ticks())
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
        display_health(soldier)
        target_group.draw(DISPLAYSURF)
        enemy_group.draw(DISPLAYSURF)
        bonus_group.draw(DISPLAYSURF)
        civilian_group.draw(DISPLAYSURF)
        bullet_group.draw(DISPLAYSURF)
        bomb_group.draw(DISPLAYSURF)
        explosion_group.draw(DISPLAYSURF)
        projectile_group.draw(DISPLAYSURF)

        # Call Update Function of all Sprites
        # Don't draw buttons if game has begun
        if (begin) and (not won) and (not killed):
            soldier_group.update(direction)
            projectile_group.update(pygame.time.get_ticks())
            bullet_group.update(
                dt, soldier.rect.center[0], soldier.rect.center[1], DISPLAYSURF
            )
            bomb_group.update(dt)
            enemy_group.update(
                soldier.rect.center[0], soldier.rect.center[1], DISPLAYSURF
            )
            for civ in civilian_group:
                if civ.rect.colliderect(soldier.rect):
                    civ.incident = True
                else:
                    civ.incident = False
        if begin and (not won):
            explosion_group.update()

        # Buttons to start the game and change parameters
        if not begin:
            begin_button = ext_begin_button_gray()
            back_button = ext_back_button()
            info_button = ext_info_button()
            if is_selected:
                rotate_left_button = ext_rotate_left_button_gray()
                rotate_right_button = ext_rotate_right_button_gray()
                flip_button = ext_flip_button_gray()
            else:
                rotate_left_button = ext_rotate_left_button_green()
                rotate_right_button = ext_rotate_right_button_green()
                flip_button = ext_flip_button_green()

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


def go_settings():
    pygame.display.set_caption("Settings")

    global checked

    # Load the background image
    background_image = pygame.image.load(get_full_path("backl.jpg"))
    background_image.set_alpha(150)
    background_image = pygame.transform.scale(background_image, (900, 600))
    background = pygame.Surface(DISPLAYSURF.get_size())
    background.blit(background_image, (0, 0))

    # Define the rectangles
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
    cancel_text = font.render("BACK", True, (255, 255, 255))
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

    pygame.display.set_caption("Main Page")
    background = pygame.Surface(DISPLAYSURF.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    DISPLAYSURF.blit(background, (0, 0))

    home_img = pygame.image.load(get_full_path("soldier_home.png"))
    home_img = pygame.transform.scale(home_img, (disp_width / 2, 0.8 * disp_height))
    icon_img = pygame.image.load(get_full_path("icon.png"))
    icon_img = pygame.transform.scale(icon_img, (130, 80))
    background1 = pygame.Surface((disp_width, 0.85 * disp_height))
    background1.fill("#333333")

    while True:
        DISPLAYSURF.blit(background, (0, 0))
        DISPLAYSURF.blit(background1, (0, 0.15 * disp_height))
        background1.blit(home_img, (25, 10))
        DISPLAYSURF.blit(icon_img, (10, upper_strip / 2 - icon_img.get_height() / 2))
        starts = ext_start_button()
        if starts.collidepoint(pygame.mouse.get_pos()):
            starts = ext_start_button_hover()
        settings = ext_settings_button()
        if settings.collidepoint(pygame.mouse.get_pos()):
            settings = ext_settings_button_hover()
        about = ext_about_button()
        if about.collidepoint(pygame.mouse.get_pos()):
            about = ext_about_button_hover()
        games = create_button_new(
            430, 460, 160, 32, pygame.font.SysFont("Arial", 23), "Saved Games", 450, 465
        )

        buttons = [starts, games, settings, about]
        draw_text_middle(
            "HOME",
            pygame.font.SysFont("BOLD", 25),
            "#f9430a",
            disp_width / 2 + topbar_btn_width / 2,
            upper_strip / 2,
            DISPLAYSURF,
        )
        draw_text(
            "UNLEASH YOUR",
            pygame.font.SysFont("impact", 35),
            (255, 255, 255),
            2 * disp_width / 3,
            disp_height / 4,
            DISPLAYSURF,
        )
        draw_text(
            "INNER",
            pygame.font.SysFont("impact", 35),
            (255, 255, 255),
            2 * disp_width / 3,
            disp_height / 4 + 40,
            DISPLAYSURF,
        )
        draw_text(
            "WARRIOR",
            pygame.font.SysFont("impact", 35),
            "#f9430a",
            2 * disp_width / 3
            + pygame.font.SysFont("impact", 35)
            .render("INNER ", True, (255, 255, 255))
            .get_width(),
            disp_height / 4 + 40,
            DISPLAYSURF,
        )
        draw_text_left_align(
            "OBSTACLES :",
            pygame.font.SysFont("BOLD", 30),
            "#f9430a",
            disp_width / 3,
            disp_height / 2 + 35 / 2,
            DISPLAYSURF,
        )
        draw_text_left_align(
            str(e_slider.slider_value),
            pygame.font.SysFont("BOLD", 30),
            "#ffffff",
            disp_width / 3
            + pygame.font.SysFont("BOLD", 30)
            .render("OBSTACLES : ", True, WHITE)
            .get_width(),
            disp_height / 2 + 35 / 2,
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
                                # intermediate()
                                start()
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
