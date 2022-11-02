'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-09-26 19:49:33
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 19:39:56
FilePath: /Python-Learn/homework/work2.py
Description: 一只青蛙一次只能跳一级或者两级台阶，青蛙跳到100级台阶有多少种跳法？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
sum = 0


def main():
    sum = find(100)
    print("All methods:%d" % (sum))


def find(n):
    if n <= 1:
        return 1
    dp = [0]*(n+1)
    dp[0] = dp[1] = 1
    for i in range(2, n+1):
        dp[i] = dp[i-1]+dp[i-2]
    return dp[n]


if __name__ == "__main__":
    main()
