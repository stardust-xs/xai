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

from typing import Sequence, Union

import cv2
import numpy as np

from xai import __version__
from xai.utils.logger import SilenceOfTheLog

log = SilenceOfTheLog(__file__).log()


def smart_text_box(frm: np.ndarray,
                   lft: Union[float, int],
                   top: Union[float, int],
                   rgt: Union[float, int],
                   btm: Union[float, int],
                   txt: str,
                   tcr: Sequence = (255, 255, 255),
                   bcr: Sequence = (0, 0, 0),
                   alp: float = 0.5,
                   thk: int = 1,
                   fnt: Union[int, str] = cv2.FONT_HERSHEY_SIMPLEX,
                   lnt: Union[int, str] = cv2.LINE_AA) -> None:
  """
  Display information about the detections like confidence, count, etc.
  in an OpenCV rectangular box relative to the detected object. Random
  information like version, elapsed time, fps, etc. can also be shown
  using this function.

  Args:
    frm: Numpy array of the image frame.
    lft: Left coordinate value.
    top: Top coordinate value.
    rgt: Right coordinate value.
    btm: Bottom coordinate value.
    txt: Text to be displayed.
    tcr: Text color.
    bcr: Text box color.
    alp: Text box opacity OR alpha channel.
    thk: Text box thickness.
    fnt: OpenCV font to use.
    lnt: OpenCV line type.
  """
  lft, top, rgt, btm = tuple(map(round, (lft, top, rgt, btm)))

  txt = txt.upper()
  brk_cnt = txt.count('\n')
  adj = max([idx for idx in txt.split('\n')], key=lambda x: len(x))

  # Default position of the smart text box is at the top-right side
  # of the detection.
  x3, y3 = (rgt + 5), (top + 25)

  # If bounding box is at the left edge of the view - display the text
  # box at the left edge. If bounding box is at the right edge of the
  # view - display the text box at the left side. This ensures the
  # smart text box won't go beyond the horizontal view.
  if x3 < 0:
    x3 = 0
  elif (x3 + (len(adj) * 7) > frm.shape[1]):
    x3 = lft - (len(adj) * 7 + 24)

  # If the bounding box is high up towards the top, display the text
  # box at the bottom of bounding box. This ensures the bounding box
  # won't go beyond the vertical view.
  if y3 < 30:
    x3 = rgt if x3 < 0 else lft
    y3 = btm + 30

  # NOTE: These adjustments are subjective and may vary in future.
  x4, y4 = int(x3), int(y3 - 25)
  x5, y5 = int(x3 + 19 + (len(adj) * 7)), int((y3 + brk_cnt * 20) - 1)

  mask = frm.copy()
  cv2.rectangle(mask, (x4, y4), (x5, y5), bcr, -1)
  cv2.addWeighted(mask, alp, frm, 1 - alp, 0, frm)

  for idx in txt.split('\n'):
    # 0.4 is the font size.
    cv2.putText(frm, idx, (int(x3 + 7), int(y3 - 9)), fnt, 0.4, tcr, thk, lnt)
    y3 = y3 + 20
