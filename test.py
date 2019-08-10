import yfinance as yf

msft = yf.Ticker("AAPL")

df = msft.balance_sheet

col = df.columns.values
index = df.index.values;

print(col)
print(index)

print(df.shape)

print(df)