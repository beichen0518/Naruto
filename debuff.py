from abc import ABCMeta, abstractmethod


class DeBuff(object, metaclass=ABCMeta):
    """debuff"""

    def __init__(self, name, effect_time=3):
        self._name = name
        self._effect_time = effect_time

    @property
    def name(self):
        return self._name

    @property
    def effect_time(self):
        return self._effect_time

    @effect_time.setter
    def effect_time(self, effect_time):
        self._effect_time = effect_time

    @abstractmethod
    def take_effect(self):
        pass




class Firing(DeBuff):
    """灼烧"""

    def take_effect(self, myself):
        if self._effect_time > 0 and myself.hp > 0:
            self._effect_time -= 1
            re = myself.limit_hp // 20
            myself.reduce_hp(re)
            return self._name, re


class Paralysis(DeBuff):
    """麻痹"""

    def take_effect(self, myself):
        if self._effect_time > 0:
            self._effect_time -= 1
            myself.effect = True
            if self._effect_time == 0:
                myself.effect = False
        else:
            myself.effect = False


