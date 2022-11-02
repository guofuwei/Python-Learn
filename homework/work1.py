'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-09-26 19:49:33
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 19:39:37
FilePath: /Python-Learn/homework/work1.py
Description: 100的阶乘是多少？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def main():
    sum = 1
    for i in range(1, 101):
        sum = sum*i
    print("100!=%d" % sum)


if __name__ == "__main__":
    main()
