import os
import time
import requests
import subprocess
from datetime import datetime, timedelta
import pytz
import ntplib

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def check_and_update_time():
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    current_time = datetime.fromtimestamp(response.tx_time, pytz.timezone('America/Sao_Paulo'))
    date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    os.system(f'date -s "{date_time}"')
    print('System time updated')

def launch_scripts():
    # if you want to run scripts in the background
    subprocess.Popen(['python3', 'rng_collect.py'])
    subprocess.Popen(['python3', 'send_aws.py'])

def main():
    while True:
        if check_internet():
            check_and_update_time()
            launch_scripts()
            break
        else:
            print('No internet connection. Waiting for 30 seconds to try again...')
            time.sleep(30)

if __name__ == "__main__":
    main()
