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
"""Utility for using the ML components easily & natively."""

import glob
import os
import shutil
from pathlib import Path
from typing import List, Optional

# TODO(xames3): Remove suppressed pyright warnings.
# pyright: reportMissingTypeStubs=false
import numpy as np
import matplotlib.pyplot as plt
from keras.callbacks.callbacks import History

from mle.constants import defaults
from mle.utils import symlinks
from mle.utils.common import now


def training_session_date(timestamp_format: str = '%m%d%y') -> str:
  """Returns date timestamp of model training."""
  return str(now().strftime(timestamp_format))


def train_test_val_directories(directory: str,
                               session_name: str = None) -> List:
  """Creates train, test and validation directories.

  Creates train, test and validation directories with respective name of
  the directory and returns the list of created directories.

  Args:
    directory: Directory whose train, test and validation directories
               needs to be created.
    session_name: Name of the current training session.

  Returns:
    List of created directories.
  """
  session_name = session_name if session_name else training_session_date()
  dirs = ['train', 'test', 'validation']
  sym_dirs = [os.path.join(symlinks.train, session_name),
              os.path.join(symlinks.test, session_name),
              os.path.join(symlinks.validation, session_name)]
  new_dirs = []
  for idx, sym_idx in zip(dirs, sym_dirs):
    dirname = os.path.join(sym_idx, ''.join([idx, '_', Path(directory).stem]))
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
    new_dirs.append(dirname)
  return new_dirs


def create_train_test_val_split(directory: str,
                                session_name: str = None,
                                train_sample: Optional[int] = None) -> None:
  """Creates train, test and validation split of the dataset.

  Creates train, test and validation split of the dataset as per the
  requirement. The default test and validation split is going to be 20%
  of the train_sample.

  Args:
    directory: Directory whose train, test and validation split needs to
               be created.
    session_name: Name of the current training session.
    train_sample: Number (default: None) of training samples to use.
  """
  # You can find the reference code here:
  # https://towardsdatascience.com/a-comprehensive-hands-on-guide-to-transfer-learning-with-real-world-applications-in-deep-learning-212bf3b2f27a
  np.random.seed(42)
  # Using glob for getting all the files under ./<directory>/ directory.
  files = glob.glob(f'{directory}/*')
  all_files = [name for name in files if Path(directory).stem in name]
  # If number of train_sample is not provided, it'll take 30% of all the
  # available files.
  if train_sample is None:
      train_sample = int(defaults.SMALL_TRAIN_SPLIT * len(all_files))
  # Creating an array of randomly chosen training files from all the
  # available files.
  train_files = np.random.choice(all_files, size=train_sample, replace=False)
  # Removing the files that have been used for training purpose.
  all_files = list(set(all_files) - set(train_files))
  # Creating an array of randomly chosen test files from all the
  # available files excluding training files.
  test_files = np.random.choice(all_files,
                                size=int(defaults.TEST_SPLIT * train_sample),
                                replace=False)
  # Removing the files that have been used for testing purpose.
  all_files = list(set(all_files) - set(test_files))
  # Creating an array of randomly chosen validation files from all the
  # available files excluding training files & test files.
  val_files = np.random.choice(all_files,
                                size=int(defaults.VALIDATION_SPLIT *
                                        train_sample),
                                replace=False)
  # Creating train, test and validation directories.
  train_dir, test_dir, validation_dir = train_test_val_directories(directory,
                                                                   session_name)
  # Copying files to their respective directory.
  for file in train_files:
    shutil.copy(file, train_dir)
  for file in test_files:
    shutil.copy(file, test_dir)
  for file in val_files:
    shutil.copy(file, validation_dir)


def create_small_dataset(directory: str,
                         session_name: str = None,
                         train_sample: Optional[int] = None) -> None:
  """Creates a smaller dataset.

  Creates a smaller dataset than the original for 'N' number of training
  samples.

  Args:
    directory: Directory to be used for creating small dataset.
    session_name: Name of the current training session.
    train_sample: Number (default: None) of training samples to use.

  Usage:
    create_small_dataset('D:/mle/mle/data/raw/vzen', 'xa_2000', 2000)
  """
  all_files = glob.glob(f'{os.path.join(symlinks.train, directory)}/*')
  # Loop to perform train, test and validation split for the mentioned
  # directory.
  for idx in all_files:
    create_train_test_val_split(idx, session_name, train_sample)


def fit_generator_plot(history: History,
                       parameter: str,
                       session_name: str,
                       show_plot: bool = False,
                       save_plot: bool = True) -> None:
  """Save and show history plot for 'fit_generator()'.

  Save and show history plot for selected parameter, accuracy or loss in
  'fit_generator()'.

  Args:
    history: History object (dict) which stores stats of the trained
             model.
    parameter: History parameter, accuracy or loss.
    session_name: Name of the current training session.
    show_plot: Boolean (default: False) value to display the plot.
    save_plot: Boolean (default: True) value to save the plot.

  Note:
    The saved plots would be saved in ./stats/ directory with the
    'session_name'.
  """
  plt.plot(history.history[parameter], label=f'training_{parameter}')
  plt.plot(history.history[f'val_{parameter}'], label=f'validation_{parameter}')
  plt.legend()
  if save_plot:
    plt.savefig(os.path.join(symlinks.stats, f'{session_name}_{parameter}'))
  if show_plot:
    plt.show()
