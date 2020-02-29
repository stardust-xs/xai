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
"""Utility for creating and writing data in csv files."""

import csv
import os
from typing import Any, List

from mle.constants import defaults


def update_data(file: str, header: List, *args: Any) -> None:
  """Update data in the `csv` file."""
  if os.path.isfile(file) and os.path.getsize(file) > 0:
    write_data(file, *args)
  else:
    write_header(file, header, *args)


def write_data(file: str, *args: Any) -> None:
  """Write row of data to the `csv` file."""
  with open(file, 'a', newline='', encoding=defaults.DEF_CHARSET) as _file:
    _csv = csv.writer(_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    _csv.writerow([*args])


def write_header(file: str, header: List, *args: Any) -> None:
  """Write header of data to the `csv` file."""
  with open(file, 'w', newline='', encoding=defaults.DEF_CHARSET) as _file:
    _csv = csv.writer(_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    _csv.writerow(header)
    _csv.writerow([*args])
