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
"""Module to define colors for HUD overlays."""

import random

red = [48, 59, 255]
blue = [255, 122, 0]
green = [100, 217, 76]
yellow = [0, 204, 255]
orange = [0, 149, 255]
teal = [250, 200, 90]
purple = [214, 86, 88]
pink = [85, 45, 255]
white = [255, 255, 255]
black = [0, 0, 0]

colors_list = [red, blue, green, yellow, orange, teal, purple, pink, black]
random_color = random.choice(colors_list)
