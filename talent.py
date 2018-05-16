from random import randint
from abc import ABCMeta
from Naruto.debuff import Firing


class Talent(object, metaclass=ABCMeta):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class XieLunYan(Talent):
    """写轮眼"""

    def tian_zhao(self, other, warth):
        r = randint(1, 3)
        if r == 3 and warth >= 30:
            re = other.limit_hp // 10
            other.reduce_hp(re)
            other.debuffs['灼烧'] = Firing('灼烧')
            return self._name, re



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


class WarmBlood(Talent):

    def life_bloom(self, my):
        val = int(my.hp * 0.01)
        my.reduce_hp(val)
        my.attack += val
        return self._name, val


class GuaLi(Talent):

    def guali(self, my):
        my.attack = int(my.attack * 1.5)


class BaiShe(Talent):

    def baishe(self, my):
        val = int(my.limit_hp * 0.08)
        my.restore_hp(val)
        return self._name, val


