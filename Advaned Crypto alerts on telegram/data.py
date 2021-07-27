import os
from datetime import date
from datetime import timedelta
import ccxt
import pandas as pd

days=60
today=date.today()
since=today-timedelta(days = days)

from_datetime = since
from_timestamp = ccxt.binance.parse8601(from_datetime)


with open('symbols.csv') as f:
    lines = f.read().splitlines()
    for symbol in lines:
        print(symbol)
        exchange=ccxt.binance()
        markets=exchange.load_markets()
        kldata=exchange.fetch_ohlcv(symbol+'/USDT','1d',from_timestamp,limit=days)
        data=pd.DataFrame(kldata,columns=['DateTime','Open','High','Low','Close','Volume'])
        data.to_csv("datasets/{}.csv".format(symbol))


