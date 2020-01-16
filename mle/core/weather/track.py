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
"""Core utility for making weather API calls."""

from typing import Optional, Tuple, Union

import requests

from mle.vars import dev


def wind_direction(degree: Union[float, int]) -> str:
  """Returns direction of the wind."""
  directions = ['northern', 'northeastern', 'eastern', 'southeastern',
                'southern', 'southwestern', 'western', 'northwestern']
  idx = int((degree + 11.25) / 22.5)
  return directions[idx % len(directions)]


def weather(darksky_key: str,
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
  # TODO(xames3): Add support for fetching latitude and longitudes.
  # Using default coordinates for testing.
  latitude, longitude = 19.1668795, 72.9562182
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
          wind_direction(obj['currently']['windBearing']),
          obj['currently']['cloudCover'], obj['currently']['uvIndex'],
          obj['currently']['visibility'], obj['currently']['ozone'])
