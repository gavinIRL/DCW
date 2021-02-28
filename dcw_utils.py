import os
import datetime
import json
import requests
import numpy as np
import pandas as pd
import numba as nb
import time
from requests.exceptions import HTTPError

# This is the class that contains the workhorse functions
# I admit it is a really confused class, over 50% static methods


class DCWUtils():

    def __init__(self, exchange="Bitfinex", wallet=None):
        self.exchange = exchange
        self.wallet = wallet
        if self.exchange == "Binance":
            self.url_base = "https://api.binance.com/api/v3/"
            # Actually 1000 weight/minute but better to use a slower pace
            self.update_rate = 1000
        elif self.exchange == "Bitfinex":
            self.url_base = "https://api-pub.bitfinex.com/v2/"
            self.update_rate = 1000
        else:
            print("Only Bitfinex and Binance supported so far")

    def request_api(self, suffix):
        url = self.url_base + suffix
        try:
            response = requests.request("GET", url)
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 404:
                print("Incorrect input, got 404'd")
                return False
            elif response.status_code == 429 or response.status_code == 418:
                wait_seconds = int(response.headers["Retry-After"])
                print("Making too many requests, on the naughty step for " +
                      str(wait_seconds)+" seconds")
                time.sleep(wait_seconds)
                return False
            else:
                print(response.status_code)
                return False
        # This is to catch in case the above raises errors rather than returning codes
        except HTTPError as err:
            if err.code == 404:
                print("Incorrect input, got 404'd")
                return False
            elif err.code == 429 or err.code == 418:
                wait_seconds = int(response.headers["Retry-After"])
                print("Making too many requests, on the naughty step for " +
                      str(wait_seconds)+" seconds")
                time.sleep(wait_seconds)
                return False
            else:
                print(err.code)
                return False

    def calculate_RSI(closelist, alpha=14):
        # Calculate the SMMA and then RSI given a sequence of closes
        pass

    @staticmethod
    def convert_ms_to_datetime(ms: int):
        base_datetime = datetime.datetime(1970, 1, 1)
        delta = datetime.timedelta(0, 0, 0, ms)
        target_date = base_datetime + delta
        return target_date

    @staticmethod
    def create_suffix_bitfinex(currency="BTC", base="USD", data_type="Candle", custom_time=False, custom_limit=False):
        pass

    @staticmethod
    def create_suffix_binance(currency="BTC", base="USDT", data_type="Candle", custom_time=False, custom_limit=False):
        pass

    def get_coin_list(self, raw=False):
        if self.exchange == "Binance":
            data = self.create_suffix_binance()
            # Need to only send back the pairs that contain USD
        elif self.exchange == "Bitfinex":
            return self.request_api()
        else:
            return False

    def get_tick(self, pair, return_data="CHL"):
        if self.exchange == "Binance":
            data = self.request_api("ticker/price?symbol="+pair)
            return str(data["price"]).strip("0")

    def get_coin_candle(self, currency="BTC", base="USDT", interval="15m", limit=10, target=False, include_time=True, time_ms=False):
        if self.exchange == "Binance":
            data = self.request_api(
                "klines?symbol="+currency+base+"&interval="+interval+"&limit="+str(limit))
            # This will simply return the raw data
            if not target:
                return data
            # Otherwise return the requested data
            return_data = []
            return_time_data = []
            for timepoint in data:
                if include_time:
                    return_time_data.append(timepoint[0])
                if target == "Open Time":
                    # This gets sent back anyway if include_time is true
                    continue
                elif target == "Open":
                    return_data.append(timepoint[1])
                elif target == "High":
                    return_data.append(timepoint[2])
                elif target == "Low":
                    return_data.append(timepoint[3])
                elif target == "Close":
                    return_data.append(timepoint[4])
                elif target == "Volume":
                    return_data.append(timepoint[5])
                elif target == "Close Time":
                    return_data.append(timepoint[6])
                elif target == "Quote Asset Volume":
                    return_data.append(timepoint[7])
                elif target == "Number of Trades":
                    return_data.append(timepoint[8])
                else:
                    # Incorrect target provided
                    return False
            if not include_time:
                return return_data
            else:
                # Convert times to datetime objects if milliseconds is false
                if not time_ms:
                    for i, entry in enumerate(return_time_data):
                        return_time_data[i] = self.convert_ms_to_datetime(
                            entry)
                return list(zip(return_time_data, return_data))
        elif self.exchange == "Bitfinex":
            return self.create_suffix_bitfinex()
        else:
            return False

    def get_net_worth(self, currency_list):
        pass

    @staticmethod
    def get_wallet():
        pass

    @staticmethod
    def set_wallet(currency_list):
        pass

    @nb.jit(fastmath=True, nopython=True)
    def calculate_rsi(list, deltas, avg_gain, avg_loss, n):

        # Use Wilder smoothing method
        def up(x): return x if x > 0 else 0
        def down(x): return -x if x < 0 else 0
        i = n+1
        for d in deltas[n+1:]:
            avg_gain = ((avg_gain * (n-1)) + up(d)) / n
            avg_loss = ((avg_loss * (n-1)) + down(d)) / n
            if avg_loss != 0:
                rs = avg_gain / avg_loss
                list[i] = 100 - (100 / (1 + rs))
            else:
                list[i] = 100
            i += 1

        return list

    def get_rsi(list, n=14):

        deltas = np.append([0], np.diff(list))

        avg_gain = np.sum(deltas[1:n+1].clip(min=0)) / n
        avg_loss = -np.sum(deltas[1:n+1].clip(max=0)) / n

        list = np.empty(deltas.shape[0])
        list.fill(np.nan)
        list = DCWUtils.calculate_rsi(list, deltas, avg_gain, avg_loss, n)
        # Now remove the NaN's when returning
        list = list[~np.isnan(list)]
        return list

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


if __name__ == "__main__":
    # playground for testing
    dcw = DCWUtils("Binance")
    #print(dcw.request_api("candles/trade:1m:tBTCUSD/hist?limit=10", True))
    #output = dcw.get_coin_candle(target="High")
    # for line in output:
    #    print(line)
    # result = DCWUtils.get_rsi([100, 120, 130, 125, 128, 116,
    #                            104, 98, 87, 88, 90, 95, 99], n=6)
    # print(result)
