'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-01 16:55:26
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-03 01:32:01
FilePath: /Python-Learn/file_share_copy/guiclient.py
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

FAIL = -1
OK = 0

EMPTY_LIST = "空空如也"
DefaultName = "当前未选中文件"
DefaultIP = "localhost"
DefaultPort = "11000"
RemoteFileBefore = "[remote]"

q = queue.Queue(1)


class GuiClient:
    """"
    文件共享的gui版本
    """

    def __init__(self, url, dir):
        self.window = tkinter.Tk()
        self.server = None
        self.root_path = dir
        self.current_path = dir
        self.url = url

        n = NodeServer(url, dir)
        t = Thread(target=n._start, args=(q,))
        notify_thread = Thread(target=self.recv_notify)
        notify_thread.setDaemon(True)
        notify_thread.start()
        t.setDaemon(True)
        t.start()
        sleep(0.1)
        self.server = ServerProxy(url)
        self.server.ping()
        print("本地节点:"+self.url+"已启动")

    def recv_notify(self):
        while True:
            mode = q.get(block=True)
            if mode == -1:
                self.server_log.insert(END, "文件发生变动")
                self.display_dir()
            else:
                self.server_status.set("主服务器@"+str(mode)+"从机")

    def statuc_check(func):    # func接收body
        def ware(self, *args, **kwargs):    # self,接收body里的self,也就是类实例
            # print('This is a decrator!')
            if self.server:        # 判断类属性
                return func(self, *args, **kwargs)
                self.server_log.insert(END, "未连接到服务器，无效操作")
                return
        return ware

    def init_gui(self):
        "初始化Gui页面"
        self.window.title("文件共享")
        self.window.geometry("900x600")

        lbl_ip = tkinter.Label(self.window, text="主服务器IP地址")
        self.ent_ip = tkinter.Entry(
            self.window, textvariable=tkinter.StringVar(value=DefaultIP))
        lbl_port = tkinter.Label(self.window, text="主服务器端口号")
        self.ent_port = tkinter.Entry(
            self.window, textvariable=tkinter.StringVar(value=DefaultPort))
        lbl_server = tkinter.Label(self.window, text="服务器状态")

        self.server_status = tkinter.StringVar()
        self.server_status.set("主服务器@0从机")
        lbl_server_status = tkinter.Label(
            self.window, textvariable=self.server_status)

        btn_chdir = tkinter.Button(
            self.window, text="改变目录", width=15, command=self.change_directory)
        btn_crdir = tkinter.Button(
            self.window, text="创建目录", width=15, command=self.create_directory)
        btn_deldir = tkinter.Button(
            self.window, text="删除目录", width=15, command=self.delete_directory)
        btn_delfile = tkinter.Button(
            self.window, text="删除文件", width=15, command=self.delete_file)
        btn_downfile = tkinter.Button(
            self.window, text="下载文件", width=15, command=self.download_file)
        btn_upfile = tkinter.Button(
            self.window, text="上传文件", width=15, command=self.upload_file)
        btn_connect = tkinter.Button(
            self.window, text="加入集群", width=15, command=self.connect_server)
        btn_disconnect = tkinter.Button(
            self.window, text="离开集群", width=15, command=self.close_connection)

        self.server_log = tkinter.Listbox(self.window, width=38, height=23)
        self.file_list = tkinter.Listbox(
            self.window, width=54, height=30)

        lbl_select = tkinter.Label(self.window, text="当前选择的文件或文件夹:")
        lbl_file_list = tkinter.Label(self.window, text="服务器文件列表如下")
        btn_select_file = tkinter.Button(
            self.window, text="选择该文件（文件夹）", width=15, command=self.select_file)

        self.selected_name = tkinter.StringVar()
        self.selected_name.set(DefaultName)
        self.lbl_select_file = tkinter.Label(
            self.window, textvariable=self.selected_name)

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
        self.init_gui()
        self.display_dir()
        self.window.mainloop()

    def display_dir(self):
        try:
            dirlist = self.server.get_list(self.current_path)
            # dirlist = []
        except:
            return FAIL
        self.file_list.insert(END, "当前文件列表如下:")
        if self.current_path != self.root_path:
            self.file_list.insert(END, "(回到上一级目录)")
        if not dirlist:
            self.file_list.insert(END, EMPTY_LIST)
        for item in dirlist:
            self.file_list.insert(END, item)
        return OK

    def select_file(self):
        if self.file_list.get(self.file_list.curselection()):
            if self.file_list.get(self.file_list.curselection()) == DefaultName or self.file_list.get(self.file_list.curselection()) == EMPTY_LIST:
                return
            self.selected_name.set(
                self.file_list.get(self.file_list.curselection()))

    def connect_server(self):
        ip = self.ent_ip.get()
        port = self.ent_port.get()
        if not ip:
            self.server_log.insert(END, "服务器地址不能为空\n")
            return
        elif not port:
            self.server_log.insert(END, "服务器端口不能为空\n")
            return
        url = "http://"+ip+":"+port
        try:
            ret = self.server.add_cluster(url)
            # print(ret)
            self.server_log.insert(END, "连接成功!\n")
            self.server_status.set("从节点@"+url)
            ret = self.display_dir()
            if ret == OK:
                self.server_log.insert(END, "文件列表拉取成功!\n")
            else:
                self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
                self.close_connection()
        except:
            self.server_log.insert(END, "连接失败")

    def change_directory(self):
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
            # print(self.selected_name.get())
            ret = self.server.change_dir(
                self.current_path, self.selected_name.get())
            # print(ret)
            if ret == OK:
                self.current_path = os.path.join(
                    self.current_path, self.selected_name.get()[5:])
                self.server_log.insert(
                    END, "改变目录成功，当前目录是"+self.current_path+"\n")
            else:
                self.server_log.insert(END, "未选择文件夹\n")
            self.display_dir()

        except:
            self.server_log.insert(END, "服务器错误，无法拉取文件列表，断开连接\n")
            self.close_connection()

    def create_directory(self):
        input_name = askstring(
            "创建文件夹", "请输入要创建的文件夹名称")
        # print(input_name)
        if not input_name:
            self.server_log.insert(END, "文件名不能为空")
            return

        try:
            ret = self.server.create_dir(
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

    def delete_directory(self):
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件夹")
            return
        try:
            # print(self.selected_name.get())
            ret = self.server.delete_dir(
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

    def delete_file(self):
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件")
            return
        try:
            # print(self.selected_name.get())
            ret = self.server.delete_file(
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

    def download_file(self):
        if self.selected_name.get() == DefaultName or not self.selected_name.get() or self.selected_name.get() == "(回到上一级目录)":
            self.server_log.insert(END, "未选择文件")
            return
        try:
            ret, data = self.server.fetch(
                self.current_path, self.selected_name.get())
            filename = self.selected_name.get()
            if filename[:len(RemoteFileBefore)] == RemoteFileBefore:
                filename = filename[len(RemoteFileBefore):]
            if os.path.isfile(os.path.join(self.current_path, filename)):
                filename = filename+str(int(time.time()))
            print(filename)
            if ret == OK:
                with open(os.path.join(self.current_path, filename), encoding="utf-8", mode="w") as f:
                    f.write(data)
                self.server_log.insert(END, "下载文件成功")
                self.display_dir()
            else:
                self.server_log.insert(END, data)
        except:
            self.server_log.insert(END, "服务器错误，断开连接\n")
            self.close_connection()

    def upload_file(self):
        filename = askopenfilename()
        try:
            data = open(file=filename, encoding="utf-8").read()
        except:
            self.server_log.insert(END, "读取文件失败")
            return
        try:
            ret, msg = self.server.upload(
                self.current_path, os.path.basename(filename), data)
            # print(ret)
            if ret == OK:
                self.server_log.insert(END, "上传成功!")
                self.display_dir()
            else:
                self.server_log.insert(END, msg)
        except:
            self.server_log.insert(END, "服务器错误，断开连接")
            self.close_connection()

    def close_connection(self):
        if self.server != None:
            try:
                self.server.node_leave(self.url)
            except:
                pass
        self.server_log.insert(END, "已离开集群\n")
        self.server_status.set("主服务器@0从机")


def main():
    if not sys.argv[1:]:
        print("请使用python center_server.py [url] [dir]启动")
        return
    url, dir = sys.argv[1:]
    client = GuiClient(url, dir)
    client._start()


if __name__ == "__main__":
    main()
