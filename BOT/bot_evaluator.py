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
        print(self.data_for_eval)

    def calculate_buy_sell(self):
        pass

    def calculate_performance(self):
        pass


if __name__ == "__main__":
    be = BotEvaluator()
    be.grab_historical_data()
