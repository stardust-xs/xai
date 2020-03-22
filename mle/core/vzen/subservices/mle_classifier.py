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
"""A subservice for training classification models."""

import os
from typing import List, Tuple

from keras import optimizers
from keras.applications import vgg16
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.models import Sequential, Model
from keras.preprocessing.image import ImageDataGenerator

from mle.constants import defaults
from mle.utils import symlinks
from mle.utils.components import accuracy_vs_loss_plot as plt
from mle.utils.components import create_image_classification_labels as labels
from mle.utils.components import scale_image_dataset


def cnn_classification_model(session_name: str,
                             model_name: str = None,
                             model_path: str = symlinks.models,
                             input_shape: Tuple = defaults.MLE_IMG_INPUT_SHAPE,
                             batch_size: int = 30,
                             loss: str = 'binary_crossentropy',
                             optimizer: str = optimizers.RMSprop(lr=1e-4),
                             epochs: int = 100,
                             steps_per_epoch: int = 100,
                             validation_steps: int = 50,
                             metrics: List = ['accuracy'],
                             rescale: float = 1./255,
                             shear_range: float = 0.2,
                             zoom_range: float = 0.3,
                             horizontal_flip: bool = True,
                             rotation_range: int = 50,
                             shift_range: float = 0.2,
                             fill_mode: str = 'nearest',
                             verbose: bool = True,
                             show_plot: bool = True,
                             save_plot: bool = True) -> None:
  """Basic CNN based classification model generator."""
  _, _, train_images, validation_images = scale_image_dataset(session_name)
  train_labels, validation_labels = labels(session_name)
  # Performing image data generation by rescaling, zooming, rotating &
  # whatnot on the training data. This step is essential when the input
  # training images are quite less.
  train_data = ImageDataGenerator(rescale=rescale,
                                  shear_range=shear_range,
                                  zoom_range=zoom_range,
                                  horizontal_flip=horizontal_flip,
                                  rotation_range=rotation_range,
                                  width_shift_range=shift_range,
                                  height_shift_range=shift_range,
                                  fill_mode=fill_mode)
  # Creating validation image data using the same 'ImageDataGenerator'.
  validation_data = ImageDataGenerator(rescale=rescale)
  # Accessing the 'train data' generator from 'train_dir' directory and
  # resizing the images to the 'target_size' in batches of 'batch_size'.

  train_generator = train_data.flow(train_images, train_labels, batch_size)

  # Similarly, accessing the 'validation_data' generator from it's
  # respective 'validation_dir' directory, rescaling to required
  # 'target_size' and accessing batches of 'batch_size'.

  validation_generator = validation_data.flow(validation_images,
                                              validation_labels,
                                              int(batch_size / 0.6))
  model = Sequential()
  model.add(Conv2D(16, kernel_size=(3, 3),
                   activation='relu', input_shape=input_shape))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Flatten())
  model.add(Dense(512, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(512, activation='relu'))
  model.add(Dropout(0.3))
  model.add(Dense(1, activation='sigmoid'))
  # Option to display the model summary i.e. information of the all the
  # layers that are present.
  verbose_value = 0
  if verbose:
    model.summary()
    verbose_value = 1
  # Using session name as the model name if no model name is provided.
  model_name = model_name if model_name else f'{session_name}.h5'
  # Add the model tuning hyperparameters.
  # Default optimizer is 'Adam', loss is 'Categorical crossentropy' &
  # metrics to consider is 'Accuracy'.
  model.compile(optimizer, loss, metrics)
  history = model.fit_generator(train_generator,
                                steps_per_epoch=steps_per_epoch,
                                epochs=epochs,
                                validation_data=validation_generator,
                                validation_steps=validation_steps,
                                verbose=verbose_value)
  plt(history, session_name, 'MLE CNN model', epochs, show_plot, save_plot)
  model.save(os.path.join(model_path, model_name))


cnn_classification_model('xa_300', epochs=1)
