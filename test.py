import yfinance as yf

msft = yf.Ticker("MSFT")

df = msft.financials

col = df.columns.values
index = df.index.values;

print(type(col))
print(col[0])
