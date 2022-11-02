from xmlrpc.client import ServerProxy
from os.path import join, isfile, abspath, isdir
from os import listdir
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
from time import sleep
import sys
import os
import shutil
import queue
from threading import Thread, Timer


SimpleXMLRPCServer.allow_reuse_address = 1

OK = 0
FAIL = -1
EMPTY = ""

keep_q = queue.Queue(1)
SLEEP_TIME = 1

STOPTHREAD = "__STOPTHREAD__"
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
        self.term = 1
        self.is_master = True
        self.master_url = url
        if self.is_master:
            self._master_init()
        self.slave_count = 0
        self.node = [self.url]

    def _master_init(self):
        self.keep_alive_thread = Thread(target=self.is_keep_alive)
        self.keep_alive_thread.daemon = True
        self.keep_alive_thread.start()

    def change_to_slave(self):
        keep_q.put(STOPTHREAD)

    def recv_add(self, url):
        if not self.is_master:
            return FAIL, EMPTY
        else:
            if not self.node.count(url):
                self.node.append(url)
                keep_q.put(self.node.copy())

                print(url+":join")
                no_notify = []
                no_notify.append(url)
                self.node_broadcast(no_notify)
                self.slave_count = self.slave_count+1
                self.notify_gui(self.slave_count)
                return OK, [self.node.copy(), self.term]
            else:
                return OK, [self.node.copy(), self.term]

    def notify_gui(self, mode=-1):
        self.q.put(mode)

    def add_cluster(self, url):
        try:
            ret, msg = ServerProxy(url).recv_add(self.url)
            if ret == FAIL:
                return FAIL, EMPTY
            else:
                self.master_url = url
                self.is_master = False
                self.change_to_slave()

                self.node = msg[0]
                self.term = msg[1]
                print(self.node)
                return OK, EMPTY
        except:
            return FAIL, EMPTY

    def node_notify(self, node):
        self.node = node.copy()
        print(self.node)
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
        for other in self.node.copy():
            if other == self.url:
                continue
            try:
                print(other)
                ret, data = ServerProxy(other).remote_fetch(query)
                print(ret)
                if ret == OK:
                    return ret, data
            except:
                self.node.remove(other)
        return FAIL, EMPTY

    def ping(self):
        return OK

    def hello(self, node):
        """
        将其他节点添加到已知节点
        """
        self.node = node.copy()
        return OK

    def get_list(self, client_current_path):
        file_list_atfer = []
        # return OK
        for item in listdir(client_current_path):
            if isdir(join(client_current_path, item)):
                file_list_atfer.append("(dir)"+item)
            else:
                file_list_atfer.append(item)
        for url in self.node.copy():
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
                self.node.remove(url)
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

    def notify_other_node(self):
        for url in self.node.copy():
            if url == self.url:
                continue
            try:
                ServerProxy(url).notify_gui()
            except:
                print('notify other gui error')
                self.node.remove(url)
        print("notify other node ok")

    def node_leave(self, url):
        self.node.remove(self.url)
        if not self.is_master:
            try:
                ServerProxy(self.master_url).recv_leave(self.url)
                return OK, EMPTY
            except:
                self.try_change_master()
        else:
            if self.node == []:
                return OK, EMPTY
            else:
                for url in self.node:
                    try:
                        ServerProxy(url).change_to_master(
                            [self.node, self.term])
                        ServerProxy(url).broadcast_new_master()
                        return OK, EMPTY
                    except:
                        continue
                    return OK, EMPTY

    def try_change_to_master(self):
        pass

    def chang_to_master(self, node, term):
        self._master_init()
        self.node = node
        self.term = term
        self.is_master = True
        self.master_url = self.url

    def broadcast_new_master(self):
        for url in self.node:
            if url == self.url:
                continue
            try:
                ServerProxy(url).notify_new_master(self.url)
            except:
                self.node.remove(url)
                self.node_broadcast()

    def notify_new_master(self, url):
        self.master_url = url
        self.is_master = False

    def recv_leave(self, url):
        print(url+":leave")
        self.node.remove(url)
        self.slave_count = self.slave_count-1
        self.notify_gui(self.slave_count)

        keep_q.put(self.node.copy())
        self.node_broadcast()

    def node_broadcast(self, no_notify=[], new_node=[]):
        if new_node != []:
            self.node = new_node
        for url in self.node.copy():
            try:
                if url in no_notify or url == self.url:
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
                tmp = keep_q.get_nowait()
                if tmp == STOPTHREAD:
                    break
                else:
                    node = tmp
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
                self.node_broadcast([], node)


def main():
    url, dir, secert = sys.argv[1:]
    n = NodeServer(url, dir, secert)
    n._start()


if __name__ == "__main__":
    main()
