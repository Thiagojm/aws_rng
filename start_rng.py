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
    # Opening scripts in new terminal windows
    subprocess.Popen(['lxterminal', '-e', 'python3 /home/pi/Desktop/aws_rng/rng_collect.py; bash'])
    subprocess.Popen(['lxterminal', '-e', 'python3 /home/pi/Desktop/aws_rng/send_aws.py; bash'])

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
