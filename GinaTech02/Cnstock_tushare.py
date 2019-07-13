import tushare as tu

import GinaTech02.Cnstock_bean as stock
import GinaTech02.Config as cfg
import GinaTech02.Util as util


def get_tushare_api():
    token = cfg.CONSTANT.Tushare_Token
    tu.set_token(token)
    pro = tu.pro_api()
    return pro

def read_cnstocklist():
    pro = get_tushare_api()
    data = pro.stock_basic(exchange='', list_status='L',
                           fields='ts_code, name, area, industry, enname, market, exchange, list_status, list_date, is_hs' )
    if data.empty:
        print("stock basic list is empty.  tushare.")
    list = []
    for i in range(0, len(data)):
        item = stock.Stock_item()
        item.ts_code = data.iat[i,0]
        item.name = data.iat[i,1]
        item.area = data.iat[i,2]
        item.industry = data.iat[i,3]
        item.enname = data.iat[i,4]
        item.market = data.iat[i,5]
        item.exchange = data.iat[i,6]
        item.list_status = data.iat[i,7]
        item.list_date = util.date_cn2us(data.iat[i,8])
        item.is_hs = data.iat[i,9]
        list.append(item)
    return list

def read_cnstock_daily(ts_code, start_date, end_date):
    pro = get_tushare_api()
    dt_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code, trade_date, open, high, low, close, pct_chg, vol')
    list = []
    for i in range(0, len(dt_daily)):
        item = stock.Stock_daily()
        item.ts_code = dt_daily.iat[i,0]
        item.trade_date = util.date_cn2us(dt_daily.iat[i,1])
        item.open = util.toFloat(dt_daily.iat[i,2])
        item.high = util.toFloat(dt_daily.iat[i,3])
        item.low = util.toFloat(dt_daily.iat[i,4])
        item.close = util.toFloat(dt_daily.iat[i,5])
        item.pct_chg = util.toFloat(dt_daily.iat[i,6])
        item.vol = util.toFloat(dt_daily.iat[i,7])
        item.volume_ratio = 0
        item.turnover_rate = 0
        item.pe = 0
        list.append(item)
    return list

def update_cnstock_basic(list, ts_code, start_date, end_date):
    pro = get_tushare_api()
    dt_basic = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date, fields='ts_code, trade_date, turnover_rate, volume_ratio, pe')
    for i in range(0, len(dt_basic)):
        for item in list:
            if item.ts_code == dt_basic.iat[i,0] and item.trade_date == util.date_cn2us(dt_basic.iat[i,1]):
                item.turnover_rate = util.toFloat(dt_basic.iat[i,2])
                item.volume_ratio = util.toFloat(dt_basic.iat[i,3])
                item.pe = util.toFloat(dt_basic.iat[i,4])
    return list


def read_cnstock_dailyandbasic(ts_code, trade_date):
    list = read_cnstock_daily(ts_code, trade_date, trade_date)
    list = update_cnstock_basic(list, ts_code, trade_date, trade_date)
    return list

def read_cnstock_dailyandbasic(ts_code, start_date, end_date):
    list = read_cnstock_daily(ts_code, start_date, end_date)
    list = update_cnstock_basic(list, ts_code, start_date, end_date)
    return list

