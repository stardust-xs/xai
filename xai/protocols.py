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

"""A simple collection of protocols to run in the background."""

import datetime
import errno
import os
import re
import time
from typing import Optional, TextIO, Tuple, Union

import comtypes
import geopy
import psutil
import pywinauto
import requests
from pkg_resources import resource_filename

from xai.utils.logger import SilenceOfTheLog
from xai.utils.misc import Neo, check_internet, now, toast, write_data

try:
  from win32gui import GetForegroundWindow, GetWindowText
  from win32process import GetWindowThreadProcessId
  from win32api import GetFileVersionInfo
except ImportError:
  print('ImportError: Win32 not installed. Please run `pip install pywin32`')
  exit(0)

log = SilenceOfTheLog(__file__)


class BabyMonitorProtocol(object, metaclass=Neo):
  """
  Baby Monitor Protocol

  The Baby Monitor Protocol is a daemon class running in the background
  to observe and record everything the user interacts with on the
  screen. The protocol records everything like the application(s) used,
  websites browsed by the user, etc. along with the amount of time the
  user has spent on it while using the computer.

  This data is stored locally for further use and more particularly for
  behaviourial analysis.
  """

  def __init__(self) -> None:
    """Instantiate class."""
    self._protocol = 'Baby Monitor Protocol'

    self._act = None
    self._hnd = None
    self._app = None
    self._url = None
    self._dmn = None
    self._exe = None
    self._usr = None
    self._inf = None

    self._uia = pywinauto.Application(backend='uia')
    self._title = 'Address and search bar'

    self._limit = '23:59:59'
    self._format = '%H:%M:%S'
    self._headers = ['activity', 'app', 'url', 'domain', 'executable', 'user',
                     'started', 'stopped', 'spent', 'days', 'hours', 'mins',
                     'secs']

    self._log = log.log(self._protocol)
    self._refresh = 1.0
    self._exception = 30.0

    self._path = resource_filename('xai', '/data/.baby_monitor/')

    try:
      os.mkdir(self._path)
    except OSError as _error:
      if _error.errno != errno.EEXIST:
        raise

  def _time_spent(self, delta: datetime.timedelta) -> Tuple[int, ...]:
    """Return time spent on each application."""
    raw = datetime.datetime.strptime(str(delta), self._format)
    return raw.day - 1, raw.hour, raw.minute, raw.second

  def _app_name(self, path: TextIO) -> str:
    """
    Return name of the application from the executable path using the
    Windows resource table.

    Args:
      path: Path of the executable file.

    Returns:
      Application name.

    Raises:
      NameError: If a valid executable is not found in resource tables.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/a/31119785
    try:
      lang, page = GetFileVersionInfo(path, '\\VarFileInfo\\Translation')[0]
      file_info = u'\\StringFileInfo\\%04X%04X\\FileDescription' % (lang, page)
      self._inf = GetFileVersionInfo(path, file_info)
    except NameError:
      self._log.error(f'{self._protocol} could not resolve application name.')
      self._inf = 'unknown'
    finally:
      return self._inf

  def _handle_info(self) -> Optional[Tuple[str, ...]]:
    """
    Return active window handle information like the active window name
    (window title), program name, executable name & the logged username.

    Returns:
      Tuple of active handle info if the process is running else None.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/a/47936739
    wnd = GetForegroundWindow()
    pid = GetWindowThreadProcessId(wnd)[-1]

    # This "if" condition ensures that we use only the active instances
    # of a process.
    if psutil.pid_exists(pid):
      hnd = GetWindowText(wnd)
      app = self._app_name(psutil.Process(pid).exe())
      exe = psutil.Process(pid).name()
      usr = psutil.Process(pid).username()
      return hnd, app, exe, usr
    return None

  def _absolute_url(self, browser: str) -> Optional[str]:
    """
    Return visited absolute URL.

    Args:
      browser: Name of the browser.

    Returns:
      Absolute URL address.

    Note:
      Currently, X.AI supports parsing URLs from Google Chrome only.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/a/59917905
    if browser != 'Google Chrome':
      return None

    try:
      self._uia.connect(title_re='.*Chrome.*', active_only=True)
      _wnd = self._uia.top_window()
      return 'https://' + _wnd.child_window(title=self._title,
                                            control_type='Edit').get_value()
    except (pywinauto.findwindows.ElementNotFoundError, comtypes.COMError):
      # These exceptions are ignored as they're not true exceptions but
      # are raised due to lack of proper function call.
      pass
    except Exception as _url_error:
      self._log.exception(_url_error)

  def activate(self) -> None:
    """Activate Baby Monitor protocol."""
    # Keep the protocol running irrespective of exceptions by suspending
    # the execution for 30 secs.
    while True:
      try:
        self._log.info(f'{self._protocol} activated.')
        toast(msg=f'{self._protocol} activated.')
        start_time = now()

        act_url = None
        act_dmn = None

        while True:
          # Return current active window handle along with application
          # name, executable file name and the user running the session.
          self._act = self._handle_info()

          if self._act:
            act_hnd, act_app, act_exe, act_usr = (*self._act,)

            # If time exceeds beyond self._limit, update the today's
            # date and save records to a new file. If the window handle
            # continues to stay the same beyond set time limit, the
            # record will be saved to newer file.
            if now().strftime(self._format) >= self._limit:
              _raw_date = now() + datetime.timedelta(days=1)
            else:
              _raw_date = now()

            self._file = os.path.join(self._path, '{}.csv')
            self._file = self._file.format(_raw_date.strftime('%d_%m_%y'))

            # Skip 'Task Switching' application and other application
            # switching overlays using 'Alt + Tab' or 'Win + Tab'.
            if act_hnd and act_hnd != 'Task Switching':
              if (self._hnd != act_hnd and
                  now().strftime(self._format) != self._limit):
                end_time = now()
                total_time = end_time - start_time
                spent_secs = total_time.total_seconds()
                time_spent = self._time_spent(total_time)

                # Record applications which are used for more than a
                # second, this enables skipping the 'Task Switching'
                # app. Also the below condition prevents inclusion of
                # blank entries in the recorded CSV.
                if time_spent != (0, 0, 0, 0) and self._hnd:
                  try:
                    # Return None if the active app isn't Google Chrome
                    # else return the absolute url.
                    act_url = self._absolute_url(act_app)

                    # Return domain name of the visited URL if not None.
                    if act_url:
                      act_dmn = re.match(r'(.*://)?([^/?]+)./*', act_url)[0]
                    else:
                      act_dmn = None

                    write_data(self._file, self._headers, self._hnd, self._app,
                               self._url, self._dmn, self._exe, self._usr,
                               start_time, end_time, spent_secs, *time_spent)

                  except PermissionError:
                    self._log.error('File accessed by another application.')
                    toast(msg='File accessed by another application.')
                  finally:
                    start_time = now()

              self._hnd = act_hnd
              self._app = act_app
              self._url = act_url
              self._dmn = act_dmn
              self._exe = act_exe
              self._usr = act_usr

          # Check if the window is switched after a second.
          time.sleep(self._refresh)
      except KeyboardInterrupt:
        self._log.warning(f'{self._protocol} interrupted.')
        toast(msg=f'{self._protocol} interrupted.')
        exit(0)
      except psutil.AccessDenied:
        self._log.error(f'{self._protocol} encountered an application crash.')
        toast(msg=f'{self._protocol} encountered an application crash.')
      except Exception as _error:
        self._log.exception(_error)
        toast(msg=f'{self._protocol} stopped abruptly.')
      finally:
        # Suspend the execution for 30 seconds if an exception occurs
        # before re-activating the protocol.
        time.sleep(self._exception)


class SilverLiningProtocol(object):
  """
  Silver Lining Protocol

  The Silver Lining Protocol is a daemon class running in the background
  to fetch and record weather for a particular address. This protocol
  exists for compensating the lack of available & usable weather data
  for a particular city.

  This data is stored locally for predicting weather for that location.
  """

  def __init__(self, address: str) -> None:
    """
    Instantiate class.

    Args:
      address: Address to resolve in latitude & longitude.
    """
    self._protocol = 'Silver Lining Protocol'

    self._address = address
    self._url = 'https://api.darksky.net/forecast/'
    self._directions = ['northern', 'northeastern', 'eastern', 'southeastern',
                        'southern', 'southwestern', 'western', 'northwestern']

    self._limit = '23:59:59'
    self._format = '%H:%M:%S'
    self._headers = ['time', 'year', 'month', 'day', 'hour', 'mins', 'latitude',
                     'longitude', 'summary', 'temp', 'max_temp', 'min_temp',
                     'apptemp', 'max_apptemp', 'min_apptemp', 'dewpoint',
                     'humidty', 'pressure', 'windspeed', 'windgust',
                     'windbearing', 'winddirection', 'cloudcover', 'uv',
                     'visibility', 'ozone']

    self._log = log.log(self._protocol, 'info')
    self._refresh = 1.0
    self._exception = 30.0

    self._path = resource_filename('xai', '/data/.silver_lining/')

    try:
      os.mkdir(self._path)
    except OSError as _error:
      if _error.errno != errno.EEXIST:
        raise

  def _direction(self, deg: Union[float, int]) -> str:
    """Returns direction of the wind based upon degree."""
    return self._directions[int((deg + 11.25) / 22.5) % len(self._directions)]

  def _coordinates(self) -> Tuple[float, float]:
    """Return co-ordinates for particular location or address."""
    geolocator = geopy.geocoders.Nominatim(user_agent='X.AI')
    location = geolocator.geocode(self._address)
    return location.latitude, location.longitude

  def _conditions(self, darksky_key: str) -> Optional[Tuple]:
    """
    Return weather conditions for a particular address by making an API
    call to 'DarkSky.net'.

    Args:
      darksky_key: DarkSky API key.

    Returns:
      Tuple with various weather related parameters.

    Raises:
      ValueError: If the method is called without valid API key.

    Note:
      This method uses 'DarkSky' for retreiving weather details of an
      address by making an API call. Hence it is necessary to create an
      account to access the API key before using this method.

      You can create it here: 'https://darksky.net/'.
      Only 1000 API calls can be made per day on the 'free' tier.
    """
    lat, lng = self._coordinates()

    # Considering metric system only.
    url = f'{self._url}{darksky_key}/{lat},{lng}?units=si'
    try:
      obj = requests.get(url).json()
      return (obj['latitude'],
              obj['longitude'],
              obj['currently']['summary'],
              obj['currently']['temperature'],
              obj['daily']['data'][0]['temperatureMax'],
              obj['daily']['data'][0]['temperatureMin'],
              obj['currently']['apparentTemperature'],
              obj['daily']['data'][0]['apparentTemperatureMax'],
              obj['daily']['data'][0]['apparentTemperatureMin'],
              obj['currently']['dewPoint'],
              obj['currently']['humidity'],
              obj['currently']['pressure'],
              obj['currently']['windSpeed'],
              obj['currently']['windGust'],
              obj['currently']['windBearing'],
              self._direction(obj['currently']['windBearing']),
              obj['currently']['cloudCover'],
              obj['currently']['uvIndex'],
              obj['currently']['visibility'],
              obj['currently']['ozone'])
    except ValueError:
      self._log.error(f'{self._protocol} cannot validate API key.')
      return None

  def activate(self) -> None:
    """Activate Silver Lining protocol."""
    # Keep the protocol running irrespective of exceptions by suspending
    # the execution for 30 secs.
    while True:
      try:
        self._log.info(f'{self._protocol} activated.')
        toast(msg=f'{self._protocol} activated.')
        next_update_time = now()

        while True:
          # If time exceeds beyond self._limit, update the today's
          # date and save records to a new file. If the window handle
          # continues to stay the same beyond set time limit, the
          # record will be saved to newer file.
          if now().strftime(self._format) >= self._limit:
            _raw_date = now() + datetime.timedelta(days=1)
          else:
            _raw_date = now()

          self._file = os.path.join(self._path, '{}.csv')
          self._file = self._file.format(_raw_date.strftime('%d_%m_%y'))

          update_time = now()

          # Make an API call every 30 mins and calculate the next update
          # time.
          if (update_time >= next_update_time and
              now().strftime(self._format) != self._limit):
            next_update_time = (update_time +
                                datetime.timedelta(minutes=self._exception))

            # Check if the internet is available before making an API.
            if check_internet():
              try:
                conditions = self._conditions(os.environ['DARKSKY_KEY'])
                write_data(self._file, self._headers, update_time,
                           update_time.year, update_time.month,
                           update_time.day, update_time.hour,
                           update_time.minute, *conditions)
              except (ConnectionError, ConnectionResetError):
                self._log.warning('Internet connection is questionable.')
                toast(msg='Internet connection is questionable.')
              except PermissionError:
                self._log.error('File accessed by another application.')
                toast(msg='File accessed by another application.')
            else:
              self._log.error('Internet connection not available.')
              toast(msg='Internet connection not available.')

          # Check if the weather is checked after a second.
          time.sleep(self._refresh)
      except KeyboardInterrupt:
        self._log.warning(f'{self._protocol} interrupted.')
        toast(msg=f'{self._protocol} interrupted.')
        exit(0)
      except geopy.exc.GeocoderTimedOut:
        self._log.error(f'{self._protocol} timed out.')
        toast(msg=f'{self._protocol} timed out.')
      except ConnectionError:
        self._log.error(f'{self._protocol} reached maximum try limit.')
        toast(msg=f'{self._protocol} reached maximum try limit.')
      except Exception as _error:
        self._log.exception(_error)
        toast(msg=f'{self._protocol} stopped abruptly.')
      finally:
        # Suspend the execution for 30 seconds if an exception occurs
        # before re-activating the protocol.
        time.sleep(self._exception)
