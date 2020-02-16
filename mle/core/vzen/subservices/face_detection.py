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

import os
from typing import Optional

# TODO(xames3): Remove suppressed pyright warnings.
# pyright: reportMissingImports=false
# pyright: reportMissingTypeStubs=false
import cv2
import dlib
import numpy as np
from imutils import face_utils

from mle.utils.common import mle_path
from mle.utils.opencv import draw_box_with_tuple, rescale
from mle.vars import colors, models

# This is the path where used models are stored.
models_path = os.path.join(mle_path, 'core/vzen/models/')
caffe_model = os.path.join(models_path, models.FACE_CAFFEMODEL)
prototext = os.path.join(models_path, models.FACE_PROTOTEXT)
face_detector = dlib.get_frontal_face_detector()
face_landmarks = dlib.shape_predictor(os.path.join(models_path,
                                                   models.FACE_LANDMARKS))
# Loading serialized CaffeModel for face detection.
# TODO(xames3): Create face recognition caffemodel for XA.
net = cv2.dnn.readNetFromCaffe(prototext, caffe_model)


def detect_faces(frame: np.ndarray,
                 confidence: Optional[float] = models.DETECTED_FACE_CONFIDENCE,
                 landmarks: Optional[bool] = False) -> None:
  """Detect faces in the frame.

  Detect faces in the frame and draw bounding box around the detected
  faces.

  Args:
    frame: Numpy array of the captured frame.
    confidence: Floating (default: 0.7) value for facial confidence.

  Note:
    Faces will only be detected if the confidence scores are above the
    `models.DETECTED_FACE_CONFIDENCE` value.
  """
  height, width = frame.shape[:2]
  # You can learn more about blob here:
  # https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/
  blob = cv2.dnn.blobFromImage(rescale(frame, 300, 300), 1.0, (299, 299),
                               (104.0, 177.0, 123.0))
  # cv2.dnn.blobFromImage(frame, scalefactor, size, mean)
  # frame: Frame which we need to preprocess before feeding to DNN.
  # scalefactor: If we need to scale the blob, alter this parameter.
  # size: Spatial size our CNN expects. Ideal values are 224 x 224,
  #       227 x 227 & 299 x 299.
  # mean: Mean subtraction values.
  net.setInput(blob)
  detected_faces = net.forward()
  # Loop over all the detected faces in the frame.
  for idx in range(detected_faces.shape[2]):
    coords = detected_faces[0, 0, idx, 3:7] * np.array([width, height,
                                                        width, height])
    detected_confidence = detected_faces[0, 0, idx, 2]
    # If the detected faces have confidence score less than
    # DETECTED_FACE_CONFIDENCE threshold, skip it.
    if detected_confidence < confidence:
      continue
    x0, y0, x1, y1 = coords.astype('int')
    draw_box_with_tuple(frame, (x0, y0), (x1, y1))
    if landmarks:
      apply_landmarks(frame)


def apply_landmarks(frame: np.ndarray) -> None:
  """Applies facial landmarks.

  Applies 5 point facial landmarks to the detected face.

  Args:
    frame: Numpy array of the captured frame.
  """
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_detector(gray_frame, 0)
  # Loop over all the faces in the frame.
  for face in faces:
    x, y, _, _ = face_utils.rect_to_bb(face)
    shape = face_landmarks(gray_frame, face)
    shape = face_utils.shape_to_np(shape)
    # Draw detected face landmarks - eyes and nose tip.
    for (x, y) in shape:
      cv2.circle(frame, (x, y), 2, colors.red, -1)


def count_faces(frame: np.ndarray) -> int:
  """Count total number of faces in the frame."""
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  return len(face_detector(gray_frame, 0))
