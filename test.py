import tushare as tu

import GinaTech02.Config as cfg
import GinaTech02.Util as ut

pro = tu.pro_api(cfg.CONSTANT.Tushare_Token)

st_date = ut.to_cndate("20190701")
df = pro.daily_basic(ts_code='000002.SZ', start_date=st_date, end_date='20190712')

print(df)