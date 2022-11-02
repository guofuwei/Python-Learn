'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 19:39:28
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 19:45:37
FilePath: /Python-Learn/homework/work3.py
Description: 100个人集中在一个房间，至少有两个人生日相同的概率有多大？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def main():
    p = 1
    for i in range(0, 100):
        p = p*(365-i)/365
    print("100个人至少有两个人生日相同的概率是"+str((1-p)*100)+"%")


if __name__ == "__main__":
    main()
