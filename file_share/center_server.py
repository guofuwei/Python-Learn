'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-02 17:01:16
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-04 15:24:37
FilePath: /Python-Learn/file_share/center_server.py
Description: 中心服务器

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
from threading import Thread
from time import sleep
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys
import queue

# 跳过TCP关闭连接的TIME_WAIT，直接复用地址
SimpleXMLRPCServer.allow_reuse_address = True


OK = 0
FAIL = -1
EMPTY = ""

# 心跳线程的时间间隔
SLEEP_TIME = 1

# 用来和心跳线程通信的管道
q = queue.Queue(1)


def get_port(url) -> int:
    """从url中提取端口号

    Args:
        url (str): url

    Returns:
        int: 端口号
    """
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])


class CenterNode:
    """中心服务器
    """

    def __init__(self, url):
        """初始化中心服务器

        Args:
            url (str): url
        """
        self.url = url
        self.node = []

    def node_get_msg(self, url) -> list:
        """节点服务加入网络，获取节点信息

        Args:
            url (str): url

        Returns:
            list: 节点信息
        """
        # 当前节点列表中没有该节点
        if not self.node.count(url):
            # 将该节点加入节点列表
            self.node.append(url)
            # 通知心跳线程节点变化
            q.put(self.node.copy())

            print(url+":join")
            no_notify = []
            no_notify.append(url)
            # 向除了新加入节点之外的节点更新节点信息
            self.node_broadcast(no_notify)

        return self.node.copy()

    def node_leave(self, url):
        """处理节点离开

        Args:
            url (str): url
        """
        print(url+":leave")
        # 在节点列表中移除该节点
        self.node.remove(url)
        # 通知心跳线程节点变化
        q.put(self.node)
        # 广播节点信息变化
        self.node_broadcast()

    def node_broadcast(self, no_notify=[], new_node=[]):
        """广播节点信息变化

        Args:
            no_notify (list, optional): 忽略广播的节点url. Defaults to [].
        """
        if new_node != []:
            self.node = new_node
            print("remain node:", end="")
            print(self.node)
        for url in self.node.copy():
            try:
                # 忽略该节点
                if url in no_notify:
                    continue
                ret = ServerProxy(url).node_notify(self.node.copy())
                print(ret)
            except:
                print("broadcast error")
                self.node.remove(url)

    def is_keep_alive(self):
        """心跳线程
        """
        node = []
        while True:
            # 休眠
            sleep(SLEEP_TIME)

            try:
                # 获取最新的节点列表
                node = q.get_nowait()
            except:
                pass
            # print(node)
            node_copy = node.copy()
            for url in node_copy:
                try:
                    ServerProxy(url).ping()
                except:
                    # 移除超时的节点
                    print(url+":timeout and removed")
                    node.remove(url)
            if node_copy != node:
                # 广播节点信息
                self.node_broadcast([], node)

    def _start(self):
        """启动服务器
        """
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        print("中心服务器已在"+self.url+"上运行")
        s.register_instance(self)
        s.serve_forever()


def main():
    """main函数
    """
    if not sys.argv[1]:
        print("请使用python center_server.py [url]启动")
        return
    url = sys.argv[1]
    n = CenterNode(url)
    # 启动心跳线程
    keep_alive_thread = Thread(target=n.is_keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()
    print("心跳线程已启动")
    n._start()
    keep_alive_thread.join()


if __name__ == "__main__":
    main()
