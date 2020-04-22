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

from typing import Tuple

import cv2
import numpy as np

from dlib import rectangle, shape_predictor
from mle.constants import colors, defaults, models
from mle.utils.opencv import display_detection


def convert_to_numpy(predictor: shape_predictor) -> np.ndarray:
  """Converts shape predictor object to a numpy array.

  Converts the facial landmarks shape predictor to a numpy array.

  Args:
    predictor: Dlib's shape predictor object with facial landmarks.
  """
  # You can find the reference code here:
  # https://github.com/qhan1028/Headpose-Detection/blob/5465c1bff0eb68524dfe82608be9aad4aade84e3/headpose.py#L75
  shape_coords = []
  for idx in models.LANDMARKS_2D_INDEX[1]:
    shape_coords += [[predictor.part(idx).x, predictor.part(idx).y]]
  return (np.array(shape_coords).astype(np.int)).astype(np.double)


def calculate_orientation_angles(frame: np.ndarray,
                                 landmarks: np.ndarray) -> Tuple:
  """Calculate face orientation."""
  # You can find the reference code here:
  # https://github.com/qhan1028/Headpose-Detection/blob/5465c1bff0eb68524dfe82608be9aad4aade84e3/headpose.py#L107
  height, width, _ = frame.shape
  focal_length = width
  center_x, center_y = width / 2, height / 2
  camera_matrix = np.array([[focal_length, 0, center_x],
                            [0, focal_length, center_y],
                            [0, 0, 1]], dtype=np.double)
  # This is something which presumes there's no lens distortion.
  lens_distortion_bias = np.zeros((4, 1))
  (_, rotation_vector,
   translation_vector) = cv2.solvePnP(models.LANDMARKS_3D_COORDS[1],
                                      landmarks, camera_matrix,
                                      lens_distortion_bias)
  rotational_matrix = cv2.Rodrigues(rotation_vector)[0]
  projection_matrix = np.hstack((rotational_matrix, translation_vector))
  degrees = -cv2.decomposeProjectionMatrix(projection_matrix)[6]
  return degrees[:, 0]


def detect_faces_using_caffe(frame: np.ndarray,
                             neural_net: np.ndarray,
                             predictor: shape_predictor,
                             min_confidence: float = defaults.MIN_CONFIDENCE,
                             text_color: Tuple = colors.WHITE,
                             box_color: Tuple = colors.RED,
                             box_opacity: float = 0.2,
                             box_thickness: int = 0) -> None:
  """Detect faces in the frame.

  Detect faces in the frame and draw bounding box around the detected
  faces with respective information for the face.

  Args:
    frame: Numpy array of the image frame.
    neural_net: Numpy array of the localized face in the frame.
    predictor: Dbib's shape predictor object with facial landmarks.
    min_confidence: Minimum face detection confidence score.
    text_color: Displayed text color.
    box_color: Box color.
    box_opacity: Box opacity.
    box_thickness: Box thickness.
  """
  detected_faces = []
  height, width, _ = frame.shape
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # Loop over all the localized faces in the frame
  for idx in np.arange(0, neural_net.shape[2]):
    confidence = neural_net[0, 0, idx, 2]
    if confidence > min_confidence:
      bounding_box = neural_net[0, 0, idx, 3:7] * np.array([width, height,
                                                            width, height])
      left, top, right, bottom = bounding_box.astype('int')
      # Calculate Yaw, Pitch & Roll of the face
      landmarks = predictor(gray_frame, rectangle(left, top, right, bottom))
      landmarks = convert_to_numpy(landmarks)
      x, y, z = calculate_orientation_angles(frame, landmarks)
      # Appending coordinates to count the number of detected faces
      detected_faces.append([left, top])
      box_color = colors.COLOR_LIST[len(detected_faces)]
      text = (f'{len(detected_faces):0>3} : {round(confidence * 100, 2)}%')
      display_detection(frame, left, top, right, bottom, text,
                        text_color, box_color, box_opacity, box_thickness)
