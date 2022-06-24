
import time
from datetime import datetime




## waits if time between 23:00 and 7:59 [sleeping time] ##
def wait_if_sleeping_time():
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    hours = int(time_string[:2])
    minutes = int(time_string[3:5])
    if hours in [0, 1, 2, 4, 5, 6, 7, 23]:
        current_seconds = ((60 * hours) + minutes) * 60
        seconds_in_8_hours = 8 * 60 * 60
        if hours in [23]:
            seconds_in_24_hours = 24 * 60 * 60
            seconds_to_wait = seconds_in_24_hours - current_seconds + seconds_in_8_hours
            time.sleep(seconds_to_wait)
        else:
            seconds_to_wait = seconds_in_8_hours - current_seconds
            time.sleep(seconds_to_wait)



## waits if day off [saturday] ##
def wait_if_day_off():
    week_day = datetime.today().weekday()
    if week_day == 5:
        now = datetime.now()
        time_string = now.strftime("%H:%M:%S")
        hours = int(time_string[:2])
        minutes = int(time_string[3:5])
        current_seconds = ((60 * hours) + minutes) * 60
        seconds_in_8_hours = 8 * 60 * 60
        seconds_in_24_hours = 24 * 60 * 60
        seconds_to_wait = seconds_in_24_hours - current_seconds + seconds_in_8_hours
        time.sleep(seconds_to_wait)

