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

from mle.constants import defaults
from mle.utils import symlinks
from mle.utils.common import timestamp


def train_test_val_directories(directory: str,
                               session_name: str = None) -> List:
  """Create train, test & validation directories.

  Create train, test and validation directories with respective name of
  the directory and returns the list of created directories. The created
  directories have either 'train', 'test' or 'validation' prefix
  seperated by an underscore.

  Args:
    directory: Directory which has all the files for the dataset.
    session_name: Name of the current training session.

  Returns:
    List of symlinks of created directories.

  Note:
    Please ensure you add remove the 'prefix + underscore' before
    creating the classifying labels.
  """
  # If no session name is specified, create session using the date.
  session_name = session_name if session_name else timestamp('%m%d%y')
  # List of directories to create.
  dirs = ['train', 'test', 'validation']
  sym_dirs = [os.path.join(symlinks.train, session_name),
              os.path.join(symlinks.test, session_name),
              os.path.join(symlinks.validation, session_name)]
  new_dirs = []
  # Create subdirectories within train, test & validation directories.
  for idx, sym_idx in zip(dirs, sym_dirs):
    dirname = os.path.join(sym_idx, ''.join([idx, '_', Path(directory).stem]))
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
    new_dirs.append(dirname)
  return new_dirs


def create_train_test_val_split(directory: str,
                                session_name: str = None,
                                train_sample: int = None,
                                unify_data: bool = False) -> None:
  """Create train, test & validation split of a dataset.

  Create train, test and validation split of a dataset as per the
  requirement. The default test & validation split is going to be 15% of
  the 'train_sample'.
  If 'train_sample' is not provided, it'll create a dataset with 70% of
  the actual training data.

  Args:
    directory: Directory which has all the files for the dataset.
    session_name: Name of the current training session.
    train_sample: Number (default: None) of training samples to use.
    unify_data: Boolean (default: False) value to create a single train,
                test & validation directories for all the classes
  """
  # You can find the reference code here:
  # https://towardsdatascience.com/a-comprehensive-hands-on-guide-to-transfer-learning-with-real-world-applications-in-deep-learning-212bf3b2f27a
  np.random.seed(42)
  # Using glob for getting all the files under ./<directory>/ directory.
  files = glob.glob(f'{directory}/*')
  all_files = [name for name in files if Path(directory).stem in name]
  # If number of 'train_sample' is not provided, it'll take 70% of all
  # the available files.
  if train_sample is None:
      train_sample = int(defaults.TRAIN_SPLIT * len(all_files))
  # Creating an array of randomly chosen training files from all the
  # available files.
  train_files = np.random.choice(all_files, size=train_sample, replace=False)
  # Removing the files that have been already used for training purpose.
  all_files = list(set(all_files) - set(train_files))
  # Similarly, creating an array of randomly chosen test files from all
  # the available files excluding training files.
  test_files = np.random.choice(all_files,
                                size=int(defaults.TEST_SPLIT * train_sample), 
                                replace=False)
  # Removing the files that have been already used for testing purpose.
  all_files = list(set(all_files) - set(test_files))
  # Repeating the process of array creation by randomly choosing
  # validation files from the available files excluding both  training &
  # test files.
  validation_files = np.random.choice(all_files,
                                      size=int(defaults.VALIDATION_SPLIT
                                               * train_sample),
                                      replace=False)
  # Individual file objects to copy in their respective directories.
  files = [train_files, test_files, validation_files]
  if unify_data:
    # Creating train, test and validation directories under session name.
    session_name = session_name if session_name else timestamp('%m%d%y')
    sym_dirs = [os.path.join(symlinks.train, f'{session_name}/train'),
                os.path.join(symlinks.test, f'{session_name}/test'),
                os.path.join(symlinks.validation, f'{session_name}/validation')]
    # Looping over all the files and copying them in their respective
    # directories.
    for idx, sym_idx in zip(files, sym_dirs):
      # Displaying progress bar for copying files into respective
      # directories.
      with tqdm(total=len(idx), desc='Copying', unit=' files') as progress_bar:
        if not os.path.isdir(sym_idx):
          os.makedirs(sym_idx)
        for file in idx:
          shutil.copy(file, sym_idx)
          progress_bar.update(1)
  else:
    # Creating train, test & validation directories.
    (train_dir,
     test_dir,
     validation_dir) = train_test_val_directories(directory, session_name)
    sym_dirs = [train_dir, test_dir, validation_dir]
    # Looping over all the files and copying them in their respective
    # directories.
    for idx, sym_idx in zip(files, sym_dirs):
      # Displaying progress bar for copying files into respective
      # directories.
      with tqdm(total=len(idx), desc='Copying', unit=' files') as progress_bar:
        for file in idx:
          shutil.copy(file, sym_idx)
          progress_bar.update(1)


