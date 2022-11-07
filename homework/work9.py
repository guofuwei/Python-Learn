'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-05 20:25:18
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 20:28:45
FilePath: /Python-Learn/homework/work9.py
Description: 汉诺塔问题编程解答

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def hanoi(n, x, y, z):
    """递归解决汉诺塔问题

    Args:
        n (int): 圆盘的层数
        x (int): x柱
        y (int): y柱
        z (int): z柱
    """
    if n == 1:
        print(x, '-->', z)
    else:
        # 将X塔上1~n-1个圆盘移到Y塔上，以Z塔为辅助塔
        hanoi(n-1, x, z, y)
        # 将第n个圆盘移到Z塔上
        print(x, '-->', z)
        # 把Y塔上编号1~n-1的圆盘移到Z上，以X为辅助塔
        hanoi(n-1, y, x, z)


def main():
    n = int(input('请输入汉诺塔层数：'))
    hanoi(n, 'x', 'y', 'z')


if __name__ == "__main__":
    main()
