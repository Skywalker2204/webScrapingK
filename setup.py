#!/usr/bin/env python3
# -*- coding: utf-8 -*-from setuptools import setup
setup(
    name = 'webScrapingK',
    version = '0.1.0',
    packages = ['webScrapingK'],
    entry_points = {
        'console_scripts': [
            'webScrapingK = webScrapingK.__main__:main'
        ]
    })