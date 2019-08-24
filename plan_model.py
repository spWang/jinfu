#!/usr/bin/python
# -*- coding: utf-8 -*-


STANDARD_LILV = 9 #年化利率高于多少时通知我
STANDARD_SHENGYU = 10000 #高于多少剩余金额时通知我


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

        lilvOK = True if (self.lilv>=STANDARD_LILV) else False
        progressOK = True if (self.progress<100) else False
        shenyuOK = True if (self.shengyu>STANDARD_SHENGYU) else False


        return lilvOK and progressOK and shenyuOK


    def __str__(self):
        shengyu = self.shengyu
        unit = "元"
        if shengyu>10000:
            shengyu/=10000
            unit = "万元"

        return "进度：{progress}%\n年化利率：{lilv}%\n借款期限：{jiekuanqixian}\n每万元收益：{shouyi}元\n剩余金额：{shengyu}{unit}\n".format(progress=self.progress,lilv=self.lilv,jiekuanqixian=self.jiekuanqixian,shouyi=self.shouyi,shengyu=shengyu,unit=unit)
        pass