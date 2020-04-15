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

from typing import Tuple

import cv2
import numpy as np

from mle.constants import colors


def rescale(frame: np.ndarray,
            width: int = None,
            height: int = None,
            interpolation: int = cv2.INTER_AREA) -> np.ndarray:
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
    frame_height, frame_width, _ = frame.shape
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


def draw_description_box(frame: np.ndarray,
                         x0_y0: Tuple[int, int],
                         x1_y1: Tuple[int, int],
                         description: str,
                         description_text_color: Tuple = colors.WHITE,
                         description_box_color: Tuple = colors.BLACK,
                         description_box_opacity: float = 0.3,
                         description_box_thickness: int = 1) -> None:
  """Draw box for adding description for the detection.

  Draw a description box relative to the bounding box. This box displays
  label/name, confidence score, etc. of the detected object.

  Args:
    frame: Numpy array of the image frame.
    overlay: Copy of the image frame.
    x0_y0: Tuple of top left coordinates.
    x1_y1: Tuple of bottom right coordinates.
    confidence: Confidence score of the detection.
    description: Description of the detected object.
    description_text_color: Description text color (default: white).
    description_box_color: Description box (default: black) color.
    description_box_opacity: Opacity (default: 0.3) of the description
                             box.
    description_box_thickness: Thickness (default: 1) of the description
                               box.

  Note:
    The description box is inspired by the Tesla Auto-pilot AI
    description box. It stays relatively close to the bounding box and
    switches it's position relative to the motion.
  """
  # You can find the reference label video here:
  # https://www.youtube.com/watch?v=_1MHGUC_BzQ&list=LLDNJ8g4d0prqef0UNX8XkeQ
  # Unpacking tuples into 4 seperate points.
  (x0, y0), (_, y1) = x0_y0, x1_y1
  # Position of the description box by default. Start from the
  # X - coordinate, just above the bounding box.
  break_count = description.count('\n')
  x_bias = max([idx for idx in description.split('\n')], key=lambda x: len(x))
  x3, y3 = x0, (y0 - (5 + break_count * 20))
  # If bounding box is at the left edge of the view, display the
  # description box at the left edge.
  if x3 < 0:
    x3 = 0
  # If bounding box is at the right edge of the view, display the
  # description box at the right edge by considering the description in
  # it.
  elif (x3 + 10 + (len(x_bias) * 7) > frame.shape[1]):
    x3 = x3 - (x3 + 10 + len(x_bias) * 7 - (frame.shape[1])) - 10
  # If the bounding box is high up towards the top, display th
  # description box at the bottom of bounding box.
  if y3 < 30:
    y3 = y1 + 30
  # Initializing new coordinates with adjustments.
  # NOTE: These adjustments are subjective and may vary in future.
  x4, y4 = int(x3), int(y3 - 25)
  x5, y5 = int(x3 + 17 + (len(x_bias) * 7)), int((y3 + break_count * 20) - 1)
  # Adding an alpha bounding box, similar to draw_bounding_box().
  overlay = frame.copy()
  cv2.rectangle(overlay, (x4, y4), (x5, y5), description_box_color, -1)
  cv2.rectangle(frame, (x4, y4), (x5, y5),
                description_box_color, description_box_thickness)
  cv2.addWeighted(overlay, description_box_opacity, frame,
                  1 - description_box_opacity, 0, frame)
  # Adding description.
  for idx in description.split('\n'):
    cv2.putText(frame, idx, (int(x3 + 7), int(y3 - 10)),
                cv2.FONT_HERSHEY_DUPLEX, 0.4, description_text_color)
    y3 = y3 + 20


def draw_bounding_box(frame: np.ndarray,
                      x0_y0: Tuple[int, int],
                      x1_y1: Tuple[int, int],
                      description: str,
                      description_text_color: Tuple = colors.WHITE,
                      description_box_color: Tuple = colors.BLACK,
                      description_box_opacity: float = 0.3,
                      description_box_thickness: int = 1,
                      bounding_box_color: Tuple = colors.RED,
                      bounding_box_opacity: float = 0.3,
                      bounding_box_thickness: int = 2) -> None:
  """Draw bounding box.

  Draws the bounding box around the detection using its coordinates.

  Args:
    frame: Numpy array of the image frame.
    x0_y0: Tuple of top left coordinates.
    x1_y1: Tuple of bottom right coordinates.
    description: Description of the detected object.
    description_text_color: Description text color (default: white).
    description_box_color: Description box (default: black) color.
    description_box_opacity: Opacity (default: 0.3) of the description
                             box.
    description_box_thickness: Thickness (default: 1) of the description
                               box.
    bounding_box_color: Bounding box (default: red) color.
    bounding_box_opacity: Opacity (default: 0.3) of the detected region.
    bounding_box_thickness: Thickness (default: 2) of the bounding box.

  Note:
    For Haar based detections, modify the x1_y1 tuple like below:
    draw_bounding_box(frame, x0, y0, (x1 - x0), (y1 - y0), 'XAMES3')
  """
  overlay = frame.copy()
  cv2.rectangle(overlay, x0_y0, x1_y1, bounding_box_color, -1)
  # Main bounding box for the detection.
  cv2.rectangle(frame, x0_y0, x1_y1, bounding_box_color,
                bounding_box_thickness)
  # Add transparent/alpha overlay on the frame.
  cv2.addWeighted(overlay, bounding_box_opacity, frame,
                  1 - bounding_box_opacity, 0, frame)
  # Draw description box relative to the bounding box.
  draw_description_box(frame, x0_y0, x1_y1, description,
                       description_text_color, description_box_color,
                       description_box_opacity, description_box_thickness)


def draw_statistics_box(frame: np.ndarray,
                        x0_y0: Tuple[int, int],
                        description: str,
                        description_text_color: Tuple = colors.WHITE,
                        description_box_color: Tuple = colors.BLACK,
                        description_box_opacity: float = 0.3,
                        description_box_thickness: int = 1) -> None:
  """Draw box for displaying statisticse.

  Draws box for displaying statistics box at particular point. 

  Args:
    frame: Numpy array of the image frame.
    description: Description/Statistics to be displayed
    x0_y0: Tuple of top left coordinates.
    description_text_color: Description text color (default: white).
    description_box_color: Description box (default: black) color.
    description_box_opacity: Opacity (default: 0.3) of the description
                             box.
    description_box_thickness: Thickness (default: 1) of the description
                               box.
  """
  # Default information template.
  draw_description_box(frame, x0_y0, (x0_y0[0], (x0_y0[1] - 5)), description,
                       description_text_color, description_box_color,
                       description_box_opacity, description_box_thickness)
