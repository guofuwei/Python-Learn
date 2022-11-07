'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-05 19:43:11
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 20:01:27
FilePath: /Python-Learn/homework/work7.py
Description: . 有两个序列a,b，大小都为n,序列元素的值任意整形数，无序；要求：通过交换a,b中的元素，使序列a元素的和与序列b元素的和之间的差最小

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

import random


def mean(sorted_list) -> tuple[list, list]:
    """将一个已排序列表分为两个距离最小的列表

    Args:
        sorted_list (list): 需要拆分的列表

    Returns:
        list: 列表1
        list: 列表2
    """
    if not sorted_list:
        return (([], []))
    big = sorted_list[-1]
    small = sorted_list[-2]
    big_list, small_list = mean(sorted_list[:-2])
    big_list.append(small)
    small_list.append(big)
    big_list_sum = sum(big_list)
    small_list_sum = sum(small_list)
    if big_list_sum > small_list_sum:
        return ((big_list, small_list))
    else:
        return ((small_list, big_list))


def random_list(num, limit1, limit2) -> list:
    """生成随机序列

    Args:
        num (int): 随机序列长度个数
        limit1(int): 随机数下限
        limit2(int): 随机数上限

    Returns:
        list: 生成的随机序列
    """
    random_list = []
    for i in range(0, num):
        random_list.append(random.randint(limit1, limit2))
    return random_list


def distance_list(list1, list2) -> int:
    """计算两个列表和的距离

    Args:
        list1 (list): 列表1
        list2 (list): 列表2

    Returns:
        int: 距离
    """
    return abs(sum(list1)-sum(list2))


def main():
    """main
    """
    # 生成两个随机序列
    l1 = random_list(10, -100, 100)
    l2 = random_list(10, -100, 100)
    print("列表1:", end="")
    print(l1)
    print("列表1:", end="")
    print(l2)
    print("两个列表原距离为:%s" % distance_list(l1, l2))
    # 对两个列表进行处理
    l1.extend(l2)
    l1.sort()
    l1, l2 = mean(l1)
    # 打印处理后的两列表距离
    print("处理后两列表如下")
    print("列表1:", end="")
    print(l1)
    print("列表1:", end="")
    print(l2)
    print("两个列表处理后距离为:%s" % distance_list(l1, l2))


if __name__ == "__main__":
    main()
