#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import urllib2
import time
import random
import send
from Model import *
from bs4 import BeautifulSoup
import sys
from selenium import webdriver


sys.setrecursionlimit(1000000)

JINFU_URL = "https://www.ysfas.com/finance.do"

BASE_SECOND = 1 #间隔时间
RANDOM_SECOND = 5 #间隔时间加的随机数的最大值

TIMEOUT = 60 #请求超时时长

count = 1


def check_youxuanbiao(soup):
    print "出借专区的数据:"

    for item in soup.find_all('div',class_='fml_inve_main fml_hide'):
        print item
    pass

    return


    youxuanbiao_list = [MoneyModel(), MoneyModel(), MoneyModel(),MoneyModel()]

    youxuanbiao_lilv_list = [] #利率
    youxuanbiao_date_length_list =[] #投资期限
    youxuanbiao_process_list = [] #投资的进度
    youxuanbiao_shouyi_value_list = [] #每万元收益金额
    youxuanbiao_shouyi_type_list = [] #收益的类型

    for k in soup.find_all('div', class_='area_li_divcen h90'):
        # print k.text
        klist = k.find_all('p',class_='textc fonts20 co_595959')
        for j in klist:
            date_length = j.text.encode("utf-8")
            if "%" in date_length:
                youxuanbiao_lilv_list.append(j.text.encode("utf-8"))
            else:
                youxuanbiao_date_length_list.append(date_length+"个月")
        pass

    for k in soup.find_all('div', class_='fonts14 co_595959 mb20'):
        print k.text
        youxuanbiao_process_list.append(k.text.encode("utf-8"))

    for k in soup.find_all('div', class_='area_li_divdown'):
        # print k.text
        klist = k.find_all('p',class_='shouyi')
        for j in klist:
            shouyi_list = j.text.strip().split('\n')
            for k in range(len(shouyi_list)):
                type = shouyi_list[k].encode("utf-8")
                if "收益" in type:
                    youxuanbiao_shouyi_type_list.append(type)
                else:
                    value = shouyi_list[k-1].encode("utf-8")
                    youxuanbiao_shouyi_value_list.append(value)
        pass

    #赋值优选标利率
    for index,lilv in enumerate(youxuanbiao_lilv_list):
        model = youxuanbiao_list[index]
        model.lilv=lilv
        model.type = Type.Type_youxuanbiao

    #赋值优选标投资时长
    for index,date_length in enumerate(youxuanbiao_date_length_list):
        model = youxuanbiao_list[index]
        model.date_length=date_length

    #赋值优选标的进度
    for index,process in enumerate(youxuanbiao_process_list):
        model = youxuanbiao_list[index]
        model.process=process

    #赋值优选标的收益类型
    for index,value in enumerate(youxuanbiao_shouyi_type_list):
        model = youxuanbiao_list[index]
        model.youxuan_type=value

    #赋值优选标的收益值
    for index,value in enumerate(youxuanbiao_shouyi_value_list):
        model = youxuanbiao_list[index]
        model.youxuan_shouyi=value

    #检验结果
    result = False
    for model in youxuanbiao_list:
        print model
        if model.data_ok:
            result = True

    return result,youxuanbiao_list
    pass


def deal_respose(html=""):
    if not len(html):
        print "响应无内容"
        exit
        return
    pass

    soup = BeautifulSoup(html, "html5lib")
    print soup
    return
    youxuanbiao_l = check_youxuanbiao(soup)

    jinfujihua_l = None
    zhuanrangzhuanqu_l = None

    result1 = jinfujihua_l[0]
    result2 = youxuanbiao_l[0]
    result3 = zhuanrangzhuanqu_l[0]

    jinfujihua_list = jinfujihua_l[1]
    youxuanbiao_list = youxuanbiao_l[1]
    zhuanrangzhuanqu_list = zhuanrangzhuanqu_l[1]

    jinfujihua = "\n"
    for model in jinfujihua_list:
        jinfujihua = jinfujihua + str(model)+"\n"

    youxuanbiao = "\n"
    for model in youxuanbiao_list:
        youxuanbiao = youxuanbiao + str(model)+"\n"

    zhuanrangzhuanqu = "\n"
    for model in zhuanrangzhuanqu_list:
        zhuanrangzhuanqu = zhuanrangzhuanqu + str(model)+"\n"

    if result1:
        title = "成功监控到金服计划标"
        countstr="监控次数:"+str(count)
        content = title+jinfujihua+countstr
        print title,content
        send.send_jinfu_mail(mail_title=title,mail_content=content)

    if result2:
        title = "成功监控到优选标"
        countstr = "监控次数:" + str(count)
        content = title + jinfujihua + countstr
        print title,content
        send.send_jinfu_mail(mail_title=title,mail_content=content)

    if result3:
        title = "成功监控到转让专区"
        countstr = "监控次数:" + str(count)
        content = title + jinfujihua + countstr
        print title,content
        send.send_jinfu_mail(mail_title=title,mail_content=content)
        print
    if result1 or result2 or result3:
        print "监控次数:"+str(count)
        exit(1)
        pass
    pass


def query_html():
    socket.setdefaulttimeout(TIMEOUT)
    send_headers = {
        'Host': 'www.ysfas.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    try:
        req = urllib2.Request(JINFU_URL, headers=send_headers)
        response = urllib2.urlopen(req)
        html_div = response.read()
        deal_respose(html_div)
    except Exception, e:
        # send.send_jinfu_mail(mail_title="接口请求失败",content="接口请求失败")
        raise e

def launch(base_second=BASE_SECOND,random_second=RANDOM_SECOND):
    sleep_legth = base_second+random.randint(0,random_second)
    print "间隔时长:",sleep_legth
    query_html()
    time.sleep(sleep_legth)
    global count
    count=count+1
    print "执行次数:",count
#    launch()

def main():
    print "拉取数据中"
    launch()
    print random.randint(0,4)


if __name__ == '__main__':
    main()
    print "正常结束"
    pass