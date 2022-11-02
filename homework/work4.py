'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 19:46:25
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 20:01:36
FilePath: /Python-Learn/homework/work4.py
Description: 有一个五位数abcde，乘以4以后变成edcba，abcde是多少？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def num2bit(value) -> list:
    return list(map(str, str(value)))


def main():
    for i in range(10000, 100000):
        bit_list = num2bit(i)
        bit_list.reverse()
        if int("".join(bit_list)) == i*4:
            print(i)


if __name__ == "__main__":
    main()
