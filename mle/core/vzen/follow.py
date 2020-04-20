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
from dlib import shape_predictor

from mle.constants import defaults as dx
from mle.core.vzen.subservices.detector import detect_faces_using_caffe
from mle.utils import symlinks
from mle.utils.common import log, now, seconds_to_datetime, toast
from mle.utils.opencv import disconnect, display_statistics

# Logging MLE's follow module's activities.
log = log(__file__)
net = cv2.dnn.readNetFromCaffe(symlinks.prototext, symlinks.caffemodel)
predictor = shape_predictor(symlinks.landmarks_68_pts)

while True:
  stream = cv2.VideoCapture(0)
  log.info('Vzen service started.')
  toast('MLE VZen', 'VZen service started.', 3.0, False)
  time.sleep(dx.REFRESH_TIMER)
  frame_number = 0
  start = now()
  try:
    # Keep the service running.
    while stream.isOpened():
      _, frame = stream.read()
      height, width, _ = frame.shape
      elapsed_time = seconds_to_datetime((now() - start).seconds)
      statistics = f'{elapsed_time}'
      # Calculate and display statistics.
      if frame_number > dx.BUFFER_FRAMES:
        fps = round((frame_number / (now() - start).seconds), 2)
        statistics = f'{elapsed_time} : {fps} FPS'
      display_statistics(frame, 5, height, statistics)
      # You can learn more about blob here:
      # https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
      net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (299, 299),
                                         (104.0, 177.0, 123.0)))
      detect_faces_using_caffe(frame, net.forward(), predictor)
      # detect_faces1_using_caffe(frame)
      # Terminate the stream after pressing 'Esc' key.
      cv2.imshow('MLE VZen', frame)
      if cv2.waitKey(1) & 0xFF == int(27):
        disconnect(stream)
        log.warning('VZen service terminated.')
        exit(0)
      frame_number += 1
    else:
      log.warning('VZen service broken.')
      toast('MLE VZen - Warning Notification',
            'VZen service broken.', 3.0, False)
      time.sleep(dx.EXCEPTION_TIMER)
  except KeyboardInterrupt:
    log.error('VZen service interrupted.')
    toast('MLE VZen - Error Notification',
          'VZen service interrupted.', 3.0, False)
    exit(0)
  except Exception:
    log.critical('Something went wrong with vzen service.')
    toast('MLE VZen - Error Notification',
          'Something went wrong with the service.', 3.0, False)
    disconnect(stream)
    log.warning('Restarting VZen service.')
    time.sleep(dx.EXCEPTION_TIMER)
