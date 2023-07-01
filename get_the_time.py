import requests
from datetime import datetime
import time

def get_current_time():
    url = 'http://worldtimeapi.org/api/timezone/America/Sao_Paulo'
    try:
        response = requests.get(url)
        data = response.json()
        time_online = data['datetime']   

        # Parse the current time string into a datetime object
        dt = datetime.fromisoformat(time_online)

        # Extract the day, month, year, hour, minute, and second components
        day = '{:02d}'.format(dt.day)
        month = '{:02d}'.format(dt.month)
        year = dt.year
        hour = '{:02d}'.format(dt.hour)
        minute = '{:02d}'.format(dt.minute)
        second = '{:02d}'.format(dt.second)
        
        return f"{year}{month}{day}-{hour}{minute}{second}"
    except Exception as e:
        print("Unable to get time online, getting from system.")
        return time.strftime(
                f"%Y%m%d-%H%M%S")

        
print(get_current_time())