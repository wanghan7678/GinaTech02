import GinaTech02.Cnstock_tushare as ts
fstr = 'ts_code, employees, main_business, business_scope'
pro = ts.get_tushare_api()
df = pro.stock_company(exchange='SSE', fields=fstr)

print(df.iat[1,0])
print(df.iat[1,1])
print(df.iat[1,2])
print(df.iat[1,3])


