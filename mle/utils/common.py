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
import os
import pstats
import random
import socket
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

# TODO(xames3): Remove suppressed pyright warnings.
# pyright: reportMissingTypeStubs=false
from fuzzywuzzy import fuzz, process
from win10toast import ToastNotifier

from mle.constants import colors, defaults


def find_string(string: str,
                search: List,
                min_score: int = 70) -> Optional[str]:
  """Find string in the list using fuzzy logic.

  Find the matching string from the list. It works similar to `find`
  method but uses fuzzy logic for evaluating and guessing the correct
  word.

  Args:
    string: Approximate or exact string to find in the list.
    search: List in which the string needs to be searched in.
    min_score: Minimum score (default: 70) to make an approximate guess.

  Returns:
    Best guesses string from the list.

  Raises:
    ValueError: If no matching string is found in the `search` list.
  """
  # This will give a list of 3 best matches for our search query. The
  # number of best matches can be varied by altering the value of
  # `limit` parameter.
  guessed = process.extract(string, search, limit=3,
                            scorer=fuzz.partial_ratio)

  for best_guess in guessed:
    current_score = fuzz.partial_ratio(string, best_guess)
    if current_score > min_score and current_score > 0:
      return best_guess[0]
    else:
      raise ValueError(f'Couldn\'t find "{string}" in the given list.')


def check_internet(timeout: Union[float, int] = 10.0) -> bool:
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


def toast(name: str, message: str, timeout: int = 15) -> None:
  """Display toast message."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  notifier = ToastNotifier()
  notifier.show_toast(title=name, msg=message, duration=timeout, threaded=True)


def vzen_toast(name: str, message: str, timeout: int = 3) -> None:
  """Display toast message for VZen services without threading."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  notifier = ToastNotifier()
  notifier.show_toast(title=name, msg=message, duration=timeout)


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


def ordered_rename(directory: str, prefix: Optional[str] = None) -> None:
  """Rename files in order possibly with an optional prefix.

  Batch rename files in a directory with an optional prefix or just by
  default numeric order.

  Args:
    directory: Directory path of the files to be renamed.
    prefix: Optional (default: None) prefix for the renamed files.

  Note:
    Use this function when you need to batch rename files in an ordered
    manner. This can be performed before starting the training process.
  """
  prefix = ''.join([prefix, '_']) if prefix else ''
  for idx, file in enumerate(sorted(os.listdir(directory))):
    file = os.path.join(directory, file)
    os.rename(file, file.replace(Path(file).stem, ''.join([prefix, str(idx)])))


def pick_random_color() -> Tuple:
  """Randomly selects a color from `mle.constants.colors.py`"""
  return random.choice(colors.COLOR_LIST)
