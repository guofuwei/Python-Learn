'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-11-02 17:01:16
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-02 23:40:33
FilePath: /Python-Learn/file_share_copy/center_server.py
Description: 

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
from platform import node
from threading import Thread, Lock
from time import sleep
from xml.etree.ElementTree import QName
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys
import queue


SimpleXMLRPCServer.allow_reuse_address = True


OK = 0
FAIL = -1
EMPTY = ""

SLEEP_TIME = 1

lock = Lock()
q = queue.Queue(1)


def get_port(url):
    '从url中提取端口'
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])


class CenterNode:
    '''
    P2P改进后节点
    '''

    def __init__(self, url):
        self.url = url
        self.node = []

    def node_get_msg(self, url):
        if not self.node.count(url):
            self.node.append(url)
            q.put(self.node.copy())

            print(url+":join")
            no_notify = []
            no_notify.append(url)
            self.node_broadcast(no_notify)

        return self.node.copy()

    def node_leave(self, url):
        print(url+":leave")
        self.node.remove(url)

        q.put(self.node)
        self.node_broadcast()

    def node_broadcast(self, no_notify=[]):
        for url in self.node.copy():
            try:
                if url in no_notify:
                    continue
                ret = ServerProxy(url).node_notify(self.node.copy())
                print(ret)
            except:
                print("broadcast error")
                self.node.remove(url)

    def is_keep_alive(self):
        node = []
        while True:
            sleep(SLEEP_TIME)

            try:
                node = q.get_nowait()
            except:
                pass
            # print(node)
            node_copy = node.copy()
            for url in node_copy:
                try:
                    ServerProxy(url).ping()
                except:
                    print(url+":timeout and removed")
                    node.remove(url)
            if node_copy != node:
                self.node_broadcast()

    def _start(self):
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        print("心跳线程已启动")
        print("中心服务器已在"+self.url+"上运行")
        s.register_instance(self)
        s.serve_forever()


def main():
    if not sys.argv[1]:
        print("请使用python center_server.py [url]启动")
        return
    url = sys.argv[1]
    n = CenterNode(url)
    keep_alive_thread = Thread(target=n.is_keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()
    n._start()
    keep_alive_thread.join()


if __name__ == "__main__":
    main()
