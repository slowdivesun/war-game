import pygame
from constants import disp_height, disp_width, DISPLAYSURF, stats_font, stats_font_bold

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

stats_text_array = [
    "Time Taken: ",
    "Bonus Collected: ",
    "Civilians rescued: ",
    "Tast 1 status: ",
    "Task 2 status: ",
    "Status: "
    # "Hits taken: ",
    # "Average Projectile Margin: ",
]


class Stats:
    def __init__(self):
        self.time = 14
        self.civ = 0
        self.bon = 0
        self.hits = 0
        self.task1 = False
        self.task2 = False
        self.based_reached = False
        self.status = False


stats = Stats()


def display_stats():
    stats_array = [
        stats.time,
        stats.bon,
        stats.civ,
        "Completed" if stats.task1 else "Failed",
        "Completed" if stats.task2 else "Failed",
        "Won" if (stats.task1 and stats.task2 and stats.based_reached) else "Lost",
    ]
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
    display = True
    while display:
        clock.tick(50)
        index += 1
        if j < len(lines):
            if index > len(lines[j]):
                index = 0
                j += 1
            if j < len(lines) - 1:
                text_surface = stats_font.render(lines[j][:index], True, (0, 0, 0))
            if j == len(lines) - 1:
                # if lines[j][:index] == "Complete":
                #     text_surface = stats_font_bold.render(
                #         lines[j][:index], True, "green"
                #     )
                # elif lines[j][:index] == "Incomplete":
                #     text_surface = stats_font_bold.render(lines[j][:index], True, "red")
                # else:
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                display = False

        pygame.display.update()
