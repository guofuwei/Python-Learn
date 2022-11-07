'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-05 20:29:29
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 20:36:33
FilePath: /Python-Learn/homework/work10.py
Description: 八皇后问题编程解答

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

C = 0


def run(num=8):
    """启动

    Args:
        num (int, optional): 皇后数. Defaults to 8.
    """
    result = [-1] * num
    row = 0
    backtrack(result, row)


def backtrack(result, row):
    """递归回溯解决问题

    Args:
        result (array): 答案列表
        row (int): 行数
    """
    n = len(result)
    if row == n:
        global C
        C += 1
        print(result)
        return
    for i in range(n):
        result[row] = i
        if isvalid(result, row):
            backtrack(result, row+1)


def isvalid(ans, pos) -> bool:
    """判读当前位置是否已经超出了棋盘

    Args:
        ans (array): 答案列表
        pos (int): 位置

    Returns:
        bool: True:合法 False:非法
    """
    valid = True
    for i in range(pos):
        diag = pos - i
        if ans[pos] in [ans[i], ans[i] - diag, ans[i] + diag]:
            valid = False
            break
    return valid


def main():
    """main
    """
    run(num=8)
    print('solution num:', C)


if __name__ == '__main__':
    main()
