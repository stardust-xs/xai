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

from typing import List, Optional, Tuple, Union

import cv2
import numpy as np

from mle.vars.colors import green, yellow


def rescale(frame: np.ndarray,
            width: Optional[int] = None,
            height: Optional[int] = None,
            interpolation: Optional[object] = cv2.INTER_AREA) -> np.ndarray:
  """Rescale the frame.
  
  Rescale the stream to a desirable size. This is required before
  performing the necessary operations.

  Args:
    frame: Numpy array of the image frame.
    width: Width (default: None) to be rescaled to.
    height: Height (default: None) to be rescaled to.
    interpolation: Interpolation algorithm (default: INTER_AREA) to be
                   used.

  Returns:
    Rescaled numpy array for the input frame.

  Example:
    >>> import cv2
    >>> from mle.utils.opencv import rescale
    >>> 
    >>> stream = cv2.VideoCapture(0) 
    >>> 
    >>> while True:
    ...   _, frame = stream.read()
    ...   frame = rescale(frame, width=300, interpolation=cv2.INTER_LANCZOS4)
    ...   cv2.imshow('Test feed', frame)
    ...   if cv2.waitKey(5) & 0xFF == int(27):
    ...     break
    >>> stream.release()
    >>> cv2.destroyAllWindows()
    >>>
  """
  dimensions = None
  frame_height, frame_width = frame.shape[:2]
  # If both width & height are None, then return the original frame.
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


def disconnect(stream: np.ndarray) -> None:
  """Disconnect stream and exit the program."""
  stream.release()
  cv2.destroyAllWindows()


def draw_box_with_tuple(frame: np.ndarray,
                        start_xy: Tuple,
                        end_xy: Tuple,
                        color: Optional[List] = yellow,
                        thickness: Optional[int] = 1) -> None:
  """Draw bounding box using the Numpy tuple.

  Draws the bounding box around the detection using tuple of numpy
  coordinates.

  Args:
    frame: Numpy array of the image frame.
    start_xy: Tuple of top left coordinates.
    end_xy: Tuple of bottom right coordinates.
    color: Bounding box (default: yellow) color.
    thickness: Thickness (default: 1) of the bounding box.

  Note:
    This method can be used for drawing the bounding boxes around
    objects whose coordinates are derived from a Machine Learning based
    model. For Haar based detections, use `draw_box_with_coords()`.
  """
  return cv2.rectangle(frame, start_xy, end_xy, color, thickness)


def draw_box_with_coords(frame: np.ndarray, x: Union[int], y: Union[int],
                         w: Union[int], h: Union[int],
                         color: Optional[List] = green,
                         thickness: Optional[int] = 1) -> None:
  """Draw bounding box using individual coords.

  Draws a bounding box around the detected object using all 4 available
  coordinates. This function is ideal to use with Haar based detections.

  Args:
    frame: Numpy array of the image frame.
    x: Top left X-position of the detected object.
    y: Top left Y-position of the detected object.
    w: Bottom right X-position of the detected object.
    w: Bottom right Y-position of the detected object.
    color: Bounding box (default: green) color.
    thickness: Thickness (default: 1) of the bounding box.
  """
  return cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
