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
"""Utility for using the machine learning components natively."""

import glob
import os
import shutil
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks.callbacks import History
from keras.preprocessing.image import img_to_array as i2a
from keras.preprocessing.image import load_img as li
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

from mle.constants import defaults as dx
from mle.utils import symlinks
from mle.utils.common import timestamp


def _train_test_directories(directory: str,
                            session: str = None) -> List:
  """Create train & test directories.

  Create train & test directories for training purposes.

  Args:
    directory: Directory which has all the files for the dataset.
    session: Name of the current training session.

  Returns:
    List of symbolic links of created directories.
  """
  # If no session is specified, create session using current date
  session = session if session else timestamp('%m%d%y')
  dirs = ['train', 'test']
  sym_dirs = [os.path.join(symlinks.train, session),
              os.path.join(symlinks.test, session)]
  new_dirs = []
  # Create subdirectories within train & test directories
  for idx, sym_idx in zip(dirs, sym_dirs):
    dirname = os.path.join(sym_idx, ''.join( [idx, '_', Path(directory).stem]))
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
    new_dirs.append(dirname)
  return new_dirs


def create_train_test_split(directory: str,
                            session: str = None,
                            train_samples: int = None,
                            unify_data: bool = False) -> None:
  """Create train-test split of a dataset.

  Create train-test split of a dataset as per the requirement.

  Args:
    directory: Directory which has all the files for the dataset.
    session: Name of the current training session.
    train_samples: Number of training samples to use.
    unify_data: Boolean value to create a single train & test directory
                for all the classes.

  Note:
    If 'train_samples' is not provided, it'll create a dataset with 70%
    of the actual training data.
    The default test split is going to be 30% of the 'train_samples'.
  """
  # You can find the reference code here:
  # https://towardsdatascience.com/a-comprehensive-hands-on-guide-to-transfer-learning-with-real-world-applications-in-deep-learning-212bf3b2f27a
  files = glob.glob(f'{directory}/*')
  all_files = [name for name in files if Path(directory).stem in name]
  # If number of 'train_samples' is not provided, it'll take 70% of all
  # the available files
  if train_samples is None:
    train_samples = int(dx.TRAIN_SPLIT * len(all_files))
  # Creating an array of randomly chosen training files from all the
  # available files
  train_files = np.random.choice(
    all_files, size=train_samples, replace=False)
  # Removing the files that have been already used for training purpose
  all_files = list(set(all_files) - set(train_files))
  # Similarly, creating an array of randomly chosen test files from all
  # the available files excluding training files
  test_samples = int(dx.TEST_SPLIT * train_samples)
  test_files = np.random.choice(all_files, size=test_samples, replace=False)
  all_files = list(set(all_files) - set(test_files))
  # Individual file objects to copy in their respective directories
  files = [train_files, test_files]
  if unify_data:
    session = session if session else timestamp('%m%d%y')
    sym_dirs = [os.path.join(symlinks.train, f'{session}/train'),
                os.path.join(symlinks.test, f'{session}/test')]
    for idx, sym_idx in zip(files, sym_dirs):
      # Displaying progress bar for copying files into directories
      with tqdm(total=len(idx), desc='Copying', unit=' files') as progress_bar:
        if not os.path.isdir(sym_idx):
          os.makedirs(sym_idx)
        for file in idx:
          shutil.copy(file, sym_idx)
          progress_bar.update(1)
  else:
    (train_dir, test_dir) = _train_test_directories(directory, session)
    sym_dirs = [train_dir, test_dir]
    for idx, sym_idx in zip(files, sym_dirs):
      # Displaying progress bar for copying files into directories
      with tqdm(total=len(idx), desc='Copying', unit=' files') as progress_bar:
        for file in idx:
          shutil.copy(file, sym_idx)
          progress_bar.update(1)


def create_dataset(directory: str,
                   session: str = None,
                   train_samples: int = None,
                   unify_data: bool = False) -> None:
  """Create dataset.

  Create a dataset with 'N' number of training samples.

  Args:
    directory: Directory which has all the files for the dataset.
    session: Name of the current training session.
    train_samples: Number of training samples to use.
    unify_data: Boolean value to create a single train & test directory
                for all the classes.

  Example:
    >>> from mle.utils.components import create_dataset
    >>>
    >>> create_dataset('D:/mle/mle/data/raw/vzen', 'mle_session', 2000)
    >>>
  """
  all_files = glob.glob(f'{os.path.join(symlinks.train, directory)}/*')
  for idx in all_files:
    create_train_test_split(idx, session, train_samples, unify_data)


def rename_image_dataset(session: str) -> None:
  """Rename image dataset.

  Rename images with respective directory name. This is required for
  creating the classification labels. This step is of utmost importance
  for classification datasets which are similar to Cats vs Dog datasets.

  Args:
    session: Name of the current training session.

  Note:
    This function will not work on the datasets created by setting
    'unify_data' argument to True in create_dataset().
  """
  dirs = ['train', 'test']
  sym_dirs = [os.path.join(symlinks.train, session),
              os.path.join(symlinks.test, session)]
  # Looping through all the directories and renaming the files by
  # prefixing the 'classification label'
  for idx, sym_idx in zip(dirs, sym_dirs):
    for directory in glob.glob(f'{sym_idx}/*'):
      for _idx, temp in enumerate(glob.glob(f'{directory}/*')):
        extension = os.path.splitext(temp)[1]
        name = (os.path.basename(directory)).split(f'{idx}_')[1]
        file = os.path.join(directory, f'{name}.{_idx}{extension}')
        os.rename(temp, file)


