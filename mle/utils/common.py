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
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable, Sequence, Union

from rapidfuzz import fuzz, process
from win10toast import ToastNotifier

from mle.constants import defaults as dx
from mle.utils import symlinks


def fuzzy_search(keyword: str, search_in: Sequence) -> str:
  """Search using fuzzy logic.

  Search using fuzzy logic with an approximate or exact keyword.

  Args:
    keyword: Approximate or exact keyword to keyword.
    search_in: Material in which the keyword needs to be searched in.

  Returns:
    Best guess from the material.

  Examples:
    - Find files in directories:
      >>> import os
      >>> from mle.utils.common import fuzzy_search
      >>>
      >>> fuzzy_search('okami', os.listdir('D:/multimedia/music/'))
      'Okami - Kamiki Village.mp3'
      >>>

    - Find first sentence which has the matching word:
      >>> import os
      >>> from mle.utils.common import fuzzy_search
      >>>
      >>> test_list = ['The quick', 'brown fox jumps', 'over lazy dog']
      >>> fuzzy_search('barwn', test_list)
      'brown fox jumps'
      >>>
  """
  return process.extractOne(keyword, search_in, scorer=fuzz.partial_ratio)[0]


def check_internet(timeout: float = 10.0) -> bool:
  """Check the internet connectivity."""
  # You can find the reference code here:
  # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
  try:
    socket.create_connection((dx.PING_URL, dx.PING_PORT), timeout=timeout)
    return True
  except socket.error:
    return False


def toast(name: str, message: str,
          timeout: float = 15.0, thread: bool = True) -> None:
  """Display toast message."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  try:
    if os.name == 'nt':
      notifier = ToastNotifier()
      notifier.show_toast(title=name, msg=message,
                          duration=timeout, threaded=thread)
    else:
      os.system(f'notify-send {name} {message}')
  except (KeyboardInterrupt, AttributeError, OSError):
    pass


def now() -> datetime:
  """Return current time without microseconds."""
  return datetime.now().replace(microsecond=0)


def profile(function: Callable) -> Callable:
  """Decorator that uses cProfile to profile a function."""
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


def timestamp(timestamp_format: str = '%d_%m_Y_%H_%M_%S') -> str:
  """Returns string with current timestamp with a specified format."""
  return now().strftime(timestamp_format)


def log(file: str, level: str = 'debug') -> logging.Logger:
  """Log MLE events.

  Create log file and log necessary events.

  Args:
    file: Current file name.
    level: Logging level.

  Returns:
    Logger object which records logs in ./logs/ directory.
  """
  logger = logging.getLogger(file)
  logger.setLevel(f'{level.upper()}')
  name = Path(os.path.join(symlinks.logs, f'{Path(file.lower()).stem}.log'))
  formatter = logging.Formatter('%(asctime)s.%(msecs)05d    %(levelname)-8s    '
                                '%(filename)s:%(lineno)-16s    %(message)-8s',
                                '%Y-%m-%d %H:%M:%S')
  # Write logs to a file.
  file_handler = logging.FileHandler(os.path.join(symlinks.logs, name))
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  # Print logs as output.
  stream_handler = logging.StreamHandler(sys.stdout)
  stream_handler.setFormatter(formatter)
  logger.addHandler(stream_handler)
  return logger


def seconds_to_datetime(second: int) -> str:
  """Convert seconds to datetime string."""
  mins, secs = divmod(int(second), 60)
  hours, mins = divmod(mins, 60)
  return '%02d:%02d:%02d' % (hours, mins, secs)


def generate_ordinal(number: Union[float, int]) -> str:
  """Generate ordinal representation of a number."""
  _number = int(number)
  suffix = ['th', 'st', 'nd', 'rd', 'th'][min(_number % 10, 4)]
  if 11 <= (_number % 100) <= 13:
    suffix = 'th'
  return f'{_number}{suffix}'
