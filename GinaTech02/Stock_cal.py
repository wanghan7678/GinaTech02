import numpy as np

import GinaTech02.TechCalculator as tc

SAMPLE_DATASIZE = 60
FEATURE_NUM = 26
LABEL_THREAD = 0.04

class stock_cal:

    _symbol = ""
    _datasize = 0

    _inputdata = {}
    country = 'us'
    _cal_data = {'pct_change':[],'ma5':[],'ma10':[],'ma20':[],
                'obv':[],'faststc_pk':[],'faststc_dk':[],'boll_upper':[],'boll_mid':[],'boll_lower':[],
                'dmi_pdi':[],'dmi_mdi':[],'dmi_adx':[],'wmsr_wr1':[],'wmsr_wr2':[],'mtm':[],'sar':[],'pvt':[],
                'turnover_rate':[],'ad':[],'trange':[]}

    def __init__(self, symbol, country):
        self._symbol = symbol
        self.country = country

    def set_symbol(self, symbol):
        self._symbol = symbol

    def set_inputdata(self, input):
        self._inputdata = input
    def set_datasize(self, size):
        self._datasize = size
    def set_country(self, tr):
        self.country = tr


    def read_data(self, input):
        self._inputdata = input
        self._datasize = len(input['close'])

    def _cal_indicators(self):
        cal = tc.Tech_Calculator()
        cal.set_dailydata(self._inputdata, self._symbol)
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
        #turnover = self.cal_turnoverratio()
        turnover = cal.get_turnover(self.country)
        #print("turnover: %d"%len(turnover))
        ad = cal.get_chaikinAD()
        trange = cal.get_Trange()
        self._cal_data['pct_change']=pct_change
        self._cal_data['ma5']=ma5
        self._cal_data['ma10']=ma10
        self._cal_data['ma20']=ma20
        self._cal_data['obv']=obv
        self._cal_data['faststc_pk']=faststc['faststc_pk']
        self._cal_data['faststc_dk']=faststc['faststc_dk']
        self._cal_data['boll_upper']=boll['boll_upper']
        self._cal_data['boll_mid']=boll['boll_mid']
        self._cal_data['boll_lower']=boll['boll_lower']
        self._cal_data['dmi_pdi']=dmi['dmi_pdi']
        self._cal_data['dmi_mdi']=dmi['dmi_mdi']
        self._cal_data['dmi_adx']=dmi['dmi_adx']
        self._cal_data['wmsr_wr1']=wmsr['wmsr_wr1']
        self._cal_data['wmsr_wr2']=wmsr['wmsr_wr2']
        self._cal_data['mtm']=mtm
        self._cal_data['sar']=sar
        self._cal_data['pvt']=pvt
        self._cal_data['turnover']=turnover
        self._cal_data['ad']=ad
        self._cal_data['trange']=trange


    def cal_ma5up10crosses(self):
        indices = []
        ma5 = self._cal_data['ma5']
        ma10 = self._cal_data['ma10']
        for i in range(0, len(ma5)-1):
            if ma5[i] <= ma10[i] and ma5[i+1]>ma10[i+1]:
                indices.append(i+1)
        return indices


    def cal_label(self, index):
        r = 0
        if index+6<=self._datasize:
            c2=self._inputdata['close'][index+1]
            c6=self._inputdata['close'][index+6]
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
            samples[j] = [self._inputdata['open'][i],self._inputdata['high'][i],self._inputdata['low'][i],self._inputdata['close'][i],self._inputdata['volume'][i],
                          self._cal_data['pct_change'][i],
                          self._cal_data['ma5'][i],self._cal_data['ma10'][i],self._cal_data['ma20'][i]
                          ,self._cal_data['obv'][i],self._cal_data['faststc_pk'][i],self._cal_data['faststc_dk'][i],self._cal_data['boll_upper'][i],self._cal_data['boll_mid'][i]
                          ,self._cal_data['boll_lower'][i],self._cal_data['dmi_pdi'][i],self._cal_data['dmi_mdi'][i],self._cal_data['dmi_adx'][i],self._cal_data['wmsr_wr1'][i]
                          ,self._cal_data['wmsr_wr2'][i],self._cal_data['mtm'][i],self._cal_data['sar'][i],
                          self._cal_data['pvt'][i],
                          self._cal_data['turnover'][i]
                          ,self._cal_data['ad'][i],self._cal_data['trange'][i]]
            j+=1
        samples = np.nan_to_num(samples)
        return samples

    def get_ma5up10_samplestargets(self):
        self._cal_indicators()
        crosses = self.cal_ma5up10crosses()
        list = []
        #s = self._symbol +", length of input: " + str(
        #    len(self._inputdata["close"])) + ", len of cal: " + str(len(self._cal_data['pct_change']))
        #print("create samples: %s"%s)
        for i in crosses:
            if i >= 59 and i< self._datasize-6:
                try:
                    list.append([self.create_sample(i), self.cal_label(i)])
                except Exception as err:
                    s = self._symbol+": i="+str(i)+", length of input: "+str(len(self._inputdata["close"]))+", len of cal: "+str(len(self._cal_data['pct_change']))
                    print(s)
                    print("create sample error.")
                    print(str(err))
                    raise Exception
        return list

    def iflastone_ma5up10(self):
        ma5 = self._cal_data['ma5']
        ma10 = self._cal_data['ma10']
        cross = False
        i = self._datasize -2
        if ma5[i]<=ma10[i] and ma5[i+1]>ma10[i+1]:
            cross = True
        return cross


    def get_predict_samples(self):
        self._cal_indicators()
        cross = self.iflastone_ma5up10()
        if cross:
            return self.create_sample(self._datasize-1)
        else:
            return None




