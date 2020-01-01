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
"""The ``mle.core.tracker.track`` module.

This module tracks the user activities based on the current screen being
used. Also, this module packs the necessary functions which provide more
details about the active/current screen.

Todo:
    * Remove ``pylint`` warning comments.

"""
# The following comment should be removed at some point in the future.
# pylint: disable=import-error
# pylint: disable=no-name-in-module

from datetime import timedelta
from typing import Tuple, Union

import psutil
import win32gui
import win32process
from win32api import GetFileVersionInfo


def split_time_spent(total_time: timedelta) -> Tuple[int, int, int, int]:
    """Split time spent on each application."""
    days, secs = total_time.days, total_time.seconds
    hours = days * 24 + secs // 3600
    mins = (secs % 3600) // 60
    secs = secs % 60

    return days, hours, mins, secs


def get_name_from_exe(path: str) -> Union[None, str]:
    """Get application name using resource tables."""
    # You can find the reference code here:
    # https://stackoverflow.com/a/31119785
    try:
        lang, page = GetFileVersionInfo(path, '\\VarFileInfo\\Translation')[0]
        name = u'\\StringFileInfo\\%04X%04X\\FileDescription' % (lang, page)
        return GetFileVersionInfo(path, name)
    except Exception:
        return None


def get_active_window() -> Union[Tuple[None, None, None, None], Tuple]:
    """Get the active working window and return it's details."""
    # You can find the reference code here:
    # https://stackoverflow.com/a/47936739
    active = win32gui.GetForegroundWindow()
    handle = win32gui.GetWindowText(active)
    pid = win32process.GetWindowThreadProcessId(active)[-1]

    if psutil.pid_exists(pid):
        name = get_application_name(pid)
        exe = get_process_name(pid)
        user = get_username(pid)
        return handle, name, exe, user
    else:
        return None, None, None, None


def get_application_name(pid: int) -> Union[None, str]:
    """Get application name from it's pid."""
    # You can read the description here:
    # https://psutil.readthedocs.io/en/latest/#psutil.Process.exe
    try:
        return get_name_from_exe(psutil.Process(pid).exe())
    except Exception:
        return None


def get_process_name(pid: int) -> Union[None, str]:
    """Get process name from it's pid."""
    # You can read the description here:
    # https://psutil.readthedocs.io/en/latest/#psutil.Process.name
    try:
        return psutil.Process(pid).name()
    except Exception:
        return None


def get_username(pid: int) -> Union[None, str]:
    """Get name of the user who owns the process from it's pid."""
    # You can read the description here:
    # https://psutil.readthedocs.io/en/latest/#psutil.Process.username
    try:
        return psutil.Process(pid).username()
    except Exception:
        return None
