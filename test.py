import yfinance as yf


print(yf.Ticker('MSFT').info['currentPrice'])