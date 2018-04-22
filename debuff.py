from abc import ABCMeta, abstractmethod


class DeBuff(object, metaclass=ABCMeta):
    """debuff"""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def take_effect(self):
        pass


class Firing(DeBuff):
    """灼烧"""

    def take_effect(self, myself):
        if myself.hp > 0:
            re = myself.limit_hp // 20
            myself.hp -= re
            return self._name, re


