#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tkinter as tk  # 使用Tkinter前需要先导入
import re

from config import MonitoringConfig
from setup import Monitoring
from tkinter.messagebox import *


class App(tk.Tk):
    def __init__(self):
        self.window = tk.Tk.__init__(self)

        #利率提示文本
        self.lilvLabel = tk.Label(self,text="最低利率（%）")
        self.lilvLabel.pack()

        # 利率输入框
        defalutLilv = tk.StringVar()
        self.lilvEntry = tk.Entry(self,textvariable=defalutLilv)
        defalutLilv.set(MonitoringConfig().lilv)
        self.lilvEntry.bind('<Key>', printkey)
        self.lilvEntry.pack()

        #利率确定
        # self.lilvConfirmBtn = tk.Button(self,text="确定",command=self.lilvConfirmBtnClick)
        # self.lilvConfirmBtn.pack()

        # 剩余金额提示文本
        self.shengyuLabel = tk.Label(self, text="最低剩余金额（元）")
        self.shengyuLabel.pack()

        # 剩余金额输入框
        defalutShengyu = tk.StringVar()
        self.shengyuEntry = tk.Entry(self,textvariable=defalutShengyu)
        defalutShengyu.set(MonitoringConfig().shengyu)
        self.shengyuEntry.bind('<Key>', printkey)
        self.shengyuEntry.pack()

        # 剩余金额确定
        self.shengyuConfirmBtn = tk.Button(self, text="确定", command=self.shengyuConfirmBtnClick)
        self.shengyuConfirmBtn.pack()


        self.startbtn = tk.Button(self,text="启动",command=self.startbtnClick)
        self.startbtn.pack()

        self.stopbtn = tk.Button(self,text="停止监控",command=self.stopbtnClick)
        self.stopbtn.pack()

    def stopbtnClick(self):
        Monitoring.stop()

    def startbtnClick(self):
        Monitoring.start()

    # def lilvConfirmBtnClick(self):
    #     value = self.lilvEntry.get()
    #
    #     try:
    #         lilv = float(value)
    #         if lilv <0 or lilv > 100:
    #             showinfo("错误", "必须输入0-100的数字")
    #             return
    #         MonitoringConfig().lilv = lilv
    #         showinfo("成功","设置成功");
    #     except Exception, e:
    #         showinfo("错误",e)


    def shengyuConfirmBtnClick(self):

        #利率
        lilvStr = self.lilvEntry.get()
        try:
            lilv = float(lilvStr)
            if lilv < 0 or lilv > 100:
                showinfo("错误", "必须输入0-100的数字")
                return
        except Exception, e:
            showinfo("错误", e)
            return

        #剩余金额
        shengyuStr = self.shengyuEntry.get()
        try:
            shengyu = float(shengyuStr)
            if shengyu <0:
                showinfo("错误", "必须输入大于0的数字")
                return
        except Exception, e:
            showinfo("错误",e)
            return

        MonitoringConfig().lilv = lilv
        MonitoringConfig().shengyu = shengyu
        showinfo("成功", "设置成功");

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
