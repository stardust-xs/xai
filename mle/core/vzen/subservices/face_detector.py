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
"""A subservice for face detection and recognition."""

from typing import Tuple, Union

import cv2
import numpy as np
from imutils import face_utils

from dlib import get_frontal_face_detector, shape_predictor
from mle.constants import colors, defaults
from mle.utils import symlinks
from mle.utils.opencv import draw_bounding_box, rescale


def detect_faces(frame: np.ndarray,
                 confidence: float = defaults.DETECTED_FACE_CONFIDENCE,
                 bounding_box_color: Tuple = colors.RED,
                 bounding_box_thickness: int = 2,
                 label_color: Tuple = colors.WHITE,
                 label_box_color: Tuple = colors.BLACK,
                 label_box_opacity: Union[float, int] = 0.3,
                 label_box_thickness: int = 1,
                 label_box_overlay_color: Tuple = colors.BLACK,
                 bounding_box_opacity: Union[float, int] = 0.1,
                 bounding_box_overlay_color: Tuple = colors.RED) -> None:
  """Detect faces in the frame.

  Detect faces in the frame and draw bounding box around the detected
  faces.

  Args:
    frame: Numpy array of the captured frame.
    confidence: Floating (default: 0.7) value for facial confidence.
    label_color: Label color (default: white).
    bounding_box_color: Bounding box (default: yellow) color.
    bounding_box_thickness: Thickness (default: 1) of the bounding box.
    bounding_box_opacity: Opacity (default: 0.2) of the detected region.
    bounding_box_overlay_color: Overlayed color (default: red).

  Note:
    * Faces will only be detected if the confidence scores are above the
      'defaults.DETECTED_FACE_CONFIDENCE' value.
    * Using landmarks can slow down the stream and the overall
      usability. Hence, use sparingly!
  """
  label = 'Detected face'
  height, width = frame.shape[:2]
  # You can learn more about blob here:
  # https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
  blob = cv2.dnn.blobFromImage(rescale(frame, 300, 300), 1.0, (299, 299),
                               (104.0, 177.0, 123.0))
  # Loading serialized CaffeModel for face detection.
  net = cv2.dnn.readNetFromCaffe(symlinks.prototext, symlinks.caffemodel)
  net.setInput(blob)
  detected_faces = net.forward()
  # Loop over all the detected faces in the frame.
  for idx in range(detected_faces.shape[2]):
    coords = detected_faces[0, 0, idx, 3:7] * np.array([width, height,
                                                        width, height])
    detected_confidence = detected_faces[0, 0, idx, 2]
    # If the detected faces have confidence score more than
    # DETECTED_FACE_CONFIDENCE, draw bounding boxes around them.
    if detected_confidence > confidence:
      x0, y0, x1, y1 = coords.astype('int')
      # Draw a bounding box across the detected face and add the
      # corresponding label relative to it.
      draw_bounding_box(frame, (x0, y0), (x1, y1), detected_confidence, label,
                        bounding_box_color, bounding_box_thickness, label_color,
                        label_box_color, label_box_opacity, label_box_thickness,
                        label_box_overlay_color, bounding_box_opacity,
                        bounding_box_overlay_color)


def apply_landmarks(frame: np.ndarray,
                    radius: int = 2,
                    landmarks_color: Tuple = colors.MEDIUM_VIOLET_RED) -> None:
  """Applies facial landmarks.

  Applies 5 point facial landmarks to the detected face instead of 68.
  This implementation is based on Adrian Rosebrock's, `(Faster) Facial
  landmark detector with dlib` blog.

  Args:
    frame: Numpy array of the captured frame.
    radius: Radius of the circle representing the landmark point.
    landmarks_color: Landmark (default: medium violet red) color.

  Note:
    Using landmarks can slow down the stream and the overall usability.
    Hence, use sparingly!
  """
  # You can find the reference code here:
  # https://www.pyimagesearch.com/2018/04/02/faster-facial-landmark-detector-with-dlib/
  detector = get_frontal_face_detector()
  landmarks = shape_predictor(symlinks.face_landmarks)
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = detector(gray_frame, 0)
  # Use len(faces) to get the count of faces in the frame.
  # Loop over all the faces in the frame.
  for face in faces:
    x, y, _, _ = face_utils.rect_to_bb(face)
    shape = landmarks(gray_frame, face)
    shape = face_utils.shape_to_np(shape)
    # Draw detected face landmarks -> eyes and nose tip.
    for (x, y) in shape:
      cv2.circle(frame, (x, y), radius, landmarks_color, -1)
