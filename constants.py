import pygame

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BTN_GRAY = (17, 125, 28)
BTN_GREEN = (96, 102, 97)

# Create the Screen
disp_width = 900
disp_height = 600
DISPLAYSURF = pygame.display.set_mode((disp_width, disp_height))

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


# Define Fonts
font = pygame.font.SysFont("bahnschrift", 30)  # NOTE: font size
emoji_font = pygame.font.SysFont("segoeuisymbol", 30)
arial_font = pygame.font.SysFont("Arial", 30)
stats_font = pygame.font.SysFont("couriernew", 20)

# Sound effects
civilian_sound = pygame.mixer.Sound("./sounds/civilian.wav")
bonus_sound = pygame.mixer.Sound("./sounds/coin.wav")
lost_sound = pygame.mixer.Sound("./sounds/gameover.wav")
won_sound = pygame.mixer.Sound("./sounds/won.wav")
clink_sound = pygame.mixer.Sound("./sounds/clinking.wav")
explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")


# top button parameters
upper_strip = disp_height * 0.15
topbar_btn_width = disp_width / 6
