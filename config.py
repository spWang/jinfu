#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 8.5 = 一个月
# 9.0 = 三个月
# 9.5 = 六个月

DEFAULT_LILV = 9.4
DEFAULT_SHENGYU = 10000

def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton



@singleton
class MonitoringConfig(object):

    #利率
    _lilv = DEFAULT_LILV
    @property
    def lilv(self):
        return self._lilv

    @lilv.setter
    def lilv(self, value):
        self._lilv = value

    # 竞标最低金额
    _shengyu = DEFAULT_SHENGYU
    @property
    def shengyu(self):
        return self._shengyu

    @shengyu.setter
    def shengyu(self, value):
        self._shengyu = value