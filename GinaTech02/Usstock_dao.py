import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import GinaTech02.Config as cf
import GinaTech02.Usstock_bean as stock


class dao_base(object):
    def get_session(self):
        engine = sqlalchemy.create_engine(cf.CONSTANT.Database_Url2, poolclass=sqlalchemy.pool.NullPool,echo=False)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session

    def add_itemlist(self, item_list):
        session = self.get_session()
        if item_list is None:
            print("input list is None")
            session.close()
            return
        for item in item_list:
            session.add(item)
        try:
            session.commit()
        except Exception as err:
            print("add_item list integrity error")
            print("Duplicated item....skipped.        "+str(err))
        else:
            print("insert data...")
        finally:
            print("close sql session")
            session.close()

    def add_oneItemEachTime(self, item_list):
        for item in item_list:
            ls = [item]
            self.add_itemlist(ls)


class dao_ussstock_item(dao_base):

    def add_ussstock_item(self, item_list):
        print("Insert Us Stock Items...")
        super().add_itemlist(item_list)
        print("Finished the insert")

    def get_all_symbols(self):
        session = super().get_session()
        result = session.query(stock.Usstock_item.symbol).all()
        list = []
        for row in result:
            st = str(row.symbol).strip()
            list.append(st)
        session.close()
        return list
    def get_all_item(self):
        session = super().get_session()
        result = session.query(stock.Usstock_item).all()
        list = []
        for row in result:
            item = stock.Usstock_item()
            item.symbol = row.symbol
            item.name = row.name
            item.last_sale = row.last_sale
            item.market_cap = row.market_cap
            item.ipo_year = row.ipo_year
            item.sector = row.sector
            item.industry = row.industry
            item.sum_quote = row.sum_quote
            list.append(item)
        session.close()
        return list
    def get_marketcap(self, symbol):
        session = super().get_session()
        result = session.query(stock.Usstock_item.market_cap).filter(stock.Usstock_item.symbol==symbol).all()
        rs = ''
        for row in result:
            rs = row.market_cap
        session.close()
        return rs



class dao_usstock_daily(dao_base):
    def add_ussstock_item(self, item_list):
        print("  Insert Us Stock daily data....")
        super().add_itemlist(item_list)

    def get_smybol_lists(self, trade_date):
        session=super().get_session()
        result = session.query(stock.Usstock_daily).distinct(stock.Usstock_daily.symbol).filter(stock.Usstock_daily.trade_date==trade_date).all()
        list=[]
        for row in result:
            s= str(row.symbol)
            s = s.strip()
            list.append(s)
        session.close()
        return list

    def get_onestocklists_alldays(self, symbol):
        session = super().get_session()
        result = session.query(stock.Usstock_daily).filter(stock.Usstock_daily.symbol==symbol).order_by(stock.Usstock_daily.trade_date).all()
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

    def get_allsmybollists(self):
        session = super().get_session()
        result = session.query(stock.Usstock_daily).distinct(stock.Usstock_daily.symbol)
        list = []
        for row in result:
            list.append(row.symbol)
        session.close()
        return list

    def get_latesttradedate(self,symbol):
        session = super().get_session()
        result = session.query(func.max(stock.Usstock_daily.trade_date)).filter(stock.Usstock_daily.symbol==symbol).scalar()
        return result

class dao_usstock_result(dao_base):
    def add_predict_result(self, item_list):
        print("   Insert Result...")
        super().add_itemlist(item_list)


class dao_usstock_company(dao_base):
    def add_usstock_company(self, item_list):
        print("   Insert Company Info...")
        super().add_itemlist(item_list)

class dao_usstock_fina(dao_base):
    def add_usstock_fina(self, item_list):
        print("   Insert company fina...")
        super().add_itemlist(item_list)

    def get_allsymbollist(self):
        session = super().get_session()
        result = session.query(stock.Usstock_fina).distinct(stock.Usstock_fina.symbol)
        list = []
        for row in result:
            list.append(row.symbol)
        session.close()
        return list