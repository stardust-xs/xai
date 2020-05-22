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
Core VZen recognition.

Performs recognition, tracking and motion analysis based on the camera
input.
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
  """Auxillary class for different type of boxes."""

  _fnt = cv2.FONT_HERSHEY_SIMPLEX
  _lnt = cv2.LINE_AA

  def __init__(self) -> None:
    """Create a new MotherBox object."""
    pass

  def info(self, frm: np.ndarray, lft: Union[float, int],
           top: Union[float, int], btm: Union[float, int], inf: str,
           txt: Sequence = (255, 255, 255), box: Sequence = (0, 0, 0),
           alp: float = 0.3, thk: int = 1) -> None:
    """
    Display information in a box relative to the detection. This box
    displays textual informations like statistics, label/name,
    confidence score, etc. for the detection.

    Args:
      frm: Numpy array of the image frame.
      lft: Left coordinate value.
      top: Top coordinate value.
      btm: Bottom coordinate value.
      inf: Information to be displayed.
      txt: Text color.
      box: Bounding box color.
      alp: Bounding box opacity OR alpha channel.
      thk: Bounding box thickness.
    """
    lft, top, btm = int(lft), int(top), int(btm)

    adj = max([idx for idx in inf.split('\n')], key=lambda x: len(x))
    brk_cnt = inf.count('\n')

    # Position of the box by default.
    # Start from the X - coordinate, just above the bounding box.
    x3, y3 = lft, (top - (5 + brk_cnt * 20))

    # If bounding box is at the left edge of the view - display the text
    # box at the left edge. If bounding box is at the right edge of the
    # view - display the text box at the right edge by considering the
    # text as well. This ensures the bounding box won't go beyond the
    # horizontal view.
    if x3 < 0:
      x3 = 0
    elif (x3 + 10 + (len(adj) * 7) > frm.shape[1]):
      x3 = x3 - (x3 + 10 + len(adj) * 7 - (frm.shape[1])) - 10

    # If the bounding box is high up towards the top, display the text
    # box at the bottom of bounding box. This ensures the bounding box
    # won't go beyond the vertical view.
    if y3 < 30:
      y3 = btm + 30

    # NOTE: These adjustments are subjective and may vary in future.
    x4, y4 = int(x3), int(y3 - 25)
    x5, y5 = int(x3 + 14 + (len(adj) * 7)), int((y3 + brk_cnt * 20) - 1)

    mask = frm.copy()
    cv2.rectangle(mask, (x4, y4), (x5, y5), box, -1)
    cv2.addWeighted(mask, alp, frm, 1 - alp, 0, frm)

    for idx in inf.split('\n'):
      cv2.putText(frm, idx, (int(x3 + 7), int(y3 - 9)),
                  self._fnt, 0.4, txt, lineType=self._lnt)
      y3 = y3 + 20

  def bbox(self, frm: np.ndarray, lft: Union[float, int],
           top: Union[float, int], rgt: Union[float, int],
           btm: Union[float, int], inf: str, txt: Sequence = (255, 255, 255),
           box: Sequence = (0, 0, 0), alp: float = 0.3, thk: int = 1) -> None:
    """
    Draw a bounding box around the detected object.

    Args:
      frm: Numpy array of the image frame.
      lft: Left coordinate value.
      top: Top coordinate value.
      rgt: Right coordinate value.
      btm: Bottom coordinate value.
      inf: Information to be displayed.
      txt: Text color.
      box: Bounding box color.
      alp: Bounding box opacity OR alpha channel.
      thk: Bounding box thickness.
    """
    lft, top, rgt, btm = int(lft), int(top), int(rgt), int(btm)

    cv2.rectangle(frm, (lft, top), (rgt, btm), box, thk, self._lnt)
    self.info(frm, lft, top, btm, inf, txt, box, alp, thk)


