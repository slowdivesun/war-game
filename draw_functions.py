def draw_text(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x, y))


def draw_text_middle(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))


def draw_text_right_align(text, font, text_color, x, y, surf):
    img = font.render(text, True, text_color)
    surf.blit(img, (x - img.get_width(), y - img.get_height() / 2))
