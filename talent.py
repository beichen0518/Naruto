from random import randint
from abc import ABCMeta


class Talent(object, metaclass=ABCMeta):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class XieLunYan(Talent):
    """写轮眼"""

    def tian_zhao(self, other, warth):
        r = randint(1, 4)
        if r == 3 and warth >= 30:
            re = other.limit_hp // 4
            other.reduce_hp(re)
            return self._name, re
        else:
            return False


class RenZhuLi(Talent):
    """人柱力"""

    def __init__(self, name):
        super().__init__(name)
        self._status = False

    def wei_shou_hua(self, my):
        if (not self._status) and my.hp <= 0.3 * my.limit_hp:
            my.attack *= 1.5
            my.restore_hp(my.limit_hp)
            self._status = True
            return self._name

