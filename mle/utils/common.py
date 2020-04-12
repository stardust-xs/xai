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
"""Utility for performing common functions."""

import cProfile
import io
import logging
import os
import pstats
import random
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Tuple, Union

from rapidfuzz import fuzz, process
from win10toast import ToastNotifier

from mle.constants import colors, defaults
from mle.utils import symlinks


def find_string(string: str, search: List) -> str:
  """Find string in the list using fuzzy logic.

  Find the matching string from the list. It works similar to `find`
  method but uses fuzzy logic for evaluating and guessing the correct
  word.

  Args:
    string: Approximate or exact string to find in the list.
    search: List in which the string needs to be searched in.

  Returns:
    Best guess string from the list.
  """
  return process.extractOne(string, search, scorer=fuzz.partial_ratio)


def check_internet(timeout: float = 10.0) -> bool:
  """Check the internet connectivity."""
  # You can find the reference code here:
  # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
  try:
    socket.create_connection((defaults.PING_URL, defaults.PING_PORT),
                             timeout=timeout)
    return True
  except OSError:
    pass
  return False


def toast(name: str, message: str, timeout: float = 15) -> None:
  """Display toast message."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  try:
    if os.name == 'nt':
      notifier = ToastNotifier()
      notifier.show_toast(title=name, msg=message,
                          duration=timeout, threaded=True)
    else:
      os.system(f'notify-send {name} {message}')
  except (KeyboardInterrupt, AttributeError):
    pass


def vzen_toast(name: str, message: str, timeout: float = 3) -> None:
  """Display toast message for VZen services without threading."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  try:
    if os.name == 'nt':
      notifier = ToastNotifier()
      notifier.show_toast(title=name, msg=message, duration=timeout)
    else:
      os.system(f'notify-send {name} {message}')
  except (KeyboardInterrupt, AttributeError):
    pass


def now() -> datetime:
  """Return current time without microseconds."""
  # This function can be used for calculating start time and time delta.
  return datetime.now().replace(microsecond=0)


def profile(function: Callable) -> Callable:
  """Decorator that uses cProfile to profile a function."""
  # Profiling is necessary and should be used for optimizing the overall
  # performance.
  def inner(*args, **kwargs):
    prof = cProfile.Profile()
    prof.enable()
    retval = function(*args, **kwargs)
    prof.disable()
    string = io.StringIO()
    ps = pstats.Stats(prof, stream=string).sort_stats('cumulative')
    ps.print_stats()
    print(string.getvalue())
    return retval

  return inner


def pick_random_color() -> Tuple:
  """Randomly selects a color from `./constants/colors.py`"""
  return random.choice(colors.COLOR_LIST)


def timestamp(timestamp_format: str = '%d_%m_Y_%H_%M_%S') -> str:
  """Returns string with current timestamp with a specified format."""
  return now().strftime(timestamp_format)


def log(file: str, level: str = 'debug') -> logging.Logger:
  """Create log file and log print events.

  Args:
    file: Current file name.
    level: Logging level.

  Returns:
    Logger object which records logs in ./logs/ directory.
  """
  logger = logging.getLogger(file)
  logger.setLevel(f'{level.upper()}')
  name = f'{Path(file.lower()).stem}.log'
  name = Path(os.path.join(symlinks.logs, name))
  formatter = logging.Formatter('%(asctime)s.%(msecs)05d    %(levelname)-8s    '
                                '%(filename)s:%(lineno)-16s    %(message)-8s',
                                '%Y-%m-%d %H:%M:%S')
  # Create log file.
  file_handler = logging.FileHandler(os.path.join(symlinks.logs, name))
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  # Print log statement.
  stream_handler = logging.StreamHandler(sys.stdout)
  stream_handler.setFormatter(formatter)
  logger.addHandler(stream_handler)
  # Return logger object.
  return logger


def seconds_to_datetime(second: int) -> str:
  """Convert seconds to datetime string."""
  mins, secs = divmod(second, 60)
  hours, mins = divmod(mins, 60)
  return '%02d:%02d:%02d' % (hours, mins, secs)


def generate_ordinal(number: Union[float, int]) -> str:
  """Generate ordinal representation of a number."""
  _number = int(number)
  suffix = ['th', 'st', 'nd', 'rd', 'th'][min(_number % 10, 4)]
  if 11 <= (_number % 100) <= 13:
    suffix = 'th'
  return f'{_number}{suffix}'
