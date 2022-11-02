from tkinter.tix import Tree
from xmlrpc.client import ServerProxy, Fault
from os.path import join, isfile, abspath, isdir
from os import listdir
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys
import os
import shutil


SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 400
ACCESS_DENIED = 403

OK = 0
FAIL = -1
EMPTY = ""

RemoteFileBefore = "[remote]"


def path_check(dir, name):
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ""))


def get_port(url):
    '从url中提取端口'
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])


def get_real_dirname(dirname):
    return dirname[5:]


class NodeServer:
    '''
    P2P改进后节点
    '''

    def __init__(self, url, dirname):
        self.url = url
        self.dirname = dirname
        self.known = list()

    def node_notify(self, node):
        self.known = node.copy()
        print(self.known)
        self.notify_gui()
        return "notify ok"

    def fetch(self, client_current_path, query):
        '''
        获取文件
        '''
        if isdir(join(client_current_path, query)):
            return FAIL, "请选择文件，而不是文件夹"
        if query[:len(RemoteFileBefore)] == RemoteFileBefore:
            return self._broadcast(query)
        else:
            return self._handle(client_current_path, query)

    def remote_fetch(self, filename):
        filename = filename[len(RemoteFileBefore):]
        if isfile(join(self.dirname, filename)):
            with open(join(self.dirname, filename), encoding="utf-8") as f:
                data = f.read()
            return OK, data
        return FAIL, EMPTY

    def upload(self, client_current_path, filename, data):
        if not filename:
            return FAIL, "上传文件名为空"
        if isfile(join(client_current_path, filename)):
            return FAIL, "该文件已存在"
        try:
            with open(join(client_current_path, filename),
                      mode="w", encoding="utf-8") as f:
                f.write(data)
            self.notify_other_node()
            return OK, "OK"
        except:
            return FAIL, "写入失败"

    def _handle(self, client_current_path, query):
        """
        在本节点查询文件
        """
        dir = client_current_path
        name = join(dir, query)
        if not isfile(name):
            return FAIL, EMPTY
        if not path_check(dir, name):
            return FAIL, EMPTY

        with open(name, encoding='utf-8') as f:
            data = f.read()
        return OK, data

    def _broadcast(self, query):
        """
        在未查询过的已知节点中广播继续查询
        """
        for other in self.known.copy():
            if other == self.url:
                continue
            try:
                print(other)
                ret, data = ServerProxy(other).remote_fetch(query)
                print(ret)
                if ret == OK:
                    return ret, data
            except:
                self.known.remove(other)
        return FAIL, EMPTY

    def ping(self):
        return OK

    def hello(self, node):
        """
        将其他节点添加到已知节点
        """
        self.known = node.copy()
        return OK

    def get_list(self, client_current_path):
        file_list_atfer = []
        # return OK
        for item in listdir(client_current_path):
            if isdir(join(client_current_path, item)):
                file_list_atfer.append("(dir)"+item)
            else:
                file_list_atfer.append(item)
        for url in self.known.copy():
            try:
                if url == self.url:
                    continue
                # print(url)
                list = ServerProxy(url).get_remote_list()
                # print(list)
                file_list_atfer.append("[remote] "+url)
                for item in list:
                    file_list_atfer.append(item)
            except:
                self.known.remove(url)
        return file_list_atfer

    def get_remote_list(self):
        file_list = []
        for item in listdir(self.dirname):
            if not isdir(join(self.dirname, item)):
                file_list.append("[remote]"+item)
        return file_list

    def change_dir(self, client_current_path, dirname):
        dirname = get_real_dirname(dirname)
        if not isdir(join(client_current_path, dirname)):
            return FAIL
        else:
            return OK

    def create_dir(self, client_current_path, dirname):
        if not dirname:
            return FAIL
        try:
            os.mkdir(join(client_current_path, dirname))
            return OK
        except:
            return FAIL

    def delete_dir(self, client_current_path, dirname):
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

    def delete_file(self, client_current_path, filename):
        # print(filename)
        if not filename:
            return FAIL
        if isdir(join(client_current_path, get_real_dirname(filename))):
            return FAIL
        try:
            # print(filename)
            os.remove(join(client_current_path, filename))
            return OK
        except:
            return FAIL

    def _start(self, q):
        self.q = q
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()

    def notify_gui(self):
        self.q.put(1)

    def notify_other_node(self):
        for url in self.known.copy():
            if url == self.url:
                continue
            try:
                ServerProxy(url).notify_gui()
            except:
                print('notify other gui error')
                self.known.remove(url)
        print("notify other gui suceess")


def main():
    url, dir, secert = sys.argv[1:]
    n = NodeServer(url, dir, secert)
    n._start()


if __name__ == "__main__":
    main()
