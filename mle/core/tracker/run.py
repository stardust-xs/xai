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
"""The `mle.core.tracker.run` module.

The core inspiration behind this module is to record the time spent on
each application by the user. This data aims to provide 3 key insights:
	1. How long the user uses a particular application or system?
	2. Recommendations for using applications.
	3. Overusage warning of a particular application.

The module is configured to run at windows boot and keep it running in
background tracking the time spent on each application. And not only
that but, record the usage of each application in a csv file on a daily
basis.

The generated reports are stored under `./mle/data/tracker/` directory
with their respective dates.
"""

import os
import time
from datetime import datetime, timedelta

from win10toast import ToastNotifier

from mle.core.tracker.track import get_active_window, split_time_spent
from mle.utils.common import mle_path
from mle.utils.write import update_data
from mle.vars import dev

toast = ToastNotifier()
header = ['activity', 'app', 'executable', 'user', 'started',
          'stopped', 'spent', 'days', 'hours', 'mins', 'secs']
previous_window = previous_app = previous_exe = previous_user = ''
data_path = os.path.join(mle_path, 'data\\tracker')
csv = ''.join([datetime.now().strftime(dev.CSV_TS_FORMAT), '.csv'])
file = os.path.join(data_path, csv)

try:
	toast.show_toast(title='MLE Activity Tracker', msg='Tracker service started.')
	start_time = datetime.now().replace(microsecond=0)
	# Keep the service running.
	while True:
		active_window, active_app, active_exe, active_user = get_active_window()
		# If the current time exceeds beyond the DAY_LIMIT save new records
		# to new file.
		if datetime.now().strftime(dev.DAY_LIMIT_FORMAT) >= dev.DAY_LIMIT:
			new_date = datetime.now() + timedelta(days=1)
			csv = ''.join([new_date.strftime(dev.CSV_TS_FORMAT), '.csv'])
			file = os.path.join(data_path, csv)
		# Skip Task Switching application.
		if active_window and active_window != 'Task Switching':
			if (previous_window != active_window
					and datetime.now().strftime(dev.DAY_LIMIT_FORMAT) != dev.DAY_LIMIT):
				end_time = datetime.now().replace(microsecond=0)
				total_time = end_time - start_time
				spent_secs = total_time.total_seconds()
				usage = split_time_spent(total_time)
				# Only track applications which are used for more than 1 second.
				if usage != (0, 0, 0, 0):
					update_data(file, header, previous_window, previous_app, 
											previous_exe, previous_user, start_time, end_time,
											spent_secs, usage[0], usage[1], usage[2], usage[3])
					start_time = datetime.now().replace(microsecond=0)
			previous_window = active_window
			previous_app = active_app
			previous_exe = active_exe
			previous_user = active_user
		# Check if the application is changed after 1 second.
		time.sleep(1)
except Exception:
	toast.show_toast(title='MLE Activity Tracker - Error notification',
									 msg='Tracker service failure.')
	raise Exception('Tracker service failure.')
