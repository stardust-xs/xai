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

import os
import socket
from datetime import datetime
from typing import List, Optional, Union

from fuzzywuzzy import fuzz, process
from win10toast import ToastNotifier

from mle.vars import dev

mle_path = os.path.dirname(os.path.dirname(__file__))


def find_string(string: str,
                search: List,
                min_score: Optional[int] = 70) -> Optional[str]:
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
  guessed = process.extract(string, search, limit=3, scorer=fuzz.partial_ratio)

  for best_guess in guessed:
    current_score = fuzz.partial_ratio(string, best_guess)
    if current_score > min_score and current_score > 0:
      return best_guess[0]
    else:
      raise ValueError(f'Couldn\'t find "{string}" in the given list.')


def check_internet(timeout: Optional[Union[float, int]] = 10.0) -> bool:
  """Check the internet connectivity."""
  # You can find the reference code here:
  # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
  try:
    socket.create_connection((dev.PING_URL, dev.PING_PORT), timeout=timeout)
    return True
  except OSError:
    pass
  return False


def toast(name: str, message: str, timeout: Optional[int] = 15) -> None:
  """Display toast message."""
  # You can find the example code here:
  # https://github.com/jithurjacob/Windows-10-Toast-Notifications#example
  notifier = ToastNotifier()
  notifier.show_toast(title=name, msg=message, duration=timeout, threaded=True)


def now() -> datetime:
  """Return current time without microseconds."""
  return datetime.now().replace(microsecond=0)
