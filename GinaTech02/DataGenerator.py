import threading

import numpy as np

import GinaTech02.Cnstock_dao as cdbo
import GinaTech02.Stock_cal as scal
import GinaTech02.Usstock_dao as udbo
import GinaTech02.Util as util

lock = threading.Lock()

def toStandard(input):
    array = np.array(input)
    array -= array.mean(axis=0)
    array /= array.std(axis=0)
    array=np.nan_to_num(array)
    return array

def get_symbolists_us():
    stockitem = udbo.dao_ussstock_item()
    symbol = stockitem.get_all_symbols()
    return symbol
def get_symbolists_cn():
    stockitem = cdbo.cnstock_item_dao()
    symbol = stockitem.get_all_tscode()
    return symbol


def check_dataintegration(dict):
    rs = True
    if dict is None:
        rs = False
    if dict['close'] is None:
        rs = False
    if len(dict['close'])<scal.SAMPLE_DATASIZE:
        rs = False
    return rs


def get_samplelists_us(symbolists, rows):
    stockdaily = udbo.dao_usstock_daily()
    list = []
    for i in rows:
        s = symbolists[i]
        dict = stockdaily.get_onestocklists_alldays(s)
        if check_dataintegration(dict):
            stcal = scal.stock_cal(s, country='us')
            stcal.read_data(dict)
            r1 = stcal.get_ma5up10_samplestargets()
            for item in r1:
                list.append(item)
    return list

def get_samplelists_cn(symbolists, rows):
    stockdaily = cdbo.cnstock_daily_dao()
    list = []
    for i in rows:
        s = symbolists[i]
        dict = stockdaily.get_onestocklists_alldays(s)
        if check_dataintegration(dict):
            stcal = scal.stock_cal(s, country='cn')
            stcal.read_data(dict)
            r1 = stcal.get_ma5up10_samplestargets()
            for item in r1:
                list.append(item)
    return list



def data_generator(min_index, max_index, shuffle=False, batch_size=32, country='us'):
    #global lock
    if country == 'us':
        symbollist = get_symbolists_us()
    else:
        symbollist = get_symbolists_cn()

    rowcnt = len(symbollist)
    if max_index is None:
        max_index = rowcnt - 1
    if max_index > rowcnt:
        max_index = rowcnt
    if min_index <0:
        min_index = 0
    if min_index >= max_index:
        min_index = 0
    i = min_index
    while True:
        if shuffle:
            rows = np.random.randint(min_index, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index
            rows = np.arange(i, min(i+batch_size, max_index))
            i+= len(rows)
        if lock.acquire(1):
            if country == 'us':
                list = get_samplelists_us(symbollist, rows)
            else:
                list = get_samplelists_cn(symbollist, rows)

            samples = np.zeros((len(list), scal.SAMPLE_DATASIZE, scal.FEATURE_NUM))
            targets = np.zeros((len(list),))
            for j in range(0, len(list)):
                try:
                    samples[j] = np.array(list[j][0])
                    targets[j] = util.toInt(list[j][1])
                except ValueError as err:
                    print("Cannot broadcast input array into shape(60,26):  %s" %str(err))
            samples = toStandard(samples)
            lock.release()
            yield samples, targets


def get_stepsnum_us(start, end):
    symlist = get_symbolists_us()
    rows = range(start, end)
    list = get_samplelists_us(symlist, rows)
    r = len(list)
    return r

train_gen_us = data_generator(500, 7000, shuffle=True, country='us')
val_gen_us = data_generator(0, 500, shuffle=True, country='us')

train_gen_cn = data_generator(10, 100, shuffle=True, country='cn')
val_gen_cn = data_generator(0, 10, shuffle=True, country='cn')

val_steps_us =1379 #for 0 to 900
val_steps_cn =1379


def get_predictlist_us():
    symbolist = get_symbolists_us()
    stockdaily = udbo.dao_usstock_daily()
    samplelist, lablelist=[],[]
    if lock.acquire(1):
        for sy in symbolist:
            dict = stockdaily.get_onestocklists_alldays(sy)
            if check_dataintegration(dict):
                stockcal = scal.stock_cal(sy, country='us')
                stockcal.read_data(dict)
                r = stockcal.get_predict_samples()
                if r is not None:
                    samplelist.append(r)
                    lablelist.append(sy)
    samples = np.zeros((len(samplelist), scal.SAMPLE_DATASIZE, scal.FEATURE_NUM))
    for i in range(0, len(samplelist)):
        samples[i] = samplelist[i]
    list = [samples, lablelist]
    lock.release()
    return list

def get_predictlist_cn():
    symbolist = get_symbolists_cn()
    stockdaily = cdbo.cnstock_daily_dao()
    samplelist, labellist = [],[]
    if lock.acquire(1):
        for sy in symbolist:
            dict = stockdaily.get_onestocklists_alldays(sy)
            if check_dataintegration(dict):
                    stockcal = scal.stock_cal(sy, country='cn')
                    stockcal.read_data(dict)
                    r = stockcal.get_predict_samples()
                    if r is not None:
                        samplelist.append(r)
                        labellist.append(sy)
    samples = np.zeros((len(samplelist), scal.SAMPLE_DATASIZE, scal.FEATURE_NUM))
    for i in range(0, len(samplelist)):
        samples[i] = samplelist[i]
    list = [samples, labellist]
    lock.release()
    return list