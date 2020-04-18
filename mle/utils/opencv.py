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
"""Utility for making convenient use of OpenCV."""

from typing import Sequence, Union

import cv2
import numpy as np

from mle.constants import colors


def resize(frame: np.ndarray,
           width: int = None,
           height: int = None,
           interpolation: int = cv2.INTER_AREA) -> np.ndarray:
  """Resize the frame.

  Resize video frame to a desirable height and/or width.

  Args:
    frame: Numpy array of the image frame.
    width: Width to be resized to.
    height: Height to be resized to.
    interpolation: Interpolation algorithm to be used.

  Returns:
    Resized frame with new dimensions.

  Raises:
    cv2.error: OpenCV's non-exit exception.

  Example:
    >>> from mle.utils.opencv import resize
    >>> 
    >>> frame = resize(frame, width=500, height=200)
    >>> frame.shape
    (500, 200, 3)
  """
  try:
    dimensions = None
    frame_height, frame_width, _ = frame.shape
    # If both width & height are None, then don't resize
    if width is None and height is None:
      return frame
    if width and height:
      dimensions = (width, height)
    elif width is None:
      ratio = height / float(frame_height)
      dimensions = (int(frame_width * ratio), height)
    else:
      ratio = width / float(frame_width)
      dimensions = (width, int(frame_height * ratio))
    return cv2.resize(frame, dimensions, interpolation=interpolation)
  except cv2.error:
    return frame


def disconnect(stream: np.ndarray) -> None:
  """Disconnect stream and release cv2 object."""
  stream.release()
  cv2.destroyAllWindows()


def display_text(frame: np.ndarray,
                 left: Union[float, int],
                 top: Union[float, int],
                 bottom: Union[float, int],
                 text: str,
                 text_color: Sequence = colors.WHITE,
                 box_color: Sequence = colors.BLACK,
                 box_opacity: float = 0.3,
                 box_thickness: int = 1) -> None:
  """Display text.

  Display text in a box relative to the detection. This box displays
  texts like label/name, confidence score, etc. for the detection.

  Args:
    frame: Numpy array of the image frame.
    left: Left coordinate value.
    top: Top coordinate value.
    right: Right coordinate value.
    bottom: Bottom coordinate value.
    text: Text to be displayed.
    text_color: Displayed text color.
    box_color: Box color.
    box_opacity: Box opacity.
    box_thickness: Box thickness.
  """
  left, top, bottom = int(left), int(top), int(bottom)
  break_count = text.count('\n')
  x_bias = max([idx for idx in text.split('\n')], key=lambda x: len(x))
  x3, y3 = left, (top - (5 + break_count * 20))
  # Ensure the bounding box won't go beyond the horizontal view
  if x3 < 0:
    x3 = 0
  elif (x3 + 10 + (len(x_bias) * 7) > frame.shape[1]):
    x3 = x3 - (x3 + 10 + len(x_bias) * 7 - (frame.shape[1])) - 10
  # Ensure the bounding box won't go beyond the vertical view
  if y3 < 30:
    y3 = bottom + 30
  # Initializing new coordinates with adjustments
  # NOTE: These adjustments are subjective and may vary in future
  x4, y4 = int(x3), int(y3 - 25)
  x5, y5 = int(x3 + 17 + (len(x_bias) * 7)), int((y3 + break_count * 20) - 1)
  # Adding detection mask, similar to display_detection()
  mask = frame.copy()
  cv2.rectangle(mask, (x4, y4), (x5, y5), box_color, -1)
  cv2.rectangle(frame, (x4, y4), (x5, y5), box_color, box_thickness)
  cv2.addWeighted(mask, box_opacity, frame, 1 - box_opacity, 0, frame)
  # Adding text with line breaks
  for idx in text.split('\n'):
    cv2.putText(frame, idx, (int(x3 + 7), int(y3 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, lineType=cv2.LINE_AA)
    y3 = y3 + 20


def display_detection(frame: np.ndarray,
                      left: Union[float, int],
                      top: Union[float, int],
                      right: Union[float, int],
                      bottom: Union[float, int],
                      text: str,
                      text_color: Sequence = colors.WHITE,
                      box_color: Sequence = colors.BLACK,
                      box_opacity: float = 0.3,
                      box_thickness: int = 1) -> None:
  """Display detected object.

  Display detected object by drawing rectangular bounding box around it.

  Args:
    frame: Numpy array of the image frame.
    left: Left coordinate value.
    top: Top coordinate value.
    right: Right coordinate value.
    bottom: Bottom coordinate value.
    text: Text to be displayed.
    text_color: Displayed text color.
    box_color: Box color.
    box_opacity: Box opacity.
    box_thickness: Box thickness.
  """
  left, top, right, bottom = int(left), int(top), int(right), int(bottom)
  # Adding detection mask
  mask = frame.copy()
  cv2.rectangle(mask, (left, top), (right, bottom), box_color, -1)
  cv2.addWeighted(mask, box_opacity, frame, 1 - box_opacity, 0, frame)
  cv2.rectangle(frame, (left, top), (right, bottom), box_color, box_thickness)
  # Display text box relative to the detections
  display_text(frame, left, top, bottom, text, text_color, box_color,
               box_opacity, box_thickness)


def display_statistics(frame: np.ndarray,
                       left: Union[float, int],
                       top: Union[float, int],
                       text: str,
                       text_color: Sequence = colors.WHITE,
                       box_color: Sequence = colors.BLACK,
                       box_opacity: float = 0.3,
                       box_thickness: int = 1) -> None:
  """Display statistics.

  Display statistics in a box. 

  Args:
    frame: Numpy array of the image frame.
    left: Left coordinate value.
    top: Top coordinate value.
    text: Text to be displayed.
    text_color: Displayed text color.
    box_color: Box color.
    box_opacity: Box opacity.
    box_thickness: Box thickness.
  """
  display_text(frame, left, top, top - 5, text, text_color, box_color,
               box_opacity, box_thickness)
