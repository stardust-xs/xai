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
"""Utility for creating symbolic links between directories & files."""

import os

from mle.vars import models

# Parent directory symlink.
parent_sl = os.path.dirname(os.path.dirname(__file__))

# Subsequent symlinks.
data_sl = os.path.join(parent_sl, 'data')
files_sl = os.path.join(parent_sl, 'files')
models_sl = os.path.join(parent_sl, 'models')
stats_sl = os.path.join(parent_sl, 'stats')

# Child symlinks.
monitor_sl = os.path.join(data_sl, 'monitor')
vzen_sl = os.path.join(data_sl, 'vzen')

# Symlinks to save all data_sl for training purposes.
usage_sl = os.path.join(monitor_sl, 'usage')
weather_sl = os.path.join(monitor_sl, 'weather')
train_faces_sl = os.path.join(vzen_sl, 'train_faces')

# Symlinks to all models related to OpenCV.
caffemodel_sl = os.path.join(models_sl, models.FACE_CAFFEMODEL)
prototext_sl = os.path.join(models_sl, models.FACE_PROTOTEXT)
face_landmarks_sl = os.path.join(models_sl, models.FACE_LANDMARKS)
east_text_detector_sl = os.path.join(models_sl, models.EAST_TEXT_DETECTOR)
face_encodings_sl = os.path.join(models_sl, models.FACE_ENCODINGS)
