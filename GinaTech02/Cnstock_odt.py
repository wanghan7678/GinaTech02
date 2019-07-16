import datetime

from opendatatools import stock

import GinaTech02.Cnstock_bean as cnstk
import GinaTech02.Config as cfg
import GinaTech02.Util as util


def toDate(inputtime):
    datestr = str(inputtime)
    strlist = datestr.split(' ')
    if len(strlist)>0:
        dst=strlist[0]
        dt = datetime.datetime.strptime(dst, cfg.CONSTANT.DATE_FORMAT_US)
        return dt


def read_cnstock_daily(ts_code, start_date, end_date):
    df, msg = stock.get_daily(ts_code, start_date=start_date, end_date=end_date)
    list = []
    for i in range(0, len(df)):
        item = cnstk.Stock_daily()
        item.ts_code = df.iat[i,6]
        item.trade_date = toDate(df.iat[i,7])
        item.open = util.toFloat(df.iat[i,4])
        item.high = util.toFloat(df.iat[i,1])
        item.low = util.toFloat(df.iat[i,3])
        item.close = util.toFloat(df.iat[i,2])
        item.pct_chg = util.toFloat(df.iat[i,5])
        item.vol = util.toFloat(df.iat[i,9])
        item.volume_ratio = -1
        item.turnover_rate = util.toFloat(df.iat[i,8])
        item.pe = -1
        list.append(item)
    return list