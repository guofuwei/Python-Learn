'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 20:26:56
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-05 19:39:15
FilePath: /Python-Learn/homework/work6.py
Description: 一普查员问一位女士,“你有多少个孩子,他们多少岁?”女士回答:“我有三个孩子,他们的岁数相乘是36,岁数相加就等于隔离间屋的门牌号码.”普查员立刻走到隔邻,看了一看,回来说:”我还需要多少资料.”女士回答:“我现在很忙,我最大的孩子正在楼上睡觉.”普查员说:”谢谢,我己知道了 问题:那三个孩子的岁数是多少？

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def age_find(nums):
    age_list = []
    sum_list = []
    # 寻找nums的三个公因数
    for a in range(1, nums+1):
        for b in range(1, a+1):
            for c in range(1, b+1):
                if a*b*c == nums:
                    age_list.append([a, b, c])
                    sum_list.append(a+b+c)
                else:
                    continue
    # 返回
    return age_list, sum_list


def main():
    age_list, sum_list = age_find(36)
    # 对公因数之和进行排序
    sum_list.sort()
    # 寻找有相同两个相同公因数的三个公因数
    i = [m-1 for m in range(1, len(sum_list)) if sum_list[m] ==
         sum_list[m-1]]
    age = age_list[i[0]]  # 计算出此时其中一种年龄情况的可能
    if age[0] != age[1]:
        print
    else:
        print(age_list[i[0]+1])


if __name__ == '__main__':
    main()
