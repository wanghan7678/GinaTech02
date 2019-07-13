import numpy as np

import GinaTech02.Cnstock_bean as stock
import GinaTech02.Usstock_dao as usdao
import GinaTech02.Util as util


class cnstock_item_dao(usdao.dao_base):

    def get_all_tscode(self):
        session = super().get_session()
        result = session.query(stock.Stock_item.ts_code).filter(stock.Stock_item.list_status=='L').all()
        list = []
        for row in result:
            list.append(row.ts_code)
        session.close()
        return list

    def insert_newlist(self, obj_list):
        stocklist = obj_list
        print("insert chinese stock list...")
        super().add_itemlist(stocklist)


class cnstock_daily_dao(usdao.dao_base):
    def insert_newlist(self, obj_list):
        list = obj_list
        print("insert chinese stock daily and basic data into database....")
        super().add_itemlist(list)

    def get_existing_symbollist(self):
        session = super().get_session()
        result = session.query(stock.Stock_daily.ts_code).distinct(stock.Stock_daily.ts_code).all()
        list = []
        for row in result:
            list.append(row.ts_code)
        session.close()
        return list

    def get_existing_symbollist2(self, trade_date):
        session = super().get_session()
        result = session.query(stock.Stock_daily).distinct(stock.Stock_daily.symbol).filter(
            stock.Stock_daily.trade_date == trade_date).all()
        list = []
        for row in result:
            s = str(row.symbol)
            s = s.strip()
            list.append(s)
        session.close()
        return list

    def get_turnoverratio_list(self, ts_code):
        session = super().get_session()
        result = session.query(stock.Stock_daily.turnover_rate).filter(stock.Stock_daily.ts_code==ts_code).order_by(stock.Stock_daily.trade_date).all()
        list = np.zeros(len(result), dtype=float)
        for i in range(0, len(result)):
            list[i] = util.toFloat(result.iat[i,0])
        session.close()
        return list

    def get_onestocklists_alldays(self, symbol):
        session = super().get_session()
        result = session.query(stock.Stock_daily).filter(stock.Stock_daily.symbol==symbol).order_by(stock.Stock_daily.trade_date).all()
        lists = {}
        openl, highl, lowl, closel, volumel = [],[],[],[],[]
        for row in result:
            openl.append(row.open)
            highl.append(row.high)
            lowl.append(row.low)
            closel.append(row.close)
            volumel.append(row.volume)
        lists['open']=openl
        lists['high']=highl
        lists['low']=lowl
        lists['close']=closel
        lists['volume']=volumel
        session.close()
        return lists
