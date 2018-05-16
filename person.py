from random import randint
from abc import ABCMeta, abstractmethod


import pygame


from Naruto.talent import *
from Naruto.skills import *
from Naruto.tools import is_none


class Person(object, metaclass=ABCMeta):
    """所有角色的父类"""

    def __init__(self, name, attack, hp, x=0, y=0, shield=0):
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
        self._pro_attack = 5
        self._fir_skill = SkillAttack('')
        self._image = ''
        self._x = x
        self._y = y
        self._injured = False
        self._effect = False


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
    def debuffs(self):
        return self._debuffs

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, effect):
        self._effect = effect

    def attack_to(self, other):

        choice = randint(1, 10)
        if choice <= self._pro_attack:
            other.reduce_shield(self._attack)
            return '%s使用了普通攻击对%s造成了%d的伤害' % (self._name, other.name, self._attack)
        else:
            info = self._fir_skill.is_used(self._attack)
            other.reduce_shield(info['value'])
            return '%s使用了%s对%s造成了%d的伤害' % (self._name, info['name'], other.name, info['value'])

    def reduce_shield(self, attack):
        """减少护盾"""
        s_remain = self._shield - attack
        if s_remain < 0:
            self._shield = 0
            self.reduce_hp(-s_remain)
        else:
            self._shield = s_remain

    def reduce_hp(self, re):
        """减少血"""
        if self.hp > 0:
            self._hp -= re
            self._hp = self._hp if self._hp > 0 else 0
        self._injured = True

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
                yield '%s受到了%d点的%s伤害' % (self._name, infor[1], infor[0])

    def all_status(self):
        debuffs = ''
        del_debuffs = []
        for key in self._debuffs:
            if self._debuffs[key].effect_time == 0:
                del_debuffs.append(key)
        for del_debuff in del_debuffs:
            del self._debuffs[del_debuff]
        for debuff in self._debuffs.keys():
            debuffs += debuff + ' '
        return ['%s ATT：%d' % (self._name, self._attack), 'HP：%d SH：%d' %
                (self._hp, self._shield), 'debuff: %s' % debuffs]

    def draw(self, screen, x, y):
        person = pygame.image.load(self._image).convert()
        if self._injured:
            a_list = [1, -1, -1, 1]
            for a in a_list:
                person = pygame.transform.rotate(person, a)
                screen.blit(person, (x, y))

        if self.is_die():
            person.set_alpha(100)
        screen.blit(person, (x, y))
        self._injured = False

    def is_die(self):
        if self._hp > 0:
            return False
        else:
            return True


class MingRen(Person):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._talent = RenZhuLi('尾兽化')
        self._fir_skill = SkillAttack('螺旋丸')
        self._sec_skill = XianRen('仙人模式')
        self._th_skill = LiuDao('六道模式')
        self._image = './images/鸣人普通状态1.jpg'

    def t_use(self):
        info = self._talent.wei_shou_hua(self)
        if info is not None:
            self._image = './images/鸣人尾兽化1.jpg'
            return '%s使用了%s' % (self.name, info)

    def sec_use(self):
        info = self._sec_skill.is_used(self)
        if info is not None:
            self._image = './images/鸣人仙人模式1.jpg'
            return info

    def th_use(self, myteams):
        info = self._th_skill.is_used(self, myteams)
        if info is not None:
            self._image = './images/鸣人六道模式1.jpg'
            return info

    def attack_s(self, other, myteams, others, warth):
        if not self._effect:
            info1 = self.t_use()
            info2 = self.sec_use()
            info3 = self.th_use(myteams)
            return is_none(info1, info2, info3)
        return ['忍术发动失败']


