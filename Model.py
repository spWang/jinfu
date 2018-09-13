#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

#金服计划标准
STANDARD_lilv = 11.5 #最低的年化利率
STANDARD_date_length = 12 #最长的投资期限
STANDARD_state = "立即加入"
# STANDARD_state = "还款中"

#优选标标准
STANDARD_youxuan_lilv = 9.5  #最低的年化利率
STANDARD_youxuan_date_length = 6 #最长的投资期限
STANDARD_youxuan_process = 100 #投资的进度不能超过百分之这么多

#转让专区标准
STANDARD_zhuanrangzhuanqu_lilv = 11.5  #最低的年化利率
STANDARD_zhuanrangzhuanqu_date_length = 12 #最长的投资期限
STANDARD_zhuanrangzhuanqu_process = 100 #投资的进度不能超过百分之这么多

class Type(Enum):
    Type_jinfujihua=1
    Type_youxuanbiao=2
    Type_zhuanrangzhuanqu=3


#金服计划的标
class MoneyModel(object):

    '''利率  借款期限 剩余金额'''
    def __init__(self,
                 lilv="",
                 date_length="",
                 last_money="",
                 state="",
                 shouyi="",
                 process="",
                 youxuan_type = "",
                 youxuan_shouyi = 0,
                 type=Type(1)
                 ):
        self.lilv=lilv
        self.date_length=date_length
        self.last_money=last_money
        self.state = state
        self.shouyi=shouyi
        self.process=process
        self.type=type
        self.youxuan_type=youxuan_type
        self.youxuan_shouyi=youxuan_shouyi
        pass

    @property
    def data_ok(self):
        # print self.lilv,self.date_length,self.state

        lilv_ok = False
        date_length_ok = False
        state_ok = False
        process_ok = False
        shouyi_type_ok = False

        #检验标准
        lilv_s = STANDARD_lilv
        date_length_s = STANDARD_date_length
        state_s = STANDARD_state
        process_s = STANDARD_youxuan_process

        if self.type == Type.Type_youxuanbiao:
            lilv_s = STANDARD_youxuan_lilv
            date_length_s = STANDARD_youxuan_date_length
            process_s = STANDARD_youxuan_process
        elif self.type == Type.Type_zhuanrangzhuanqu:
            lilv_s = STANDARD_youxuan_lilv
            date_length_s = STANDARD_youxuan_date_length
            process_s = STANDARD_zhuanrangzhuanqu_process
        else:
            lilv_s = STANDARD_lilv
            state_s = STANDARD_state
            date_length_s = STANDARD_date_length
            pass

        lilv_str = self.lilv.strip("%")
        if len(lilv_str)>0 and float(lilv_str) >= lilv_s:
            lilv_ok = True
            pass

        date_length_str = self.date_length.strip("个月")
        if len(date_length_str)>0 and int(date_length_str) <= date_length_s:
            date_length_ok = True
            pass

        if len(self.state)>0 and self.state == state_s:
            state_ok = True
            pass

        process_str = self.process.strip("%")
        if len(process_str)>0 and float(process_str)<process_s:
            process_ok = True
            pass

        if "每万元收益" == self.youxuan_type:
            shouyi_type_ok = True

        can_touzi = state_ok or process_ok

        if lilv_ok and date_length_ok and can_touzi and shouyi_type_ok:
            return True

        return False
        pass

    def __str__(self):
        return ""+' '.join([self.lilv,self.date_length,self.last_money,self.state,self.shouyi,self.process,self.youxuan_type,self.youxuan_shouyi])
        pass