#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import MonitoringConfig

class PlanModel(object):

    def __init__(self,
                 progress=0.0,
                 lilv=0,
                 jiekuanqixian='',#带单位
                 shouyi=0,
                 shengyu=0,
                 fuli=False #每万元复利收益 不要这一种的
                 ):
        self.progress = progress
        self.lilv = lilv
        self.jiekuanqixian = jiekuanqixian
        self.shouyi = shouyi
        self.shengyu = shengyu
        self.fuli = fuli
        pass

    @property
    def ok(self):
        if self.fuli:
            return False

        baseLilv = MonitoringConfig().lilv
        print "要求利率是："+str(baseLilv)


        baseShengyu = MonitoringConfig().shengyu
        print "要求剩余金额是："+str(baseShengyu)

        lilvOK = True if (self.lilv>=baseLilv) else False
        progressOK = True if (self.progress<100) else False
        shenyuOK = True if (self.shengyu>baseShengyu) else False


        return lilvOK and progressOK and shenyuOK


    def __str__(self):
        shengyu = self.shengyu
        unit = "元"
        if shengyu>10000:
            shengyu/=10000
            unit = "万元"
        shouyiText = '每万元收益'
        if self.fuli:
            shouyiText = "每万元复利收益"

        return "进度：{progress}%\n年化利率：{lilv}%\n借款期限：{jiekuanqixian}\n{shouyiText}：{shouyi}元\n剩余金额：{shengyu}{unit}\n".format(progress=self.progress,lilv=self.lilv,jiekuanqixian=self.jiekuanqixian,shouyiText=shouyiText,shouyi=self.shouyi,shengyu=shengyu,unit=unit)
        pass