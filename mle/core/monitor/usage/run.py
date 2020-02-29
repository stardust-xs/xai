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
"""The `mle.core.monitor.usage.run` module.

The core inspiration behind this module is to record the time spent on
each application by the user. This data aims to provide 3 key insights:
  1. How long the user uses a particular application or system?
  2. Application recommendations specifically catered for the user.
  3. Overusage warning of a particular application.

The module is configured to run at windows boot and keep it running in
background monitoring the time spent on each application. And not only
that but, record the usage of each application in a csv file on a daily
basis.

The generated reports are stored in `./mle/data/raw/monitor/usage/` with
their respective dates.
"""

import os
import time
from datetime import datetime, timedelta

from mle.constants import defaults
from mle.core.monitor.usage.app import get_active_window, split_time_spent
from mle.utils import symlinks
from mle.utils.common import now, toast
from mle.utils.write import update_data

header = ['activity', 'app', 'executable', 'user', 'started',
          'stopped', 'spent', 'days', 'hours', 'mins', 'secs']
previous_window = previous_app = previous_exe = previous_user = None

try:
  toast('MLE Application Monitor', 'Application monitoring service started.')
  start_time = now()
  # Keep the service running.
  while True:
    active_window, active_app, active_exe, active_user = get_active_window()
    # If current time exceeds beyond DAY_LIMIT, save records to new file.
    if datetime.now().strftime(defaults.DAY_LIMIT_FORMAT) >= defaults.DAY_LIMIT:
      timestamp = datetime.now() + timedelta(days=1)
    else:
      timestamp = datetime.now()
    csv = ''.join([timestamp.strftime(defaults.CSV_TS_FORMAT), '.csv'])
    file = os.path.join(symlinks.usage, csv)
    # Skip Task Switching application.
    if active_window and active_window != 'Task Switching':
      if (previous_window != active_window
          and datetime.now().strftime(defaults.DAY_LIMIT_FORMAT)
          != defaults.DAY_LIMIT):
        end_time = now()
        total_time = end_time - start_time
        spent_secs = total_time.total_seconds()
        usage = split_time_spent(total_time)
        # Only track applications which are used for more than 1 second.
        if usage != (0, 0, 0, 0):
          try:
            update_data(file, header, previous_window, previous_app,
                        previous_exe, previous_user, start_time, end_time,
                        spent_secs, usage[0], usage[1], usage[2], usage[3])
          except PermissionError:
            toast('MLE Application Monitor - Error Notification',
                  'File accessed by another application.')
          finally:
            start_time = now()
      previous_window = active_window
      previous_app = active_app
      previous_exe = active_exe
      previous_user = active_user
    # Check if the application is changed after 1 second.
    time.sleep(1)
except Exception:
  toast('MLE Application Monitor - Error Notification',
        'Something went wrong with the service.')
