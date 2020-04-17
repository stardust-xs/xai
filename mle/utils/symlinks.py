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

from mle.constants import models as _models

# Parent directory symlink
parent = os.path.dirname(os.path.dirname(__file__))

# Subsequent symlinks
data = os.path.join(parent, 'data')
files = os.path.join(parent, 'files')
logs = os.path.join(parent, 'logs')
models = os.path.join(parent, 'models')
resources = os.path.join(parent, 'resources')
stats = os.path.join(parent, 'stats')

# Child symlinks
raw = os.path.join(data, 'raw')
test = os.path.join(data, 'test')
train = os.path.join(data, 'train')
validation = os.path.join(data, 'validation')

# Grandchild symlinks
monitor = os.path.join(raw, 'monitor')
vzen = os.path.join(raw, 'vzen')

# Symlinks to save all data for training purposes
usage = os.path.join(monitor, 'usage')
weather = os.path.join(monitor, 'weather')

# Symlinks to all models related to OpenCV
caffemodel = os.path.join(models, _models.CAFFEMODEL)
prototext = os.path.join(models, _models.PROTOTEXT)
landmarks_5_pts = os.path.join(models, _models.LANDMARKS_5_POINTS)
landmarks_68_pts = os.path.join(models, _models.LANDMARKS_68_POINTS)
east_text_detector = os.path.join(models, _models.EAST_TEXT_DETECTOR)
yolov3_config = os.path.join(models, _models.YOLO_V3_CONFIG)
yolov3_weights = os.path.join(models, _models.YOLO_V3_WEIGHTS)

# Symlinks to all resources
arame = os.path.join(resources, 'arame.ttf')
