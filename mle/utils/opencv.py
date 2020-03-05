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

from typing import Optional, Tuple, Union

# TODO(xames3): Remove suppressed pyright warnings.
# pyright: reportMissingTypeStubs=false
import cv2
import numpy as np

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
  try:
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
  except cv2.error:
    return frame


def disconnect(stream: np.ndarray) -> None:
  """Disconnect stream and release cv2 object."""
  stream.release()
  cv2.destroyAllWindows()


def draw_label_box(frame: np.ndarray,
                   overlay: np.ndarray,
                   x0_y0: Tuple,
                   x1_y1: Tuple,
                   label: str,
                   confidence: Union[float, int],
                   label_color: Tuple = colors.WHITE,
                   color: Tuple = colors.BLACK,
                   alpha: Union[float, int] = 0.3,
                   alpha_color: Tuple = colors.BLACK,
                   thickness: int = 1) -> None:
  """Draw box for labels relative to the bounding box.

  Draws a label box relative to the bounding box. This label box display
  label/name & the confidence score of the detected object.

  Args:
    frame: Numpy array of the image frame.
    overlay: Copy of the image frame.
    x0_y0: Tuple of top left coordinates.
    x1_y1: Tuple of bottom right coordinates.
    label: Label/Name of the detected object.
    confidence: Confidence score of the detection.
    label_color: Label color (default: white).
    color: Bounding box (default: black) color.
    alpha: Opacity of the detected region overlay.
    alpha_color: Overlayed color (default: black).
    thickness: Thickness (default: 1) of the bounding box.
  """
  # Unpacking tuples into 4 seperate points.
  (x0, y0), (_, y1) = x0_y0, x1_y1
  # Position of the label box by default. Start from the X - coordinate,
  # just above the bounding box.
  x3, y3 = x0, (y0 - 5)
  # Default label - confidence template.
  label = f'{label} | {confidence}%'
  # If bounding box is at the left edge of the view, display the label
  # box at the left edge.
  if x3 < 0:
    x3 = 0
  # If bounding box is at the right edge of the view, display the label
  # box at the right edge by considering the label as well.
  elif (x3 + 10 + (len(label) * 7) > frame.shape[1]):
    x3 = x3 - (x3 + 10 + len(label) * 7 - (frame.shape[1])) - 10
  # If the bounding box is high up towards the top, display the label
  # box at the bottom of bounding box.
  if y3 < 0:
    y3 = y1 + 30
  # Initializing new coordinates with adjustments.
  # NOTE: These adjustments are subjective and may vary in future.
  x4, y4 = int(x3), int(y3 - 25)
  x5, y5 = int(x3 + 20 + (len(label) * 7)), int(y3 - 1)
  # Adding an alpha bounding box, similar to draw_bounding_box().
  cv2.rectangle(overlay, (x4, y4), (x5, y5), alpha_color, -1)
  cv2.rectangle(frame, (x4, y4), (x5, y5), color, thickness)
  cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
  # Adding label & confidence score.
  cv2.putText(frame, label, (int(x3 + 10), int(y3 - 10)),
              cv2.FONT_HERSHEY_DUPLEX, 0.4, label_color)


def draw_bounding_box(frame: np.ndarray,
                      x0_y0: Tuple,
                      x1_y1: Tuple,
                      label: str,
                      confidence: Union[float, int],
                      label_color: Tuple = colors.WHITE,
                      color: Tuple = colors.RED,
                      alpha: Union[float, int] = 0.2,
                      alpha_color: Tuple = colors.RED,
                      thickness: int = 2) -> None:
  """Draw bounding box using the Numpy tuple.

  Draws the bounding box around the detection using tuple of numpy
  coordinates.

  Args:
    frame: Numpy array of the image frame.
    x0_y0: Tuple of top left coordinates.
    x1_y1: Tuple of bottom right coordinates.
    label: Label/Name of the detected object.
    confidence: Confidence score of the detection.
    label_color: Label color (default: white).
    color: Bounding box (default: red) color.
    alpha: Opacity of the detected region overlay.
    alpha_color: Overlayed color (default: red).
    thickness: Thickness (default: 2) of the bounding box.

  Note:
    This method can be used for drawing the bounding boxes around
    objects whose coordinates are derived from a ML based models.

  Usage:
    * For Haar based detections, use the below settings -
        draw_bounding_box(frame, x0, y0, (x1 - x0), (y1 - y0))
    * For adding the detection name, add the below settings - 
        (x0, y0), (x1, y1) = x0_y0, x1_y1
        cv2.rectangle(frame, (x0, y1), (x1, y1 + 20), color, -1)
  """
  # Transparent/Alpha overlay rectangle layer.
  overlay = frame.copy()
  cv2.rectangle(overlay, x0_y0, x1_y1, alpha_color, -1)
  # Main bounding box.
  cv2.rectangle(frame, x0_y0, x1_y1, color, thickness)
  cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
  # Draw label box relative to the bounding box.
  draw_label_box(frame, overlay, x0_y0, x1_y1, label,
                 confidence, label_color, colors.BLACK)
