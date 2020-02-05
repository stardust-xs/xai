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
"""The `mle.core.detect.run` module.

The core inspiration behind this module is to use computer vision to
it's full potential and to understand more about image processing and
how different models operate in their own space.
This module will try to perform:
  1. Multiple faces/object detection without affecting the performance.
  2. Motion detection and Human activity detection.

The module should* be able to configured to run at windows boot and stay
running in background or provide some kind of service.

Any/All generated reports are stored in `./mle/data/detect/` with their
respective names.
"""

import os
import time
from datetime import datetime

import cv2
import numpy as np

from mle.utils.common import mle_path, now, toast
from mle.utils.opencv import detect_face, disconnect, rescale
from mle.vars import dev

# This is the path where inferred models are stored.
models_path = os.path.join(mle_path, 'core/detect/models/')
face_caffe_model = os.path.join(models_path, dev.FACE_CAFFEMODEL)
face_prototext = os.path.join(models_path, dev.FACE_PROTOTEXT)
face_net = cv2.dnn.readNetFromCaffe(face_prototext, face_caffe_model)

while True:
  stream = cv2.VideoCapture(0)
  time.sleep(3.0)
  toast('MLE Motion Detector', 'Motion detecting service started.')
  # Keep the service running.
  try:
    while stream.isOpened():
      _, frame = stream.read()
      frame = rescale(frame, width=400)
      frame_height, frame_width = frame.shape[:2]
      face_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                        (300, 300), (104.0, 177.0, 123.0))
      face_net.setInput(face_blob)
      detected_face = face_net.forward()
      for idx in range(detected_face.shape[2]):
        detected_face_confidence = detected_face[0, 0, idx, 2]
        if detected_face_confidence < dev.DETECTED_FACE_CONFIDENCE:
          continue
        face_coords = detected_face[0, 0, idx, 3:7] * np.array([frame_width,
                                                                frame_height,
                                                                frame_width,
                                                                frame_height])
        face_tlx, face_tly, face_brx, face_bry = face_coords.astype('int')
        detect_face(frame, (face_tlx, face_tly), (face_brx, face_bry))
      # Terminate the application after pressing 'Esc' key.
      if cv2.waitKey(5) & 0xFF == int(27):
        disconnect(stream)
        exit(0)
      cv2.imshow('MLE Motion Detector - Live feed', frame)
    else:
      print(f'Stream broke at {datetime.now()}')
      time.sleep(5.0)
  except cv2.error:
    disconnect(stream)
    print('Stream terminated abruptly.')
    # toast('MLE Motion Detector - Error Notification',
    #       'Stream terminated abruptly.')
    raise cv2.error('Something went wrong with OpenCV.')
