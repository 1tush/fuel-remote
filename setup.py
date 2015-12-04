#!/usr/bin/env python

from distutils.core import setup

setup(
    name='fuel_remote',
    version='0.1dev1',
    description='Run fuel-qa tests remote',
    author='Georgy Dyuldin',
    author_email='g.dyuldin@gmail.com',
    packages=['fuel_remote'],
    scripts=['bin/rem'],
    url="https://github.com/1tush/fuel-remote",
    install_requires=[
        'pyyaml',
    ],
)
