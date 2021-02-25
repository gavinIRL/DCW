import os
import subprocess
from datetime import datetime
import json
import requests

# This is the class that contains the workhorse methods


class DCWUtils():

    def __init__(self, exchange):
        self.exchange = exchange
        if self.exchange == "Binance":
            self.url_base = "d"
            self.update_rate = 1000
        elif self.exchange == "Bitfinex":
            self.url_base = "https://api-pub.bitfinex.com/v2/"
            self.update_rate = 1000
        else:
            print("Only Bitfinex and Binance supported so far")

    def call_api(self, suffix, raw=False):
        url = self.url_base + suffix
        data = json.loads(requests.request("GET", url).text)
        if raw:
            return data
        pass

    @staticmethod
    def convert_ms_to_datetime(ms):
        return datetime.fromtimestamp(ms).strftime("%Y-%m-%d %I:%M:%S")

    def create_suffix(self, currency="BTC", base="USD", data_type="Candle", custom_time=False, custom_limit=False):
        if self.exchange == "Binance":
            pass
        if self.exchange == "Bitfinex":
            pass

    def get_coin_list(self, raw=False):
        pass

    def get_coin_candle(self, suffix, raw=False):
        pass

    def get_net_worth(self, currency_list):
        pass

    @staticmethod
    def get_wallet():
        pass

    @staticmethod
    def set_wallet(currency_list):
        pass

    @staticmethod
    def checkSettingsFileExists():
        # check if file exists
        if os.path.isfile("settings.cfg"):
            # Need to check if the file is valid first
            # If valid then return setup complete
            return True
            # Otherwise return invalid settings file
        else:
            return False
