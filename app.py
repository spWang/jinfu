#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk  # 使用Tkinter前需要先导入
import re
from setup import Monitoring
from tkinter.messagebox import *


class App(tk.Tk):
    def __init__(self):
        self.window = tk.Tk.__init__(self)

        #利率提示文本
        self.lilvLabel = tk.Label(self,text="最低利率（%）")
        self.lilvLabel.pack()

        # 利率输入框
        self.lilvEntry = tk.Entry(self)
        self.lilvEntry.bind('<Key>', printkey)
        self.lilvEntry.pack()

        self.lilvConfirmBtn = tk.Button(self,text="确定",command=self.lilvConfirmBtnClick)
        self.lilvConfirmBtn.pack()


        self.startbtn = tk.Button(self,text="启动",command=self.startbtnClick)
        self.startbtn.pack()

        self.stopbtn = tk.Button(self,text="停止监控",command=self.stopbtnClick)
        self.stopbtn.pack()

    def stopbtnClick(self):
        Monitoring.stop()

    def startbtnClick(self):
        Monitoring.start()

    def lilvConfirmBtnClick(self):
        value = self.lilvEntry.get()

        # try:
        #     lilv = float(value)
        #     MonitoringConfig().lilv = value
        #
        # except Exception, e:
        #     showerror("必须输入0-100的数字")

        return

        ok = True
        if not isinstance(value, float) or not isinstance(value, int):
            ok = False
            print "必须是数字"

        if value < 0 or value > 100:
            print "利率范围是0到100"
            ok = False
        if not ok:
            showerror(title="错误", message="必须输入0-100的数字")
            return

        MonitoringConfig().lilv = value

    def printkey(self, event):
        print('你按下了: ' + event.char)

        if not re.findall('[0-9]+', str(event.char)):
            print "请输入数字，不包含百分号"

pass

def printkey(event):

    if not re.findall('[0-9]+', str(event.char)):
        print "必须输入数字"


def main():

    app = App()
    app.title('My Window')
    app.geometry('500x300')
    app.mainloop()

    return

    window = tk.Tk()
    window.title('My Window')
    window.geometry('500x300')
    l = tk.Label(window, text='你好！this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)
    l.pack()

    en = tk.Entry(window)
    en.pack()
    en.bind('<Key>', printkey)

    window.mainloop()


if __name__ == '__main__':
    main()
