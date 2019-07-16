import GinaTech02.Cnstock_odt as odt

list = odt.read_cnstock_daily('002413.SZ', start_date='2014-04-01', end_date='2014-04-20')

for row in list:
    print(row.trade_date)