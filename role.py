from abc import ABCMeta, abstractmethod

import pygame


class Role(object, metaclass=ABCMeta):

    def __init__(self, name):
        self._name = name
        self._teams = [None] * 5
        self._index = 0

    def append(self, person):
        self._teams[0] = person
        self._index += 1

    @abstractmethod
    def display(self):
        pass


class Player(Role):

    def display(self, screan):
        init_x = 300
        init_y = 390
        for index, team in enumerate(self._teams):
            team.draw(screan, init_x + 160 * index, init_y)


class Computer(Role):

    def display(self, screan):
        init_x = 300
        init_y = 70
        for index, team in enumerate(self._teams):
            team.draw(screan, init_x + 160 * index, init_y)