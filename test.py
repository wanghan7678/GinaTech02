import yfinance as yf

msft = yf.Ticker("YI")

df = msft.financials

col = df.columns.values
index = df.index.values;

print(type(col))
print(col)
