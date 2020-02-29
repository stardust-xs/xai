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

from setuptools import find_packages, setup

from mle.constants import project


def use_readme() -> str:
  """Use `README.md` for parsing long description."""
  with open('README.md') as file:
    return file.read()


with open('requirements.txt', 'r') as requirements:
  required_packages = [package.rstrip() for package in requirements]

setup(
  name=project.PROJECT_NAME,
  version=project.PROJECT_VERSION,
  url=project.PROJECT_LINK,
  author=project.AUTHOR,
  author_email=project.AUTHOR_EMAIL,
  maintainer=project.AUTHOR,
  maintainer_email=project.AUTHOR,
  classifiers=[
    'Development Status :: 1 - Planning',
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
    'Topic :: Communications :: Chat',
    'Topic :: Communications :: Email',
    'Topic :: Database',
    'Topic :: Education :: Testing',
    'Topic :: Home Automation',
    'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    'Topic :: Multimedia',
    'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Players',
    'Topic :: Multimedia :: Video :: Capture',
    'Topic :: Office/Business :: Scheduling',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Software Development',
    'Topic :: Software Development :: Documentation',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Networking :: Monitoring :: Hardware Watchdog',
    'Topic :: System :: Networking :: Time Synchronization',
  ],
  license=project.PROJECT_LICENSE,
  description=__doc__,
  long_description=use_readme(),
  long_description_content_type='text/markdown',
  keywords='mle machine learning artificial intelligence pandas numpy cv2',
  zip_safe=False,
  install_requires=required_packages,
  python_requires='~=3.6',
  include_package_data=True,
  packages=find_packages(),
)
