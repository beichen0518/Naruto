from abc import ABCMeta
from random import randint, choice
from Naruto.debuff import Paralysis


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

    def is_used(self, myself, myteams):
        if self._status and myself.hp < myself.limit_hp * 0.15:
            myself.attack *= 1.5
            restore = myself.limit_hp * 0.5
            for other in myteams:
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

    def is_used(self, myself, others):
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


class ZhouHu(Skill):

    def is_used(self, myself, other, warth):
        if warth > 30 and randint(1, 5) == 3:
            a_num = myself.attack * 6
            other.reduce_shield(a_num)
            return '%s使用了%s对%s造成了%d的伤害' % \
                   (myself.name, self._name, other.name, a_num)


class XiXiang(Skill):

    def is_used(self, myself, other, warth):

        if warth > 50 and randint(1, 3) == 2:
            a_num = myself.attack * 15
            other.reduce_shield(a_num)
            myself.reduce_hp(myself.limit_hp)
            return '%s使用了%s对%s造成了%d的伤害,%s阵亡' % \
                   (myself.name, self._name, other.name, a_num, myself.name)


class ZhangXianShu(Skill):

    def is_used(self, myself, myteams):
        if randint(1, 2) == 2:

            live_list = []
            blood_list = []
            val = myself.attack * 3
            for other in myteams:
                if not other.is_die():
                    live_list.append(other)
                    blood_list.append(other.hp)
            if myself.baihao:
                for one in live_list:
                    one.restore_hp(val)
                return '%s使用了%s恢复全体%d点生命值' % (myself.name, self._name, val)
            else:
                least_blood = min(blood_list)
                for one in live_list:
                    if one.hp == least_blood:
                        one.restore_hp(val)
                        return '%s使用了%s恢复了%s %d点生命值' % (myself.name, self._name, one.name, val)


class BaiHao(Skill):

    def is_used(self, myself, warth):
        if warth > 50 and self._status:
            myself.attack = int(myself.attack * 1.5)
            myself.baihao = True
            self._status = False
            return '%s使用了%s' % (myself.name, self._name)


class SheNiZhouFu(Skill):

    def is_used(self, myself, other, warth):
        if warth > 10 and randint(1, 4) == 3:
            other.debuffs['麻痹'] = Paralysis('麻痹', 2)
            return '%s对%s使用了%s' % (myself.name, other.name, self._name)


class HuiTuZhuanSheng(Skill):

    def is_used(self, myself, myteams, warth):
        if warth > 50 and randint(1, 5) == 3:
            die_list = []
            for myteam in myteams:
                if myteam.is_die():
                    die_list.append(myteam)
            luckone = choice(die_list)
            val = luckone.limit_hp // 4
            luckone.restore_hp(val)
            return '%s使用%s复活了%s' % (myself.name, self._name, luckone.name)