def create_dataset(directory: str,
                   session_name: str = None,
                   train_sample: int = None,
                   unify_data: bool = False) -> None:
  """Create dataset.

  Create a dataset with 'N' number of training samples. The default
  test & validation split is going to be 20% of the 'train_sample'.
  If 'train_sample' is not provided, it'll create a dataset with 70% of
  the actual training data.

  Args:
    directory: Directory to be used for creating small dataset.
    session_name: Name of the current training session.
    train_sample: Number (default: None) of training samples to use.
    unify_data: Boolean (default: False) value to create a single train,
                test & validation directories for all the classes

  Usage:
    create_dataset('D:/mle/mle/data/raw/vzen', 'xa_2000', 2000, False)
  """
  # Symlink to all the files under training directory.
  all_files = glob.glob(f'{os.path.join(symlinks.train, directory)}/*')
  # Loop to perform train, test & validation split for the mentioned
  # directory.
  for idx in all_files:
    create_train_test_val_split(idx, session_name, train_sample, unify_data)


def rename_image_classification_dataset(session_name: str) -> None:
  """Rename image dataset with respective directory name.

  Rename images with respective directory name. This is required for
  creating the classification labels.

  Args:
    session_name: Name of the current training session.

  Note:
    This function will not work on the datasets created by setting
    'unify_data' argument to True in create_dataset().
  """
  # List of directories whose files need to be renamed.
  dirs = ['train', 'test', 'validation']
  sym_dirs = [os.path.join(symlinks.train, session_name),
              os.path.join(symlinks.test, session_name),
              os.path.join(symlinks.validation, session_name)]
  # Looping through all the directories and renaming the files by
  # prefixing the 'classification label'.
  for idx, sym_idx in zip(dirs, sym_dirs):
    for directory in glob.glob(f'{sym_idx}/*'):
      for _idx, temp in enumerate(glob.glob(f'{directory}/*')):
        extension = os.path.splitext(temp)[1]
        name = (os.path.basename(directory)).split(f'{idx}_')[1]
        file = os.path.join(directory, f'{name}.{_idx}{extension}')
        os.rename(temp, file)


def load_image_classification_dataset(session_name: str,
                                      target_size: Tuple = defaults.MLE_IMG_SIZE
                                      ) -> Tuple:
  """Load an image classification dataset.

  Load an image classification dataset before feeding it to the model.
  This function returns a list of array of the train-validation of
  images for both train-validation images.

  Args:
    session_name: Name of the current training session.
    target_size: Dimension (default: (220, 220)) to which the image
                 array needs to be resized.

  Returns:
    Tuple of train-validation image array lists.
  """
  # The path to the actual training & validation directory where all
  # training and validation data is stored.
  train_dir = os.path.join(symlinks.train, session_name)
  validation_dir = os.path.join(symlinks.validation, session_name)
  # Creating list of training & validation symlinks.
  train_files = glob.glob(f'{train_dir}/train/*')
  validation_files = glob.glob(f'{validation_dir}/validation/*')
  # Creating list of training & validation files.
  files_list = [train_files, validation_files]
  # Initializing empty lists to use it smartly in a for loop for images
  # array.
  train_images, validation_images = [], []
  images_array = [train_images, validation_images]
  # Looping through all the images in training & validation directory,
  # loading them & resizing the array to a 'target_size' and then
  # converting the image data.
  for file, image in zip(files_list, images_array):
    with tqdm(total=len(file), desc='Loading', unit=' files') as progress_bar:
      for idx in file:
        image.append(i2a(li(idx, target_size=target_size)))
        progress_bar.update(1)
  # Returning tuple of list of training & validation images.
  return train_images, validation_images


def scale_image_dataset(session_name: str,
                        target_size: Tuple = defaults.MLE_IMG_SIZE) -> Tuple:
  """Scale an image dataset array.

  Scale an image dataset array's each pixel value between (0, 255) to
  values between (0, 1).
  This step is very important since NN models work well with smaller
  values.

  Args:
    session_name: Name of the current training session.
    target_size: Dimension (default: (200, 200)) to which the images
                 needs to be resized.

  Returns:
    Tuple of scaled train-validation image arrays.
  """
  # Using 'load_image_classification_dataset()' to create a list of
  # train-validation image data.
  (train_images,
   validation_images) = load_image_classification_dataset(session_name,
                                                          target_size)
  # Converting training-validation image data into numpy array.
  train_images = np.array(train_images)
  validation_images = np.array(validation_images)
  # Cast values of train-validation numpy arrays as a float value.
  scaled_train_images = train_images.astype('float32')
  scaled_validation_images = validation_images.astype('float32')
  # Scale individual pixel value to range (0, 1).
  scaled_train_images /= 255
  scaled_validation_images /= 255
  # Return scaled pixel values for both train & validation images..
  return scaled_train_images, scaled_validation_images, train_images, validation_images


