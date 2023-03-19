import pandas as pd

# Permanently changes the pandas settings
pd.set_option('display.max_columns', 15)


class HistoricalData:
    def __init__(self, client):
        self.client = client

    def get_earliest_timestamp(self, tradepair):
        return

    def get_historical_data(self, tradepair, interval, start_date=None, end_date=None):
        # Get and print earliest timestamp for tradepair
        if start_date is None:
            start_date = self.client._get_earliest_valid_timestamp(symbol=tradepair, interval=interval)

        # get historical data and save as df
        bars = self.client.get_historical_klines(symbol=tradepair, interval=interval, start_str=start_date, end_str=end_date, limit=1000)
        historical_data = pd.DataFrame(bars)
        historical_data["Date"] = pd.to_datetime(historical_data.iloc[:, 0], unit="ms")
        historical_data.columns = ["Open Time", "Open", "High", "Low", "Close",
                                   "Volume", "Close Time", "Quote Asset Volume",
                                   "Number of Trades", "Taker Buy Base Asset Volume",
                                   "Taker Buy Quote Asset Volume", "Ignore", "Date"]
        historical_data = historical_data[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
        historical_data.set_index("Date", inplace=True)
        for column in historical_data.columns:
            historical_data[column] = pd.to_numeric(historical_data[column], errors="coerce")
        return historical_data

    def get_historical_from_file(self, path):
        url = path
        df = pd.read_csv(path, header=None)
        df["Date"] = pd.to_datetime(df.iloc[:, 0], unit="ms")
        df.columns = ["Open Time", "Open", "High", "Low", "Close", "Volume",
                      "Clos Time", "Quote Asset Volume", "Number of Trades",
                      "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore", "Date"]
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
        df.set_index("Date", inplace=True)
        return df
