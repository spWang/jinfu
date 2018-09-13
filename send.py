#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import smtplib
import socket
import getpass
from email.mime.text import MIMEText
import subprocess

xxx_sender_mail="shuaipeng.wang@xxx.com"
xxx_to_list=['shuaipeng.wang@xxx.com']
xxx_mail_host="mail.xxx.com"
xxx_sender_username="githooks.ios@xxx.com"
xxx_sender_pwd="chuth-7?7vephaJere"

me_sender_mail="wsp810@163.com"
me_to_list=["wsp810@163.com"]
me_mail_host="smtp.163.com"
me_sender_username="wsp810@163.com"
me_sender_pwd="abc666888"

def send_jinfu_mail(mail_title="",mail_content=""):
    send_mail(mail_title=mail_title,mail_content=mail_content)

    send_mail(mail_host=me_mail_host,
              sender_username=me_sender_username,
              sender_pwd=me_sender_pwd,
              sender_mail=me_sender_mail,
              mail_to_list=me_to_list,
              mail_title=mail_title,
              mail_content=mail_content)
    pass

#默认为mail服务
def send_mail(mail_host=me_mail_host,
                sender_username=me_sender_username,
                sender_pwd=me_sender_pwd,
                sender_mail=me_sender_mail,
                mail_to_list=me_to_list,
                mail_title="",
                mail_content=""):

    print "正在发送通知邮件"
    me = "监控服务"+"<"+sender_username+">"
    msg = MIMEText(mail_content,'plain', 'utf-8')
    msg['Subject'] = mail_title
    msg['From'] = me
    msg['To'] = ";".join(mail_to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(sender_username,sender_pwd)
        server.sendmail(me, mail_to_list, msg.as_string())
        server.close()
        print "通知邮件已经发送成功。"
        return True
    except Exception, e:
        print "通知邮件发送失败。"
        print e
        return False
    pass

def main():
    # send_mail_for_fail()
    pass


if __name__ == '__main__':
    main()
    pass