class ZuoZhu(Person):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._is_xuzuo = False
        self._talent = XieLunYan('天照')
        self._fir_skill = SkillAttack('千鸟')
        self._sec_skill = XuZuo('须佐能乎')
        self._th_skill = JianYu('建御雷神')
        self._image = './images/佐助普通模式1.jpg'

    @property
    def is_xuzuo(self):
        return self._is_xuzuo

    @is_xuzuo.setter
    def is_xuzuo(self, is_xuzuo):
        self._is_xuzuo = is_xuzuo

    def t_attack_to(self, other, warth):
        infor = self._talent.tian_zhao(other, warth)
        if infor is not None:
            return '%s使用了%s对%s造成了%d的伤害' % (self._name, infor[0], other.name, infor[1])

    def sec_use(self):
        info = self._sec_skill.is_used(self)
        if info is not None:
            self._image = './images/佐助须佐能乎1.jpg'
            return info

    def th_use(self, others):
        info = self._th_skill.is_used(self, others)
        if info is not None:
            return info

    def attack_s(self, other, myteams, others, warth):
        if not self._effect:
            info1 = self.t_attack_to(other, warth)
            info2 = self.sec_use()
            info3 = self.th_use(others)
            return is_none(info1, info2, info3)
        return ['忍术发动失败']


class Kai(Person):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._talent = WarmBlood('生命绽放')
        self._fir_skill = SkillAttack('朝孔雀')
        self._sec_skill = ZhouHu('昼虎')
        self._th_skill = XiXiang('夕象')
        self._image = './images/迈特凯.jpg'

    def t_use(self):
        info = self._talent.life_bloom(self)
        if info is not None:
            return '%s使用了%s' % (self.name, info[0])

    def sec_use(self, other, warth):
        info = self._sec_skill.is_used(self, other, warth)
        if info is not None:
            return info

    def th_use(self, other, warth):
        info = self._th_skill.is_used(self, other, warth)
        if info is not None:
            return info

    def attack_s(self, other, myteams, others, warth):
        if not self._effect:
            info1 = self.t_use()
            info2 = self.sec_use(other, warth)
            info3 = self.th_use(other, warth)
            return is_none(info1, info2, info3)
        return ['忍术发动失败']


class ChunYeYing(Person):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._baihao = False
        self._talent = GuaLi('怪力')
        self._fir_skill = SkillAttack('春诛打')
        self._sec_skill = ZhangXianShu('掌仙术')
        self._th_skill = BaiHao('百豪之术')
        self._image = './images/小樱.jpg'
        self._talent.guali(self)

    @property
    def baihao(self):
        return self._baihao

    @baihao.setter
    def baihao(self, baihao):
        self._baihao = baihao

    def sec_use(self, myteams):
        info = self._sec_skill.is_used(self, myteams)
        if info is not None:
            return info

    def th_use(self, warth):
        info = self._th_skill.is_used(self, warth)
        if info is not None:
            self._image = './images/小樱百豪之术.jpg'
            return info

    def attack_s(self, other, myteams, others, warth):
        if not self._effect:
            info2 = self.sec_use(myteams)
            info3 = self.th_use(warth)
            return is_none(info2, info3)
        return ['忍术发动失败']


class DaSheWan(Person):

    def __init__(self, name, attack, hp, shield=0):
        super().__init__(name, attack, hp)
        self._talent = BaiShe('白蛇之身')
        self._fir_skill = SkillAttack('潜影蛇肢')
        self._sec_skill = SheNiZhouFu('蛇睨咒缚')
        self._th_skill = HuiTuZhuanSheng('秽土转生')
        self._image = './images/大蛇丸.jpg'

    def t_use(self):
        info = self._talent.baishe(self)
        if info is not None:
            return '%s的%s生效，恢复%s的生命' % (self.name, info[0], info[1])

    def sec_use(self, other, warth):
        info = self._sec_skill.is_used(self, other, warth)
        if info is not None:
            return info

    def th_use(self, myteams, warth):
        info = self._th_skill.is_used(self, myteams, warth)
        if info is not None:
            return info

    def attack_s(self, other, myteams, others, warth):
        if not self._effect:
            info1 = self.t_use()
            info2 = self.sec_use(other, warth)
            info3 = self.th_use(myteams, warth)
            return is_none(info1, info2, info3)
        return ['忍术发动失败']











