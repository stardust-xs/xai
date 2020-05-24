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

"""
Core VZen.
"""

import time
from typing import Sequence, Union

import cv2
import numpy as np
from pkg_resources import resource_filename

from xai.utils.logger import SilenceOfTheLog
from xai.utils.misc import Neo, now, toast, seconds_to_datetime
from xai import __version__

log = SilenceOfTheLog(__file__).log()


class MotherBox(object, metaclass=Neo):
  """
  Mother Box

  The Mother Box class is an auxillary class for different types of
  OpenCV based boxes. These boxes can be used for drawing detections,
  displaying information and/or for visual cues.
  """
  pass
