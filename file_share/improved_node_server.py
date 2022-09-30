from xmlrpc.client import ServerProxy, Fault
from os.path import join, isfile, abspath
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 400
ACCESS_DENIED = 403

OK = 0
FAIL = -1
EMPTY = ""


class UnhandledQuery(Fault):
    def __init__(self, msg="Couldn't handle the query"):
        super().__init__(UNHANDLED, msg)


class AccessDenied(Fault):
    def __init__(self, msg="Access Denied"):
        super().__init__(ACCESS_DENIED, msg)


def path_check(dir, name):
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ""))


def get_port(url):
    '从url中提取端口'
    name = urlparse(url)[1]
    parts = name.split(":")
    return int(parts[-1])


class ImprovedNode:
    '''
    P2P改进后节点
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
        try:
            return self._handle(query)
        except UnhandledQuery:
            history.append(self.url)
            if len(history) > MAX_HISTORY_LENGTH:
                raise
            return self._broadcast(query, history)

    def _handle(self, query):
        """
        在本节点查询文件
        """
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):
            raise UnhandledQuery
        if not path_check(dir, name):
            raise AccessDenied
        return OK, open(name, encoding='utf-8').read()

    def _broadcast(self, query, history):
        """
        在未查询过的已知节点中广播继续查询
        """
        for other in self.known.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                return s.query(query, history)
            except Fault as f:
                if f.faultCode == UNHANDLED:
                    pass
                else:
                    self.known.remove(other)
            except:
                self.known.remove(other)
        raise UnhandledQuery

    def hello(self, other):
        """
        将其他节点添加到已知节点
        """
        self.known.add(other)
        return OK

    def fetch(self, query, secert):
        if secert != self.secert:
            raise AccessDenied
        _, data = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(data)
        f.close()
        return OK

    def _start(self):
        s = SimpleXMLRPCServer(("", get_port(self.url)), logRequests=False)
        s.register_instance(self)
        s.serve_forever()


def main():
    url, dir, secert = sys.argv[1:]
    n = ImprovedNode(url, dir, secert)
    n._start()


if __name__ == "__main__":
    main()
