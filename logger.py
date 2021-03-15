# This is meant as a standalone logging script for creating bot training datasets
# To-do list:
# 1) Bring in relevant functions and make custom lightweight versions so it is truly standalone
# 2) Need to increase the buffer size to 15
# 3) Need to store values for calculating rsi(14) for 1hr and everything below that
# 4) The final csv file format should be as follows:
# time ms, price, ma(50)5m, ma(50)1h, rsi(6)5m, rsi(6)1h, rsi(14)5m, rsi(14)1h
# 5) Potentially update the format to include more information later
from dcw_utils import DCWUtils
import time


class StandaloneLogger():
    def __init__(self):
        self.market_currency_list = [
            "BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "DOTUSDT", "XRPUSDT", "LTCUSDT", "XLMUSDT",
            "BCHUSDT", "DOGEUSDT", "XEMUSDT", "ATOMUSDT", "XMRUSDT", "EOSUSDT", "TRXUSDT"]
        self.log_loop_tracker = 0
        self.fresh_prices = []
        for curr in self.market_currency_list:
            self.fresh_prices.append(1.2)


if __name__ == "main":
    sl = StandaloneLogger()
    dcw = DCWUtils("Binance")

    def update_prices():
        while sl.log_loop_tracker < 1000:
            current_time = time.time()
            fresh_data = dcw.get_tick(sl.market_currency_list)
            for pair, price in fresh_data.items():
                index = sl.market_currency_list.index(pair)
                sl.fresh_prices[index] = price
            dcw.csv_logger(pairs=sl.market_currency_list, time_list=[
                current_time], existing_data=[sl.fresh_prices], path="C:/DCWLog/Test/")
            sl.log_loop_tracker += 1
            time.sleep(1.5)
