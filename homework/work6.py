'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 20:26:56
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 20:37:28
FilePath: /Python-Learn/homework/work6.py
Description: 

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''


def age_sort(nums):
    d = []
    e = []
    for a in range(1, nums+1):
        for b in range(1, a+1):
            for c in range(1, b+1):
                if a*b*c == nums:
                    d.append([a, b, c])
                    e.append(a+b+c)
    # 枚举出三个孩子所有可能的年龄情况并将年龄和计算出来
                else:
                    continue
    print(d)
    print(e)
    e.sort()
    print(e)  # 对列表直接sort（排序）,时间复杂度时nlogn
    i = [m-1 for m in range(1, len(e)) if e[m] ==
         e[m-1]]  # 对所有年龄情况的年龄和排序找相同的年龄的情况
    age = d[i[0]]  # 计算出此时其中一种年龄情况的可能
    if age[0] != age[1]:
        return age
    else:
        return d[i[0]+1]


age = age_sort(36)
print(age)
