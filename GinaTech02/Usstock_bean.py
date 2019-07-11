from __future__ import unicode_literals, absolute_import

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()

class Usstock_item(ModelBase):
    __tablename__ = 'data_usstock_list'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(length=45))
    name = Column(String(length=100))
    last_sale = Column(String(length=45))
    market_cap = Column(String(length=45))
    ipo_year = Column(String(length=100))
    sector = Column(String(length=45))
    industry = Column(String(length=100))
    sum_quote = Column(String(length=45))

class Usstock_daily(ModelBase):
    __tablename__ = 'data_usstock_daily'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(length=45))
    trade_date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Float)

class Usstock_tech01(ModelBase):
    __tablename__ = 'cal_usstock_tech01'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(length=45))
    trade_date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    pct_change=Column(Float)
    volume = Column(Float)
    ma5 = Column(Float)
    ma10 = Column(Float)
    ma20 = Column(Float)
    pe = Column(Float)
    obv = Column(Float)
    faststc_pk = Column(Float)
    faststc_dk = Column(Float)
    boll_upper = Column(Float)
    boll_mid = Column(Float)
    boll_lower = Column(Float)
    dmi_pdi = Column(Float)
    dmi_mdi= Column(Float)
    dmi_adx = Column(Float)
    wmsr_wr1 = Column(Float)
    wmsr_wr2 = Column(Float)
    mtm = Column(Float)
    sar = Column(Float)
    pvt = Column(Float)
    turnover_rate = Column(Float)
    volume_ratio = Column(Float)