#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


me_sender_mail="wsp810@163.com"
me_to_list=["wsp810@163.com"]
me_mail_host="smtp.163.com"
me_sender_username="wsp810@163.com"
me_sender_pwd="abc666888"

def send_jinfu_mail(mail_title="",mail_content=""):

    print "邮件内容:\n"+mail_content
    print "正在发送通知邮件\n"

    send_mail(mail_host=me_mail_host,
              sender_username=me_sender_username,
              sender_pwd=me_sender_pwd,
              mail_to_list=me_to_list,
              mail_title=mail_title,
              mail_content=mail_content)

#默认为mail服务
def send_mail(mail_host=me_mail_host,
              sender_username=me_sender_username,
              sender_pwd=me_sender_pwd,
              mail_to_list=me_to_list,
              mail_title="",
              mail_content=""):


    msg = MIMEText(mail_content,'plain', 'utf-8')

    msg['Subject'] = Header(mail_title,'utf-8')

    msg['From'] = "yin_sheng_jin_fu"+"<"+sender_username+">"

    msg['To'] = ";".join(mail_to_list)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(sender_username,sender_pwd)
        server.sendmail(sender_username, mail_to_list, msg.as_string())
        server.close()
        print "通知邮件已经发送成功。"
        return True
    except Exception, e:
        print "通知邮件发送失败。"
        print e.decode('unicode-escape').encode('utf-8')
        exit(-1)
        return False
    pass

def main():
    send_jinfu_mail(mail_title="DDD",mail_content="ddd")
    pass


if __name__ == '__main__':
    main()
    pass