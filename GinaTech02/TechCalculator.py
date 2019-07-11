import numpy as np
import talib

import GinaTech02.Util as util

DATASIZE = 60
CALCSIZE = 200

FASTK_PERIOD = 10
FASTD_PERIOD = 3
BOLLER_PERIOD=10
DMI_PERIOD=14
WR1_PERIOD=6
WR2_PERIOD=13
MTM_PERIOD=12

#in the sequence order:按照时间顺序，早的在前面。
class Tech_Calculator(object):
    openlist, closelist, highlist, lowlist, vollist = [0],[0],[0],[0],[0]
    symbol = ''
    length = 0

    def set_dailydata(self,inputdata, symbol):
        self.openlist = np.array(inputdata['open'], dtype=float)
        self.closelist = np.array(inputdata['close'],dtype=float)
        self.highlist = np.array(inputdata['high'], dtype=float)
        self.lowlist = np.array(inputdata['low'], dtype=float)
        self.vollist = np.array(inputdata['volume'],dtype=float)
        self.length = util.toFloat(len(inputdata['close']))
        self.symbol = symbol


    #the latest time data is on the top
    def get_obv(self):
        obv_list = talib.OBV(self.closelist, self.vollist)
        obv_list = np.nan_to_num(obv_list)
        return obv_list

    def get_faststc(self):
        list = talib.STOCHF(high=self.highlist, low=self.lowlist, close=self.closelist, fastk_period=FASTK_PERIOD, fastd_period=FASTD_PERIOD, fastd_matype=0)
        list = np.nan_to_num(list)
        fk = list[0]
        fd = list[1]
        #result = {"fastk":fk[::-1], "fastd":fd[::-1]}
        result = {'faststc_pk':fk, 'faststc_dk':fd}
        return result

    def get_boll(self):
        list = talib.BBANDS(self.closelist, timeperiod=BOLLER_PERIOD, nbdevup=2, nbdevdn=2, matype=0)
        list = np.nan_to_num(list)
        upper = list[0]
        middle= list[1]
        lower = list[2]
        #result = {"upper":upper[::-1], "middle":middle[::-1],"lower":lower[::-1]}
        result = {'boll_upper':upper,'boll_mid':middle,'boll_lower':lower}
        return result

    def get_dmi(self):
        adx = talib.ADX(self.highlist,self.lowlist,self.closelist,timeperiod=DMI_PERIOD)
        adx = np.nan_to_num(adx)
        pdi = talib.PLUS_DI(self.highlist, self.lowlist, self.closelist,timeperiod=DMI_PERIOD)
        pdi = np.nan_to_num(pdi)
        mdi = talib.MINUS_DI(self.highlist,self.lowlist,self.closelist,timeperiod=DMI_PERIOD)
        mdi = np.nan_to_num(mdi)
        #result = {"adx": adx[::-1],"pdi":pdi[::-1],"mdi":mdi[::-1]}
        result={'dmi_adx':adx,'dmi_pdi':pdi,'dmi_mdi':mdi}
        return result
    def get_wmsr(self):
        wr1 = talib.WILLR(self.highlist, self.lowlist, self.closelist, timeperiod=WR1_PERIOD)
        wr2 = talib.WILLR(self.highlist, self.lowlist, self.closelist, timeperiod=WR2_PERIOD)
        wr1 = np.nan_to_num(wr1)
        wr2 = np.nan_to_num(wr2)
        #result = {"wr1":wr1[::-1],"wr2":wr2[::-1]}
        result = {'wmsr_wr1':wr1,'wmsr_wr2':wr2}
        return result
    def get_mtm(self):
        mtm = talib.MOM(self.closelist, timeperiod=MTM_PERIOD)
        mtm = np.nan_to_num(mtm)
        #mtm = mtm[::-1]
        return mtm
    def get_sar(self):
        sar = talib.SAR(self.highlist, self.lowlist, acceleration=0,maximum=0)
        sar = np.nan_to_num(sar)
        #sar = sar[::-1]
        return sar
    def get_pvt(self):
        close = self.closelist
        vol = self.vollist
        list = []
        for i in range(0,len(close)):
            pvt = 0
            if i>0 and close[i-1]!=0:
                pvt =((close[i]-close[i-1])/close[i-1])*vol[i]
            list.append(pvt)
        #list = list[::-1]
        return list

    def get_SMA(self, timeperiod = 5):
        close = self.closelist
        array = np.array(close, dtype=float)
        ma = []
        try:
            ma = talib.SMA(array, timeperiod=timeperiod)
        except Exception as err:
            print("talib.sma exception: %s" %str(err))
        ma = np.nan_to_num(ma)
        return ma

    def get_ma5up10_indices(self):
        ma5 = self.get_SMA(5)
        ma10 = self.get_SMA(10)
        n = len(ma5)-1
        list = []
        for i in range(0,n-1):
            upc = False
            if ma10[i] >= ma5[i] and ma10[i+1] < ma5[i+1]:
                upc = True
            if upc:
                list.append(i)
        return list

    def get_pctchange(self):
        size = len(self.closelist)
        list = []
        pct = 0
        for i in range(0, size):
            if(self.openlist[i]!=0):
               pct = (self.closelist[i]-self.openlist[i])/self.openlist[i]
            else:
                pct = 0
            list.append(pct)
        return list

    def get_chaikinAD(self):
        ad = talib.AD(self.highlist, self.lowlist, self.closelist, self.vollist)
        ad = np.nan_to_num(ad)
        return ad
    def get_Trange(self):
        trange = talib.TRANGE(self.highlist, self.lowlist, self.closelist)
        trange = np.nan_to_num(trange)
        return trange