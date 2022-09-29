from curses.ascii import EM
from xmlrpc.client import ServerProxy
from os.path import join, isfile
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys

MAX_HISTORY_LENGTH = 6

OK = 0
FAIL = -1
EMPTY = ""


def get_port(url):
    '从url中提取端口'
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])


class SimpleNode:
    '''
    P2P简单节点
    '''

    def __init__(self, url, dirname, secert):
        self.url = url
        self.dirname = dirname
        self.secert = secert
        self.known = set()

    def query(self, query, history=[]):
        '''
        首先在本节点查询文件，当查询失败后，尝试在已知节点中继续查询
        '''
        code, data = self._handle(query)
        if code == OK:
            return code, data
        else:
            history.append(self.url)
            if len(history) > MAX_HISTORY_LENGTH:
                return FAIL, EMPTY
            return self._broadcast(query, history)

    def _handle(self, query):
        """
        在本节点查询文件
        """
        filename = join(self.dirname, query)
        if not isfile(filename):
            return FAIL, EMPTY
        return OK, open(filename, encoding='utf-8').read()

    def _broadcast(self, query, history):
        """
        在未查询过的已知节点中广播继续查询
        """
        for other in self.known.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                code, data = s.query(query, history)
                if code == OK:
                    return code, data
            except:
                self.known.remove(other)
        return FAIL, EMPTY

    def hello(self, other):
        """
        将其他节点添加到已知节点
        """
        self.known.add(other)
        return OK

    def fetch(self, query, secert):
        if secert != self.secert:
            return FAIL
        code, data = self.query(query)
        if code == OK:
            f = open(join(self.dirname, query), 'w')
            f.write(data)
            f.close()
            return OK
        else:
            return FAIL

    def _start(self):
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()


def main():
    url, dir, secert = sys.argv[1:]
    n = SimpleNode(url, dir, secert)
    n._start()


if __name__ == "__main__":
    main()
