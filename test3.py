'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-02 20:00:37
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-02 20:34:14
FilePath: /Python-Learn/test3.py
Description: 

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
from threading import Thread, Lock
from time import sleep
import queue

lock = Lock()
node = list()
q = queue.Queue(1)


def add1():
    global node
    # lock.acquire()
    node.append(1)
    # lock.release()


def print1():
    while True:
        global node
        sleep(1)
        print(node)


def main():
    t = Thread(target=print1)
    t.setDaemon(True)
    t.start()
    while True:
        sleep(1.5)
        add1()
        # print(node)
    t.join()


main()
