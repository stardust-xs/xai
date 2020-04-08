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
from mle.utils.opencv import draw_bounding_box


def convert_to_numpy(face_predictor: shape_predictor) -> np.ndarray:
  """Converts the DLib's shape predictor object to a numpy array.

  Converts the facial landmarks shape predictor to a Numpy array.

  Args:
    face_predictor: DLib's shape predictor object with facial landmarks.
  """
  # You can find the reference code here:
  # https://github.com/qhan1028/Headpose-Detection/blob/5465c1bff0eb68524dfe82608be9aad4aade84e3/headpose.py#L75
  shape_coords = []
  for idx in models.LANDMARKS_2D_INDEX_LIST[1]:
    shape_coords += [[face_predictor.part(idx).x, face_predictor.part(idx).y]]
  return (np.array(shape_coords).astype(np.int)).astype(np.double)


def calculate_facial_orientation_angles(frame: np.ndarray,
                                        face_landmarks: np.ndarray) -> Tuple:
  """Calculate orientation of the face with respect to the camera.

  Calculates the orientation of the face using numpy data from the
  facial landmarks captured with respect to the camera.

  Args:
    frame: Numpy array of the captured frame.
    face_landmarks: Numpy array of the possible facial landmarks.

  Returns:
    Tuple of parameters which I really don't have much idea about.

  TODO (xames3): Add proper docstring for this function.
  """
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
  # Rotational & Translational vector.
  (_, rotation_vector,
   translation_vector) = cv2.solvePnP(models.LANDMARKS_3D_COORDS_LIST[1],
                                      face_landmarks, camera_matrix,
                                      lens_distortion_bias)
  rotational_matrix = cv2.Rodrigues(rotation_vector)[0]
  projection_matrix = np.hstack((rotational_matrix, translation_vector))
  degrees = -cv2.decomposeProjectionMatrix(projection_matrix)[6]
  return degrees[:, 0]


def detect_faces(frame: np.ndarray,
                 localized_faces: np.ndarray,
                 face_predictor: shape_predictor,
                 confidence: float = defaults.DETECTED_FACE_CONFIDENCE,
                 random_detection_color: bool = True,
                 description_text_color: Tuple = colors.WHITE,
                 description_box_color: Tuple = colors.BLACK,
                 description_box_opacity: float = 0.3,
                 description_box_thickness: int = 1,
                 bounding_box_color: Tuple = colors.RED,
                 bounding_box_opacity: float = 0.3,
                 bounding_box_thickness: int = 2) -> None:
  """Detect faces in the frame.

  Detect faces in the frame and draw bounding box around the detected
  faces with respective information for the face.

  Args:
    frame: Numpy array of the captured frame.
    localized_faces: Coordinates of the localized face in the frame.
    face_predictor: DLib's shape predictor object with facial landmarks.
    confidence: Floating (default: 0.4) value for facial confidence.
    random_detection_color: Boolean (default: True) value to use random
                            colors for each detected face.
    description_text_color: Description text color (default: white).
    description_box_color: Description box (default: black) color.
    description_box_opacity: Opacity (default: 0.3) of the description
                             box.
    description_box_thickness: Thickness (default: 1) of the description
                               box.
    bounding_box_color: Bounding box (default: red) color.
    bounding_box_thickness: Thickness (default: 2) of the bounding box.
    bounding_box_opacity: Opacity (default: 0.3) of the detected region.

  Note:
    Faces will only be detected if the confidence scores are above the
    'defaults.DETECTED_FACE_CONFIDENCE' value.
  """
  detected_faces = []
  height, width, _ = frame.shape
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # Loop over all the localized faces in the frame.
  for idx in np.arange(0, localized_faces.shape[2]):
    detection_confidence = localized_faces[0, 0, idx, 2]
    # If the localized faces have confidence score more than
    # DETECTED_FACE_CONFIDENCE, draw bounding boxes around them.
    if detection_confidence > confidence:
      bounding_box = localized_faces[0, 0, idx, 3:7] * np.array([width, height,
                                                                 width, height])
      x0, y0, x1, y1 = bounding_box.astype('int')
      # Calculate Yaw, Pitch & Roll of the face.
      face_landmarks = face_predictor(gray_frame, rectangle(x0, y0, x1, y1))
      face_landmarks = convert_to_numpy(face_landmarks)
      x, y, z = calculate_facial_orientation_angles(frame, face_landmarks)
      # Appending coordinates to count the number of detected faces.
      detected_faces.append([x0, y0])
      if random_detection_color:
        bounding_box_color = colors.COLOR_LIST[len(detected_faces)]
        description_box_color = bounding_box_color
      detection_confidence = round(detection_confidence * 100, 2)
      description = (f'ID : #{len(detected_faces)}\nSCORE : '
                     f'{detection_confidence}%\nX : {x:+06.2f} Y : {y:+06.2f} '
                     f'Z : {z:+06.2f}')
      # Draw a bounding box across the detected face and add the
      # corresponding information for it.
      draw_bounding_box(frame, (x0, y0), (x1, y1), description,
                        description_text_color, description_box_color,
                        description_box_opacity, description_box_thickness,
                        bounding_box_color, bounding_box_opacity,
                        bounding_box_thickness)
