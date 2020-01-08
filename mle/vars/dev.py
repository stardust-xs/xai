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
"""The ``mle.vars.dev`` module.

This module manages variables for the project development.

These are pre-defined values to build a composite development
environment, which can affect and/or update all the depending values at
once. These values should be checked and updated periodically.

"""
# Local time zone details
# You can find all the choices here:
# https://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Kolkata'

# Language used by the project
# You can find all the choices here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANG_CODE = 'en-gb'

# Default encoding used for all read-write objects.
DEF_CHARSET = 'utf-8'

# Supported browsers
BROWSERS = ['Firefox', 'Google Chrome', 'Internet Explorer', 'Microsoft Edge']

# Tracker limit for a day
DAY_LIMIT = '23:59:59'

# Tracker day limit format
DAY_LIMIT_FORMAT = '%H:%M:%S'

# Csv named format
CSV_TS_FORMAT = '%d_%m_%y'

# Default urls
# This url is used for checking if the internet connection exists.
# Any valid url will work.
PING_URL = 'www.google.com'
PING_PORT = 80

# Using ``DarkSky.net`` for making weather related API calls.
WEATHER_URL = 'https://api.darksky.net/forecast/'
