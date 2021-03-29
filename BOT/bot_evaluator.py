# This class will provide the functions for evaluating a bot object
# It will be called by the playground object
# It will randomly select existing data
# And then apply the given bot object to calculate when a buy/sell occurs
# Calculate the metrics associated with the given bot behaviour
# And then finally pass performance metrics back to the playground object
from os import walk
import csv
import random


class BotEvaluator():
    def __init__(self) -> None:
        self.data_for_eval = []
        self.starting_price = 0

    def grab_historical_data(self):
        list_filenames = []
        mypath = "C:\\DCWLog\\Test\\BTCUSDT\\"
        for (_, _, filenames) in walk(mypath):
            list_filenames.extend(filenames)
            break
        # print(list_filenames)
        # Randomly choose one of the files for assessment (skeleton only)
        with open(mypath+random.choice(list_filenames)) as csv_file:
            reader = csv.reader(csv_file)
            self.data_for_eval = list(reader)
        # The csv file format is as follows:
        # time hh:mm:ss, price, ma(50)5m, ma(50)1h, rsi(6)5m, rsi(6)1h, rsi(14)5m, rsi(14)1h
        # print(len(self.data_for_eval))
        self.starting_price = self.data_for_eval[0][1]
        print(self.starting_price)

    def calculate_buy_sell(self):
        pass

    def calculate_performance(self):
        pass


if __name__ == "__main__":
    be = BotEvaluator()
    be.grab_historical_data()
