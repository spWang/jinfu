#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import random

import requests

from plan_model import *

import send

from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

sys.setrecursionlimit(1000000)

QUERY_INTERVAL = [5,10] #监控每两次请求的间隔时间，在这个范围内取值

LONG_SLEEP = 60*30 #监控到了后，过多长时间再次开始监控

count = 1 #监控计数

def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def plan_model_with_li(li):
    liText = li.text.replace('\t', '');

    planModel = PlanModel();

    # 去除空行元素
    itemArr = []
    for item in liText.split('\n'):
        if item == "":
            continue
        itemArr.append(item)

    #是否是 每万元复利收益
    fuli = False
    if "每万元复利收益" in liText:
        fuli = True
    planModel.fuli = fuli

    # 进度
    progress = itemArr[2]
    progress = progress.replace('%', '')
    planModel.progress = float(progress)

    # 年化利率
    lilv = itemArr[5]
    lilv = lilv.replace('%', '')
    planModel.lilv = float(lilv)

    # 借款期限
    jiekuanqixian = itemArr[7]
    planModel.jiekuanqixian = jiekuanqixian

    # 万元收益
    shouyi = itemArr[9]
    shouyi = shouyi.replace('元', '')
    planModel.shouyi = shouyi

    # 剩余金额
    shengyu = itemArr[11]
    shengyu = shengyu.replace('剩余金额：', '')
    wan = True if ("万" in shengyu) else False
    shengyu = shengyu.replace('万', '').replace('元', '').replace(',', '')
    shengyuMoney = float(shengyu)  # 转成数字

    # 处理剩余金额的万元的情况
    if wan:
        shengyuMoney *= 10000
    planModel.shengyu = shengyuMoney

    return planModel

def deal_respose(html=""):
    if not len(html):
        print "响应无内容"
        send.send_jinfu_mail(mail_title="监控失败：网页无内容",mail_content="银盛金服接口请求失败")
        exit(0)
        return
    pass

    soup = BeautifulSoup(html, "html5lib")

    liArr = soup.find_all('li',class_='pt30 pb30')

    planModelOKArr = []

    for li in liArr:
        planModel = plan_model_with_li(li)
        if planModel.ok:

            planModelOKArr.append(planModel)

    if len(planModelOKArr)>0:
        print "恭喜你有合格的标了"
        content = ""
        for model in planModelOKArr:
            content += str(model)+"\n\n"

        send.send_jinfu_mail(mail_title="恭喜你监控到合格的竞标了", mail_content=content)

        #监控到后过更长时间再次启动
        print "再次开始监控倒计时："+str(LONG_SLEEP/60)+"分"
        time.sleep(LONG_SLEEP)


def query_html():

    url = 'https://www.ysfas.com/financeLists.do'

    send_headers = {
        'Host': 'www.ysfas.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Content - Type':'application / x - www - form - urlencoded;charset = UTF - 8'
    }
    try:
        response = requests.post(url, headers=send_headers)
        deal_respose(response.text)
    except Exception, e:
        send.send_jinfu_mail(mail_title="监控服务请求接口失败",mail_content="接口请求失败")
        exit(-1)
        raise e

def launch(base_second=QUERY_INTERVAL[0],random_second=QUERY_INTERVAL[1]-QUERY_INTERVAL[0]):

    sleep_legth = base_second+random.randint(0,random_second)
    print "倒计时："+str(sleep_legth)+"\n"
    query_html()
    time.sleep(sleep_legth)
    global count
    count=count+1
    print now_time()
    print "监控次数："+str(count)
    launch()

def main():
    print now_time()
    print "开启监控中"
    launch()
    print random.randint(0,4)


if __name__ == '__main__':
    main()
    print "正常结束"
    pass