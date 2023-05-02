import pygame
from constants import disp_height, disp_width, DISPLAYSURF, stats_font

stats_height = 0.8 * disp_height
stats_width = 0.9 * disp_width
stats_topleft = (0.1 * disp_width / 2, 0.2 * disp_height / 2)
text_width = 0.8 * stats_width
text_height = 0.8 * stats_height

rect = pygame.Rect(
    disp_width / 2 - stats_width / 2,
    disp_height / 2 - stats_height / 2,
    stats_width,
    stats_height,
)

alpha = 128
rect_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
rect_surf.fill((209, 209, 209, alpha))

stats_array = [14, 2, 1, 2, 50.7]
stats_text_array = [
    "Time Taken: ",
    "Civilians rescued: ",
    "Bonus Collected: ",
    "Hits taken: ",
    "Average Projectile Margin: ",
]


def display_stats():
    lines = []
    for i in range(len(stats_text_array)):
        words = (stats_text_array[i] + str(stats_array[i])).split()
        line = ""
        for word in words:
            if stats_font.size(line + " " + word)[0] > 0.7 * DISPLAYSURF.get_width():
                lines.append(line.strip())
                line = ""
            line += " " + word
        lines.append(line.strip())
    clock = pygame.time.Clock()
    index = 0
    j = 0
    surfaces = []
    y = 0
    DISPLAYSURF.blit(
        rect_surf,
        (disp_width / 2 - stats_width / 2, disp_height / 2 - stats_height / 2),
    )
    while True:
        clock.tick(50)
        index += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if j < len(lines):
            if index > len(lines[j]):
                index = 0
                j += 1
            if j < len(lines):
                text_surface = stats_font.render(lines[j][:index], True, (0, 0, 0))

        if len(surfaces) > 0:
            for k in range(len(surfaces)):
                DISPLAYSURF.blit(
                    surfaces[k],
                    (
                        stats_topleft[0] + (stats_width - text_width) / 2,
                        stats_topleft[1] + (stats_height - text_height) / 2 + 40 * k,
                    ),
                )
                y = k + 1
        if j < len(lines):
            if index + 1 > len(lines[j]):
                surfaces += [text_surface]
        if j < len(lines):
            DISPLAYSURF.blit(
                text_surface,
                (
                    stats_topleft[0] + (stats_width - text_width) / 2,
                    stats_topleft[1] + (stats_height - text_height) / 2 + 40 * y,
                ),
            )

        pygame.display.update()
