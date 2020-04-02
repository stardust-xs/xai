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

# MLE Refresh delay.
# Duration (in secs.) after which MLE refreshes her memory. Lower sleep
# duration provides more granular results. Sleeping after every 1 second
# doesn't affect performance by any means.
REFRESH_TIMER = 1.0

# Critical exception sleep time.
# Duration (in secs.) MLE should wait/sleep before restarting the
# service in a while loop.
EXCEPTION_TIMER = 30.0 

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

# Weather API check timer.
# Duration (in mins.) after which MLE makes an API call for the weather.
WEATHER_CHECK_TIMER = 30.0

# MLE VZen's buffer frame threshold.
# This value defines the number of frames MLE's VZen service should
# process in order to start calculating the FPS & elapsed time of the
# service.
BUFFER_FRAME_THRESHOLD = 120

# MLE's machine learning confidence scores.
# These values are MLE's minimum threshold/confidence scores for making
# a particular prediction. These scores factor in while making an
# accurate prediction.
# Minimum confidence score for determining if the made prediction is a
# face or not.
DETECTED_FACE_CONFIDENCE = 0.3
# Minimum confidence score for determining if the predicted face is of
# XA's or not.
# NOTE: This value is subject to vary/exist depending on the accuracy.
DETECTED_XA_FACE_CONFIDENCE = 0.85

# Train, Test and Validation splits ratio.
# These values decide how the complete dataset needs to be divided into
# proportional parts. For instance, if you 2 directories dir_A & dir_B
# and each directory holds 100 files; then 70% (140 files cumulative of
# both dir_A & dir_B) will be used as the input training data while 15%
# (30 files) will be used for testing & validation purpose.
# Training data split threshold.
TRAIN_SPLIT = 0.7
# Testing & Validation data split threshold.
TEST_SPLIT = VALIDATION_SPLIT = 0.15

# Image dataset target sizes.
# These values represent a sequence of integers in which the image data
# array needs to be resized into. Different image classification models
# have different yet specific target sizes.
# MLE model image data target size.
MLE_IMG_SIZE = (220, 220)
# VGG16 model image data target size.
VGG_IMG_SIZE = [224, 224]

# Image dataset input shape.
# This shape represents height, width and the color channel of an image.
# The width & height should be equal to image's 'target_size'.
MLE_IMG_INPUT_SHAPE = (*MLE_IMG_SIZE, 3)
