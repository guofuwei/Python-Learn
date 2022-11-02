'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-01 20:04:03
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-01 20:22:22
FilePath: /Python-Learn/homework/work5.py
Description: 运用Monte Carno 方法计算圆周率的近似值。

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
from random import random

times = int(input('请输入蒙特卡罗模拟次数：'))
hits = 0
for i in range(times):  # 循环
    x = random()  # 产生随机数
    y = random()
    if x*x+y*y <= 1:
        hits += 1
print(4.0*hits/times)
