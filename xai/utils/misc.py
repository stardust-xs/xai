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

"""Collection of miscellaneous utilities."""

import csv
import os
import socket
from datetime import datetime
from typing import Sequence, Union

import psutil
from win10toast import ToastNotifier

socket_addr = ('www.google.com', 80)

_UTF = 'utf-8'


class Neo(type):
    """
    Neo

    Neo is a Singleton class.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Neo, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def check_internet(timeout: float = 10.0) -> bool:
    """Check the internet connectivity."""
    # You can find the reference code here:
    # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
    try:
        socket.create_connection(socket_addr, timeout=timeout)
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


def toast(title: str = 'X.AI', msg: str = None,
          duration: float = 5.0, threaded: bool = True) -> None:
    """
    Display toast message.

    Args:
      title: Title of the toast.
      msg: Toast message to display.
      duration: Toast message duration.
      threaded: Thread-safe boolean.

    Raises:
      KeyboardInterrupt: If user cancels the execution.
      AttributeError: If thread-safe mechanism fails to run.
      OSError: If something goes wrong while running command on console.
    """
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


def write_data(file: str, header: Sequence, *args) -> None:
    """
    Write data into csv file.

    Args:
      file: Filepath of csv file.
      header: Sequence of the headers in the csv file.
    """
    with open(file, 'a', newline='', encoding=_UTF) as raw:
        csv_obj = csv.writer(raw, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # This ensure that the header is written just once even though the
        # rows are appended consecutively.
        if not (os.path.isfile(file) and os.path.getsize(file) > 0):
            csv_obj.writerow(header)

        csv_obj.writerow([*args])


def get_process_memory():
  """Docstring to be updated."""
  process = psutil.Process(os.getpid())
  return process.memory_info()