def create_image_classification_labels(session_name: str) -> Tuple:
  """Encode image classification labels.

  Encode image classification labels to numeric values. These values
  represent the labels using an Integer. For instance, if you 2 classes
  XA & Unknown; then XA would be encoded as 0 & Unknown would be encoded
  as 1. If there were to be more classes, the number will increase.

  Args:
    session_name: Name of the current training session.

  Returns:
    Tuple of training & validation label encodings.
  """
  # The path to the actual training & validation directory where all
  # training and validation data is stored.
  train_dir = os.path.join(symlinks.train, session_name)
  validation_dir = os.path.join(symlinks.validation, session_name)
  # Creating list of training & validation symlinks.
  train_files = glob.glob(f'{train_dir}/train/*')
  validation_files = glob.glob(f'{validation_dir}/validation/*')
  # Creating list of training & validation files.
  files_list = [train_files, validation_files]
  # Initializing empty lists to use it smartly in a for loop for
  # encoding labels.
  train_labels, validation_labels = [], []
  labels = [train_labels, validation_labels]
  # Get train & validation labels from the name of that image. Since
  # we presume that the classification dataset has images with labels
  # as their filenames.
  # For e.g: ./train/xa/xa.42069.png OR ./train/unknown/unknown.69.png.
  for file, label in zip(files_list, labels):
    with tqdm(total=len(file), desc='Encoding', unit=' files') as progress_bar:
      for idx in file:
        label.append(idx.split('\\')[1].split('.')[0].strip())
        progress_bar.update(1)
  # Encode labels using Sklearn's LabelEncoder().
  label_encoder = LabelEncoder()
  label_encoder.fit(train_labels)
  return (label_encoder.transform(train_labels),
          label_encoder.transform(validation_labels))


def accuracy_vs_loss_plot(history: History,
                          session_name: str,
                          plot_title: str,
                          epochs: int,
                          show_plot: bool = False,
                          save_plot: bool = True) -> None:
  """Save and show Accuracy vs Loss plot.

  Save and show an accuracy vs loss plot for a particular model.

  Args:
    history: History object (dict) which stores statistics of the
             trained model.
    session_name: Name of the current training session.
    plot_title: Name/Title for the plot.
    epochs: Number of times to train the model.
    show_plot: Boolean (default: False) value to display the plot.
    save_plot: Boolean (default: True) value to save the plot.

  Note:
    The saved plots would be saved in ./stats/<session_name>/ directory
    with the 'session_name'.
  """
  # Skip further execution if number of epochs is 1.
  if epochs > 1:
    # Create directory to store the plots.
    directory = os.path.join(symlinks.stats, session_name)
    if not os.path.isdir(directory):
      os.makedirs(directory)
    # Create an instance of a plot with only 2 sublots, Accuracy & loss.
    figure, (accuracy, loss) = plt.subplots(1, 2, figsize=(12, 4))
    # Plot title.
    figure.suptitle(plot_title, fontsize=12)
    # Defining our range of epochs.
    epoch_list = list(range(1, epochs + 1))
    # Accuracy plot.
    accuracy.plot(epoch_list, history.history['accuracy'], 
                  label=f'Training accuracy')
    accuracy.plot(epoch_list, history.history['val_accuracy'],
                  label=f'Validation accuracy')
    accuracy.set_xticks(np.arange(0, epochs + 1, 5))
    accuracy.set_ylabel('Accuracy')
    accuracy.set_xlabel('Epoch')
    accuracy.set_title('Accuracy')
    # Loss plot.
    loss.plot(epoch_list, history.history['loss'], label=f'Training loss')
    loss.plot(epoch_list, history.history['val_loss'], label=f'Validation loss')
    loss.set_xticks(np.arange(0, epochs + 1, 5))
    loss.set_ylabel('Loss')
    loss.set_xlabel('Epoch')
    loss.set_title('Loss')
    # Options to save & display the plot.
    if save_plot:
      plt.savefig(os.path.join(directory, f'{session_name}'))
    if show_plot:
      plt.show()
