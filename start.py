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
    xiaoying1 = ChunYeYing('春野樱1', 1200, 30000)
    zuozhu1 = ZuoZhu('佐助1', 1200, 30000)
    dashewan1 = DaSheWan('大蛇丸1', 1200, 30000)
    kai1 = Kai('迈特凯', 1200, 30000)
    zuozhu2 = ZuoZhu('佐助2', 1200, 30000)
    dashewan2 = DaSheWan('大蛇丸2', 1200, 30000)
    kai2 = Kai('迈特凯2', 1200, 30000)
    mingren2 = MingRen('旋涡鸣人2', 1200, 30000)
    xiaoying2 = ChunYeYing('春野樱2', 1200, 30000)
    player = Player('WXZ')
    player.append(mingren1)
    player.append(xiaoying1)
    player.append(zuozhu1)
    player.append(dashewan1)
    player.append(kai1)
    player.init()
    computer = Computer('简单电脑')
    computer.append(zuozhu2)
    computer.append(dashewan2)
    computer.append(kai2)
    computer.append(mingren2)
    computer.append(xiaoying2)
    computer.init()

    myfight = Fighting(player, computer, screen)
    myfight.start()
    myupdate = GameUpdate(screen, player, computer, myfight)
    myupdate.setDaemon(True)
    myupdate.start()
    pygame.display.flip()
    music_file = './music/高梨康治 - 黒点.mp3'
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(loops=-1, start=0.0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sleep(0.05)

    pygame.quit()


if __name__ == '__main__':
    main()