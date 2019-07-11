from datetime import datetime

from opendatatools import usstock
from tiingo import TiingoClient

import GinaTech02.Config as cfg
import GinaTech02.Usstock_bean as stock
import GinaTech02.Util as util


def get_allsymbol_items():
    df, msg = usstock.get_symbols()
    if df.empty:
        print("Symbol list data empty.")
        return None
    else:
        data_list = []
        for i in range(0, len(df)):
            astk = stock.Usstock_item()
            astk.symbol = str(df.iat[i, 0])
            astk.name = str(df.iat[i, 1])
            astk.last_sale = str(df.iat[i, 2])
            astk.market_cap = str(df.iat[i, 3])
            astk.ipo_year = str(df.iat[i, 4])
            astk.sector = str(df.iat[i, 5])
            astk.industry = str(df.iat[i, 6])
            astk.sum_quote = str(df.iat[i, 7])
            data_list.append(astk)
        return data_list

def get_daily_bysymbol(smybol):
    df, msg = usstock.get_daily(smybol)
    if df is None or df.empty:
        print("%s Daily data empty." %smybol)
        return None
    df = df.tail(cfg.CONSTANT.DATASIZE)
    data_list = []
    print("reading... %s %s" %(smybol,str(len(df))))
    for i in range(0, len(df)):
        item = stock.Usstock_daily()
        item.symbol = smybol
        item.trade_date = datetime.strptime(df.iat[i,0], '%Y-%m-%d')
        item.open = util.toFloat(df.iat[i,1])
        item.high = util.toFloat(df.iat[i,2])
        item.low = util.toFloat(df.iat[i,3])
        item.close = util.toFloat(df.iat[i,4])
        item.adj_close = util.toFloat(df.iat[i,5])
        item.volume = util.toFloat(df.iat[i,6])
        data_list.append(item)
    return data_list

def get_TiingoClient():
    config = {}
    config['session']=True
    config['api_key']=cfg.CONSTANT.Tiing_Token
    client = TiingoClient(config)
    return client

def get_onedaily(symbol, trade_date):
    client = get_TiingoClient()
    pr = client.get_ticker_price(symbol, startDate=trade_date, endDate=trade_date,frequency='daily')
    list = []
    for row in pr:
        item = stock.Usstock_daily()
        item.symbol = symbol
        item.trade_date = trade_date
        item.close = util.toFloat(row['close'])
        item.open = util.toFloat(row['open'])
        item.high = util.toFloat(row['high'])
        item.low = util.toFloat(row['low'])
        item.adj_close = util.toFloat(row['adjClose'])
        item.volume = util.toFloat(row['volume'])
        list.append(item)
    print("read data...%s"%(symbol+str(trade_date)))
    return list
