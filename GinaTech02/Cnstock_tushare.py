import tushare as tu

import GinaTech02.Cnstock_bean as stock
import GinaTech02.Config as cfg
import GinaTech02.Util as util

TUSHARE_DAILYFIELDS='ts_code, trade_date, open, high, low, close, pct_chg, vol'
TUSHARE_COMPNAYFIELDS='ts_code, exchange, chairman, manager, secretary, reg_capital, setup_date, province, city, introduction, website, email, office, employees, main_business, business_scope'
TUSHARE_FINAFIELDS = 'ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, revenue_ps, extra_item, profit_dedt, gross_margin, current_ratio, quick_ratio, cash_ratio, assets_turn, interst_income, daa, edit, editda, netdebt, bps, roe, roa, npta, debt_to_assets'

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

def create_item_fromdataset(dt_data):
    dt_daily = dt_data
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


def read_cnstock_daily2(trade_date):
    pro = get_tushare_api()
    dt_daily = pro.daily(trade_date=trade_date, fields=TUSHARE_DAILYFIELDS)
    list = create_item_fromdataset(dt_daily)
    return list

def read_cnstock_daily(ts_code, start_date, end_date):
    pro = get_tushare_api()
    dt_daily = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=True)
    list = create_item_fromdataset(dt_daily)
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

def update_cnstock_basic2(list, trade_date):
    pro = get_tushare_api()
    dt_basic = pro.daily_basic(ts_code='', trade_date=trade_date, fields='ts_code, trade_date, turnover_rate, volume_ratio, pe')
    for i in range(0, len(dt_basic)):
        for item in list:
            if item.ts_code == dt_basic.iat[i,0] and item.trade_date == util.date_cn2us(dt_basic.iat[i,1]):
                item.turnover_rate = util.toFloat(dt_basic.iat[i,2])
                item.volume_ratio = util.toFloat(dt_basic.iat[i,3])
                item.pe = util.toFloat(dt_basic.iat[i,4])
    return list

def read_cnstock_dailyandbasic2(daystr):
    list = read_cnstock_daily2(trade_date=daystr)
    list = update_cnstock_basic2(list, trade_date=daystr)
    return list

def read_cnstock_dailyandbasic(ts_code, start_date, end_date):
    list = read_cnstock_daily(ts_code, start_date, end_date)
    list = update_cnstock_basic(list, ts_code, start_date, end_date)
    return list

def __addCompanyList(list, dataset):
    df = dataset
    for i in range(0, len(df)):
        item = stock.Stock_company()
        item.ts_code = df.iat[i,0]
        item.exchange = df.iat[i,1]
        item.chairman = df.iat[i,2]
        item.manager = df.iat[i,3]
        item.secretary = df.iat[i,4]
        item.re_capital = util.toFloat(df.iat[i,5])
        item.setup_date = df.iat[i,6]
        item.province = df.iat[i,7]
        item.city = df.iat[i,8]
        item.introduction = df.iat[i,9]
        item.website = df.iat[i,10]
        item.email = df.iat[i,11]
        item.office = df.iat[i,12]
        item.employees = util.toInt(df.iat[i,13])
        item.main_business = df.iat[i,14]
        item.business_scope = df.iat[i,15]
        list.append(item)
    return list

def read_cnstock_company():
    pro = get_tushare_api()
    print("reading SZSE company information from tushare.")
    df = pro.stock_company(exchange='SZSE', fields=TUSHARE_COMPNAYFIELDS)
    list = []
    list = __addCompanyList(list, df)
    print("reading SSE company information from tushare.")
    df = pro.stock_company(exchange="SSE",  fields=TUSHARE_COMPNAYFIELDS)
    list = __addCompanyList(list, df)
    return list

def read_cnstock_fina(ts_code_list, end_date_cnstr):
    pro = get_tushare_api()
    list = []
    for ts_code in ts_code_list:
        print("reading %s financial indicators from tushare." %ts_code)
        df = pro.query('fina_indicator', ts_code=ts_code, start_date='20190101', end_date=end_date_cnstr,
                       fields=TUSHARE_FINAFIELDS)
        for i in range(0, len(df)):
            item = stock.Stock_fina()
            item.ts_code = df.iat[i,0]
            item.ann_date = util.date_cn2us(df.iat[i,1])
            item.end_date = util.date_cn2us(df.iat[i,2])
            item.eps = util.toFloat(df.iat[i,3])
            item.dt_eps = util.toFloat(df.iat[i, 4])
            item.total_revenue_ps = util.toFloat(df.iat[i, 5])
            item.revenue_ps = util.toFloat(df.iat[i, 6])
            item.extra_item = util.toFloat(df.iat[i, 7])
            item.profit_dedt = util.toFloat(df.iat[i, 8])
            item.gross_margin = util.toFloat(df.iat[i, 9])
            item.current_ratio = util.toFloat(df.iat[i, 10])
            item.quick_ratio = util.toFloat(df.iat[i, 11])
            item.cash_ratio = util.toFloat(df.iat[i, 12])
            item.assets_turn = util.toFloat(df.iat[i, 13])
            item.interst_income = util.toFloat(df.iat[i, 14])
            item.daa = util.toFloat(df.iat[i, 15])
            item.edit = util.toFloat(df.iat[i, 16])
            item.editda = util.toFloat(df.iat[i, 17])
            item.netdebt = util.toFloat(df.iat[i, 18])
            item.bps = util.toFloat(df.iat[i, 19])
            item.roe = util.toFloat(df.iat[i, 20])
            item.roa = util.toFloat(df.iat[i, 21])
            item.npta = util.toFloat(df.iat[i, 22])
            item.debt_to_assets = util.toFloat(df.iat[i, 23])
            list.append(item)
    return list