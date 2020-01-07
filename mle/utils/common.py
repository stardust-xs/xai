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
"""The ``mle.utils.common`` module.

This module implements the common functions that are very generic in
their operation and can-be/are used within the project. These functions
also provide cross project usage i.e the functions from this module can
be used by other python projects.

Todo:
    * Remove ``pylint`` warning comments.

"""
# The following comment should be removed at some point in the future.
# pylint: disable=import-error
# pylint: disable=no-name-in-module

import os
from typing import List, Optional, Union

import requests
from fuzzywuzzy.fuzz import partial_ratio
from fuzzywuzzy.process import extract

from mle.vars.dev import PING_URL

mle_path = os.path.dirname(os.path.dirname(__file__))


def find_string(string: str,
                str_list: List,
                min_score: Optional[int] = 70) -> Optional[str]:
    """Find string in a list using fuzzy logic.

    Finds the matching string in the list. It works similar to
    ``.find()`` method but uses fuzzy logic for guessing text from any
    valid list.

    Args:
        string: Approximate or Exact string to find in the list.
        str_list: List in which the string needs to be searched in.
        min_score: Minimum score needed to make an approximate guess.
                   Default: 70

    Returns:
        String value to be searched in the list.

    Raises:
        ValueError: If no similar string is found in the list.
    """
    # This will give us list of 3 best matches for our search query.
    guessed = extract(string, str_list, limit=3, scorer=partial_ratio)

    for best_guess in guessed:
        current_score = partial_ratio(string, best_guess)
        if current_score > min_score and current_score > 0:
            return best_guess[0]
        else:
            raise ValueError(f'Couldn\'t find "{string}" in the given list.')


def check_internet(timeout: Optional[Union[float, int]] = 10.0) -> bool:
    """Check the internet connectivity."""
    # You can find the reference code here:
    # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
    try:
        _ = requests.get(PING_URL, timeout=timeout)
        return True
    except ConnectionError:
        return False
