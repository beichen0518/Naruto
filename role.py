from abc import ABCMeta, abstractmethod
from time import sleep

import pygame


class Role(object, metaclass=ABCMeta):

    def __init__(self, name):
        self._name = name
        self._teams = [None] * 5
        self._index = 0
        self._range = 0
        self._init_x = 0
        self._init_y = 0
        self._info = []
        self._warth = 0

    @property
    def teams(self):
        return self._teams

    @property
    def init_x(self):
        return self._init_x

    @property
    def init_y(self):
        return self._init_y

    @property
    def range(self):
        return self._range

    @property
    def info(self):
        return self._info

    @property
    def name(self):
        return self._name

    @property
    def warth(self):
        return self._warth

    def add_warth(self, val):
        self._warth += val
        if self._warth < 0:
            self._warth = 0

    def clear_info(self):
        self._info = []

    def init(self):
        for index, team in enumerate(self._teams):
            team.x = self._init_x + 160 * index
            team.y = self._init_y

    def append(self, person):
        self._teams[self._index] = person
        self._index += 1

    def display(self, screen):
        for team in self._teams:
            team.draw(screen, team.x, team.y)

    def select(self, other):
        if not self._teams[self._range].is_die():
            opp = self._range
            others_die = False
            while other.teams[opp % 5].is_die():
                opp += 1
                if opp > self._range + 5:
                    others_die = True
                    break
            if not others_die:
                opp = opp % 5
                return opp

    def attack(self, other):
        opp = self.select(other)
        if opp is not None:
            other_x = other.teams[opp].x
            other_y = other.teams[opp].y
            if self._teams[self._range].y > other_y:
                other_y += 180
            else:
                other_y -= 180
            times = 10
            x_speed = (self._teams[self._range].x - other_x) // times
            y_speed = (self._teams[self._range].y - other_y) // times
            for _ in range(times):
                self._teams[self._range].x -= x_speed
                self._teams[self._range].y -= y_speed
                sleep(0.06)
            info = self._teams[self._range].attack_to(other.teams[opp])[:]
            self._info.append(info)

            for _ in range(times):
                sleep(0.05)
                self._teams[self._range].x += x_speed
                self._teams[self._range].y += y_speed

        self._range += 1
        self._range %= 5

    def status_effect(self):
        for team in self._teams:
            for info in team.debuffs_effect():
                self._info.append(info)

    def skill_attack(self, other):
        opp = self.select(other)
        if opp is not None:
            infos = self._teams[self._range].attack_s(other.teams[opp], self._teams, other.teams, self._warth)[:]
            for info in infos:
                self._info.append(info)


class Player(Role):

    def __init__(self, name):
        super().__init__(name)
        self._init_x = 300
        self._init_y = 390


class Computer(Role):

    def __init__(self, name):
        super().__init__(name)
        self._init_x = 300
        self._init_y = 70
