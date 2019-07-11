import threading

import numpy as np

import GinaTech02.Usstock_cal as ucal
import GinaTech02.Usstock_dao as dbo
import GinaTech02.Util as util

lock = threading.Lock()

def toStandard(input):
    array = np.array(input)
    array -= array.mean(axis=0)
    array /= array.std(axis=0)
    array=np.nan_to_num(array)
    return array

def get_symbolists():
    stockitem = dbo.dao_ussstock_item()
    symbol = stockitem.get_all_symbols()
    return symbol

def check_dataintegration(dict):
    rs = True
    if dict is None:
        rs = False
    if dict['close'] is None:
        rs = False
    if len(dict['close'])<ucal.SAMPLE_DATASIZE:
        rs = False
    return rs


def get_samplelists(symbolists, rows):
    stockdaily = dbo.dao_usstock_daily()
    list = []
    for i in rows:
        s = symbolists[i]
        dict = stockdaily.get_onestocklists_alldays(s)
        if check_dataintegration(dict):
            stockcal = ucal.usstock_calresult(s)
            stockcal.read_data(dict)
            r1 = stockcal.get_ma5up10_samplestargets()
            for item in r1:
                list.append(item)
    return list


def data_generator(min_index, max_index, shuffle=False, batch_size=32):
    #global lock
    symbollist = get_symbolists()
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
            list = get_samplelists(symbollist, rows)

            samples = np.zeros((len(list), ucal.SAMPLE_DATASIZE, ucal.FEATURE_NUM))
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


def get_stepsnum(start, end):
    symlist = get_symbolists()
    rows = range(start, end)
    list = get_samplelists(symlist, rows)
    r = len(list)
    return r

train_gen = data_generator(900, 4000, shuffle=True)
val_gen = data_generator(0, 900, shuffle=True)
val_steps =1379 #for 0 to 900

def get_predictlist():
    symbolist = get_symbolists()
    stockdaily = dbo.dao_usstock_daily()
    samplelist, lablelist=[],[]
    if lock.acquire(1):
        for sy in symbolist:
            dict = stockdaily.get_onestocklists_alldays(sy)
            if check_dataintegration(dict):
                stockcal = ucal.usstock_calresult(sy)
                stockcal.read_data(dict)
                r = stockcal.get_predict_samples()
                if r is not None:
                    samplelist.append(r)
                    lablelist.append(sy)
    samples = np.zeros((len(samplelist), ucal.SAMPLE_DATASIZE, ucal.FEATURE_NUM))
    for i in range(0, len(samplelist)):
        samples[i] = samplelist[i]
    list = [samples, lablelist]
    lock.release()
    return list