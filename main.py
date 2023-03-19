import pandas as pd
from tabulate import tabulate
import account as ac
from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request

kline_intervals = {"1MINUTE": '1m', "3MINUTE": '3m', "5MINUTE": '5m',
                   "15MINUTE": '15m', "30MINUTE": '30m', "1HOUR": '1h', "2HOUR": '2h',
                   "4HOUR": '4h', "6HOUR": '6h', "8HOUR": '8h', "12HOUR": '12h',
                   "1DAY": '1d', "3DAY": '3d', "1WEEK": '1w', "1MONTH": '1M'}


def time_ago(weeks=None, days=None, hours=None, minutes=None, seconds=None):
    now = datetime.utcnow()
    if weeks is not None:
        return str(now - timedelta(weeks=weeks))
    elif days is not None:
        return str(now - timedelta(days=days))
    elif hours is not None:
        return str(now - timedelta(hours=hours))
    elif minutes is not None:
        return str(now - timedelta(minutes=minutes))
    elif seconds is not None:
        return str(now - timedelta(seconds=seconds))
    else:
        return str(now)


# app = Flask(__name__)
api_key = os.environ.get("binance_read_api_key")
secret_key = os.environ.get("binance_read_secret_key")
account = ac.Account(api_key, secret_key)

def main():
    """
    GET ACCOUNT INFO
    """
    # create account info object
    account_info = account.account_info

    # get crypto balances df
    balances = account_info.get_balances()
    print("All balances: ")
    print(balances, "\n")

    # get specific balance
    eth_balance = account_info.get_balance("ETH")
    print("ETH balances: ")
    print(eth_balance, "\n")

    # get account snapshot
    snap, snap_balances = account_info.get_snapshot("SPOT")
    print("Your account snapshot: ", "\n")
    print(snap, "\n")
    print("Your account snapshot balances: ", "\n")
    print(snap_balances, "\n")

    # get exchange info
    exchange_info = account_info.get_rate_limits()
    print("Your rate limit: ")
    print(tabulate(exchange_info, headers='keys'), "\n")

    # get all account coin info
    coins = account_info.get_all_coin_info()
    print("All coin info: ")
    print(coins, "\n")
    #
    # get coin info
    coin_info = account_info.get_coin_info("ETH")
    print("Your account info on ETH :")
    print(coin_info, "\n")

    # get trade fee
    trade_fee = account_info.get_trade_fee("BTCUSDT")
    print("Trade fee for BTCUSDT: ")
    print(trade_fee, "\n")

    # get trading pair info
    trading_pair_info = account_info.get_trade_pair_info("BTCUSDT")
    print("Trade pair info for BTCUSDT: ")
    print(trading_pair_info, "\n")

    """
    GET MARKET INFO
    """
    market_info = account.market_info

    # get any trade pair info
    btcusdt_info = market_info.get_ticker_info("BTCUSDT")
    print("BTCUSDT INFO: ")
    print(btcusdt_info, "\n")

    # get price usdt
    ethusdt_price = market_info.get_price_usdt("ETH")
    print("ETHUSDT PRICE: ")
    print(ethusdt_price, '\n')

    # get all prices
    all_prices = market_info.get_all_prices()
    print("ALL PRICES: ")
    print(all_prices, '\n')

    # get all pairs
    all_eth_pairs = market_info.get_all_sym_pairs("ETH")
    print("ALL ETH PAIRS: ")
    print(all_eth_pairs, "\n")

    # get all stable pairs with USD in name, can pass in own list of stables
    all_stable_ada_pairs = market_info.get_all_stable_pairs("BTC")
    print(all_stable_ada_pairs, "\n")

    # set open time
    last24_data = market_info.get_24h_data("BTCUSDT")
    print(last24_data)
    data = pd.DataFrame({'name': last24_data.keys(), 'value': last24_data.values()})
    data.set_index('name', inplace=True)
    print(data, "\n")

    """
    HISTORICAL DATA
    """
    historical_data = account.historical_data

    # get the earliest historical data for a pair
    timestamp = historical_data.get_earliest_timestamp("BTCUSDT")
    print("Earliest available data for BTCUSDT: ")
    print(timestamp, "\n")

    # get historical data in df (date format = 2023-03-18 03:00:00)
    btcusdt_daily = historical_data.get_historical_data("BTCUSDT", kline_intervals['1DAY'], "2023-03-15 03:00:00")
    print(btcusdt_daily)

    # get time ago to get historical data
    start_time = time_ago(weeks=4)

    print(start_time)
    btcusdt_4_weeks_ago = historical_data.get_historical_data("BTCUSDT", kline_intervals['1WEEK'], start_time)
    print(btcusdt_4_weeks_ago)

    # Get a local file downloaded from binance
    local_data = historical_data.get_historical_from_file(r"./BTCUSDT-1h-2023-02.csv")
    print(local_data)

    """
    STREAMING DATA
    """
    test_stream = True
    if test_stream:
        streambtc = account.streaming
        streambtc.start_stream("BTCUSDT")
        streambtc.stop_stream(10)





