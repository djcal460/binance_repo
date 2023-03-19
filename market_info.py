import pandas as pd
# Permanently changes the pandas settings
pd.set_option('display.max_columns', 15)


class MarketInfo:
    def __init__(self, client):
        self.client = client

    def get_ticker_info(self, tradepair):
        return self.client.get_symbol_ticker(symbol=tradepair)

    def get_avg_price(self, tradepair):
        return self.client.get_avg_price(symbol=tradepair)

    def get_price_usdt(self, ticker):
        return self.client.get_avg_price(symbol=ticker + "USDT")["price"]

    def get_all_prices(self):
        prices = self.client.get_all_tickers()
        prices_df = pd.DataFrame(prices)
        return prices_df

    def get_all_sym_pairs(self,ticker):
        prices = self.client.get_all_tickers()
        prices_df = pd.DataFrame(prices)
        ticker_pairs = prices_df[prices_df.symbol.str.contains(ticker)]
        return ticker_pairs

    #get all stable pairs
    def get_all_stable_pairs(self, ticker1, other_stables=["USD", "DAI", "FRAX", "FEI", "VAI", "RSV", "DJED"]):
        prices = self.client.get_all_tickers()
        prices_df = pd.DataFrame(prices)
        pairs = pd.DataFrame()
        for stable in other_stables:
            df = prices_df[prices_df.symbol.str.contains(ticker1) & prices_df.symbol.str.contains(stable)]
            pairs = pd.concat([pairs, df])
        return pairs

    def get_24h_data(self, tradepair):
        last24 = self.client.get_ticker(symbol=tradepair)
        open_time = pd.to_datetime(last24["openTime"], unit="ms")
        close_time = pd.to_datetime(last24["closeTime"], unit="ms")
        open_price = float(last24["openPrice"])
        high_price = float(last24["highPrice"])
        low_price = float(last24["lowPrice"])
        close_price = float(last24["lastPrice"])
        price_difference = close_price - open_price
        percent_difference = (close_price / open_price - 1) * 100
        last24_data = { "open_time":open_time,"close_time":close_time,"open_price":open_price,"high_price": high_price, \
                        "low_price":low_price,"close_price":close_price,"price_difference":price_difference,"percent_difference":percent_difference }
        return last24_data
