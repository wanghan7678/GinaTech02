import GinaTech02.Service as serv
import GinaTech02.Usstock_bean as stk

list = []

item = stk.Usstock_annpredict()
item.symbol = str('PIH')
item.trade_date = '2019-07-31'
item.cal_date = '2019-08-02'
item.result = 0.201436
item.comment = "GRU drop 0.4"
list.append(item)
item = stk.Usstock_annpredict()
item.symbol = str('test')
item.trade_date = '2019-07-31'
item.cal_date = '2019-08-02'
item.result = 0.201436
item.comment = "GRU drop 0.4"
list.append(item)

serv.insert_predictresult_us(list)
