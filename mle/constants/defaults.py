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
"""Module to define default values for development."""

# Default encoding used for all read-write operations.
# UTF-8 is one of the most commonly used encoding, other encodings can
# be used if required.
DEF_CHARSET = 'utf-8'

# Monitoring limit timestamp for the day. 
# Any monitored activities after this limit will log the entries into a
# new file.
DAY_LIMIT = '23:59:59'

# Timestamp format for 'strftime()' method. 
# This needs to be similar to the format used by DAY_LIMIT.
DAY_LIMIT_FORMAT = '%H:%M:%S'

# This value defines how the output CSV files are going to be stored in
# the respective directories. Currently, '01_01_20.csv' format is used.
CSV_TS_FORMAT = '%d_%m_%y'

# This url is used for checking if the internet connection exists or
# not. The ping url can be any valid url/link on the internet. 
PING_URL = 'www.google.com'

# Port used by HTTP.
# You can read more about the ports here:
# https://geekflare.com/default-port-numbers/
PING_PORT = 80

# This value defines website used for making weather related API calls.
# Please note that for making any API request, an account (free/paid) on
# the below mentioned website is required.
WEATHER_URL = 'https://api.darksky.net/forecast/'

# Confidence scores
DETECTED_FACE_CONFIDENCE = 0.7
DETECTED_TEXT_CONFIDENCE = 0.6

# Train, Test and Validation splits percentages.
SMALL_TRAIN_SPLIT = 0.3
TEST_SPLIT = VALIDATION_SPLIT = 0.2

# Face dataset image size required by VGG16 model.
VGG_IMG_SIZE = [224, 224]
