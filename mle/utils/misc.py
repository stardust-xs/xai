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

"""Utility for miscellaneous functions."""

import os
import socket
from datetime import datetime
from typing import Union

from win10toast import ToastNotifier

_URL = 'https://www.google.com/'
_PORT = 80


def check_internet(timeout: float = 10.0) -> bool:
  """Check the internet connectivity."""
  # You can find the reference code here:
  # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
  try:
    socket.create_connection((_URL, _PORT), timeout=timeout)
    return True
  except socket.error:
    return False


def now() -> datetime:
  """Return current time without microseconds."""
  return datetime.now().replace(microsecond=0)


def seconds_to_datetime(second: int) -> str:
  """Convert seconds to datetime string."""
  mins, secs = divmod(int(second), 60)
  hours, mins = divmod(mins, 60)
  return f'{hours:02d}:{mins:02d}:{secs:02d}'


def generate_ordinal(number: Union[float, int]) -> str:
  """Generate ordinal representation of a number."""
  _number = int(number)
  suffix = ['th', 'st', 'nd', 'rd', 'th'][min(_number % 10, 4)]
  if 11 <= (_number % 100) <= 13:
    suffix = 'th'
  return f'{_number}{suffix}'


def toast(title: str, msg: str,
          duration: float = 5.0, threaded: bool = True) -> None:
  """Display toast message."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  try:
    if os.name == 'nt':
      kwargs = {'title': title,
                'msg': msg,
                'icon_path': None,
                'duration': duration,
                'threaded': threaded}
      ToastNotifier().show_toast(**kwargs)
    else:
      os.system(f'notify-send {title} {msg}')
  except (KeyboardInterrupt, AttributeError, OSError):
    pass

