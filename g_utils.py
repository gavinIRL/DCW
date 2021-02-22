import os
import time
import subprocess
import webbrowser
from datetime import datetime
import json
import urllib.request


class G_Utils:

    @staticmethod
    def runProcess(process_name, sleeptimer):
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

    def getAPIKey():
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

    def getDefaultExchange():
        # This will grab the default exchange from the settings file
        pass

    def setDefaultExchange():
        # This will set the default exchange in the settings file
        pass

    def getCoinList(key, exch):
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

    def checkSettingsFileExists():
        # check if file exists
        if os.path.isfile("settings.cfg"):
            # Need to check if the file is valid first
            # If valid then return setup complete
            return "Setup Complete"
            # Otherwise return invalid settings file
        else:
            return "Setup Incomplete"

    def getNetWorth():
        # This will get the approximate net worth of the user
        # Against the latest exchange rates
        # Placeholder for now
        return 1000

    def getCoinPrice(coin, key, interval):
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


if __name__ == "__main__":
    # playground for testing
    # G_Utils.days_until_christmas()
    print(G_Utils.getCoinList(G_Utils.getAPIKey(), "binance"))
    pass
