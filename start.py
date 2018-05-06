import time

import pygame

from Naruto.person import *
from Naruto.role import *
from Naruto.thread import *

ONETIME = 0.05
DOUBLETIMES = 0.025
THREETIMES = 0.015

def main():
    pygame.init()
    pygame.display.set_caption('Naruto')
    screen = pygame.display.set_mode([1080, 640])
    screen.fill([242, 242, 242])
    mingren1 = MingRen('旋涡鸣人1', 1200, 30000)
    mingren2 = MingRen('旋涡鸣人2', 1200, 30000)
    mingren3 = MingRen('旋涡鸣人3', 1200, 30000)
    mingren4 = MingRen('旋涡鸣人4', 1200, 30000)
    mingren5 = MingRen('旋涡鸣人5', 1200, 30000)
    zuozhu1 = ZuoZhu('佐助1', 1200, 30000)
    zuozhu2 = ZuoZhu('佐助2', 1200, 30000)
    zuozhu3 = ZuoZhu('佐助3', 1200, 30000)
    zuozhu4 = ZuoZhu('佐助4', 1200, 30000)
    zuozhu5 = ZuoZhu('佐助5', 1200, 30000)
    player = Player('WXZ')
    player.append(mingren1)
    player.append(mingren2)
    player.append(mingren3)
    player.append(mingren4)
    player.append(mingren5)
    player.init()
    computer = Computer('简单电脑')
    computer.append(zuozhu1)
    computer.append(zuozhu2)
    computer.append(zuozhu3)
    computer.append(zuozhu4)
    computer.append(zuozhu5)
    computer.init()

    myfight = Fighting(player, computer, screen)
    myfight.start()
    myupdate = GameUpdate(screen, player, computer, myfight)
    myupdate.setDaemon(True)
    myupdate.start()
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sleep(0.05)

    pygame.quit()


if __name__ == '__main__':
    main()