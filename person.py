from abc import ABCMeta, abstractmethod

from Naruto.talent import *
from Naruto.debuff import *


class Role(object, metaclass=ABCMeta):
    """所有角色的父类"""

    def __init__(self, name, attack, hp, shield=0):
        """
        初始属性
        :param name: 角色名
        :param attack: 攻击力
        :param hp: 血量
        :param shield: 护盾
        """
        self._name = name
        self._attack = attack
        self._hp = hp
        self._limit_hp = hp
        self._shield = shield
        self._debuffs = {}


    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @property
    def limit_hp(self):
        return self._limit_hp

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, attack):
        self._attack = attack

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, shield):
        self._shield = shield

    @property
    def status(self):
        return self._status

    @property
    def debuffs(self):
        return self._debuffs

    def attack_to(self, other):
        """
        攻击
        :param other: 攻击对象
        :return:
        """
        other.reduce_shield(self._attack)
        return '%s使用了普通攻击对%s造成了%d的伤害' %(self._name, other.name, self._attack)

    def reduce_shield(self, attack):
        s_remain = self._shield - self._attack
        if s_remain < 0:
            self._shield = 0
            self._hp += s_remain
            self._hp = self._hp if self._hp >= 0 else 0
        else:
            self._shield -= s_remain

    def reduce_hp(self, re):
        if self.hp > 0:
            self._hp -= re

    def restore_hp(self, vol):
        """
        恢复血量
        :param vol: 恢复的量
        :return:
        """
        n_hp = self._hp + vol
        self._hp = self._limit_hp if n_hp > self._limit_hp else n_hp

    def restore_sh(self, vol):
        """
        增加护盾
        :param vol: 增加护盾的量
        :return:
        """
        self._shield += vol

    def debuffs_effect(self):
        for debuff in self._debuffs.values():
            infor = debuff.take_effect(self)
            if infor:
                yield '%s 受到了%d点的%s伤害' % (self._name, infor[1], infor[0])

    def __repr__(self):
        debuffs = ''
        for debuff in self._debuffs.keys():
            debuffs += debuff + ' '
        return '%s的生命值为 %d \n debuff : %s'% (self._name, self._hp, debuffs)

    # @abstractmethod
    # def ninjutsu(self):
    #     pass

    def is_die(self):
        if self._hp > 0:
            return False
        else:
            return True


class MingRen(Role):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._talent = RenZhuLi('尾兽化')


    def t_use(self):
        infor = self._talent.wei_show_hua(self)
        return '%s使用了%s'%(self.name, infor)


class ZuoZhu(Role):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._talent = XieLunYan('天照')

    def t_attack_to(self, other, warth):
        infor = self._talent.tian_zhao(other, warth)
        if infor:
            other.debuffs['灼烧'] = Firing('灼烧')
            return '%s 使用了%s对%s造成了%d的伤害' % (self._name, infor[0], other.name, infor[1])
