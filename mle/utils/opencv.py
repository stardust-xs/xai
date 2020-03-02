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

# TODO(xames3): Remove suppressed pyright warnings.
# pyright: reportMissingTypeStubs=false
import cv2
import numpy as np
import imutils

from mle.constants import colors


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
  """Disconnect stream and release cv2 object."""
  stream.release()
  cv2.destroyAllWindows()


def draw_bounding_box(frame: np.ndarray,
                      x0_y0: Tuple,
                      x1_y1: Tuple,
                      color: Tuple = colors.RED,
                      alpha: Union[float, int] = 0.3,
                      alpha_color: Tuple = colors.RED,
                      thickness: int = 2) -> None:
  """Draw bounding box using the Numpy tuple.

  Draws the bounding box around the detection using tuple of numpy
  coordinates.

  Args:
    frame: Numpy array of the image frame.
    x0_y0: Tuple of top left coordinates.
    x1_y1: Tuple of bottom right coordinates.
    color: Bounding box (default: red) color.
    alpha: Opacity of the detected region overlay.
    alpha_color: Overlayed color (default: red).
    thickness: Thickness (default: 1) of the bounding box.

  Note:
    This method can be used for drawing the bounding boxes around
    objects whose coordinates are derived from a Machine Learning based
    model.

  Usage:
    * For Haar based detections, use the below settings -
        draw_bounding_box(frame, x0, y0, (x1 - x0), (y1 - y0))
    * For adding the detection name, add the below settings - 
        (x0, y0), (x1, y1) = x0_y0, x1_y1
        cv2.rectangle(frame, (x0, y1), (x1, y1 + 20), color, -1)
  """
  overlay = frame.copy()
  # Transparent/Alpha overlay rectangle layer.
  cv2.rectangle(overlay, x0_y0, x1_y1, alpha_color, -1)
  # Main bounding box.
  cv2.rectangle(frame, x0_y0, x1_y1, color, thickness)
  cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def draw_centroid(frame: np.ndarray,
                  radius: int = 5,
                  color: Tuple = colors.WHITE,
                  thickness: int = 1) -> None:
  """Draw centroid for the detected shape/contour.

  Draw a centroid for the detected shape/contour or an sharp edge.

  Args:
    frame: Numpy array of the image frame.
    radius: Radius of the circle representing the centroid.
    color: Bounding box (default: white) color.
    thickness: Thickness (default: 1) of the bounding box.
  """
  # TODO(xames3): Add more details regarding below code lines.
  # Convert the colored image into grayscale.
  gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  blur_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
  threshold = cv2.threshold(blur_frame, 60, 255, cv2.THRESH_BINARY)[1]
  contours = cv2.findContours(threshold.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(contours)
  for contour in contours:
    moment = cv2.moments(contour)
    x = int(moment['m10'] / moment['m00']) if moment['m00'] > 0 else 0
    y = int(moment['m01'] / moment['m00']) if moment['m00'] > 0 else 0
    cv2.drawContours(frame, [contour], -1, color, thickness)
    cv2.circle(frame, (x, y), radius, color, -1)
