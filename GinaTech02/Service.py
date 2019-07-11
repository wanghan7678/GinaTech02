import numpy as np

import GinaTech02.Ann as ann
import GinaTech02.Config as cfg
import GinaTech02.TechCalculator as tc
import GinaTech02.Usstock_dao as dao
import GinaTech02.Usstock_odt as odt
import GinaTech02.Util as util


def insert_symbols():
    item_list = odt.get_allsymbol_items()
    st_dao = dao.dao_ussstock_item()
    st_dao.add_ussstock_item(item_list)


def insert_all_daily():
    st_dao = dao.dao_ussstock_item()
    sd_dao = dao.dao_usstock_daily()
    sym_list = st_dao.get_all_symbols()
    done_list = sd_dao.get_smybol_lists("2019-07-05")
    for i in sym_list:
        try:
            if i not in done_list:
                dl = odt.get_daily_bysymbol(i)
                sd_dao.add_itemlist(dl)
            else:
                print("%s already inserted...skipped." %str(i))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

def insert_alldaily_oneday(daystr):
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


def insert_alldaily_today():
    todaystr = util.get_today_datestr()
    insert_alldaily_oneday(todaystr)

def cal_tech(symbol):
    sd_dao = dao.dao_usstock_daily()
    datalists = sd_dao.get_onestocklists_alldays(symbol)
    openl=datalists['open']
    closel=datalists['close']
    highl=datalists['high']
    lowl=datalists['low']
    voll=datalists['volume']
    r = len(openl) - 1
    cal = tc.Tech_Calculator()
    cal.set_dailydata(openl=openl,closel=closel,highl=highl,lowl=lowl,voll=voll)
    rs = cal.get_SMA(5)
    print(r)
    print(rs[r-100:r])

    openl = np.delete(openl, r)
    closel = np.delete(closel, r)
    highl = np.delete(highl, r)
    lowl = np.delete(lowl, r)
    voll = np.delete(voll, r)
    r = len(openl) - 1

    cal = tc.Tech_Calculator()
    cal.set_dailydata(openl=openl, closel=closel, highl=highl, lowl=lowl, voll=voll)
    rs = cal.get_SMA(5)
    print(rs[r-100:r])

def ann_training():
    model = ann.create_gru_model()
    his = ann.train_model(model)
    ann.save_model(model)
    ann.draw_plot(his)

#predict the latest
def ann_predict():
    model = ann.create_gru_model()
    model.load_weights(cfg.CONSTANT.WEIGHTS_FILEPATH)
    rs = ann.predict_model(model)