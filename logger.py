# This is meant as a standalone logging script for creating bot training datasets
# To-do list:
# 3) Need to store values for calculating rsi(14) for 1hr and everything below that
# 4) The final csv file format should be as follows:
# time ms, price, ma(50)5m, ma(50)1h, rsi(6)5m, rsi(6)1h, rsi(14)5m, rsi(14)1h
# 5) Potentially update the format to include more information later
from dcw_utils import DCWUtils
import time
import datetime
import os
from requests.exceptions import HTTPError
import json
import requests
import talib as ta
import numpy as np


class StandaloneLogger():
    def __init__(self):
        self.market_currency_list = [
            "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
            "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "EOSUSDT", "TRXUSDT"]
        self.log_loop_tracker = 0
        self.buffer_counter = 1
        self.fresh_prices = []
        for curr in self.market_currency_list:
            self.fresh_prices.append(1.2)
        self.last_50_closes_5min = []
        self.last_50_closes_1hr = []

    def get_tick_logger(self, pair=False):
        if isinstance(pair, str):
            data = self.request_api_logger("ticker/price?symbol="+pair)
            return str(data["price"]).strip("0")
        elif isinstance(pair, list):
            data = self.request_api_logger("ticker/price")
            return_data = {}
            for entry in data:
                if entry["symbol"] in pair:
                    stripped = str(entry["price"]).rstrip("0")
                    return_data.update({entry["symbol"]: stripped})
            return return_data
        else:
            data = self.request_api_logger("ticker/price")
            return data

    def request_api_logger(self, suffix):
        url = "https://api.binance.com/api/v3/" + suffix
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

    @staticmethod
    def convert_ms_to_datetime_logger(ms: int):
        base_datetime = datetime.datetime(1970, 1, 1)
        delta = datetime.timedelta(0, 0, 0, ms*1000)
        target_date = base_datetime + delta
        return target_date

    def calculate_ma_logger(sequence, time_period):
        return ta.MA(np.array(sequence), time_period)

    def calculate_ema_logger(sequence, time_period):
        return ta.EMA(np.array(sequence), time_period)

    def calculate_mom_logger(sequence, time_period):
        return ta.MOM(np.array(sequence), time_period)

    def calculate_trix_logger(sequence, time_period):
        return ta.TRIX(np.array(sequence), time_period)

    def calculate_dema_logger(sequence, time_period):
        return ta.DEMA(np.array(sequence), time_period)

    def calculate_tema_logger(sequence, time_period):
        return ta.TEMA(np.array(sequence), time_period)

    def calculate_rsi_logger(sequence, time_period):
        return ta.RSI(np.array(sequence), time_period)

    def csv_writer_thread_handler(self, curr_index, filepath, indicators=True):
        # This will calculate the rsi and ma values for a given currency
        # The calculations will be based on the prices saved in StandaloneLogger class
        # And then finally it will append/write to the relevant file
        line = ""
        if indicators:
            # Need to grab the appropriate data
            # For example need to have the klines for last 50 5min segments
            # And also the last 50 1hr segments
            data_5min = []
            data_1hr = []
            ma_50_5min = self.calculate_ma_logger(data_5min, 50)[-1]
            ma_50_1hr = self.calculate_ma_logger(data_1hr, 50)[-1]
            rsi_6_5min = self.calculate_rsi_logger(data_5min, 6)[-1]
            rsi_6_1hr = self.calculate_rsi_logger(data_1hr, 6)[-1]
            rsi_14_5min = self.calculate_rsi_logger(data_5min, 14)[-1]
            rsi_14_1hr = self.calculate_rsi_logger(data_1hr, 14)[-1]
            line = line + ","+ma_50_5min+","+ma_50_1hr+"," + \
                rsi_6_5min+","+rsi_6_1hr+","+rsi_14_5min+","+rsi_14_1hr
        # And then write the data to the file
        # First check if the folder exists

        # Then check if the file already exists and then either append or write as required

    def csv_logger_lightweight(self, pairs: list, time_list=False, price_data=False, buffer=20, path=False):
        # This can accept multiple lines of data at once
        start_time = time_list[0]
        # Will use a single list instead of multiple lists for price_data in lightweight version
        # Then check whether to use the start time value
        clean_format_time = str(self.convert_ms_to_datetime_logger(
            start_time)).replace("-", "")
        clean_format_time = clean_format_time.replace(" ", "-").split(".")[0]
        clean_format_time = clean_format_time.replace(":", "")
        if self.log_start_time == 0:
            self.log_start_time = clean_format_time
        # Then update the buffer data
        self.buffer_times.append(clean_format_time)
        self.buffer_data.append(price_data.copy())
        # Then write to the files every time 10 ticks are saved up
        if self.buffer_counter >= buffer:
            self.buffer_counter = 0
            for i, pair in enumerate(pairs):

                filename = str(pair)+"-" + \
                    str(self.log_start_time)+".csv"
                if path:
                    folder_path = str(path) + str(pair) + "/"
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    filename = folder_path + str(filename)
                else:
                    folder_path = "D:/DCWLog/" + str(pair) + "/"
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    filename = folder_path + filename
                # Check if file already exists
                if not os.path.isfile(filename):
                    with open(filename, "w") as file:
                        for j, line in enumerate(self.buffer_times):
                            csv_data = self.buffer_data[j][i]
                            file.write(str(line)+","+str(csv_data)+"\n")
                # Otherwise append
                else:
                    with open(filename, "a") as file:
                        for j, line in enumerate(self.buffer_times):
                            csv_data = self.buffer_data[j][i]
                            file.write(str(line)+","+str(csv_data)+"\n")
            # Then reset the buffer
            self.buffer_times = []
            self.buffer_data = []
        else:
            self.buffer_counter += 1


if __name__ == "main":
    sl = StandaloneLogger()

    def update_prices():
        while sl.log_loop_tracker < 1000:
            current_time = time.time()
            fresh_data = sl.get_tick_logger(sl.market_currency_list)
            for pair, price in fresh_data.items():
                index = sl.market_currency_list.index(pair)
                sl.fresh_prices[index] = price
            sl.csv_logger_lightweight(pairs=sl.market_currency_list, time_list=[
                current_time], price_data=[sl.fresh_prices], path="C:/DCWLog/Test/")
            sl.log_loop_tracker += 1
            time.sleep(1.5)
