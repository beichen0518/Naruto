import time

import pygame

from Naruto.person import *


def main():
    pygame.init()
    pygame.display.set_caption('Naruto')
    screen = pygame.display.set_mode([1080, 640])
    screen.fill([242, 242, 242])
    mingren = MingRen('旋涡鸣人', 1200, 30000)
    zuozhu = ZuoZhu('佐助', 1200, 30000)
    warth = 0

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mingren.draw(screen, 300, 70)
        zuozhu.draw(screen,300, 390)
        if mingren.is_die() or zuozhu.is_die():
            break
        for debuff in mingren.debuffs_effect():
            print(debuff)
        warth += 5
        print(mingren)
        print(zuozhu)
        print(mingren.t_use())
        print(mingren.attack_to(zuozhu))
        print(mingren.sec_use())
        print(mingren.th_use(mingren))
        print(zuozhu.attack_to(mingren))
        print(zuozhu.t_attack_to(mingren, warth))
        print(zuozhu.sec_use())
        print(zuozhu.th_use(mingren))
        time.sleep(1)
        print('= ' * 10)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()