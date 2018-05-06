from abc import ABCMeta
from random import randint


class Skill(object, metaclass=ABCMeta):
    """技能"""
    def __init__(self, name):
        self._name = name
        self._status = True


class SkillAttack(Skill):

    def is_used(self, attack):
        new_attack = attack * 2
        return {'name': self._name, 'value': new_attack}


class XianRen(Skill):

    def is_used(self, myself):
        if self._status and myself.hp < myself.limit_hp * 0.2:
            myself.restore_sh(myself.limit_hp)
            myself.attack *= 2
            self._status = False
            return '%s使用了%s' % (myself.name, self._name)


class LiuDao(Skill):

    def is_used(self, myself, *others):
        if self._status and myself.hp < myself.limit_hp * 0.15:
            myself.attack *= 1.5
            restore = myself.limit_hp * 0.5
            for other in others:
                if not other.is_die():
                    other.restore_sh(restore)
                    other.restore_hp(restore)
            self._status = False
            return '%s使用了%s,我方全体恢复%d的hp和%d的护盾' % (myself.name, self._name, restore, restore)


class XuZuo(Skill):

    def is_used(self, myself):
        if self._status and myself.hp < myself.limit_hp * 0.5:
            myself.restore_sh(myself.limit_hp * 1.5)
            myself.attack *= 2
            self._status = False
            myself.is_xuzuo = True
            return '%s使用了%s' % (myself.name, self._name)


class JianYu(Skill):

    def is_used(self, myself, *others):
        if myself.is_xuzuo and randint(1,5) == 5:
            for other in others:
                if not other.is_die():
                    try:
                        a_num = myself.attack * 2
                        other.reduce_shield(a_num)
                    except UnboundLocalError:
                        pass
            return ('%s使用了%s对敌方全体造成了%d的伤害' %
                    (myself.name, self._name, a_num))