class Predetecognition(MotherBox, metaclass=Neo):
  """Core class for making detections, predictions & recognition."""

  _clr = np.random.randint(0, 255, size=(10, 3))

  def __init__(self) -> None:
    """Create a new Predetecognition object."""
    pass

  def faces(self, frm: np.ndarray, dtn: np.ndarray, conf: float = 0.4,
            txt: Sequence = (255, 255, 255), box: Sequence = (255, 255, 255),
            alp: float = 0.3, thk: int = 1) -> None:
    """Detect faces."""
    h, w, _ = frm.shape
    raw = []

    for idx in np.arange(0, dtn.shape[2]):
      _conf = dtn[0, 0, idx, 2]

      if _conf > conf:
        _box = dtn[0, 0, idx, 3:7] * np.array([w, h, w, h])
        lft, top, rgt, btm = _box.astype('int')
        raw.append(lft)
        inf = f'{round(_conf * 100, 2)}%'
        # box = tuple(self._clr[len(raw)])
        # print(box)
        super().bbox(frm, lft, top, rgt, btm, inf, txt, box, alp, thk)


class VisualizeEnvironment(Predetecognition, metaclass=Neo):
  """Core class for visualizing environment."""

  def __init__(self, src: Union[int, str] = 0):
    """Create a new VisualizeEnvironment object."""
    self._service_name = 'X.AI VZen'
    self._version = f'{self._service_name} v{__version__}'

    self._src = src
    self._buffer = 30
    self._frame_num = 0

    self._refresh = 1.0
    self._exception = 30.0

    self._log = log
    self._pdr = super()

    self._proto = resource_filename('xai', '/models/deploy.prototxt.txt')
    self._caffe = resource_filename('xai', '/models/res10_300x300.caffemodel')
    self._net = cv2.dnn.readNetFromCaffe(self._proto, self._caffe)

  def release(self, stream: np.ndarray) -> None:
    """Disconnect stream & release cv2 object."""
    stream.release()
    cv2.destroyAllWindows()

  def perceive(self) -> None:
    """Perceive environment."""
    # Keep the service running irrespective of encountered exceptions.
    # This while loop ensures that the block keeps running even if an
    # exception has raised. The block suspends for 30 secs. when a
    # critical exception is raised.
    while True:
      self._log.info('Initialized VZen service.')
      toast(f'{self._service_name}', 'Initialized VZen service.')
      started = now()

      self._stream = cv2.VideoCapture(self._src)

      try:
        # Similar to the parent loop, this loop keeps the block running
        # forever but breaks when any exceptions are raised.
        while self._stream.isOpened():
          _, frame = self._stream.read()
          _h, _w, _ = frame.shape

          # Records the time the session has started. This lets X.AI to
          # calculate the FPS at which the camera(s) are recording.
          elapsed = seconds_to_datetime((now() - started).seconds)
          stats = f'{elapsed}'

          # Calculate the FPS of the perceived vision. The FPS is
          # calculated after the perceived vision is activated 
          if self._frame_num > self._buffer:
            fps = round((self._frame_num / (now() - started).seconds), 2)
            stats = f'{elapsed} : {fps} FPS'

          self._pdr.info(frame, 5, 5, 0, stats)
          self._pdr.info(frame, (_w - 5), 5, 0, self._version)

          self._net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (900, 900),
                                                   (104.0, 177.0, 123.0)))
          self._pdr.faces(frame, self._net.forward())

          cv2.imshow(self._service_name, frame)

          if cv2.waitKey(1) & 0xFF == int(27):
            self.release(self._stream)
            break

          self._frame_num += 1
        else:
          self._log.warning('VZen service broke while streaming.')
          toast(f'{self._service_name}', 'VZen service broke.')
          time.sleep(self._exception)
      except KeyboardInterrupt:
        self._log.warning('VZen service interrupted.')
        toast(f'{self._service_name}', 'VZen service interrupted.')
        raise SystemExit(0)
      except Exception as _error:
        self._log.exception(_error)
        toast(f'{self._service_name}', 'VZen service stopped abruptly.')
      finally:
        # Sleep for 30 seconds if any exception occurs before restarting
        # the service.
        time.sleep(self._exception)


if __name__ == '__main__':
  VisualizeEnvironment().perceive()
  # _clr = np.random.randint(0, 255, size=(10, 3))
  # print(tuple((_clr)[0]))
