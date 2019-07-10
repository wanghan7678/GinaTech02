import yfinance as yf
from tiingo import TiingoClient
import GinaTech02.Config as cfg
import GinaTech02.DataGenerator as dg
import GinaTech02.Usstock_cal as cal
import GinaTech02.Usstock_dao as dbo
'''
stockdaily = dbo.dao_usstock_daily()

stockcal = cal.usstock_calresult('AAPL')
dict = stockdaily.get_onestocklists_alldays('AAPL')
stockcal.read_data(dict)
stockcal.cal_indicators()
'''

dg = dg.data_generator(0,4000)
i=0
for samples, targets in dg:
    print("iteration: %d"%i)
    i+=1