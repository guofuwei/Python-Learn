'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-05 20:13:09
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 20:25:00
FilePath: /Python-Learn/homework/work8.py
Description: 有三顶红帽子和两顶白帽子。将其中的三顶帽子分别戴在 A、B、C三人头上。这三人每人都只能看见其他两人头上的帽子，但看不见自己头上戴的帽子，并且也不知道剩余的两顶帽子的颜色。问A：“你戴的是什么颜色的帽子?” A回答说:“不知道。” 接着，又以同样的问题问B。B想了想之后，也回答说:“不知道。” 最后问C。C回答说:“我知道我戴的帽子是什么颜色了。” 当然，C是在听了A、B的回答之后而作出回答的。请尝试用编程方法解答此问题。


Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
ls = ['red', 'white', ]
'''
首先将所有情况进行遍历，然后用条件判断选出符合条件的情况，输出该情况中c的回答
'''


def main():
    # 利用循环进行遍历
    for A in ls:
        for B in ls:
            for C in ls:
                A1 = (A == 'red')  # A戴红帽子
                A2 = (A == 'white')  # A戴白帽子
                B1 = (B == 'red')  # B戴红帽子
                B2 = (B == 'white')  # B戴白帽子
                C1 = (C == 'red')  # C戴红帽子
                C2 = (C == 'white')  # C戴白帽子
                D = not B2 and not C2  # 由A的回答知道，B和C两个人不能都戴白帽子
                E = not A2 and not C2  # 由B的回答知道，A和C两个人不能都戴白帽子
                F = not A2 and not B2 and not C2  # 只有两顶白帽子
                if (D and E and F) == 1:
                    if C1 == 1:
                        print('C戴红帽子')
                    if C2 == 1:
                        print('C戴白帽子')


if __name__ == "__main__":
    main()
