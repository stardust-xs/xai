# The following comment should be removed at some point in the future.
# pylint: disable=import-error
# pylint: disable=no-name-in-module

import time
from ctypes import Structure, byref, c_uint, cdll, sizeof
from typing import Union

import uiautomation
import win32gui

from mle.vars.dev import BROWSERS


def get_browsed_url(active_app: Union[None, str]) -> Union[None, str]:
    """Get browsed url from the browser instance."""
    try:
        if active_app in BROWSERS:
            browser = win32gui.GetForegroundWindow()
            browser_control = uiautomation.ControlFromHandle(browser)
            edit_control = browser_control.EditControl()
            if edit_control.GetValuePattern().Value:
                return 'https://' + edit_control.GetValuePattern().Value
            else:
                return None
        else:
            return None
    except Exception:
        return None


def split_domain_url(browsed_url: Union[None, str]) -> Union[None, str]:
    """Split domain url from the browsed url."""
    try:
        if browsed_url:
            return 'https://' + browsed_url.split('/')[2]
        else:
            return None
    except Exception:
        return None


class LastUseInfo(Structure):
    """Don't know how this works. But works just fine."""
    # You can find the reference code here:
    # http://stackoverflow.com/questions/911856/detecting-idle-time-in-python

    fields = [('cbSize', c_uint), ('dwTime', c_uint)]


def get_idle_duration():
    """Get number of seconds spent idle by the system."""
    last_use_info = LastUseInfo()
    last_use_info.cbSize = sizeof(last_use_info)
    cdll.user32.GetLastInputInfo(byref(last_use_info))
    secs = cdll.kernel32.GetTickCount() - last_use_info.dwTime
    return int(secs / 1000.0)
