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
"""Module to define locally stored model references."""

import numpy as np

# OpenCV model names.
EAST_TEXT_DETECTOR = 'frozen_east_text_detection.pb'
PROTOTEXT = 'deploy.prototxt.txt'
CAFFEMODEL = 'res10_300x300_ssd_iter_140000.caffemodel'
LANDMARKS_5_POINTS = 'shape_predictor_5_face_landmarks.dat'
LANDMARKS_68_POINTS = 'shape_predictor_68_face_landmarks.dat'
YOLO_V3_CONFIG = 'yolov3_tiny.cfg'
YOLO_V3_CONFIG = 'yolov3_training.cfg'
YOLO_V3_WEIGHTS = 'yolov3_mle_face_416x416_3000.weights'
# YOLO_V3_WEIGHTS = 'yolov3-tiny-obj_last.weights'

# 2d facial landmark position list.
LANDMARKS_2D_INDEX = [
  [30, 8, 36, 45, 48, 54],
  [33, 17, 21, 22, 26,
   36, 39, 42, 45, 31,
   35, 48, 54, 57, 8],
  [33, 36, 39, 42, 45]
]

# 3D facial landmarks coordinates.
LANDMARKS_3D_COORDS = [
  np.array([[0.0000000,  0.000000,   0.00000],
            [0.0000000, -8.250000,  -1.62500],
            [-5.625000,  4.250000,  -3.37500],
            [5.6250000,  4.250000,  -3.37500],
            [-3.750000, -3.750000,  -3.12500],
            [3.7500000, -3.750000,  -3.12500]], dtype=np.double),
  np.array([[0.0000000,  0.000000,  6.763430],
            [6.8258970,  6.760612,  4.402142],
            [1.3303530,  7.122144,  6.903745],
            [-1.330353,  7.122144,  6.903745],
            [-6.825897,  6.760612,  4.402142],
            [5.3114320,  5.485328,  3.987654],
            [1.7899300,  5.393625,  4.413414],
            [-1.789930,  5.393625,  4.413414],
            [-5.311432,  5.485328,  3.987654],
            [2.0056280,  1.409845,  6.165652],
            [-2.005628,  1.409845,  6.165652],
            [2.7740150, -2.080775,  5.048531],
            [-2.774015, -2.080775,  5.048531],
            [0.0000000, -3.116408,  6.097667],
            [0.0000000, -7.415691,  4.070434]], dtype=np.double),
  np.array([[0.0000000,  0.000000,  6.763430],
            [5.3114320,  5.485328,  3.987654],
            [1.7899300,  5.393625,  4.413414],
            [-1.789930,  5.393625,  4.413414],
            [-5.311432,  5.485328,  3.987654]], dtype=np.double)
]
