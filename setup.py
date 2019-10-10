#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=6.0',
    'aiofiles',
    'aiohttp',
    'async_timeout',
    'av',
    'cached-property',
    'tenacity',
    'm3u8',
    'pycryptodome',
    'progress',
    'wrapt',
    'yarl'
]

setup_requirements = []

test_requirements = ['pytest', 'pytest-runner', 'pytest-asyncio', 'pytest-aiohttp']

setup(
    author="Soul Melody",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="An asynchronous terminal-based hls video stream (m3u8) downloader & combiner, with AES-128 decryption support.",
    entry_points={
        'console_scripts': [
            'hls-get=hls_get.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    include_package_data=True,
    keywords='hls_get',
    name='hls-get',
    packages=find_packages(include=['hls_get']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SoulMelody/hls-get',
    version='0.1.0',
    zip_safe=False,
)
