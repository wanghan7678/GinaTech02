from __future__ import unicode_literals, absolute_import

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()

class Stock_item(ModelBase):
    __tablename__ = 'data_cnstock_list'
    id = Column(Integer, primary_key=True)
    ts_code =Column(String(length=45))
    name = Column(String(length=45))
    area = Column(String(length=45))
    industry = Column(String(length=45))
    enname = Column(String(length=100))
    market = Column(String(length=45))
    exchange = Column(String(length=45))
    list_status = Column(String(length=45))
    list_date=Column(DateTime)
    is_hs = Column(String(length=45))
    __table_args__={"mysql_charset":"utf8mb4"}


class Stock_daily(ModelBase):
    __tablename__ = 'data_cnstock_daily'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=45))
    trade_date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    pct_chg = Column(Float)
    vol = Column(Float)
    turnover_rate = Column(Float)
    volume_ratio = Column(Float)
    pe = Column(Float)

class Stock_predict(ModelBase):
    __tablename__='ann_predict_cn'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(length=45))
    trade_date=Column(DateTime)
    cal_date=Column(DateTime)
    result = Column(Float)
    comment = Column(String(length=45))

class Stock_company(ModelBase):
    __tablename__ = 'data_cnstock_company'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=45))
    exchange = Column(String(length=45))
    chairman = Column(String(length=45))
    manager = Column(String(length=45))
    secretary = Column(String(length=45))
    re_capital = Column(Float)
    setup_date = Column(DateTime)
    province = Column(String(length=45))
    city = Column(String(length=45))
    introduction = Column(String(length=500))
    website = Column(String(length=100))
    email = Column(String(length=200))
    office = Column(String(length=200))
    employees = Column(Integer)
    main_business = Column(String(length=400))
    business_scope = Column(String(length=400))

class Stock_fina(ModelBase):
    __tablename__ = 'data_cnstock_fina'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=45))
    ann_date = Column(DateTime)
    end_date = Column(DateTime)
    eps = Column(Float)
    dt_eps = Column(Float)
    total_revenue_ps = Column(Float)
    revenue_ps = Column(Float)
    extra_item = Column(Float)
    profit_dedt = Column(Float)
    gross_margin = Column(Float)
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    cash_ratio = Column(Float)
    assets_turn = Column(Float)
    interst_income = Column(Float)
    daa = Column(Float)
    edit = Column(Float)
    editda = Column(Float)
    netdebt = Column(Float)
    bps = Column(Float)
    roe = Column(Float)
    roa = Column(Float)
    npta = Column(Float)
    debt_to_assets = Column(Float)