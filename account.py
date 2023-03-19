from binance.client import Client
import account_info as ac
import market_info as mi
import historical_data as hd
import streaming as sm


class Account:
    def __init__(self, api_key, secret_key):
        self.client = Client(api_key=api_key, api_secret=secret_key, tld="com")
        self.account_info = ac.AccountInfo(self.client)
        self.market_info = mi.MarketInfo(self.client)
        self.historical_data = hd.HistoricalData(self.client)
        self.streaming = sm.Streaming(self.client)

