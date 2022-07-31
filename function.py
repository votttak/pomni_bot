
import time
from datetime import datetime, timezone

import pytz



### helper functions START ###

def current_hour():
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.now(tz)
    time_string = berlin_now.strftime("%H:%M:%S")
    hours = int(time_string[:2]) - 1                   # -1 does't it work correctly?
    return hours


def current_minutes():
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.now(tz)
    time_string = berlin_now.strftime("%H:%M:%S")
    minutes = int(time_string[3:5])
    return minutes


## calculates current seconds
def current_seconds():
    hours = current_hour()
    minutes = current_minutes()
    current_seconds = ((60 * hours) + minutes) * 60
    return current_seconds


## seconds_till_9_am
def seconds_till_morning():
    seconds_to_wait = 0
    current_sec = current_seconds()
    hours = current_hour()
    if hours in [0,1,2,3,4,5,6,7,8]:
        seconds_to_wait = 9*60*60 - current_sec
    else:
        seconds_to_wait = 24*60*60 - current_sec + 9*60*60

    return seconds_to_wait

### helper functions END ###




## waits if time between 23:00 and 7:59 [sleeping time] ##
def wait_if_sleeping_time():
    hours = current_hour()
    minutes = current_minutes()
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
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.now(tz)
    week_day = berlin_now.weekday()
    print(week_day)
    if week_day == 5:
        current_seconds = current_seconds()
        seconds_in_8_hours = 8 * 60 * 60
        seconds_in_24_hours = 24 * 60 * 60
        seconds_to_wait = seconds_in_24_hours - current_seconds + seconds_in_8_hours
        time.sleep(seconds_to_wait)


## waits if a particular channel (e.g. books) ##
def wait_customized(channel_id):

    ## chat_ids & titles ##
    # -1001603179754: "The Art of Decision Making" Joseph Bikart
    # -1001583281992: Русская модель управления

    send_only_morning_channels = [-1001603179754]
    send_every_third_morning_channels = [-1001583281992]
    time_to_wait = None
    if channel_id in send_only_morning_channels:
        time_to_wait = seconds_till_morning() 
    elif channel_id in send_every_third_morning_channels:
        time_to_wait = seconds_till_morning() + 2*24*60*60 # waits till next morning + 2 days
        
    return time_to_wait
    