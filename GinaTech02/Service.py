import time

import requests
import urllib3

import GinaTech02.Ann as ann
import GinaTech02.Cnstock_dao as cdao
import GinaTech02.Cnstock_odt as codt
import GinaTech02.Cnstock_tushare as ctu
import GinaTech02.Usstock_bean as stk
import GinaTech02.Usstock_dao as dao
import GinaTech02.Usstock_odt as odt
import GinaTech02.Util as util


def insert_symbols_us():
    item_list = odt.get_allsymbol_items()
    st_dao = dao.dao_ussstock_item()
    st_dao.add_ussstock_item(item_list)


#insert all data for us stocks
def insert_alldaily_oneday_us(daystr):
    st_dao = dao.dao_ussstock_item()
    sd_dao = dao.dao_usstock_daily()
    sym_list = st_dao.get_all_symbols()
    done_list = sd_dao.get_smybol_lists(daystr)
    for i in sym_list:
        try:
            if i not in done_list:
                dl = odt.get_onedaily(i, daystr)
                sd_dao.add_itemlist(dl)
                print("inserted %s"%(i+daystr))
            else:
                print("%s already inserted...skipped."%str(i))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

def insert_alldaily_oneday_cn(daystr):
    st_dao = cdao.cnstock_item_dao()
    sd_dao = cdao.cnstock_daily_dao()
    sym_list = st_dao.get_all_tscode()
    done_list = sd_dao.get_existing_symbollist2(daystr)
    for i in range(0, len(sym_list)):
        ts_code = sym_list[i]
        try:
            if i not in done_list:
                daystr = util.date_us2cn()
                dl = ctu.read_cnstock_dailyandbasic(ts_code, trade_date=daystr)
                sd_dao.insert_newlist(dl)
                print("inserted %s" % (i + daystr))
            else:
                print("%s already inserted...skipped." % str(i))
        except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as err:
            print(str(err))
            print("sleeping... 300s")
            time.sleep(300)
            print("retry....")
            i -= 1
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        i+=1

def insert_predictresult_us(list):
    pr_dao = dao.dao_usstock_result()
    pr_dao.add_predict_result(list)

def insert_alldaily_today():
    todaystr = util.get_today_datestr()
    insert_alldaily_oneday_us(todaystr)
    insert_alldaily_oneday_cn(todaystr)

def ann_training_us():
    model = ann.create_gru_model()
    his = ann.train_model_us(model)
    ann.save_model2(model, filename='us_')
    ann.draw_plot(his)
def ann_training_cn():
    model = ann.create_gru_model()
    his = ann.train_model_cn(model)
    ann.save_model2(model, filename='cn_')
    ann.draw_plot(his)

def ann_training_us_wweight(weightfilepath):
    model = ann.create_gru_model()
    model.load_weights(weightfilepath)
    history = ann.train_model_us(model)
    ann.save_model2(model, filename="us")
    ann.draw_plot(history)

def ann_training_cn_wweight(weightfilepath):
    model = ann.create_gru_model()
    model.load_weights(weightfilepath)
    history = ann.train_model_cn(model)
    ann.save_model2(model, filename="cn")
    ann.draw_plot(history)

def get_latestdatefromdaily_us(symbol):
    sd_dao = dao.dao_usstock_daily()
    dt = sd_dao.get_latesttradedate(symbol)
    return dt
def get_latestdatefromdaily_cn(symbol):
    cd_dao = cdao.cnstock_daily_dao()
    dt = cd_dao.get_latesttradedate(symbol)
    return dt

#predict the latest
def ann_predict_us(weightfilepath):
    model = ann.create_gru_model()
    model.load_weights(weightfilepath)
    rs = ann.predict_model_us(model)
    pred = rs[0]
    sym = rs[1]
    list = []
    for i in range(0, len(pred)):
        item = stk.Usstock_annpredict()
        item.symbol = str(sym[i])
        item.trade_date =get_latestdatefromdaily_us(item.symbol)
        item.cal_date = util.get_today_datestr()
        item.result = util.toFloat(pred[i])
        item.comment = "GRU drop 0.4"
        list.append(item)
    insert_predictresult_us(list)

def ann_predict_cn(weightfilepath):
    model = ann.create_gru_model()
    model.load_weights(weightfilepath)
    rs = ann.predict_model_cn(model)
    pred = rs[0]
    sym = rs[1]
    list = []
    for i in range(0, len(pred)):
        item = stk.Usstock_annpredict()
        item.symbol = str(sym[i])
        item.trade_date = get_latestdatefromdaily_cn(item.symbol)
        item.cal_date = util.get_today_datestr()
        item.result = util.toFloat(pred[i])
        item.comment = 'GRU drop 0.4'
        list.append(item)
        insert_predictresult_us(list)

def insert_cnstocklist():
    stocklist = ctu.read_cnstocklist()
    stockdao = cdao.cnstock_item_dao()
    stockdao.insert_newlist(stocklist)

def insert_cnstock_all():
    stockdao = cdao.cnstock_item_dao()
    dailydao = cdao.cnstock_daily_dao()
    stocklist = stockdao.get_all_tscode()
    existinglist = dailydao.get_existing_symbollist()
    for i in range(0, len(stocklist)):
        ts_code = stocklist[i]
        if ts_code not in existinglist:
            ts_code = ts_code.strip()
            print("reading %s from tushare..."%ts_code)
            try:
                list = ctu.read_cnstock_dailyandbasic(ts_code=ts_code, start_date='20140101', end_date='20190712')
                print("insert %s into database..."%ts_code)
                dailydao.insert_newlist(list)
            except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as err:
                print(str(err))
                print("sleeping... 300s")
                time.sleep(300)
                print("retry....")
                i -= 1
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
        i+=1


def insert_cnstock_all_byodt():
    stockdao = cdao.cnstock_item_dao()
    dailydao = cdao.cnstock_daily_dao()
    stocklist = stockdao.get_all_tscode()
    existinglist = dailydao.get_existing_symbollist()
    for i in range(0, len(stocklist)):
        ts_code = stocklist[i]
        if ts_code not in existinglist:
            ts_code = ts_code.strip()
            print("reading %s from opendatatool..."%ts_code)
            list = codt.read_cnstock_daily(ts_code=ts_code, start_date='2014-01-01', end_date='2019-07-12')
            print("insert %s into database..."%ts_code)
            dailydao.insert_newlist(list)
        i+=1
