#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    print('Flask-Webpack-Current needs setuptools in order to build. ' +
          'Install it using your package manager ' +
          '(usually python-setuptools) or via pip (pip install setuptools).')
    sys.exit(1)

setup(name='Flask-Webpack-Current',
      version=open('VERSION', 'r').read()[:-1],
      author='Nick Janetakis, Alexey Trifonov',
      author_email='nick.janetakis@gmail.com, avrong@outlook.com',
      url='https://github.com/avrong/flask-webpack-current',
      description='Flask extension for managing assets with Webpack.',
      license='GPLv3',
      install_requires=['setuptools', 'Flask'],
      tests_require=['pytest'],
      packages=['flask_webpack_current'],
      package_data={'Flask-Webpack-Current': ['VERSION']},
      zip_safe=False,
      data_files=[])