# #Define Flask routes
# @app.route('/account/balances')
# def get_account_balances():
#     balances = account.account_info.get_balances()
#     return balances.to_json()
#
# @app.route('/account/balance/<string:ticker>')
# def get_account_balance(ticker):
#     balance = account.account_info.get_balance(ticker)
#     return jsonify(balance)
#
# @app.route('/account/snapshot/<string:account_type>')
# def get_account_snapshot(account_type):
#     snap, balances = account.account_info.get_snapshot(account_type)
#     return snap.to_json()
#
# @app.route('/account/rate_limits')
# def get_rate_limits():
#     rate_limits = account.account_info.get_rate_limits()
#     return jsonify(rate_limits)
#
# @app.route('/account/coins')
# def get_all_coin_info():
#     coins = account.account_info.get_all_coin_info()
#     return coins.to_json()
#
# @app.route('/account/coin_info/<string:ticker>')
# def get_coin_info(ticker):
#     coin_info = account.account_info.get_coin_info(ticker)
#     return coin_info.to_json()
#
# @app.route('/account/trade_fee/<string:tradepair>')
# def get_trade_fee(tradepair):
#     trade_fee = account.account_info.get_trade_fee(tradepair)
#     return trade_fee
#
# @app.route('/account/trade_pair_info/<string:tradepair>')
# def get_trade_pair_info(tradepair):
#     tradepair_info = account.account_info.get_trade_pair_info(tradepair)
#     return tradepair_info.to_json()
#
# @app.route('/market/ticker_info/<string:tradepair>')
# def get_ticker_info(tradepair):
#     ticker_info = account.market_info.get_ticker_info(tradepair)
#     return ticker_info
#
# @app.route('/market/avg_price/<string:tradepair>')
# def get_avg_price(tradepair):
#     avg_price = account.market_info.get_avg_price(tradepair)
#     return jsonify(avg_price)
#
# @app.route('/market/price_usdt/<string:ticker>')
# def get_price_usdt(ticker):
#     price_usdt = account.market_info.get_price_usdt(ticker)
#     return jsonify(price_usdt)
#
# @app.route('/market/all_prices')
# def get_all_prices():
#     all_prices = account.market_info.get_all_prices()
#     return all_prices.to_json()
#
# @app.route('/market/all_sym_pairs/<string:ticker>')
# def get_all_sym_pairs(ticker):
#     all_sym_pairs = account.market_info.get_all_sym_pairs(ticker)
#     return all_sym_pairs.to_json()
#
# @app.route('/market/all_stable_pairs/<string:ticker1>')
# def get_all_stable_pairs(ticker1):
#     all_stable_pairs = account.market_info.get_all_stable_pairs(ticker1)
#     return all_stable_pairs.to_json()
#
# @app.route('/market/24h_data/<string:tradepair>')
# def get_24h_data(tradepair):
#     data = account.market_info.get_24h_data(tradepair)
#     return jsonify(data)
#
# @app.route('/api/historicaldata', methods=['GET'])
# def get_historical_data():
#     tradepair = request.args.get('tradepair')
#     interval = request.args.get('interval')
#     start_date = request.args.get('start_date')
#     end_date = request.args.get('end_date')
#     historical_data_df = account.historical_data.get_historical_data(tradepair, interval, start_date, end_date)
#     historical_data_df.to_html()
#     return historical_data_df.to_html()
#
# # Get historical data from a local file
# @app.route('/api/historicaldata/from_file', methods=['GET'])
# def get_historical_data_from_file():
#     path = request.args.get('path')
#     historical_data_df = account.historical_data.get_historical_from_file(path)
#     return jsonify(historical_data_df.to_dict())




if __name__ == "__main__":
    main()
    # app.run(debug=True)
