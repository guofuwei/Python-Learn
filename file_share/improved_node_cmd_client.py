from cmd import Cmd
from http import client
from string import ascii_lowercase
from threading import Thread
from xmlrpc.client import Fault, ServerProxy
from random import choice
from improved_node_server import ImprovedNode
from time import sleep
import sys


SECERT_LEN = 32


def random_str(length):
    """
    返回指定长度的随机字符串
    """
    chars = []
    letters = ascii_lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)


class Client(Cmd):
    def __init__(self, url, dirname, urlfile):
        """
        初始化客户端，设置url,dirname,urlfile,并在单独的线程中启动服务器
        """
        Cmd.__init__(self)
        self.secert = random_str(SECERT_LEN)
        n = ImprovedNode(url, dirname, self.secert)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        sleep(0.1)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            if line == url:
                continue
            self.server.hello(line)

    def do_fetch(self, arg):
        "调用server fetch方法"
        try:
            self.server.fetch(arg, self.secert)
        except Fault as f:
            print(f)

    def do_query(self, arg):
        "调用server query方法"
        try:
            _, ret = self.server.query(arg)
            print(ret)
        except Fault as f:
            print(f)

    def do_exit(self, arg):
        "退出程序"
        print()
        sys.exit()

    do_EOF = do_exit


def main():
    urlfile, dir, url = sys.argv[1:]
    client = Client(url, dir, urlfile)
    client.cmdloop()


if __name__ == "__main__":
    main()
