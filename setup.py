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

"""M.L.E (Emily), a simple AI."""

import os

from setuptools import find_packages, setup

DOCLINES = __doc__.split('\n')

# This version string is semver compatible & adheres to Semantic
# Versioning Specification (SemVer) starting with version 0.1.
# You can read more about it here: https://semver.org/spec/v2.0.0.html
_version = '3.0.0'

PROJECT_NAME = 'mle'

with open('requirements.txt', 'r') as requirements:
  required_packages = [package.rstrip() for package in requirements]

# Skip downloading packages meant for Windows when running on a Linux
# machine. This ensures proper package download for the respective OS.
if os.name != 'nt':
  skip = ['pywin32', 'pywinauto', 'uiautomation', 'win10toast']
  required_packages = [idx for idx in required_packages if idx not in skip]


def use_readme() -> str:
  """Use README.md for long description."""
  with open('README.md', 'r') as file:
    return file.read()


setup(
  name=PROJECT_NAME,
  version=_version,
  url='https://github.com/xames3/mle/',
  author='XAMES3',
  author_email='xames3.developer@gmail.com',
  maintainer_email='mle.xames3@gmail.com',
  # PyPI package information.
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
    'Topic :: Multimedia :: Video :: Capture',
    'Topic :: Office/Business :: Scheduling',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Networking :: Monitoring :: Hardware Watchdog',
    'Topic :: System :: Networking :: Time Synchronization',
  ],
  license='Apache 2.0',
  description=DOCLINES[0],
  long_description=use_readme(),
  long_description_content_type='text/markdown',
  keywords='mle machine learning artificial intelligence pandas numpy cv2',
  zip_safe=False,
  install_requires=required_packages,
  python_requires='~=3.6',
  include_package_data=True,
  packages=find_packages(),
)
