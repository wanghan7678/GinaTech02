from datetime import datetime

import yfinance as yf
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

def get_oneCompany(symbol):
    client = get_TiingoClient()
    meta = client.get_ticker_metadata(symbol)
    item = stock.Usstock_company()
    item.symbol = meta['ticker']
    item.exchange_code = meta['exchangeCode']
    item.name = meta['name']
    item.description = meta['description']
    item.start_date = meta['startDate']
    item.end_date = meta['endDate']
    print("read company information...%s"%(item.symbol))
    return item;

def get_oneFina(symbol):
    client = get_TiingoClient()
    tk = yf.Ticker(symbol)
    item = stock.Usstock_fina()
    df = tk.financials
    nc = len(df.columns)
    rows, cols = df.shape
    for i in range(0, cols):
        item.end_date = df.iat[0, i]
        item.symbol = symbol
        item.total_rev = util.toFloat(df.iat[1, i])
        item.cost_of_rev = util.toFloat(df.iat[2,i])
        item.ops_exp = util.toFloat(df.iat[3,i])
        item.r_n_d = util.toFloat(df.iat[4,i])
        item.non_rec = util.toFloat(df.iat[5,i])
        item.others = util.toFloat(df.iat[6,i])
        item.total_ops = util.toFloat(df.iat[7,i])
        item.ops_li = util.toFloat(df.iat[8,i])
        item.income_cops = util.toFloat(df.iat[9,i])
        item.total_other = util.toFloat(df.iat[10,i])
        item.ebit = util.toFloat(df.iat[11,i])
        item.interest_exp = util.toFloat(df.iat[12,i])
        item.income_before_tax = util.toFloat(df.iat[13,i])
        item.income_tax_expense = util.toFloat(df.iat[14,i])
        item.min_int = util.toFloat(df.iat[15,i])
        item.net_income_cs  = util.toFloat(df.iat[16,i])
        item.disc_ops = util.toFloat(df.iat[17,i])
        item.extra_items = util.toFloat(df.iat[18,i])
        item.effect_ofac = util.toFloat(df.iat[19,i])
        item.other_items = util.toFloat(df.iat[20,i])
        item.net_income = util.toFloat(df.iat[21,i])
        item.pre_stk = util.toFloat(df.iat[22,i])
        item.net_income_to_cs = util.toFloat(df.iat[23, i])
    return item

