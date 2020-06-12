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

import os
import time
from typing import Sequence, Union

import cv2
import numpy as np
import psutil
from mtcnn import MTCNN

from xai import __version__
from xai.utils.logger import SilenceOfTheLog
from xai.utils.misc import now, resolve_size, seconds_to_datetime, toast

log = SilenceOfTheLog(__file__).log()

face_detector = MTCNN(min_face_size=31)


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


def detect_faces(frm: np.ndarray,
                 cnf: float = 0.87,
                 fcr: Sequence = (255, 255, 255),
                 tcr: Sequence = (255, 255, 255),
                 bcr: Sequence = (0, 0, 0),
                 alp: float = 0.5,
                 thk: int = 1,
                 fnt: Union[int, str] = cv2.FONT_HERSHEY_SIMPLEX,
                 lnt: Union[int, str] = cv2.LINE_AA) -> None:
  """
  Detect faces in a frame using MTCNN face detector.

  Args:
    frm: Numpy array of the image frame.
    cnf: Minimum confidence score for detection.
    fcr: Face detection bounding box color.
    tcr: Text color.
    bcr: Text box color.
    alp: Text box opacity OR alpha channel.
    thk: Text box thickness.
    fnt: OpenCV font to use.
    lnt: OpenCV line type.
  """
  # MTCNN needs RGB frame, since OpenCV reads every frame in BGR format
  # this conversion is needed.
  rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
  faces = face_detector.detect_faces(rgb)

  cnt = 1
  msk = frm.copy()

  for face in faces:
    # Considering detections which have confidence score higher than the
    # set threshold.
    if face['confidence'] > cnf:
      lft, top, rgt, btm = face['box']
      lft, top = abs(lft), abs(top)
      rgt, btm = lft + rgt, top + btm
      adj = int((rgt - lft) * 0.03)

      txt = f'CNT : {cnt:>02}\nCNF : {round(face["confidence"] * 100, 2)}%'

      cv2.addWeighted(msk, alp, frm, 1 - alp, 0, frm)
      cv2.rectangle(frm, (lft, top), (rgt, btm), fcr, thk, lnt)
      smart_text_box(frm, lft, top, rgt, btm, txt,
                     tcr, bcr, alp, thk, fnt, lnt)

      # Drawing facial landmarks - Eyes, Nose & Mouth.
      for pts in face['keypoints'].values():
        if adj > 0:
          cv2.rectangle(frm,
                        (pts[0] - adj, pts[1] - adj),
                        (pts[0] + adj, pts[1] + adj),
                        (0, 255, 0), thk, lnt)
        else:
          cv2.circle(frm, pts, 1, (5, 5, 170), -1, lnt)

      cnt += 1


class GodsEye(object):
  """Docstring to be updated."""

  def __init__(self, src: Union[int, str] = 0, scl: float = 0.75) -> None:
    """Docstring to be updated."""
    self._service = 'X.AI VZen'
    self._version = f'{self._service} v{__version__}'

    self._src = src
    self._scl = scl
    self._bfr = 30
    self._frm_num = 1

    self._log = log
    self._refresh = 1.0
    self._exception = 30.0

    self._pid = os.getpid()

  def perceive_everything(self) -> None:
    """Perceive everything."""
    # Keep the service running irrespective of encountered exceptions.
    # This while loop ensures that the block keeps running even if an
    # exception has raised. The block suspends for 30 secs. when a
    # critical exception is raised.
    while True:
      self._log.info('Initialized VZen service.')
      toast(f'{self._service}', 'Initialized VZen service.')
      started = now()

      self._stm = cv2.VideoCapture(self._src)

      try:
        # Similar to the parent loop, this loop keeps the block running
        # forever but breaks when any exceptions are raised.
        while self._stm.isOpened():
          val, frm = self._stm.read()

          # Terminate the session if 'Esc' key is pressed or if the
          # frame is in valid.
          if cv2.waitKey(1) & 0xFF == int(27) or not val:
            self._stm.release()
            cv2.destroyAllWindows()
            exit(0)

          frm = cv2.resize(frm, None, fx=self._scl, fy=self._scl,
                           interpolation=cv2.INTER_AREA)

          ram = f'RAM : {resolve_size(psutil.virtual_memory().used)}'
          smart_text_box(frm, 5, frm.shape[0] - 30, 0, 0, ram)

          # Records the time the session has started. This lets X.AI to
          # calculate the FPS at which the camera(s) are recording.
          elapsed = seconds_to_datetime((now() - started).seconds)
          fps_stats = f'{elapsed}'

          # Calculate the FPS of the perceived vision. The FPS is
          # calculated after the perceived vision is activated
          if self._frm_num > self._bfr:
            fps = round(self._frm_num / (now() - started).seconds)
            fps_stats = f'{elapsed} : {fps:>02} FPS'

          fps_stats = f'{self._version}\n{fps_stats}'
          smart_text_box(frm, 5, 5, 0, 0, fps_stats)

          detect_faces(frm)

          cv2.imshow(self._service, frm)
          self._frm_num += self._refresh
        else:
          self._log.warning('VZen service broke while streaming.')
          toast(f'{self._service}', 'VZen service broke.')
          time.sleep(self._exception)
      except KeyboardInterrupt:
        self._log.warning('VZen service interrupted.')
        toast(f'{self._service}', 'VZen service interrupted.')
      except Exception as _error:
        self._log.exception(_error)
        toast(f'{self._service}', 'VZen service stopped abruptly.')
      finally:
        # Sleep for 30 seconds if any exception occurs before restarting
        # the service.
        time.sleep(self._exception)


if __name__ == '__main__':
  GodsEye().perceive_everything()
