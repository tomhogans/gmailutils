from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Gmail',
      version=version,
      description="Gmail Utility",
      long_description="""Utilities for Gmail Services""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tom Hogans',
      author_email='tomhsx@gmail.com',
      url='',
      license='See LICENSE file',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml',
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
