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
"""Module to define model names for inference."""

# OpenCV models path
FACE_PROTOTEXT = 'deploy.prototxt.txt'
FACE_CAFFEMODEL = 'res10_300x300_ssd_iter_140000.caffemodel'
FACE_LANDMARKS = 'shape_predictor_5_face_landmarks.dat'
TEXT_EAST_DETECTOR = 'frozen_east_text_detection.pb'

# Confidence scores
DETECTED_FACE_CONFIDENCE = 0.7
DETECTED_TEXT_CONFIDENCE = 0.6
