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
"""The `mle.core.vzen.follow` module.

The core inspiration behind this module is to use computer vision to
it's full potential and to understand more about image processing and
how different models operate in their own space.
This module will try to perform:
  1. Multiple faces/object detection without affecting the performance.
  2. Motion detection and Human activity detection.

The module should* be able to configured to run at windows boot and stay
running in background or provide some kind of service or let alone run
independently.

Any/All generated reports are stored in `./mle/data/raw/vzen/` with
their respective names & logs under `./mle/logs/follow.log`.
"""

import time

import cv2

from mle.constants import defaults as dx
from mle.core.vzen.subservices.face_detector import detect_faces
from mle.utils.common import log
from mle.utils.common import toast as toast
from mle.utils.opencv import disconnect, rescale

log = log(__file__)

while True:
  try:
    stream = cv2.VideoCapture(0)
    log.info('Vzen service started.')
    toast('MLE VZen', 'VZen service started.')
    time.sleep(2.0)
    # Keep the service running.
    while stream.isOpened():
      _, frame = stream.read()
      frame = rescale(frame, width=400)
      detect_faces(frame)
      # Terminate the stream after pressing 'Esc' key.
      cv2.imshow('MLE VZen', frame)
      if cv2.waitKey(1) & 0xFF == int(27):
        disconnect(stream)
        exit(0)
    else:
      log.warning('VZen service broken.')
      toast('MLE VZen - Warning Notification', 'VZen service broken.')
      time.sleep(dx.EXCEPTION_TIMER)
  except KeyboardInterrupt:
    log.error('VZen service interrupted.')
    toast('MLE VZen - Error Notification', 'VZen service interrupted.')
  except Exception:
    log.critical('Something went wrong with vzen service.')
    toast('MLE VZen - Error Notification',
          'Something went wrong with the service.')
    log.warning('Restarting VZen service.')
    time.sleep(dx.EXCEPTION_TIMER)
