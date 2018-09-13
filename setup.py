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

sys.setrecursionlimit(1000000)

TIMEOUT = 60
YINSHENGTOUZI = "https://www.ysfas.com/index.do"

count = 1
launch_second = 10
launch_random = 5

def check_jinfujihua(soup):
    print "金服计划数据:"
    jinfujihua_list = [MoneyModel(),MoneyModel(),MoneyModel()]

    jinfujihua_lilv_list = [] #金服计划的利率
    jinfujihua_date_length_list =[] #金服计划的投资期限
    jinfujihua_state_list = [] #投资的状态

    for k in soup.find_all('div', class_='nbs3-div'):
        # print k.text
        klist = k.find_all('h3',class_='pt15')
        for j in klist:
            if "%" in j.text:
                jinfujihua_lilv_list.append(j.text.encode("utf-8"))
                pass

            date_length = j.text.encode("utf-8")
            if "个月" in date_length:
                jinfujihua_date_length_list.append(date_length)
                pass
            pass

    for k in soup.find_all("div", class_="textc mt15"):
        klist = k.find_all('a', class_='nbs2-btn')
        for j in klist:
            jinfujihua_state_list.append(j.text.encode("utf-8"))

    #赋值金服计划的利率
    for index,lilv in enumerate(jinfujihua_lilv_list):
        model = jinfujihua_list[index]
        model.lilv=lilv
        model.type = Type.Type_jinfujihua

    # 赋值金服计划的投资时长
    for index, date_length in enumerate(jinfujihua_date_length_list):
        model = jinfujihua_list[index]
        model.date_length = date_length

    #赋值金服计划的投资状态
    for index, state in enumerate(jinfujihua_state_list):
        # print index, state
        model = jinfujihua_list[index]
        model.state = state

    #检验结果
    result = False
    for model in jinfujihua_list:
        print model
        if model.data_ok:
            result = True

    return result,jinfujihua_list
    pass

def check_youxuanbiao(soup):
    print "优选标数据:"
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

def check_zhuanrangzhuanqu(soup):
    print "转让专区数据:"
    zhuanrangzhuanqu_list = [MoneyModel(), MoneyModel(), MoneyModel()]
    zhuanrangzhuanqu_lilv_list = [] #利率
    zhuanrangzhuanqu_date_length_list =[] #投资期限
    zhuanrangzhuanqu_process_list = [] #投资的进度

    for k in soup.find_all('div', class_='fl ul-lidiv w150'):
        # print k.text
        klist = k.find_all('p',class_=' fonts20 co_595959')
        for j in klist:
            textstr = j.text.encode("utf-8")
            if "%" in textstr:
                zhuanrangzhuanqu_lilv_list.append(textstr)
            if not "%" in textstr and float(textstr)<48:
                zhuanrangzhuanqu_date_length_list.append(textstr+"个月")
        pass

    for k in soup.find_all('div', class_='fl ul-lidiv w280'):
        # print k.text
        klist = k.find_all('div', class_='fonts14 co_595959')
        for j in klist:
            # print j.text
            zhuanrangzhuanqu_process_list.append(j.text.encode("utf-8"))

    #赋值转让专区利率
    for index,lilv in enumerate(zhuanrangzhuanqu_lilv_list):
        model = zhuanrangzhuanqu_list[index]
        model.lilv=lilv
        model.youxuan = True
        model.type = Type.Type_zhuanrangzhuanqu

    #赋值转让专区投资时长
    for index,date_length in enumerate(zhuanrangzhuanqu_date_length_list):
        model = zhuanrangzhuanqu_list[index]
        model.date_length=date_length

    #赋值转让专区的进度
    for index,process in enumerate(zhuanrangzhuanqu_process_list):
        model = zhuanrangzhuanqu_list[index]
        model.process=process

    #检验结果
    result = False
    for model in zhuanrangzhuanqu_list:
        print model
        if model.data_ok:
            result = True

    return result,zhuanrangzhuanqu_list
    pass

def deal_respose(html=""):
    if not len(html):
        print "响应无内容"
        return
    pass
    soup = BeautifulSoup(html)

    jinfujihua_l = check_jinfujihua(soup)
    youxuanbiao_l = check_youxuanbiao(soup)
    zhuanrangzhuanqu_l = check_zhuanrangzhuanqu(soup)

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


def fetch_data():
    socket.setdefaulttimeout(TIMEOUT)
    send_headers = {
        'Host': 'www.ysfas.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    try:
        req = urllib2.Request(YINSHENGTOUZI, headers=send_headers)
        response = urllib2.urlopen(req)
        html = response.read()
        deal_respose(html)
    except Exception, e:
        send.send_jinfu_mail(mail_title="接口请求失败",content="接口请求失败")
        # raise e

    pass

def launch(second=launch_second,random_length=launch_random):
    sleep_legth = second+random.randint(0,random_length)
    print "间隔时长:",sleep_legth
    fetch_data()
    time.sleep(sleep_legth)
    global count
    count=count+1
    print "执行次数:",count
    launch()

    pass

def main():
    print "拉取数据中"
    launch(launch_second,launch_random)
    # print random.randint(0,4)
    pass


if __name__ == '__main__':
    main()
    print "正常结束"
    pass