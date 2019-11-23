#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import random
import threading

import requests


from plan_model import *

import send

from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

sys.setrecursionlimit(1000000)

QUERY_INTERVAL = [60,120] #监控每两次请求的间隔时间，在这个范围内取值
NORMAL_SEND_INTERVAL = 3 #正常监控中每次发送邮件的时间间隔
LONG_SLEEP_SUCCESS = 60*30 #监控到了后，过多长时间再次开始监控
LONG_SLEEP_FAIL = 60*5 #监控失败，过多长时间再次开始重试


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton

@singleton
class MonitoringManager(object):

    def __init__(self):
        self.timer = None
        self.num = 0 #计次
        self.didStart = False
        self.canRequest = True
        pass


    # 开启监控
    def start(self, timeInterval = 0):

        if self.didStart:
            #print "重新开启计时"
            self.restart(timeInterval)
            return

        interval = timeInterval

        if interval == 0:
            min = QUERY_INTERVAL[0]
            max = QUERY_INTERVAL[1]
            interval = random.randint(min, max)
        # print "\n"
        print "--"*30
        print now_time()
        self.num += 1
        print "监控次数：" + str(self.num)


        self.timer = threading.Timer(interval, self._sendRequest)
        self.timer.start()
        self.didStart = True
        self.canRequest = True
        print "距离下次数据请求还需要："+format_seconds(interval)
        print  "\n"

    #重新开启
    def restart(self, timeInterval = 0):
        if not self.didStart:
            self.start()
            return
        self.stop()
        self.start(timeInterval)
        pass

    #停止监控
    def stop(self, log=False):
        if not self.didStart:
            return
        self.timer.cancel()
        self.timer = None
        self.didStart = False
        self.canRequest = False
        if log:
            print "监控服务停止"
        pass

    #暂停监控xx秒
    def suspend(self, interval):
        if not self.didStart:
            return

        self.stop();
        self.start(interval)
        pass

    def _sendRequest(self):
        if self.canRequest:
            timeOK = normal_send_mail_time()
            Monitoring.dealNormal(timeOK,"银盛监控服务持续监控中")
            Monitoring.requestHtml()
        pass
    pass


class Monitoring(object):

    @classmethod
    def requestHtml(cls):
        user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                            ]
        url = 'https://www.ysfas.com/financeLists.do'

        send_headers = {
            'Host': 'www.ysfas.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8'
        }
        send_headers['User-Agent'] = random.choice(user_agent_list)
        
        try:
            response = requests.post(url, headers=send_headers)
            Monitoring._dealResponse(response.text)
        except Exception, e:
            Monitoring._dealError(content=str(e), restartInterval=LONG_SLEEP_FAIL)
        pass

    @classmethod
    def _dealResponse(cls, html=None):
        if not html:
            Monitoring._dealError(content="html无内容", restartInterval=LONG_SLEEP_FAIL)
            return
        pass

        soup = BeautifulSoup(html, "html5lib")

        liArr = soup.find_all('li', class_='pt30 pb30')

        planModelOKArr = []

        for li in liArr:
            planModel = Monitoring._planModelWithLi(li)
            if planModel.ok:
                planModelOKArr.append(planModel)

        if len(planModelOKArr) > 0:
            print "㊗️恭喜你有合格的标了"
            config = MonitoringConfig()
            lilv = "目标最低利率是："+str(config.lilv)+"\n"
            shengyu = "目标最低剩余金额是："+str(config.shengyu)+"元\n\n"
            content = lilv+shengyu
            for model in planModelOKArr:
                content += str(model) + "\n\n"

            Monitoring._dealSuccess(content=content, restartInterval=LONG_SLEEP_SUCCESS)
        else:
            print "没有符合要求的标"
            MonitoringManager().start()
        pass

    @classmethod
    def _planModelWithLi(cls, li = None):
        if not li:
            Monitoring._dealError(content="html解析错误", restartInterval=LONG_SLEEP_FAIL)
            return
        liText = li.text.replace('\t', '');

        planModel = PlanModel();

        # 去除空行元素
        itemArr = []
        for item in liText.split('\n'):
            if item == "":
                continue
            itemArr.append(item)

        # 是否是 每万元复利收益
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

        print planModel

        return planModel
        pass


    @classmethod
    def _dealError(cls, content, restartInterval = 0):
        Monitoring._sendMailAndResart(title="银盛服务监控失败", content= content, restartInterval=restartInterval)
        pass

    @classmethod
    def _dealSuccess(cls, content, restartInterval = 0):
        Monitoring._sendMailAndResart(title="银盛监控服务成功", content= content, restartInterval=restartInterval)
        pass

    @classmethod
    def dealNormal(cls, timeOK, title):
        if not timeOK:
            return
        config = MonitoringConfig()
        lilv = "\n目标最低利率是："+str(config.lilv)+"\n"
        shengyu = "目标最低剩余金额是："+str(config.shengyu)+"元\n"
        content = title + lilv + shengyu + "发送时间:"+ now_time()
        send.send_jinfu_mail(mail_title=title, mail_content=content)
        pass


    @classmethod
    def _sendMailAndResart(cls, title, content, restartInterval = 0):
        send.send_jinfu_mail(mail_title=title, mail_content=content)

        if restartInterval == 0:
            print "不再重新开始计时"
            return
        #print "开始监控倒计时：" + format_seconds(restartInterval)
        MonitoringManager().restart(restartInterval)
        pass

    pass



def format_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d>0:
        return "%d天%d时%d分%d秒" % (d, h, m, s)
    elif h>0:
        return "%d时%d分%d秒" % (h, m, s)
    elif m>0:
        return "%d分%d秒" % ( m, s)
    else:
        return "%d秒" % (seconds)

def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def normal_send_mail_time():
    nowTime = datetime.datetime.now().strftime('%H:%M:%S')
    hour = nowTime.split(":")[0]
    minute = nowTime.split(":")[1]
    second = nowTime.split(":")[2]
    
    hourOK = int(hour)%NORMAL_SEND_INTERVAL == 0
    minuteOK = int(minute) == 0
    secondOK = int(second)>0 and int(second)<40

    return hourOK and minuteOK and secondOK

#是否是夜间
#def is_at_night():
#    nowHour = datetime.datetime.now().strftime('%H')
#    return int(nowHour) >2 and int(nowHour) <7
        
def main():
    print "开启监控中"
    Monitoring.requestHtml()
    m1 = MonitoringManager()
    m1.start()




if __name__ == '__main__':
    main()
    pass