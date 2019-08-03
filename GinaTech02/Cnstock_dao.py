from sqlalchemy.sql import func

import GinaTech02.Cnstock_bean as stock
import GinaTech02.Usstock_dao as usdao


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
        result = session.query(stock.Stock_daily.ts_code).distinct(stock.Stock_daily.ts_code).filter(
            stock.Stock_daily.trade_date == trade_date).all()
        list = []
        for row in result:
            s = str(row.ts_code)
            s = s.strip()
            list.append(s)
        session.close()
        return list

    def get_turnoverratio_list(self, ts_code):
        session = super().get_session()
        result = session.query(stock.Stock_daily.turnover_rate).filter(stock.Stock_daily.ts_code==ts_code).order_by(stock.Stock_daily.trade_date).all()
        list = []
        for row in result:
            list.append(row.turnover_rate)
        session.close()
        return list

    def get_onestocklists_alldays(self, symbol):
        session = super().get_session()
        result = session.query(stock.Stock_daily).filter(stock.Stock_daily.ts_code==symbol).order_by(stock.Stock_daily.trade_date).all()
        lists = {}
        openl, highl, lowl, closel, volumel = [],[],[],[],[]
        for row in result:
            openl.append(row.open)
            highl.append(row.high)
            lowl.append(row.low)
            closel.append(row.close)
            volumel.append(row.vol)
        lists['open']=openl
        lists['high']=highl
        lists['low']=lowl
        lists['close']=closel
        lists['volume']=volumel
        session.close()
        return lists

    def get_latesttradedate(self, symbol):
        session = super().get_session()
        result = session.query(func.max(stock.Stock_daily.trade_date)).filter(stock.Stock_daily.ts_code==symbol).scalar()
        return result

class dao_cnstock_result(usdao.dao_base):
    def add_predict_result(self, item_list):
        print("   Insert Result...")
        super().add_itemlist(item_list)

class dao_cnstock_company(usdao.dao_base):
    def add_cnstock_company(self, item_list):
        print("  Insert company...")
        super().add_oneItemEachTime(item_list)

class dao_cnstock_fina(usdao.dao_base):
    def add_cnstock_fina(self, item_list):
        print("  Insert financial indicators...")
        super().add_oneItemEachTime(item_list)