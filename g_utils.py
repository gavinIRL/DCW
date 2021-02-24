import os
import time
import subprocess
import webbrowser
from datetime import datetime
import json
import urllib.request


class G_Utils:

    @staticmethod
    def run_process(process_name, sleeptimer):
        subprocess.Popen(process_name)
        time.sleep(sleeptimer)
        print("Process Started")

    @staticmethod
    def process_exists(process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())

    @staticmethod
    def kill_process(process_name):
        os.system(f"taskkill /im {process_name}")

    @staticmethod
    def open_webpage(url):
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(chrome_path).open_new_tab(url)

    @staticmethod
    def days_until_christmas():
        now = datetime.now()
        xmas = datetime(now.year, 12, 25)
        delta = xmas - now
        return delta.days

    @staticmethod
    def days_since_date(date):
        now = datetime.now()
        delta = now-date
        return delta.days

    # All of the non-set/get functions related to crypto

    def checkSettingsFileExists():
        # check if file exists
        if os.path.isfile("settings.cfg"):
            # Need to check if the file is valid first
            # If valid then return setup complete
            return True
            # Otherwise return invalid settings file
        else:
            return False

    def call_api(suffix):
        # Highly condensed function which returns the json data from nomics
        return json.loads(urllib.request.urlopen("https://api.nomics.com/v1/"+suffix).read())

    # All of the get functions related to crypto

    def get_all_prices(key=False):
        # Uses a deprecated api call to grab price data for all currencies available
        url = "https://api.nomics.com/v1/prices?key=" + key
        raw_data = urllib.request.urlopen(url).read()
        data = json.loads(raw_data)
        list_currencies = []
        list_prices = []
        for currency in data:
            list_currencies.append(currency["currency"])
            list_prices.append(currency["price"])
        if len(list_prices) == len(list_currencies):
            return dict(zip(list_currencies, list_prices))
        else:
            return False

    def get_all_prices_old(key=False, start_time="T00%3A00%3A00Z", start_date="2021-02-12", end_time="T00%3A00%3A00Z", end_date="2021-02-14"):
        # Uses a deprecated api call to grab price data for all currencies
        # At a specific time period in the past
        url = "https://api.nomics.com/v1/prices?key=" + key + "&start=" + \
            start_date + start_time + "&end=" + end_date + end_time
        raw_data = urllib.request.urlopen(url).read()
        data = json.loads(raw_data)
        list_currencies = []
        list_open = []
        list_close = []
        for currency in data:
            list_currencies.append(currency["currency"])
            list_open.append(currency["open"])
            list_close.append(currency["close"])
        if len(list_open) == len(list_currencies):
            return dict(zip(list_currencies, list_open, list_close))
        else:
            return False

    def get_API_key():
        filename = "settings.cfg"
        # check if file exists otherwise create new file
        if os.path.isfile(filename):
            # then read for the key
            with open(filename) as f:
                line = f.readline()
                # need to check if the file is valid first
                if not "API Key = " in line:
                    return False

                else:
                    # otherwise return the key
                    return line.replace("API Key = ", "")

        else:
            # prompt the user for their api key
            # for now this will be command line, update to having a window later
            key = input("Enter your API Key: ")
            # write they key to the file
            with open(filename, "w") as file:
                file.write("API Key = " + key)
            # and finally return the key
            return key

    def get_default_exchange():
        # This will grab the default exchange from the settings file
        pass

    def get_coin_list(key, exch):
        if not key:
            # if it isn't valid print an error message
            return False
        url = "https://api.nomics.com/v1/markets?key=" + \
            key+"&ids=" + "&exchange="+exch+"&quote=BTC"
        raw_data = urllib.request.urlopen(url).read()
        data = json.loads(raw_data)
        currencyList = []
        for currency in data:
            currencyList.append(currency["base"])
        return sorted(list(set(currencyList)))

        # then do some sorting out the output

    def get_high_low_current(key, coin, interval):
        # placholder for now
        # Format of data is High/Low/Current
        data = ["297", "316", "309"]
        return data

    def get_net_worth(datetime, currencies):
        # This will get the approximate net worth of the user
        # Against previous exchange rates
        # Typically 24 hours
        # Placeholder for now
        return 900

    def get_coin_price(key=False, coin="BTC", interval="1h"):
        if not key:
            url = "https://api.nomics.com/v1/currencies/ticker?key="+key+"&ids=" + \
                coin+"&interval="+interval+"&convert=USD&per-page=100&page=1"
            raw_data = urllib.request.urlopen(url).read()
            data = json.loads(raw_data)
            for currency in data:
                print("ID: "+currency["id"])
                print("Price:"+currency["price"])
                print("Time:"+currency["price_timestamp"])
                hourdata = currency["1h"]
                print(hourdata)
                print("Price Change 1hr: " +
                      str(100*float(hourdata["price_change_pct"]))+"%")
                print("Volume Change 1hr: " +
                      str(100*float(hourdata["volume_change_pct"]))+"%")
            return 191.75
        else:
            return 191

    def get_coin_price_old(key=False, coin="BTC", time="T00%3A00%3A00Z", date="2021-02-12"):
        # Placeholder for now
        return 181

    def get_sparkline(key=False, coin="BTC", start_time="T00%3A00%3A00Z", start_date="2021-02-12", end_time="T00%3A00%3A00Z", end_date="2021-02-14"):
        if not key:
            # Placeholder for now
            url = "https://api.nomics.com/v1/currencies/sparkline?key="+key+"&ids=" + \
                coin + "&start=" + start_date + start_time + "&end=" + end_date + end_time
            # Format will be a 2D list with dates in first row and values in second
            raw_data = urllib.request.urlopen(url).read()
            data = json.loads(raw_data)
            for currency in data:
                # grab the relevant values
                pass
            return_data = [["2021-02-12", "2021-02-13",
                            "2021-02-14"], ["154", "155", "156"]]
            return return_data
        else:
            return False

    # All of the set functions related to crypto

    def set_default_exchange():
        # This will set the default exchange in the settings file
        pass


if __name__ == "__main__":
    # playground for testing
    # G_Utils.days_until_christmas()
    print(G_Utils.get_coin_list(G_Utils.get_API_key(), "binance"))
    pass
