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
"""Core utility for retreiving coordinates for an address"""

from typing import Optional, Tuple

import googlemaps


def get_coordinates(api_key: str, address: Optional[str] = None) -> Tuple:
  """Get co-ordinates for particular location or address.

  Get coordinates of an address by making an API call to `Google Maps`.

  Note:
    This function uses `Google Maps` for retreiving coordinates of an
    address by making an API call. Hence it is necessary to generate an
    API key first before using this function.
    You can get it here: `https://console.developers.google.com`

  Args:
    api_key: Google Maps API key.
    address: Address (default: None) to convert in latitude & longitude.

  Example:
    >>> import os
    >>> from mle.core.weather.locate import get_coordinates
    >>> print(get_coordinates(os.environ.get('GCP_KEY'), 'Mumbai CST'))
    (18.9398446, 72.8354475)

  Returns:
    Tuple of latitude and longitude.

  Raises:
    ValueError: If the function is called without a valid API key.
  """
  client = googlemaps.Client(key=api_key, timeout=10)
  # If address location is not provided it will make an API call for the
  # current address.
  if address:
    _address = client.geocode(address)[0]['geometry']['location']
  else:
    _address = client.geolocate()['location']
  return _address['lat'], _address['lng']
