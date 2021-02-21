import os
import time
import subprocess
import webbrowser
import sys
from datetime import datetime


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


if __name__ == "__main__":
    # playground for testing
    # G_Utils.days_until_christmas()
    pass
