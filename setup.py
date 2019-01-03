#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import io
import sys

from setuptools import setup, find_packages

assert sys.version_info >= (3, 6, 0), "whatsonpypi requires Python 3.6+"

# Package meta-data.
NAME = 'whatsonpypi'
VERSION = '0.1.1'
DESCRIPTION = "CLI tool to find package info on PyPI"
AUTHOR = "Visesh Prasad"
EMAIL = 'viseshrprasad@gmail.com'
URL = 'https://github.com/viseshrp/whatsonpypi'
REQUIRES_PYTHON = ">=3.6"
REQUIREMENTS = ['Click>=6.0', 'requests>=2.18.0', ]
SETUP_REQUIREMENTS = ['pytest-runner', ]
TEST_REQUIREMENTS = ['pytest', ]

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

with io.open('HISTORY.rst', 'r', encoding='utf-8') as history_file:
    HISTORY = history_file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README + '\n\n' + HISTORY,
    keywords='whatsonpypi',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(include=['whatsonpypi']),
    include_package_data=True,
    license="MIT license",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'whatsonpypi=whatsonpypi.__main__:main',
        ],
    },
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False,
)
