# This is meant as a standalone logging script for creating bot training datasets
# The final csv file format should be as follows:
# time ms, price, ma(50)5m, ma(50)1h, rsi(6)5m, rsi(6)1h, rsi(14)5m, rsi(14)1h, 5m volume, 1hr volume
from dcw_utils import DCWUtils
import time
import datetime
import os
from requests.exceptions import HTTPError
import json
import requests
import talib as ta
import numpy as np
import threading


class StandaloneLogger():
    def __init__(self, output_path="C:/DCWLog/Test/", buffer_size=20, candle_loop_size=50):
        self.path = output_path
        self.buffer_size = buffer_size
        self.candle_loop_size = candle_loop_size
        self.pair_list = [
            "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
            "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "EOSUSDT", "TRXUSDT"]
        self.log_loop_tracker = 0
        self.candle_loop_tracker = 1
        self.buffer_counter = 1
        self.fresh_prices = []
        self.log_start_time = 0
        self.file_list = []
        self.buffer_times = []
        self.buffer_data = []
        self.last_50_closes_5min = []
        self.last_50_closes_1hr = []
        self.last_50_oohlcvc_5min = []
        self.last_50_oohlcvc_1hr = []
        for i in range(len(self.pair_list)):
            self.fresh_prices.append(1.2)
            self.file_list.append(".")
            self.last_50_closes_5min.append([])
            self.last_50_closes_1hr.append([])
            self.last_50_oohlcvc_5min.append([])
            self.last_50_oohlcvc_1hr.append([])

        self.current_timeout = 0
        self.threads = []
        self.sleep_spacing_mult = 0.25

    def get_tick_logger(self, pair=False):
        if isinstance(pair, str):
            data = self.request_api_logger("ticker/price?symbol="+pair)
            if not data:
                return False
            return str(data["price"]).strip("0")
        elif isinstance(pair, list):
            data = self.request_api_logger("ticker/price")
            if not data:
                return False
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
                if self.current_timeout != 0:
                    if self.current_timeout < 1:
                        self.current_timeout = 0
                    else:
                        self.current_timeout = self.current_timeout/2
                return json.loads(response.text)
            elif response.status_code == 404:
                print("Incorrect input, got 404'd")
                return False
            elif response.status_code == 429 or response.status_code == 418:
                wait_seconds = int(response.headers["Retry-After"])
                self.current_timeout = wait_seconds
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

    def clean_format_time(self, raw_time: str):
        clean_format_time = str(self.convert_ms_to_datetime_logger(
            raw_time)).replace("-", "")
        clean_format_time = clean_format_time.replace(
            " ", "-").split(".")[0]
        clean_format_time = clean_format_time.replace(":", "")
        return clean_format_time

    # Having these methods more visible for clarity
    # And to prevent error of sequence not being a numpy array
    # Because I will retire from programming if I make that error once more
    @staticmethod
    def calculate_ma_logger(sequence, time_period):
        return ta.MA(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_ema_logger(sequence, time_period):
        return ta.EMA(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_mom_logger(sequence, time_period):
        return ta.MOM(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_trix_logger(sequence, time_period):
        return ta.TRIX(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_dema_logger(sequence, time_period):
        return ta.DEMA(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_tema_logger(sequence, time_period):
        return ta.TEMA(np.array(sequence, dtype=np.float32), time_period)

    @staticmethod
    def calculate_rsi_logger(sequence, time_period):
        return ta.RSI(np.array(sequence, dtype=np.float32), time_period)

    def csv_writer_thread_handler(self, curr_index, folder_path, indicators=True):
        # This will calculate the rsi and ma values for a given currency
        # The calculations will be based on the prices saved in StandaloneLogger class
        # And then finally it will append/write to the relevant file
        pair = self.pair_list[curr_index]
        # Then create the file name
        filename = str(pair)+"-" + str(self.log_start_time)+".csv"
        if folder_path:
            filename = folder_path + str(filename)
        else:
            filename = self.path + str(filename)
        # The csv file format should be as follows:
        # time, price, ma(50)5m, ma(50)1h, rsi(6)5m, rsi(6)1h, rsi(14)5m, rsi(14)1h
        list_lines = []
        # Need to grab the appropriate data
        # For example need to have the klines for last 50 5min segments
        # And also the last 50 1hr segments
        # print(self.buffer_data[0])
        for i, timepoint in enumerate(self.buffer_data):
            price = timepoint[pair]
            time_entry = self.buffer_times[i]
            data_5min = self.last_50_closes_5min[curr_index]
            data_1hr = self.last_50_closes_1hr[curr_index]
            print(np.array(data_5min))
            # ma_50_5min = self.calculate_ma_logger(data_5min, 50)[-1]
            # ma_50_1hr = self.calculate_ma_logger(data_1hr, 50)[-1]
            # data_5min = self.last_50_closes_5min[curr_index][-16:]
            # data_1hr = self.last_50_closes_1hr[curr_index][-16:]
            # rsi_6_5min = self.calculate_rsi_logger(data_5min, 6)[-1]
            # rsi_6_1hr = self.calculate_rsi_logger(data_1hr, 6)[-1]
            # rsi_14_5min = self.calculate_rsi_logger(data_5min, 14)[-1]
            # rsi_14_1hr = self.calculate_rsi_logger(data_1hr, 14)[-1]
            # volume_5m = self.last_50_oohlcvc_5min[curr_index][-1]["Volume"]
            # volume_1h = self.last_50_oohlcvc_1hr[curr_index][-1]["Volume"]
            # if indicators:
            #     line = time_entry + ","+price + ","+ma_50_5min+","+ma_50_1hr+"," + \
            #         rsi_6_5min+","+rsi_6_1hr+","+rsi_14_5min+","+rsi_14_1hr + "," + \
            #         volume_5m+","+volume_1h+"\n"
            # else:
            #     line = time_entry + ","+price + "\n"
            line = price
            list_lines.append(line)
        # for i, price in enumerate(self.buffer_data[curr_index]):
        #     time_entry = self.buffer_times[i]
        #     data_5min = self.last_50_closes_5min[curr_index]
        #     data_1hr = self.last_50_closes_1hr[curr_index]
        #     # print(data_5min)
        #     ma_50_5min = self.calculate_ma_logger(data_5min, 50)[-1]
        #     ma_50_1hr = self.calculate_ma_logger(data_1hr, 50)[-1]
        #     data_5min = self.last_50_closes_5min[curr_index][-16:]
        #     data_1hr = self.last_50_closes_1hr[curr_index][-16:]
        #     rsi_6_5min = self.calculate_rsi_logger(data_5min, 6)[-1]
        #     rsi_6_1hr = self.calculate_rsi_logger(data_1hr, 6)[-1]
        #     rsi_14_5min = self.calculate_rsi_logger(data_5min, 14)[-1]
        #     rsi_14_1hr = self.calculate_rsi_logger(data_1hr, 14)[-1]
        #     # TBD need to grab volume data and append also
        #     volume_5m = self.last_50_oohlcvc_5min[curr_index][-1]["Volume"]
        #     volume_1h = self.last_50_oohlcvc_1hr[curr_index][-1]["Volume"]
        #     if indicators:
        #         line = time_entry + ","+price + ","+ma_50_5min+","+ma_50_1hr+"," + \
        #             rsi_6_5min+","+rsi_6_1hr+","+rsi_14_5min+","+rsi_14_1hr + "," + \
        #             volume_5m+","+volume_1h+"\n"
        #     else:
        #         line = time_entry + ","+price + "\n"
        #     list_lines.append(line)
        # And then write the data to the file
        # First check if the folder exists
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        # Then check if the file already exists and then either append or write as required
        # Check if file already exists
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                for line in list_lines:
                    file.write(line)
        # Otherwise append
        else:
            with open(filename, "a") as file:
                for line in list_lines:
                    file.write(line)

    def csv_logger_lightweight(self, path=False):
        # print("Got here #1")
        # First grab the current time
        current_time = time.time()
        clean_format_time = self.clean_format_time(current_time)
        # Now grab the current prices
        price_data = self.get_tick_logger(self.pair_list)
        # print(price_data)
        # Check that there wasn't an error
        if price_data:
            # Run into a problem of not all threads being complete when get to this point unfortunately
            # Only happens at the beginning, or more accurately only matters at beginning
            # Therefore need to pause until information has come through for each currency
            sleep_length = 0.5
            while not all(self.last_50_closes_1hr):
                sleep_length += 0.5
                print("Data not fully loaded yet, sleeping for " +
                      str(sleep_length)+"s total")
                time.sleep(0.5)
            # Sleep for another second anyway to make sure
            if sleep_length > 0.5:
                print("Data loaded, continuing")
                # print(self.last_50_closes_1hr)
                # time.sleep(1.0)
            # Debug - Check of the last 5 currencies to load
            # while True:
            #     print(self.last_50_closes_1hr[:-5])
            #     time.sleep(1.0)
            #     if self.log_loop_tracker > 5000:
            #         break
            # Now update the last value in the last 50 closes
            for pair, price in price_data.items():
                curr_index = self.pair_list.index(pair)
                # print(curr_index)
                # print(self.last_50_closes_1hr[curr_index][-1])
                self.last_50_closes_5min[curr_index][-1] = price
                self.last_50_closes_1hr[curr_index][-1] = price
            # Then update the buffer data
            self.buffer_times.append(clean_format_time)
            self.buffer_data.append(price_data)
            # Then write to the files every time 10 ticks are saved up
            if self.buffer_counter >= self.buffer_size:
                # print("Got here #2")
                self.buffer_counter = 0
                # Send information to the threaded tasks
                for i, currency in enumerate(self.pair_list):
                    # Do something
                    # print("Got here #3")
                    t = threading.Thread(target=self.csv_writer_thread_handler,
                                         args=(i, path))
                    self.threads.append(t)
                    t.start()
                self.buffer_times = []
                self.buffer_data = []
            else:
                self.buffer_counter += 1
        else:
            time.sleep(sl.current_timeout)

    def get_candle(self, pair: str, interval: str, limit: int):
        data = self.request_api_logger(
            "klines?symbol="+pair+"&interval="+interval+"&limit="+str(limit))
        if not data:
            return False
        return_data = []
        for row in data:
            # Don't want all the entries
            timepoint = {}
            timepoint["Open Time"] = row[0]
            timepoint["Open"] = row[1]
            timepoint["High"] = row[2]
            timepoint["Low"] = row[3]
            timepoint["Close"] = row[4]
            timepoint["Volume"] = row[5]
            timepoint["Close Time"] = row[6]
            return_data.append(timepoint)
        return return_data

    def candle_thread_handler_5m(self, pair, sleep_timer):
        index = self.pair_list.index(pair)
        if self.current_timeout != 0:
            time.sleep(self.current_timeout)
        time.sleep(sleep_timer*self.sleep_spacing_mult)
        data5m = sl.get_candle(pair, "5m", limit=50)
        close_only = []
        for entry in data5m:
            close_only.append(entry["Close"])
        self.last_50_closes_5min[index] = close_only
        self.last_50_oohlcvc_5min = data5m.copy()

    def candle_thread_handler_1hr(self, pair, sleep_timer):
        index = self.pair_list.index(pair)
        if self.current_timeout != 0:
            time.sleep(self.current_timeout)
        time.sleep(sleep_timer*self.sleep_spacing_mult*1.5)
        data1h = sl.get_candle(pair, "1h", limit=50)
        close_only = []
        for entry in data1h:
            close_only.append(entry["Close"])
        self.last_50_closes_1hr[index] = close_only
        self.last_50_oohlcvc_1hr = data1h.copy()


def main_loop(sl: StandaloneLogger, max_loops=100, sleep_time=2.5):
    while sl.log_loop_tracker < max_loops:
        # Need to grab the candles every so often
        if sl.candle_loop_tracker == 1:
            sl.candle_loop_tracker += 1
            # Grab the candles
            for delay, pair in enumerate(sl.pair_list):
                t = threading.Thread(target=sl.candle_thread_handler_5m,
                                     args=(pair, delay))
                sl.threads.append(t)
                t.start()
                t2 = threading.Thread(target=sl.candle_thread_handler_1hr,
                                      args=(pair, delay))
                sl.threads.append(t2)
                t2.start()
        elif sl.candle_loop_tracker >= sl.candle_loop_size:
            sl.candle_loop_tracker = 1
        else:
            sl.candle_loop_tracker += 1
        # Handle the file naming at startup
        if sl.log_start_time == 0:
            current_time = time.time()
            sl.log_start_time = sl.clean_format_time(current_time)
        sl.csv_logger_lightweight()
        sl.log_loop_tracker += 1
        time.sleep(sleep_time)


if __name__ == "__main__":
    sl = StandaloneLogger(buffer_size=5)
    main_loop(sl)
