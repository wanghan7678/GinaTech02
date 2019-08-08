import GinaTech02.Usstock_odt as odt;

client = odt.get_TiingoClient()

met = client.get_ticker_metadata("AAPL")

#msft = yf.Ticker("AAPL")

#df = msft.financials
print(type(met))
print(met)