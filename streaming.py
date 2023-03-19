import time

import pandas as pd
from binance import ThreadedWebsocketManager
pd.set_option('display.max_columns', 15)



def stream_data(msg):
    ''' define how to process incoming WebSocket messages '''
    tradetime = pd.to_datetime(msg["E"], unit="ms")
    price = msg["c"]
    print("Time: {} | Price: {}".format(tradetime, price))

class Streaming:
    def __init__(self, client):
        self.client = client
        self.twm = ThreadedWebsocketManager()

    def start_stream(self, tradepair):
        self.twm.start()
        self.twm.start_symbol_miniticker_socket(callback=stream_data, symbol=tradepair)

    def stop_stream(self, seconds):
        time.sleep(seconds)
        self.twm.stop()



