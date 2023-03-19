import pandas as pd
from flask import Flask, jsonify
# Permanently changes the pandas settings
pd.set_option('display.max_columns', 15)


class AccountInfo:
    def __init__(self, client):
        self.client = client
        self.account = client.get_account()
        self.balances = client.get_account()["balances"]
        self.coins = pd.DataFrame(client.get_all_coins_info())

    def get_balances(self):
        # create balances as df
        balances = pd.DataFrame(self.balances)
        balances.free = pd.to_numeric(balances.free, errors="coerce")
        balances.locked = pd.to_numeric(balances.locked, errors="coerce")
        return balances.loc[balances.free > 0]

    def get_balance(self, ticker):
        return self.client.get_asset_balance(asset=ticker)['free']

    def get_snapshot(self, account_type):
        snap = self.client.get_account_snapshot(type=account_type)
        snap = pd.json_normalize(snap['snapshotVos'])
        snap.updateTime = pd.to_datetime(snap["updateTime"], unit="ms")
        return snap, snap["data.balances"][0]

    def get_rate_limits(self):
        return self.client.get_exchange_info()["rateLimits"]

    def get_all_coin_info(self):
        return self.coins

    def get_coin_info(self, ticker):
        return self.coins.loc[self.coins.coin == ticker]

    def get_trade_fee(self, tradepair):
        fee = self.client.get_trade_fee(symbol=tradepair)
        return fee

    def get_trade_pair_info(self, tradepair):
        tradepair_info = self.client.get_symbol_info(symbol=tradepair)
        return tradepair_info


