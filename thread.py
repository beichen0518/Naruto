from threading import Thread
from time import sleep

import pygame

from Naruto.tools import display_info


class GameUpdate(Thread):

    def __init__(self, screen, player, computer, fight):
        super().__init__()
        self._screen = screen
        self._player = player
        self._computer = computer
        self._fight = fight

    def run(self):
        while True:
            self._screen.fill([242, 242, 242])
            self._player.display(self._screen)
            self._computer.display(self._screen)
            display_info(13, '%s战意值：%d' % (self._player.name, self._player.warth), self._screen, 690, 10)
            display_info(13, '%s战意值：%d' % (self._player.name, self._player.warth), self._screen, 690, 630)
            #  显示玩家每张卡的状态
            for one in self._player.teams:
                y = 570
                for info in one.all_status():
                    y += 15
                    display_info(12, info, self._screen, one.x + 60, y)

            # 显示电脑每张卡的状态
            for one in self._computer.teams:
                y = 15
                for info in one.all_status():
                    y += 15
                    display_info(12, info, self._screen, one.x + 60, y)

            # 显示电脑的战斗信息
            y = 0
            for info in self._computer.info:
                y += 15
                if y > 320:
                    self._computer.clear_info()
                display_info(12, info, self._screen, 150, y)
            # 显示玩家的战斗信息
            y = 320
            for info in self._player.info:
                y += 15
                if y > 640:
                    self._player.clear_info()
                display_info(12, info, self._screen, 150, y)
            # 显示游戏结果
            if self._fight.fail is not None:
                if self._fight.fail == self._player.name:
                    display_info(30, '战斗失败,请重新开始游戏或退出', self._screen, 540, 320)
                if self._fight.fail == self._computer.name:
                    display_info(30, '战斗胜利,请重新开始游戏或退出', self._screen, 540, 320)
            if self._fight.show:
                display_info(30, '第 %d 回合开始' % self._fight.round, self._screen, 540, 320)
            pygame.display.update()


class Fighting(Thread):

    def __init__(self, player, computer, screen):
        super().__init__()
        self._player = player
        self._computer = computer
        self._screen = screen
        self._clock = pygame.time.Clock()
        self._fail = None
        self._round = 1
        self._show = False

    @property
    def fail(self):
        return self._fail

    @property
    def round(self):
        return self._round

    @property
    def show(self):
        return self._show

    def run(self):
        while True:
            dn = 0
            for one in self._player.teams:
                if one.is_die():
                    dn += 1
            if dn == 5:
                self._fail = self._player.name
                break
            dn = 0
            for one in self._computer.teams:
                if one.is_die():
                    dn += 1
            if dn == 5:
                self._fail = self._computer.name
                break
            if self._player.range == 0:
                self._show = True
                sleep(1)
                self._show = False
                self._round += 1
                self._player.clear_info()
                self._computer.clear_info()
                self._player.status_effect()
                self._computer.status_effect()
                self._player.add_warth(5)
                self._computer.add_warth(5)
            self._player.skill_attack(self._computer)
            self._player.attack(self._computer)
            self._computer.skill_attack(self._player)
            self._computer.attack(self._player)
            self._clock.tick(20)





























