import datetime

import numpy as np

import GinaTech02.Config as cfg


def toFloat(input):
    a = 0
    if input is None:
        return 0
    else:
        try:
            a = float(np.nan_to_num(input))
        except Exception as err:
            print("input is %s"%str(input))
            print("number to float exception: %s" %str(err))
        return a

def toInt(input):
    a=0
    if input is None:
        return 0
    else:
        try:
            a = int(np.nan_to_num(input))
        except Exception as err:
            print("input is %s" % str(input))
            print("number to int exception: %s" %str(err))
        return a

def toStd(input):
    array = np.array(input)
    array -= array.mean(axis=0)
    array /= array.std(axis=0)
    array = np.nan_to_num(array)
    return array

def cmplx_toFloat(input):
    n = 1
    if input is None:
        return 0
    input = str(input)
    input = input.strip()
    if input.endswith('M'):
        n = 1000000
    if input.endswith('B'):
        n = 1000000000
    input = input.replace('M', '')
    input = input.replace('B', '')
    input = input.replace('$', '')
    r = toFloat(input)
    return r*n

def get_today_datestr():
    dt = datetime.datetime.now().strftime(cfg.CONSTANT.DATE_FORMAT_US)
    return dt

def get_date(datestr):
    dt = datetime.strptime(datestr, cfg.CONSTANT.DATE_FORMAT_US)
    return dt