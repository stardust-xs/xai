# Copyright 2020 XAMES3. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ======================================================================
"""The `mle.core.monitor.weather.record` module.

The core inspiration behind writing this module is to compensate the
lack of available, usable and updated weather data for Mumbai location.
This data aims to provide 3 key insights:
  1. How has the weather in Mumbai been in over the course of entire/~
     year of 2020 and beyond?
  2. Weather predictions for Mumbai.
  3. How different the weather has been lately (2021 and beyond) in
     comparison to 2020?

The module is configured to run at windows boot and keep it running in
background recording the weather of Mumbai every 30 mins and logging it
in a csv file on a daily basis.

The generated reports are stored in `./mle/data/raw/monitor/weather/`
with their respective dates & logs under `./mle/logs/record.log`.
"""

import os
import time
from datetime import datetime, timedelta

from mle.constants import defaults
from mle.core.monitor.weather.fetch import weather
from mle.utils import symlinks
from mle.utils.common import check_internet, log, now, toast
from mle.utils.write import update_data

# Location for which the weather needs to be monitored.
CITY = 'Mumbai'

log = log(__file__)
header = ['time', 'year', 'month', 'day', 'hour', 'mins', 'latitude',
          'longitude', 'summary', 'temp', 'max_temp', 'min_temp', 'apptemp',
          'max_apptemp', 'min_apptemp', 'dewpoint', 'humidty', 'pressure',
          'windspeed', 'windgust', 'windbearing', 'winddirection',
          'cloudcover', 'uv', 'visibility', 'ozone']

try:
  log.info('Weather monitoring service started.')
  toast('MLE Weather Monitor', 'Weather monitoring service started.')
  next_weather_check_time = now()
  # Keep the service running.
  while True:
    # If current time exceeds beyond DAY_LIMIT, save records to new file.
    if datetime.now().strftime(defaults.DAY_LIMIT_FORMAT) >= defaults.DAY_LIMIT:
      timestamp = datetime.now() + timedelta(days=1)
      log.info('Current time exceeded daily limit. Records saved to new file.')
    else:
      timestamp = datetime.now()
    csv = ''.join([timestamp.strftime(defaults.CSV_TS_FORMAT), '.csv'])
    file = os.path.join(symlinks.weather, csv)
    # Current time of making an API call (Weather check).
    start_time = now()
    if (start_time >= next_weather_check_time
        and datetime.now().strftime(defaults.DAY_LIMIT_FORMAT)
        != defaults.DAY_LIMIT):
      next_weather_check_time = start_time + timedelta(minutes=30)
      if check_internet():
        try:
          obj = weather(os.environ['DARKSKY_KEY'], CITY)
          update_data(file, header, start_time, start_time.year,
                      start_time.month, start_time.day, start_time.hour,
                      start_time.minute, obj[0], obj[1], obj[2],
                      obj[3], obj[4], obj[5], obj[6], obj[7], obj[8],
                      obj[9], obj[10], obj[11], obj[12], obj[13],
                      obj[14], obj[15], obj[17], obj[18], obj[19])
        except (ConnectionError, ConnectionResetError):
          log.warning('Internet connection is questionable.')
          toast('MLE Weather Monitor - Error Notification',
                'Internet connection is questionable.')
        except PermissionError:
          log.error('File accessed by another application.')
          toast('MLE Weather Monitor - Error Notification',
                'File accessed by another application.')
      else:
        log.error('Internet connection not available.')
        toast('MLE Weather Monitor - Skipping Track',
              'Internet connection not available.')
    # Let the checks be made after 1 second sleep.
    time.sleep(1)
except KeyboardInterrupt:
  log.error('Weather monitoring service interrupted.')
  toast('MLE Weather Monitor - Error Notification',
        'Weather monitoring service interrupted.')
except Exception:
  log.critical('Something went wrong with the weather monitoring service.')
  toast('MLE Weather Monitor - Error Notification',
        'Something went wrong with the service.')
