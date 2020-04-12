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
"""A subservice for human detection."""

from typing import Tuple

import cv2
import numpy as np
from imutils.object_detection import non_max_suppression as nms

from mle.constants import colors
from mle.utils.opencv import draw_bounding_box


def detect_humans(frame: np.ndarray,
                  random_detection_color: bool = True,
                  label_color: Tuple = colors.WHITE,
                  label_box_color: Tuple = colors.BLACK,
                  label_box_opacity: float = 0.3,
                  label_box_thickness: int = 1,
                  bounding_box_color: Tuple = colors.YELLOW,
                  bounding_box_thickness: int = 2,
                  bounding_box_opacity: float = 0.1) -> None:
  """Detect humans in the frame.

  Detect humans in the frame and draw bounding box around the detected
  them.

  Args:
    frame: Numpy array of the captured frame.
    random_detection_color: Boolean (default: True) value to use random
                            colors for each detected human.
    label_color: Label color (default: white).
    label_box_color: Label box (default: black) color.
    label_box_opacity: Opacity (default: 0.3) of the label box.
    label_box_thickness: Thickness (default: 1) of the label box.
    bounding_box_color: Bounding box (default: red) color.
    bounding_box_thickness: Thickness (default: 2) of the bounding box.
    bounding_box_opacity: Opacity (default: 0.1) of the detected region.
  """
  hog = cv2.HOGDescriptor()
  hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
  humans, _ = hog.detectMultiScale(frame, winStride=(8, 8),
                                         padding=(8, 8), scale=1.05)
  temp = np.array([[x0, y0, x0 + x1, y0 + y1] for (x0, y0, x1, y1) in humans])
  bounding_boxes = nms(temp, probs=None, overlapThresh=0.65)
  if random_detection_color:
    bounding_box_color = colors.COLOR_LIST[len(bounding_boxes)]
    label_box_color = bounding_box_color
  label = f'ID : #{len(bounding_boxes)}'
  # Draw a bounding box across the detected person and add the
  # corresponding label relative to it.
  for (x0, y0, x1, y1) in bounding_boxes:
    draw_bounding_box(frame, (x0, y0), (x1, y1), label, label_color,
                      label_box_color, label_box_opacity,
                      label_box_thickness, bounding_box_color,
                      bounding_box_opacity, bounding_box_thickness)
