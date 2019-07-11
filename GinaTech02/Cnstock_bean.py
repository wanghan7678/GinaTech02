from __future__ import unicode_literals, absolute_import

from sqlalchemy import Column, Integer, String, DateTime
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
