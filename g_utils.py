import os
import time
import subprocess
import webbrowser
import sys
from datetime import datetime
from nomics import Nomics
import nomics


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

    def getRates(key):
        if not key:
            # if it isn't valid print an error message
            print("Invalid settings file")
        else:
            nomics = Nomics(key)
            return nomics.ExchangeRates.get_rates()

        # then do some sorting of the output

    def getMarkets(key, exch):
        if not key:
            # if it isn't valid print an error message
            print("Invalid settings file")
        else:
            nomics = Nomics(key)
            markets = nomics.Markets.get_markets(exchange=exch)
            print(markets)

        # then do some sorting out the output

    def checkSettingsFileExists():
        filename = "settings.cfg"
        # check if file exists
        if os.path.isfile(filename):
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


if __name__ == "__main__":
    # playground for testing
    # G_Utils.days_until_christmas()
    # print(G_Utils.getMarkets(G_Utils.getAPIKey(), "binance"))
    print(G_Utils.getRates(G_Utils.getAPIKey()))
    pass
