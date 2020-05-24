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

"""Utility for logging X.AI events."""

import errno
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Tuple

from pkg_resources import resource_filename

from xai.utils.misc import Neo


class LordFriezaFormatter(logging.Formatter, metaclass=Neo):
  """
  Lord Frieza Formatter

  The Lord Frieza Formatter is a log formatter class for logging various
  log levels. This custom formatter provides clean & uniform logs across
  all logging levels including exceptions.

  Name of the class is inspired by arguably the best-known villain in
  entire DragonBall franchise - Frieza, who has multiple forms
  throughout the series.
  """

  def __init__(self) -> None:
    """Instantiate class."""
    self._msg_fmt = ('%(asctime)s.%(msecs)03d    {}    {:>13}:%(lineno)04d    '
                     '%(process)05d    %(msg)s')
    self._date_fmt = '%b %d, %Y %H:%M:%S'
    self._exc_fmt = '{0} caused due to {1} on line {2}.'

  def formatException(self, exc_info: Tuple) -> str:
    """
    Format traceback exception message into a usable string.

    Args:
      exc_info: Tuple of LogRecord object.

    Returns:
      String representation of the exception message.
    """
    result = super(LordFriezaFormatter, self).formatException(exc_info)
    return repr(result)

  def format(self, record: logging.LogRecord) -> str:
    """
    Format output log message.

    Args:
      record: Log record message object.

    Returns:
      Formatted output log message.
    """
    mini = record.filename[:10] + bool(record.filename[10:]) * '...'

    fmts = {
        logging.DEBUG: self._msg_fmt.format('DBG', mini),
        logging.INFO: self._msg_fmt.format('INF', mini),
        logging.WARNING: self._msg_fmt.format('WRN', mini),
        logging.ERROR: self._msg_fmt.format('ERR', mini),
        logging.CRITICAL: self._msg_fmt.format('CTL', mini)
    }

    formatter = logging.Formatter(fmts.get(record.levelno), self._date_fmt)
    formatted = formatter.format(record)

    if record.exc_text:
      exc_fmt = self._exc_fmt.format(record.exc_info[1].__class__.__name__,
                                     str(record.msg).lower(),
                                     record.exc_info[2].tb_lineno)
      raw = formatted.replace('\n', '')
      raw = raw.replace(str(record.exc_info[-2]), exc_fmt).replace('ERR', 'EXC')
      formatted, _, _ = raw.partition('Traceback')
    return formatted


class BackThatAssUp(RotatingFileHandler, metaclass=Neo):
  """
  Back That Ass Up

  "Back that ass up" is a Rotating file handler class which basically
  creates a backup of the log to rollover once it reaches a
  predetermined size. When the log is about to be exceed the set size,
  the file is closed and a new log is silently opened for logging.

  This class ensures that the file won't grow indefinitely.
  """

  def __init__(self, file: str, mode: str = 'a',
               max_bytes: int = 0, backups: int = 0,
               encoding: str = None, delay: bool = False) -> None:
    """Instantiate class.

    Args:
      file: Log file to backup.
      mode: Log file writing mode.
      max_bytes: Maximum file size limit for backup.
      backups: Total number of backup.
      encoding: File encoding.
      delay: Delay for backup.
    """
    self._bkp_num = 0
    super(BackThatAssUp, self).__init__(filename=file,
                                        mode=mode,
                                        maxBytes=max_bytes,
                                        backupCount=backups,
                                        encoding=encoding,
                                        delay=delay)

  def doRollover(self) -> None:
    if self.stream:
      self.stream.close()

    self._bkp_num += 1
    self.rotate(self.baseFilename, f'{self.baseFilename}_{self._bkp_num}')

    if not self.delay:
      self.stream = self._open()


class SilenceOfTheLog(object, metaclass=Neo):
  """
  Silence of the Log

  The Silence of the Log is a silent logger which monitors & logs X.AI
  events. The logger silently does its job without drawing any attention
  to it.
  """

  def __init__(self, file: str) -> None:
    """
    Instantiate class.

    Args:
      file: File to log messages for.
    """
    self._file = file
    self._path = resource_filename('xai', '/logs/')

    try:
      os.mkdir(self._path)
    except OSError as _error:
      if _error.errno != errno.EEXIST:
        raise

    self._log = ''.join([self._path, '{}.log'])

  def log(self, name: str = None, level: str = 'debug',
          max_bytes: int = None, backups: int = None) -> logging.Logger:
    """
    Log X.AI events.

    Args:
      name: Name for log file.
      level: Default logging level to log messages.
      max_bytes: Maximum file size limit for backup.
      backups: Total number of backup.

    Returns:
      Logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(f'{level.upper()}')

    raw = name.lower() if name else Path(self._file.lower()).stem
    mem = int(max_bytes) if max_bytes else 1000000
    bkp = int(backups) if backups else 0

    # Create backup of the log once the file size reaches 1 Mb.
    file_handler = BackThatAssUp(self._log.format(raw.replace(' ', '_')),
                                 max_bytes=mem, backups=bkp)
    file_handler.setFormatter(LordFriezaFormatter())
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(LordFriezaFormatter())
    logger.addHandler(stream_handler)
    return logger
