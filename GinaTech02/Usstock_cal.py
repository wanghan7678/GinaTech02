import numpy as np

import GinaTech02.TechCalculator as tc
import GinaTech02.Usstock_dao as dbo
import GinaTech02.Util as util

SAMPLE_DATASIZE = 60
FEATURE_NUM = 26
LABEL_THREAD = 0.04

class usstock_calresult:

    __symbol = ""
    __datasize = 0
    __marketcap = 0

    __input_data = {}
    __cal_data = {'pct_change':[],'ma5':[],'ma10':[],'ma20':[],
                'obv':[],'faststc_pk':[],'faststc_dk':[],'boll_upper':[],'boll_mid':[],'boll_lower':[],
                'dmi_pdi':[],'dmi_mdi':[],'dmi_adx':[],'wmsr_wr1':[],'wmsr_wr2':[],'mtm':[],'sar':[],'pvt':[],
                'turnover_rate':[],'ad':[],'trange':[]}

    def __init__(self, symbol):
        self.__symbol = symbol

    def set_symbol(self, symbol):
        self.__symbol = symbol

    def read_data(self, input):
        ddb = dbo.dao_usstock_daily()
        self.__input_data = input
        stdb = dbo.dao_ussstock_item()
        rs = stdb.get_marketcap(self.__symbol)
        self.__marketcap = util.cmplx_toFloat(rs)
        self.__datasize = len(input['close'])

    def __cal_turnoverratio(self):
        tr = np.zeros((self.__datasize), dtype=float)
        for i in range(0, self.__datasize):
            if self.__marketcap != 0:
                tr[i] = (self.__input_data['close'][i]*self.__input_data['volume'][i])/self.__marketcap
            else:
                tr[i]=0
        return tr


    def __cal_indicators(self):
        cal = tc.Tech_Calculator()
        cal.set_dailydata(self.__input_data, self.__symbol)
        pct_change = cal.get_pctchange()
        ma5 = cal.get_SMA(5)
        ma10 = cal.get_SMA(10)
        ma20 = cal.get_SMA(20)
        obv = cal.get_obv()
        faststc = cal.get_faststc()
        boll = cal.get_boll()
        dmi = cal.get_dmi()
        wmsr = cal.get_wmsr()
        mtm = cal.get_mtm()
        sar = cal.get_sar()
        pvt = cal.get_pvt()
        turnover = self.__cal_turnoverratio()
        ad = cal.get_chaikinAD()
        trange = cal.get_Trange()
        self.__cal_data['pct_change']=pct_change
        self.__cal_data['ma5']=ma5
        self.__cal_data['ma10']=ma10
        self.__cal_data['ma20']=ma20
        self.__cal_data['obv']=obv
        self.__cal_data['faststc_pk']=faststc['faststc_pk']
        self.__cal_data['faststc_dk']=faststc['faststc_dk']
        self.__cal_data['boll_upper']=boll['boll_upper']
        self.__cal_data['boll_mid']=boll['boll_mid']
        self.__cal_data['boll_lower']=boll['boll_lower']
        self.__cal_data['dmi_pdi']=dmi['dmi_pdi']
        self.__cal_data['dmi_mdi']=dmi['dmi_mdi']
        self.__cal_data['dmi_adx']=dmi['dmi_adx']
        self.__cal_data['wmsr_wr1']=wmsr['wmsr_wr1']
        self.__cal_data['wmsr_wr2']=wmsr['wmsr_wr2']
        self.__cal_data['mtm']=mtm
        self.__cal_data['sar']=sar
        self.__cal_data['pvt']=pvt
        self.__cal_data['turnover']=turnover
        self.__cal_data['ad']=ad
        self.__cal_data['trange']=trange


    def cal_ma5up10crosses(self):
        indices = []
        ma5 = self.__cal_data['ma5']
        ma10 = self.__cal_data['ma10']
        for i in range(0, len(ma5)-1):
            if ma5[i] <= ma10[i] and ma5[i+1]>ma10[i+1]:
                indices.append(i+1)
        return indices


    def cal_label(self, index):
        r = 0
        if index+6<=self.__datasize:
            c2=self.__input_data['close'][index+1]
            c6=self.__input_data['close'][index+6]
            if c6 > 0 and c2!=0:
                pct = (c6-c2)/c2
                if pct>=LABEL_THREAD:
                    r=1
        return r


    def create_sample(self, index):
        begin = index - SAMPLE_DATASIZE + 1
        samples=[0]*SAMPLE_DATASIZE
        j=0
        for i in range(begin, index+1):
            samples[j] = [self.__input_data['open'][i],self.__input_data['high'][i],self.__input_data['low'][i],self.__input_data['close'][i],self.__input_data['volume'][i],
                          self.__cal_data['pct_change'][i],
                          self.__cal_data['ma5'][i],self.__cal_data['ma10'][i],self.__cal_data['ma20'][i]
                          ,self.__cal_data['obv'][i],self.__cal_data['faststc_pk'][i],self.__cal_data['faststc_dk'][i],self.__cal_data['boll_upper'][i],self.__cal_data['boll_mid'][i]
                          ,self.__cal_data['boll_lower'][i],self.__cal_data['dmi_pdi'][i],self.__cal_data['dmi_mdi'][i],self.__cal_data['dmi_adx'][i],self.__cal_data['wmsr_wr1'][i]
                          ,self.__cal_data['wmsr_wr2'][i],self.__cal_data['mtm'][i],self.__cal_data['sar'][i],
                          self.__cal_data['pvt'][i],
                          self.__cal_data['turnover'][i]
                          ,self.__cal_data['ad'][i],self.__cal_data['trange'][i]]
            j+=1
        samples = np.nan_to_num(samples)
        return samples

    def get_ma5up10_samplestargets(self):
        self.__cal_indicators()
        crosses = self.cal_ma5up10crosses()
        list = []
        #s = self.__symbol +", length of input: " + str(
        #    len(self.__input_data["close"])) + ", len of cal: " + str(len(self.__cal_data['pct_change']))
        #print("create samples: %s"%s)
        for i in crosses:
            if i >= 59 and i< self.__datasize-6:
                try:
                    list.append([self.create_sample(i), self.cal_label(i)])
                except Exception as err:
                    s = self.__symbol+": i="+str(i)+", length of input: "+str(len(self.__input_data["close"]))+", len of cal: "+str(len(self.__cal_data['pct_change']))
                    print(s)
                    print("create sample error.")
                    print(str(err))
                    raise Exception
        return list

    def iflastone_ma5up10(self):
        ma5 = self.__cal_data['ma5']
        ma10 = self.__cal_data['ma10']
        cross = False
        i = self.__datasize -2
        if ma5[i]<=ma10[i] and ma5[i+1]>ma10[i+1]:
            cross = True
        return cross


    def get_predict_samples(self):
        self.__cal_indicators()
        cross = self.iflastone_ma5up10()
        if cross:
            return self.create_sample(self.__datasize-1)
        else:
            return None










