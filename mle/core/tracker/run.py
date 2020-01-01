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
"""The ``mle.core.tracker.run`` module.

This module initiates MLE's tracking service in the background as soon
as the system boots up. The service tracks the time spent on all valid
active screens/applications and generates a csv file on daily basis.

The generated reports are stored under ``./mle/data/tracker/`` directory
with their respective dates.

Todo:
    * Remove ``pylint`` warning comments.

"""
# The following comment should be removed at some point in the future.
# pylint: disable=import-error
# pylint: disable=no-name-in-module

import os
import time
from datetime import datetime, timedelta

from win10toast import ToastNotifier

from mle.core.tracker.track import get_active_window, split_time_spent
from mle.core.tracker.write import update_data
from mle.utils.common import mle_path
from mle.vars.dev import DAY_LIMIT, DAY_LIMIT_FORMAT, TRACKER_CSV_TS_FORMAT

toast = ToastNotifier()

try:
    toast.show_toast(title="MLE Activity Tracker",
                     msg='Tracker service started.')

    previous_window = previous_app = previous_exe = previous_user = ''

    start_time = datetime.now().replace(microsecond=0)

    data_path = os.path.join(mle_path, 'data\\tracker')
    csv = ''.join([datetime.now().strftime(TRACKER_CSV_TS_FORMAT), '.csv'])
    file = os.path.join(data_path, csv)

    while True:
        active_window, active_app, active_exe, active_user = get_active_window()

        if datetime.now().strftime(DAY_LIMIT_FORMAT) >= DAY_LIMIT:
            new_date = datetime.now() + timedelta(days=1)
            csv = ''.join([new_date.strftime(TRACKER_CSV_TS_FORMAT), '.csv'])
            file = os.path.join(data_path, csv)

        if active_window and active_window != 'Task Switching':
            if (previous_window != active_window
                and datetime.now().strftime(DAY_LIMIT_FORMAT) != DAY_LIMIT):
                end_time = datetime.now().replace(microsecond=0)
                total_time = end_time - start_time
                usage = split_time_spent(total_time)

                if usage != (0, 0, 0, 0):
                    update_data(file, previous_window, previous_app,
                                previous_exe, previous_user, start_time, end_time, usage[0], usage[1], usage[2],
                                usage[3])
                    start_time = datetime.now().replace(microsecond=0)

            previous_window = active_window
            previous_app = active_app
            previous_exe = active_exe
            previous_user = active_user

        time.sleep(1)
except Exception:
    toast.show_toast(title="MLE Activity Tracker - Error notification",
                     msg='Tracker service failure.')
    raise Exception('Tracker service failure.')
