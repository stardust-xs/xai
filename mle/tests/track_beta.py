from ctypes import Structure, byref, c_uint, cdll, sizeof
from typing import Optional, Tuple, Union

import requests
import uiautomation
import win32gui

from mle.vars import dev
from mle.tests.locate import get_coordinates


def get_browsed_url() -> Union[None, str]:
  """Get browsed url from the browser instance.

  Use: url = get_browsed_url() if active_app in BROWSERS else None
  """
  try:
    browser = uiautomation.ControlFromHandle(win32gui.GetForegroundWindow())
    link = browser.EditControl().GetValuePattern().Value
    url = 'https://' + link if link else None
    return url
  except Exception:
    return None


def split_domain_url(browsed_url: Union[None, str]) -> Union[None, str]:
  """Split domain url from the browsed url."""
  try:
    if browsed_url:
      return 'https://' + browsed_url.split('/')[2]
    else:
      return None
  except Exception:
    return None


class LastUseInfo(Structure):
  """Don't know how this works. But works just fine."""
  # You can find the reference code here:
  # http://stackoverflow.com/questions/911856/detecting-idle-time-in-python
  fields = [('cbSize', c_uint), ('dwTime', c_uint)]


def get_idle_duration():
  """Get number of seconds spent idle by the system."""
  last_use_info = LastUseInfo()
  last_use_info.cbSize = sizeof(last_use_info)
  cdll.user32.GetLastInputInfo(byref(last_use_info))
  secs = cdll.kernel32.GetTickCount() - last_use_info.dwTime
  return int(secs / 1000.0)


def weather(darksky_key: str,
            maps_key: Optional[str] = None,
            address: Optional[str] = None) -> Optional[Tuple]:
  """Record weather for a particular address.

  Record weather for an address by making an API call to `DarkSky.net`.

  Note:
    * This function uses `DarkSky` for retreiving weather details of an
      address by making an API call. Hence it is necessary to create an
      account to access the API key before using this function.
      You can create it here: `https://darksky.net/`
    * Only 1000 calls can be made per day on the `free` tier.

  Returns:
    Tuple with various weather related parameters.

  Raises:
    ValueError: If the function is called without a valid API key.
  """
  maps_key = 'SOME API KEY'
  latitude, longitude = get_coordinates(maps_key, address)
  url = f'{dev.WEATHER_URL}{darksky_key}/{latitude},{longitude}?units=si'
  obj = requests.get(url).json()
  return (obj['latitude'], obj['longitude'], obj['currently']['summary'],
          obj['currently']['temperature'],
          obj['daily']['data'][0]['temperatureMax'],
          obj['daily']['data'][0]['temperatureMin'],
          obj['currently']['apparentTemperature'],
          obj['daily']['data'][0]['apparentTemperatureMax'],
          obj['daily']['data'][0]['apparentTemperatureMin'],
          obj['currently']['dewPoint'], obj['currently']['humidity'],
          obj['currently']['pressure'], obj['currently']['windSpeed'],
          obj['currently']['windGust'], obj['currently']['windBearing'],
          # wind_direction(obj['currently']['windBearing']),
          obj['currently']['cloudCover'], obj['currently']['uvIndex'],
          obj['currently']['visibility'], obj['currently']['ozone'])
