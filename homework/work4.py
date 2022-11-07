'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 19:46:25
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 19:42:02
FilePath: /Python-Learn/homework/work4.py
Description: 有一个五位数abcde，乘以4以后变成edcba，abcde是多少？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def num2bit(value) -> list:
    """取出数字的每一位，以列表的形式返回

    Args:
        value (int): 输入的数字

    Returns:
        list: 数字各位组成的列表
    """
    return list(map(str, str(value)))


def main():
    for i in range(10000, 100000):
        bit_list = num2bit(i)
        # 对数字各位列表进行取反
        bit_list.reverse()
        if int("".join(bit_list)) == i*4:
            print(i)


if __name__ == "__main__":
    main()
