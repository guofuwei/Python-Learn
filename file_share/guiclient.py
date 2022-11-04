'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-01 16:55:26
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-04 15:15:21
FilePath: /Python-Learn/file_share/guiclient.py
Description: GUI版本的客户端

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved.
'''
import tkinter
from tkinter import END
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfilename
from xmlrpc.client import Fault, ServerProxy
import os
import sys
from node_server import NodeServer
from threading import Thread
from time import sleep
import time
import queue

# 返回的标准位
FAIL = -1
OK = 0

EMPTY_LIST = "空空如也"
DefaultName = "当前未选中文件"
DefaultIP = "localhost"
DefaultPort = "11000"
RemoteFileBefore = "[remote]"

# 通知线程与本地节点服务器通信的管道
q = queue.Queue(1)


class GuiClient:
    """GuiClient文件共享客户端
    """

    def __init__(self, url, dir):
        """初始化

        Args:
            url (str): 启动的url
            dir (str): 节点服务器运行的工作目录
        """
        self.window = tkinter.Tk()  # 创建tkinter实例对象
        self.server = None
        self.root_path = dir
        self.current_path = dir
        self.url = url
        # 启动节点服务器
        n = NodeServer(url, dir)
        t = Thread(target=n._start, args=(q,))
        t.setDaemon(True)
        t.start()
        # 启动通知接受线程
        notify_thread = Thread(target=self.recv_notify)
        notify_thread.setDaemon(True)
        notify_thread.start()
        sleep(0.1)
        # 讲本地的节点服务器进行保存
        self.local_server = ServerProxy(url)
        self.local_server.ping()
        print("本地节点:"+self.url+"已启动")

    def recv_notify(self):
        """接受本地节点服务器通知的方法
        """
        # 一直循环
        while True:
            # 当管道为空的时候，线程会阻塞在这里，当有通知到来再往下执行
            q.get(block=True)
            # 写入服务器日志
            self.server_log.insert(END, "文件发生变动")
            # 刷新文件列表
            self.display_dir()

    def status_check(func):
        """装饰器，检查当前节点有无加入P2P网络，未加入网络将禁止一些操作

        Args:
            func (function): 传入的函数
        """

        def ware(self, *args, **kwargs):    # self,接收body里的self,也就是类实例
            # 当有中心服务器时
            if self.server:
                return func(self, *args, **kwargs)
            else:
                # 没有连接到中心服务器，禁止操作
                self.server_log.insert(END, "未连接到服务器，无效操作")
                return
        return ware

    def init_gui(self):
        """初始化Gui页面
        """
        self.window.title("文件共享")  # 窗口标题
        self.window.geometry("900x600")  # 窗口大小

        lbl_ip = tkinter.Label(self.window, text="中心服务器IP地址")  # 中心服务器IP地址label
        self.ent_ip = tkinter.Entry(
            self.window, textvariable=tkinter.StringVar(value=DefaultIP))  # 中心服务器IP地址输入框
        lbl_port = tkinter.Label(self.window, text="中心服务器端口号")  # 中心服务器端口号label
        self.ent_port = tkinter.Entry(
            self.window, textvariable=tkinter.StringVar(value=DefaultPort))  # 中心服务器端口号输入框
        lbl_server = tkinter.Label(self.window, text="服务器状态")  # 服务器状态的label

        self.server_status = tkinter.StringVar()
        self.server_status.set("已断开服务器连接")
        lbl_server_status = tkinter.Label(
            self.window, textvariable=self.server_status)  # 具体的服务器状态

        btn_chdir = tkinter.Button(
            self.window, text="改变目录", width=15, command=self.change_directory)  # 改变目录按钮
        btn_crdir = tkinter.Button(
            self.window, text="创建目录", width=15, command=self.create_directory)  # 创建目录按钮
        btn_deldir = tkinter.Button(
            self.window, text="删除目录", width=15, command=self.delete_directory)  # 删除目录按钮
        btn_delfile = tkinter.Button(
            self.window, text="删除文件", width=15, command=self.delete_file)  # 删除文件按钮
        btn_downfile = tkinter.Button(
            self.window, text="下载文件", width=15, command=self.download_file)  # 下载文件按钮
        btn_upfile = tkinter.Button(
            self.window, text="上传文件", width=15, command=self.upload_file)  # 上传文件按钮
        btn_connect = tkinter.Button(
            self.window, text="连接服务器", width=15, command=self.connect_server)  # 连接服务器按钮
        btn_disconnect = tkinter.Button(
            self.window, text="断开连接", width=15, command=self.close_connection)  # 断开连接按钮

        self.server_log = tkinter.Listbox(
            self.window, width=38, height=23)  # 服务器日志
        self.file_list = tkinter.Listbox(
            self.window, width=54, height=30)  # 文件列表

        lbl_select = tkinter.Label(self.window, text="当前选择的文件或文件夹:")
        lbl_file_list = tkinter.Label(self.window, text="服务器文件列表如下")
        btn_select_file = tkinter.Button(
            self.window, text="选择该文件（文件夹）", width=15, command=self.select_file)  # 选择文件按钮

        self.selected_name = tkinter.StringVar()
        self.selected_name.set(DefaultName)
        self.lbl_select_file = tkinter.Label(
            self.window, textvariable=self.selected_name)  # 已经选中的文件label

        # 将上面的组件摆放到合适的位置
        lbl_ip.grid(row=1, column=1)
        self.ent_ip.grid(row=1, column=2)
        lbl_port.grid(row=2, column=1)
        self.ent_port.grid(row=2, column=2)
        lbl_server.grid(row=3, column=1)
        lbl_server_status.grid(row=3, column=2)

        btn_chdir.grid(row=4, column=1)
        btn_crdir.grid(row=4, column=2)
        btn_deldir.grid(row=5, column=1)
        btn_delfile.grid(row=5, column=2)
        btn_downfile.grid(row=6, column=1)
        btn_upfile.grid(row=6, column=2)
        btn_connect.grid(row=7, column=1)
        btn_disconnect.grid(row=7, column=2)

        self.server_log.grid(row=8, column=1, columnspan=2)
        lbl_select.grid(row=1, column=3)
        self.lbl_select_file.grid(row=1, column=4)
        lbl_file_list.grid(row=2, column=3)
        btn_select_file.grid(row=2, column=4)
        self.file_list.grid(row=3, column=3, columnspan=2, rowspan=6)

    def _start(self):
        """启动服务器
        """
        self.init_gui()
        self.window.mainloop()

    def display_dir(self) -> int:
        """显示文件列表

        Returns:
            int: 0:成功 -1:失败
        """
        try:
            dirlist = self.local_server.get_list(self.current_path)
            # dirlist = []
        except:
            return FAIL
        self.file_list.insert(END, "当前文件列表如下:")
        # 当不是根目录时可以回到上一级目录
        if self.current_path != self.root_path:
            self.file_list.insert(END, "(回到上一级目录)")
        if not dirlist:
            self.file_list.insert(END, EMPTY_LIST)
        for item in dirlist:
            self.file_list.insert(END, item)
        return OK

    def select_file(self):
        """选择当前问价 
        """
        # 检查是否选择了非法文件
        if self.file_list.get(self.file_list.curselection()):
            if self.file_list.get(self.file_list.curselection()) == DefaultName or self.file_list.get(self.file_list.curselection()) == EMPTY_LIST:
                return
            self.selected_name.set(
                self.file_list.get(self.file_list.curselection()))

    def connect_server(self):
        """连接中心服务器
        """
        # 获取ip和port
        ip = self.ent_ip.get()
        port = self.ent_port.get()
        # 检查ip和port是否为空
        if not ip:
            self.server_log.insert(END, "服务器地址不能为空\n")
            return
        elif not port:
            self.server_log.insert(END, "服务器端口不能为空\n")
            return
        url = "http://"+ip+":"+port
        try:
            # 尝试连接中心服务器
            self.server = ServerProxy(url)
            self.node = self.server.node_get_msg(self.url)
            print(self.node)
            # 同步节点列表
            ret = self.local_server.hello(self.node.copy())
            # 打印提示信息
            self.server_log.insert(END, "连接成功!\n")
            self.server_status.set("已连接到"+url)
            # 刷新文件列表
            ret = self.display_dir()
            if ret == OK:
                self.server_log.insert(END, "文件列表拉取成功!\n")
            else:
                self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
                self.close_connection()
        except:
            self.server_log.insert(END, "连接失败")

    @status_check
    def change_directory(self):
        """改变当前目录
        """
        # 检查参数
        if self.selected_name.get() == DefaultName or not self.selected_name.get():
            self.server_log.insert(END, "未选择文件（文件夹)")
            return
        elif self.selected_name.get() == "(回到上一级目录)":
            if self.current_path == self.root_path:
                self.server_log.insert(END, "已经是根目录了!")
            else:
                self.current_path = os.path.dirname(self.current_path)
                self.server_log.insert(END, "改变目录成功，当前目录是"+self.current_path)
                self.display_dir()
                return
        try:
            # 向本地节点服务器请求
            ret = self.local_server.change_dir(
                self.current_path, self.selected_name.get())
            # print(ret)
            if ret == OK:
                self.current_path = os.path.join(
                    self.current_path, self.selected_name.get()[5:])
                self.server_log.insert(
                    END, "改变目录成功，当前目录是"+self.current_path+"\n")
            else:
                self.server_log.insert(END, "未选择文件夹\n")
            # 更新文件列表
            self.display_dir()

        except:
            self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
            self.close_connection()

    @status_check
    def create_directory(self):
        """创建文件夹
        """
        input_name = askstring(
            "创建文件夹", "请输入要创建的文件夹名称")
        # 检查参数
        if not input_name:
            self.server_log.insert(END, "文件名不能为空")
            return
        try:
            # 向本地节点服务器请求
            ret = self.local_server.create_dir(
                self.current_path, input_name)
            if ret == OK:
                self.server_log.insert(
                    END, "创建目录成功\n")
                self.display_dir()
            else:
                self.server_log.insert(END, "创建失败\n")
        except:
            self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
            self.close_connection()

    @status_check
    def delete_directory(self):
        """删除文件夹
        """
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件夹")
            return
        try:
            # 向本地节点请求
            ret = self.local_server.delete_dir(
                self.current_path, self.selected_name.get())
            # print(ret)
            if ret == OK:
                self.server_log.insert(
                    END, "删除目录成功")
                self.display_dir()
            else:
                self.server_log.insert(END, "应该选择文件夹\n")
        except:
            self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
            self.close_connection()

    @status_check
    def delete_file(self):
        """删除文件
        """
        # 检查参数
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件")
            return
        try:
            # 向本地节点服务器请求
            ret = self.local_server.delete_file(
                self.current_path, self.selected_name.get())
            # print(ret)
            if ret == OK:
                self.server_log.insert(
                    END, "删除文件成功")
                self.display_dir()
            else:
                self.server_log.insert(END, "应该选择文件\n")
        except:
            self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
            self.close_connection()

    @status_check
    def download_file(self):
        """下载文件
        """
        # 检查参数
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件")
            return
        try:
            # 尝试拉取文件数据
            ret, data = self.local_server.fetch(
                self.current_path, self.selected_name.get())
            # 对文件进行处理
            filename = self.selected_name.get()
            # 去掉远程文件名的前缀
            if filename[:len(RemoteFileBefore)] == RemoteFileBefore:
                filename = filename[len(RemoteFileBefore):]
            # 防止重名
            if os.path.isfile(os.path.join(self.current_path, filename)):
                filename = filename+str(int(time.time()))
            print(filename)
            if ret == OK:
                # 将数据写入文件
                with open(os.path.join(self.current_path, filename), encoding="utf-8", mode="w") as f:
                    f.write(data)
                self.server_log.insert(END, "下载文件成功")
                self.display_dir()
            else:
                self.server_log.insert(END, data)
        except:
            self.server_log.insert(END, "服务器错误，断开连接\n")
            self.close_connection()

    @status_check
    def upload_file(self):
        """上传文件
        """
        # 打开上传文件选择弹窗
        filename = askopenfilename()
        try:
            # 读取文件数据
            data = open(file=filename, encoding="utf-8").read()
        except:
            self.server_log.insert(END, "读取文件失败")
            return
        try:
            # 上传
            ret, msg = self.local_server.upload(
                self.current_path, os.path.basename(filename), data)
            # print(ret)
            if ret == OK:
                self.server_log.insert(END, "上传成功!")
                sleep(0.1)
            else:
                self.server_log.insert(END, msg)
            self.display_dir()
        except:
            self.server_log.insert(END, "服务器错误，断开连接")
            self.close_connection()

    def close_connection(self):
        """关闭与中心服务器连接
        """
        if self.server != None:
            try:
                # 让本地节点离开P2P网络
                self.server.node_leave(self.url)
            except:
                pass
            self.server = None
        self.server_log.insert(END, "已断开连接\n")
        self.server_status.set("已断开服务器连接")


def main():
    """main方法
    """
    if not sys.argv[1:]:
        print("请使用python center_server.py [url] [dir]启动")
        return
    # 拿取命令行传入的参数
    url, dir = sys.argv[1:]
    client = GuiClient(url, dir)
    client._start()


if __name__ == "__main__":
    main()
