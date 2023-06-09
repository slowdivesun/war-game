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
from sliders import *
from draw_functions import *
from game_buttons import create_button_func, create_button_center
from buttons import *
from load_image import load_image
from groups import (
    explosion_group,
    projectile_group,
    enemy_explosion_group,
    bonus_animation_group,
)
from game_stats import display_stats, stats

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
        self.rect.topleft = (
            screen.get_width() - self.image.get_width() - 10,
            10,
        )
        self.mask = pygame.mask.from_surface(self.image)
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


def move_entities(object1, object2):
    pos = pygame.mouse.get_pos()
    new_x = pos[0] - (object1.rect.width / 2)
    new_y = pos[1] - (object1.rect.height / 2)
    ew = object1.rect.width
    eh = object1.rect.height
    if not check_collision(new_x, new_y, ew, eh, object2):
        object1.left = pos[0] - (object1.rect.width / 2)
        object1.top = pos[1] - (object1.rect.height / 2)
        object1.rect.topleft = pos[0] - (object1.rect.width / 2), pos[1] - (
            object1.rect.height / 2
        )


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

    enemies = draw_enemies(e_slider.slider_value)
    civilians = draw_civilians(c_slider.slider_value)
    bonuses = draw_bonuses(b_slider.slider_value)
    civilian_target = ct_slider.slider_value
    bonus_target = bt_slider.slider_value

    soldier = Soldier(civilian_target, bonus_target)
    target = Target()
    soldier_group = pygame.sprite.Group((soldier))
    target_group = pygame.sprite.Group((target))
    enemy_group = pygame.sprite.Group(tuple(enemies))
    civilian_group = pygame.sprite.Group(tuple(civilians))
    bonus_group = pygame.sprite.Group(tuple(bonuses))
    bullet_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()

    if soldier.bonus >= soldier.bon_target:
        stats.task1 = True

    if soldier.civilians >= soldier.civ_target:
        stats.task2 = True

    # create_button(550, 10, 120, 50, font, "Quit", 580, 15)

    game = True
    won = False
    killed = False
    displayed = False
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
    random_button = None
    back_button = None
    info_button = None
    bomb_iteration = 0
    start_time = pygame.time.get_ticks()

    while game:
        direction = -1
        # Game Won
        if pygame.sprite.collide_mask(soldier, target):
            stats.time = (pygame.time.get_ticks() - start_time) / 1000.0
            stats.based_reached = True
            won = True

        number_of_strikes = 0
        if (
            number_of_strikes := len(
                pygame.sprite.spritecollide(soldier, bullet_group, True)
            )
        ) > 0:
            soldier.health -= number_of_strikes
            if soldier.health <= 0:
                stats.time = (pygame.time.get_ticks() - start_time) / 1000.0
                killed = True
        if soldier.health <= 0:
            killed = True
            stats.time = (pygame.time.get_ticks() - start_time) / 1000.0
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
                if bomb_iteration == 0:
                    coordinate_x, coordinate_y = generate_bomb_coordinates()
                    sold_y = soldier.rect.center[1]
                    sold_x = soldier.rect.center[0]

                    bomb = Bomb(
                        coordinate_x,
                        coordinate_y,
                        DISPLAYSURF,
                        sold_x,
                        sold_y,
                    )
                    bomb_group.add(bomb)
                # else:
                # bomb_iteration += 1
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
                            soldier.add_civilian()
                            stats.civ += 1
                            if soldier.civilians >= soldier.civ_target:
                                stats.task2 = True
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
                    for bon in bonus_group:
                        if bon.rect.collidepoint(pos):
                            bon.clicked = True
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
                    random_button = None
                if (restart_button != None) and (
                    restart_button.collidepoint(pygame.mouse.get_pos())
                ):
                    begin = True
                    won = False
                    killed = False
                    displayed = False
                    soldier.restart()
                    bomb_group.empty()
                    explosion_group.empty()
                    enemy_explosion_group.empty()
                    bullet_group.empty()
                    restart_button = None
                    menu_button = None
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
                    enemy_explosion_group.empty()
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
                    enemy_explosion_group.empty()
                    bullet_group.empty()
                if (info_button != None) and (
                    info_button.collidepoint(pygame.mouse.get_pos())
                ):
                    pass
                if (random_button != None) and (
                    random_button.collidepoint(pygame.mouse.get_pos())
                ):
                    if selected_enemy != None:
                        selected_enemy.isRandom = not selected_enemy.isRandom
            elif event.type == pygame.MOUSEBUTTONUP:
                for enemy in enemy_group:
                    enemy.clicked = False
                for civ in civilian_group:
                    civ.clicked = False
                for bon in bonus_group:
                    bon.clicked = False

        # Move the enemies, civilians and bonuses to desired position
        if not begin:
            for enemy in enemy_group:
                if enemy.clicked:
                    move_entities(enemy, target)
            for civ in civilian_group:
                if civ.clicked:
                    move_entities(civ, target)
            for bon in bonus_group:
                if bon.clicked:
                    move_entities(bon, target)

        # update bomb target coordinates
        for b in bomb_group:
            b.lim_x = soldier.rect.center[0]
            b.lim_y = soldier.rect.center[1]

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
        enemy_explosion_group.draw(DISPLAYSURF)
        bonus_animation_group.draw(DISPLAYSURF)
        projectile_group.draw(DISPLAYSURF)

        # Call Update Function of all Sprites
        # Don't draw buttons if game has begun
        if (begin) and (not won) and (not killed):
            soldier_group.update(direction)
            projectile_group.update(pygame.time.get_ticks(), dt)
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
            for p in projectile_group:  # enemy explosions
                for e in pygame.sprite.spritecollide(p, enemy_group, False):
                    p.enemy_explosion(e.location()[0], e.location()[1])
                    e.killed()
            for bon in pygame.sprite.spritecollide(soldier, bonus_group, False):
                bon.collected()
                soldier.add_bonus()
                stats.bon += 1
                pygame.mixer.Sound.play(clink_sound)
                if soldier.bonus >= soldier.bon_target:
                    stats.task1 = True
                # pygame.mixer.Sound.stop(clink_sound)
                # pygame.mixer.Sound.play(bonus_sound)
            for particle in bonus_animation_group:
                particle.emit()

        if begin and (not won):
            explosion_group.update(soldier, soldier.location_center())
            bonus_animation_group.update()
            enemy_explosion_group.update(soldier, soldier.location_center())

        # Buttons to start the game and change parameters
        if not begin:
            begin_button = ext_begin_button_gray()
            back_button = ext_back_button()
            info_button = ext_info_button()
            if is_selected:
                rotate_left_button = ext_rotate_left_button_gray()
                rotate_right_button = ext_rotate_right_button_gray()
                flip_button = ext_flip_button_gray()
                if selected_enemy.isRandom:
                    random_button = ext_random_button_gray()
                else:
                    random_button = ext_random_button_green()
            else:
                rotate_left_button = ext_rotate_left_button_green()
                rotate_right_button = ext_rotate_right_button_green()
                flip_button = ext_flip_button_green()
                random_button = ext_random_button_green()

        # Display restart button if game has ended
        if won or killed:
            restart_button = ext_restart_button()
            menu_button = ext_menu_button()
            if not displayed:
                displayed = True
                display_stats()
        if won:
            pass

        if killed:
            pass

        pygame.display.flip()

        # Time Elapsed
        dt = FPS.tick_busy_loop(60)  # CHANGE

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
        for sl in all_sliders:
            draw_slider(sl)
        pygame.draw.line(
            DISPLAYSURF,
            "white",
            (0, 5 * disp_height / 7),
            (disp_width, 5 * disp_height / 7),
        )  # DEBUG

        DISPLAYSURF.blit(
            rect_surf, (0, disp_height / 7)
        )  # this is the light background

        settings_ui(top_margin, slider_row_height, rect_surf, apply_surf, cancel_surf)
        for s in all_sliders:
            draw_slider(s)

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
        main_menu_ui()
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
