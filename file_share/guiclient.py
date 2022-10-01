import tkinter


class GuiClient:
    """"
    文件共享的gui版本
    """

    def __init__(self, window):
        self.window = tkinter.Tk()

    def init_gui(self):
        "初始化Gui页面"
        self.window.title("文件共享")
        self.window.geometry("900x600")

        lbl_ip = tkinter.Label(self.window, text="服务器IP地址")
        ent_ip = tkinter.Entry(self.window)
        lbl_port = tkinter.Label(self.window, text="服务器端口号")
        ent_port = tkinter.Entry(self.window)
        lbl_server = tkinter.Label(self.window, text="服务器状态")
        status_server = tkinter.Label(self.window, text="未连接到服务器")

        btn_chdir = tkinter.Button(self.window, text="改变目录", width=15)
        btn_crdir = tkinter.Button(self.window, text="创建目录", width=15)
        btn_deldir = tkinter.Button(self.window, text="删除目录", width=15)
        btn_delfile = tkinter.Button(self.window, text="删除文件", width=15)
        btn_downfile = tkinter.Button(self.window, text="下载文件", width=15)
        btn_upfile = tkinter.Button(self.window, text="上传文件", width=15)
        btn_connect = tkinter.Button(self.window, text="连接服务器", width=15)
        btn_disconnect = tkinter.Button(self.window, text="断开连接", width=15)

        server_log = tkinter.Listbox(self.window, width=38, height=23)
        lbl_file_list = tkinter.Label(self.window, text="服务器文件列表如下")
        file_list = tkinter.Listbox(self.window, width=54, height=30)

        # 将上面的组件摆放到合适的位置
        lbl_ip.grid(row=1, column=1)
        ent_ip.grid(row=1, column=2)
        lbl_port.grid(row=2, column=1)
        ent_port.grid(row=2, column=2)
        lbl_server.grid(row=3, column=1)
        status_server.grid(row=3, column=2)

        btn_chdir.grid(row=4, column=1)
        btn_crdir.grid(row=4, column=2)
        btn_deldir.grid(row=5, column=1)
        btn_delfile.grid(row=5, column=2)
        btn_downfile.grid(row=6, column=1)
        btn_upfile.grid(row=6, column=2)
        btn_connect.grid(row=7, column=1)
        btn_disconnect.grid(row=7, column=2)

        server_log.grid(row=8, column=1, columnspan=2)
        lbl_file_list.grid(row=1, column=3)
        file_list.grid(row=2, column=3, columnspan=2, rowspan=7)

    def _start(self):
        self.init_gui()
        self.window.mainloop()


def main():
    client = GuiClient()
    client._start()


if __name__ == "__main__":
    main()
