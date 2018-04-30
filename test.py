import time

from Naruto.person import *


def main():
    mingren = MingRen('旋涡鸣人', 1200, 30000)
    zuozhu = ZuoZhu('佐助', 1200, 30000)
    warth = 0
    while True:
        if mingren.is_die() or zuozhu.is_die():
            break
        for debuff in mingren.debuffs_effect():
            print(debuff)
        warth += 5
        print(mingren)
        print(zuozhu)
        print(mingren.t_use())
        print(mingren.attack_to(zuozhu))
        print(mingren.sec_use())
        print(mingren.th_use(mingren))
        print(zuozhu.attack_to(mingren))
        print(zuozhu.t_attack_to(mingren, warth))
        print(zuozhu.sec_use())
        print(zuozhu.th_use(mingren))
        time.sleep(1)
        print('= ' * 10)


if __name__ == '__main__':
    main()