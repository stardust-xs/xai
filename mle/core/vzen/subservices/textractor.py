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
"""A subservice for detecting and extracting text in frame."""

import os
from typing import Optional

import cv2
import numpy as np
from imutils.object_detection import non_max_suppression

from mle.utils.common import mle_path
from mle.utils.opencv import simplify_detections, draw_box_with_tuple, rescale
from mle.vars import models

# This is the path where used models are stored.
models_path = os.path.join(mle_path, 'core/vzen/models/')
east_model = os.path.join(models_path, models.TEXT_EAST_DETECTOR)
frame_w, frame_h = updated_w, updated_h = ratio_w, ratio_h = None, None
layers = ['feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3']
# Loading serialized CaffeModel for face detection.
net = cv2.dnn.readNet(east_model)


def detect_text(frame: np.ndarray,
                confidence: Optional[float] = models.DETECTED_FACE_CONFIDENCE
                ) -> None:
  height, width = frame.shape[:2]
  original_frame = frame.copy()
  # https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
  blob = cv2.dnn.blobFromImage(image=rescale(frame, 300, 300),
                               scalefactor=1.0,
                               mean=(123.68, 116.78, 103.94),
                               swapRB=True,
                               crop=False)
  net.setInput(blob)
  scores, geometry = net.forward(layers)
  rectangles, confidences = simplify_detections(scores, geometry, confidence)
  coords = non_max_suppression(np.array(rectangles), confidences)
  # Loop over all the detected text in the frame.
  for x0, y0, x1, y1 in coords:
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    # x0, y0, x1, y1 = coords.astype('int')
    draw_box_with_tuple(original_frame, (x0, y0), (x1, y1))
