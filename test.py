import tushare as ts

import GinaTech02.Config as conf

pro = ts.pro_api(conf.CONSTANT.Tushare_Token);


df = pro.query('fina_indicator', ts_code='000002.SZ', start_date='20190101', end_date='20190803')

print(df)

