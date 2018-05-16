import pygame


def is_none(*args):
    info = []
    for arg in args:
        if arg is not None:
            info.append(arg[:])
    return info


def display_info(size, info, screen, x, y):
    if info is not None:
        info_font = pygame.font.SysFont('SimHei', size)
        info_text = info_font.render(info, True, [0, 0, 0], [242, 242, 242])
        info_board = info_text.get_rect()
        info_board.center = (x, y)
        screen.blit(info_text, info_board)