def load_image_dataset(session: str, target_size: Tuple = dx.MLE_SIZE) -> Tuple:
  """Load an image dataset.

  Load an image classification dataset before feeding it to the model.

  Args:
    session: Name of the current training session.
    target_size: Dimension to which the image array needs to be resized.

  Returns:
    Tuple of train-test image array lists.
  """
  train_dir = os.path.join(symlinks.train, session)
  test_dir = os.path.join(symlinks.test, session)
  train_files = glob.glob(f'{train_dir}/train/*')
  test_files = glob.glob(f'{test_dir}/test/*')
  files_list = [train_files, test_files]
  train_images, test_images = [], []
  images_array = [train_images, test_images]
  # Looping through all the images in training & test directory, loading
  # them & resizing the array to a 'target_size' and then converting the
  # image data
  for file, image in zip(files_list, images_array):
    with tqdm(total=len(file), desc='Loading', unit=' files') as progress_bar:
      for idx in file:
        image.append(i2a(li(idx, target_size=target_size)))
        progress_bar.update(1)
  return train_images, test_images


def scale_image_dataset(session: str,
                        target_size: Tuple = dx.MLE_SIZE) -> Tuple:
  """Scale an image dataset array.

  Scale an image dataset array's each pixel value between (0, 255) to
  values between (0, 1). This step is very important since NN models
  work well with smaller values.

  Args:
    session: Name of the current training session.
    target_size: Dimension to which the image array needs to be resized.

  Returns:
    Tuple of scaled train-test image arrays.
  """
  # Using load_image_dataset() to create list of train-test image array
  (train_images, test_images) = load_image_dataset(session, target_size)
  train_images, test_images = np.array(train_images), np.array(test_images)
  scaled_train_images = train_images.astype('float32')
  scaled_test_images = test_images.astype('float32')
  scaled_train_images /= 255
  scaled_test_images /= 255
  return scaled_train_images, scaled_test_images, train_images, test_images


def encode_image_labels(session: str) -> Tuple:
  """Encode image labels.

  Encode image classification labels to numeric values. These values
  represent the labels using an integer. For instance, if you 2 classes
  XA & Unknown; then XA would be encoded as 0 & Unknown would be encoded
  as 1. If there were to be more classes, the number will increase.

  Args:
    session: Name of the current training session.

  Returns:
    Tuple of training & test label encodings.
  """
  train_dir = os.path.join(symlinks.train, session)
  test_dir = os.path.join(symlinks.test, session)
  train_files = glob.glob(f'{train_dir}/train/*')
  test_files = glob.glob(f'{test_dir}/test/*')
  files_list = [train_files, test_files]
  train_labels, test_labels = [], []
  labels = [train_labels, test_labels]
  # Get train & test labels from the name of that image. Since we
  # presume that the classification dataset has images with labels as
  # their filenames
  # For e.g: ./train/xa/xa.42069.png OR ./train/unknown/unknown.69.png
  for file, label in zip(files_list, labels):
    with tqdm(total=len(file), desc='Encoding', unit=' files') as progress_bar:
      for idx in file:
        label.append(idx.split('\\')[1].split('.')[0].strip())
        progress_bar.update(1)
  # Encode labels using Sklearn's LabelEncoder()
  label_encoder = LabelEncoder()
  label_encoder.fit(train_labels)
  return (label_encoder.transform(train_labels),
          label_encoder.transform(test_labels))


def accuracy_vs_loss_plot(history: History,
                          session: str,
                          title: str,
                          epochs: int,
                          show: bool = False,
                          save: bool = True) -> None:
  """Save and show Accuracy vs Loss plot.

  Save and show an accuracy vs loss plot for a particular model.

  Args:
    history: History object/dictionary of trained model.
    session: Name of the current training session.
    title: Title for the plot.
    epochs: Number of times to train the model.
    show: Boolean value to display the plot.
    save: Boolean value to save the plot.

  Note:
    The saved plots would be saved in ./stats/<session>/ directory
    with the 'session'.
  """
  if epochs > 1:
    directory = os.path.join(symlinks.stats, session)
    if not os.path.isdir(directory):
      os.makedirs(directory)
    # Create an instance of a plot with only 2 sublots, Accuracy & loss
    figure, (accuracy, loss) = plt.subplots(1, 2, figsize=(12, 4))
    figure.suptitle(title, fontsize=12)
    epoch_list = list(range(1, epochs + 1))
    accuracy.plot(epoch_list, history.history['accuracy'],
                  label=f'Training accuracy')
    accuracy.plot(epoch_list, history.history['val_accuracy'],
                  label=f'Testing accuracy')
    accuracy.set_xticks(np.arange(0, epochs + 1, 5))
    accuracy.set_ylabel('Accuracy')
    accuracy.set_xlabel('Epoch')
    accuracy.set_title('Accuracy')
    loss.plot(epoch_list, history.history['loss'], label=f'Training loss')
    loss.plot(  epoch_list, history.history['val_loss'], label=f'Testing loss')
    loss.set_xticks(np.arange(0, epochs + 1, 5))
    loss.set_ylabel('Loss')
    loss.set_xlabel('Epoch')
    loss.set_title('Loss')
    if save:
      plt.savefig(os.path.join(directory, f'{session}'))
    if show:
      plt.show()
