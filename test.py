import GinaTech02.DataGenerator as dg

'''
stockdaily = dbo.dao_usstock_daily()

stockcal = cal.usstock_calresult('AAPL')
dict = stockdaily.get_onestocklists_alldays('AAPL')
stockcal.read_data(dict)
stockcal.cal_indicators()
'''

dg = dg.val_gen
i=0
for samples, targets in dg:
    print("iteration: %d"%i)
    print("samples shape: %s" %str(samples.shape))
    i+=1