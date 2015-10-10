import os
import sys
import logging
import multiprocessing
from setuptools import setup, find_packages

version='0.6.1'

install_requires = ['setuptools',
                    'pyramid >= 1.4',
                    'pyramid_chameleon',
]

tests_require = install_requires + ['nose']

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='player',
      version=version,
      description=('Pyramid view layers'),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: Implementation :: CPython",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          'Topic :: Internet :: WWW/HTTP :: WSGI'],
      author='Nikolay Kim',
      author_email='fafhrd91@gmail.com',
      url='https://github.com/fafhrd91/player/',
      license='BSD',
      packages=find_packages(),
      install_requires = install_requires,
      tests_require = tests_require,
      test_suite = 'nose.collector',
      include_package_data = True,
      zip_safe = False,
      entry_points = {
          'console_scripts': [
              'player = player.script:main',
          ],
      },
  )
