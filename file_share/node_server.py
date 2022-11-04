'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-09-30 15:27:02
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-04 15:37:31
FilePath: /Python-Learn/file_share/node_server.py
Description: 节点服务器

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from xmlrpc.client import ServerProxy
from os.path import join, isfile, abspath, isdir
from os import listdir
from xmlrpc.server import SimpleXMLRPCServer
from time import sleep
from urllib.parse import urlparse
import sys
import os
import shutil

# 跳过TCP关闭连接的TIME_WAIT，直接复用地址
SimpleXMLRPCServer.allow_reuse_address = 1


# 标志位
OK = 0
FAIL = -1
EMPTY = ""

RemoteFileBefore = "[remote]"


def path_check(dir, name) -> str:
    """检查路径是否合法

    Args:
        dir (str): 目录名
        name (str): 文件名

    Returns:
        str: 合法路径
    """
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ""))


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


def get_real_dirname(dirname) -> str:
    """去除目录的前缀名(dir)

    Args:
        dirname (str):  目录名

    Returns:
        str: 去除前缀的真实目录名
    """
    return dirname[5:]


class NodeServer:
    '''
    P2P节点服务器
    '''

    def __init__(self, url, dirname):
        """初始化节点服务器

        Args:
            url (str): url
            dirname (str): 节点服务器工作目录
        """
        self.url = url
        self.dirname = dirname
        self.known = list()  # 目前已知的节点

    def node_notify(self, node) -> str:
        """接受中心服务器的节点通知

        Args:
            node (list): 节点列表

        Returns:
            str: msg
        """
        self.known = node.copy()
        print(self.known)
        # 通知更新GUI客户端文件列表
        self.notify_gui()
        return "notify ok"

    def fetch(self, client_current_path, query) -> tuple[int, str]:
        """获取文件

        Args:
            client_current_path (str): 客户端当前路径
            query (str): 查找对象

        Returns:
            int: 状态吗 OK:0 FAIL:-1
            str:返回的数据或失败提示信息
        """
        if isdir(join(client_current_path, query)):
            return FAIL, "请选择文件，而不是文件夹"
        # 当拉取文件为远程文件时
        if query[:len(RemoteFileBefore)] == RemoteFileBefore:
            return self._broadcast(query)
        # 当拉取文件为本地文件时
        else:
            return self._handle(client_current_path, query)

    def remote_fetch(self, filename) -> tuple[int, str]:
        """回应远程拉取文件

        Args:
            filename (_type_): _description_

        Returns:
            int: 状态吗 OK:0 FAIL:-1
            str:返回的数据或失败提示信息
        """
        # 得到真实文件名
        filename = filename[len(RemoteFileBefore):]
        if isfile(join(self.dirname, filename)):
            with open(join(self.dirname, filename), encoding="utf-8") as f:
                data = f.read()
            return OK, data
        return FAIL, EMPTY

    def upload(self, client_current_path, filename, data) -> tuple[int, str]:
        """上传文件处理

        Args:
            client_current_path (str):  客户端当前目录
            filename (str): 文件名
            data (str): 文件数据

        Returns:
            int: 状态吗 OK:0 FAIL:-1
            str:返回的数据或失败提示信息
        """
        # 检查参数
        if not filename:
            return FAIL, "上传文件名为空"
        if isfile(join(client_current_path, filename)):
            return FAIL, "该文件已存在"
        try:
            with open(join(client_current_path, filename),
                      mode="w", encoding="utf-8") as f:
                f.write(data)
            # 通知其他节点该节点上传了文件
            self.notify_other_node()
            return OK, "OK"
        except:
            return FAIL, "写入失败"

    def _handle(self, client_current_path, query) -> tuple[int, str]:
        """在本节点查询文件

        Args:
            client_current_path (str): 客户端当前目录
            query (str): 文件名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
            str:返回的数据或失败提示信息
        """
        dir = client_current_path
        name = join(dir, query)
        if not isfile(name):
            return FAIL, EMPTY
        # 获得合法路径
        if not path_check(dir, name):
            return FAIL, EMPTY

        with open(name, encoding='utf-8') as f:
            data = f.read()
        return OK, data

    def _broadcast(self, query) -> tuple[int, str]:
        """在未查询过的已知节点中广播继续查询

        Args:
            query (str): 文件名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
            str:返回的数据或失败提示信息
        """
        for other in self.known.copy():
            # 跳过自己
            if other == self.url:
                continue
            try:
                # print(other)
                # 在其他节点查询
                ret, data = ServerProxy(other).remote_fetch(query)
                print(ret)
                if ret == OK:
                    return ret, data
            except:
                self.known.remove(other)
        return FAIL, EMPTY

    def ping(self) -> int:
        """回应中心服务器的心跳包

        Returns:
            int: 状态 OK:0 FAIL:-1
        """
        return OK

    def hello(self, node):
        """更新本地节点信息

        Args:
            node (list): 节点列表

        Returns:
            int: 状态 OK:0 FAIL:-1
        """
        self.known = node.copy()
        return OK

    def get_list(self, client_current_path) -> list:
        """获取文件信息

        Args:
            client_current_path (str): 客户当前路径

        Returns:
            list: 查询到的文件列表
        """
        file_list_atfer = []
        # 现在本地进行查询
        for item in listdir(client_current_path):
            # 对目录名加上前缀
            if isdir(join(client_current_path, item)):
                file_list_atfer.append("(dir)"+item)
            else:
                file_list_atfer.append(item)
        # 在其他节点查询公共文件
        for url in self.known.copy():
            try:
                if url == self.url:
                    continue
                list = ServerProxy(url).get_remote_list()
                file_list_atfer.append("[remote] "+url)
                for item in list:
                    file_list_atfer.append(item)
            except:
                self.known.remove(url)
        return file_list_atfer

    def get_remote_list(self) -> list:
        """回应远程查询文件列表

        Returns:
            list: 查询到的文件列表
        """
        file_list = []
        # 只在工作根目录查询，不递归查询
        for item in listdir(self.dirname):
            # 跳过文件夹
            if not isdir(join(self.dirname, item)):
                file_list.append("[remote]"+item)
        return file_list

    def change_dir(self, client_current_path, dirname) -> int:
        """改变目录处理逻辑

        Args:
            client_current_path (str): 客户端当前目录
            dirname (str): 目录名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
        """
        # 获取真实目录名
        dirname = get_real_dirname(dirname)
        if not isdir(join(client_current_path, dirname)):
            return FAIL
        else:
            return OK

    def create_dir(self, client_current_path, dirname) -> int:
        """创建目录处理逻辑

        Args:
            client_current_path (str): 客户端当前目录
            dirname (str): 目录名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
        """
        if not dirname:
            return FAIL
        try:
            os.mkdir(join(client_current_path, dirname))
            return OK
        except:
            return FAIL

    def delete_dir(self, client_current_path, dirname) -> int:
        """删除目录处理逻辑

        Args:
            client_current_path (str): 客户端当前目录
            dirname (str): 目录名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
        """
        if not dirname:
            return FAIL
        dirname = get_real_dirname(dirname)
        if not isdir(join(client_current_path, dirname)):
            return FAIL
        try:
            shutil.rmtree(join(client_current_path, dirname),
                          ignore_errors=True)
            return OK
        except:
            return FAIL

    def delete_file(self, client_current_path, filename) -> int:
        """删除文件处理逻辑

        Args:
            client_current_path (str): 客户端当前目录
            filename (str): 文件名

        Returns:
            int: 状态吗 OK:0 FAIL:-1
        """
        if not filename:
            return FAIL
        if isdir(join(client_current_path, get_real_dirname(filename))):
            return FAIL
        try:
            os.remove(join(client_current_path, filename))
            # 通知其他节点
            self.notify_other_node()
            sleep(0.1)
            return OK
        except:
            return FAIL

    def notify_gui(self) -> int:
        """向管道中写入数据，通知GUI客户端

            Returns:
            int: 状态吗 OK:0 FAIL:-1
        """
        self.q.put(1)
        return OK

    def notify_other_node(self):
        """通知其他节点本地上传了文件
        """
        for url in self.known.copy():
            # 排除自己
            if url == self.url:
                continue
            try:
                ret = ServerProxy(url).notify_gui()
                print("notify "+url+":"+str(ret))
            except:
                print('notify other gui error')
                self.known.remove(url)
        print("notify other gui suceess")

    def _start(self, q):
        """启动节点服务器

        Args:
            q (queue.Queue): 管道
        """
        self.q = q
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()


def main():
    """main函数
    """
    url, dir, secert = sys.argv[1:]
    n = NodeServer(url, dir, secert)
    n._start()


if __name__ == "__main__":
    main()
