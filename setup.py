#!/usr/bin/env python3
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata = {}

here = os.path.abspath(os.path.dirname(__file__))

NAME = "autosub"

with open(os.path.join(here, NAME, "metadata.py"), encoding='utf-8') as metafile:
    exec(metafile.read(), metadata)

setup(
    name=metadata['NAME'],
    version=metadata['VERSION'],
    description=metadata['DESCRIPTION'],
    long_description=metadata['LONG_DESCRIPTION'],
    author=metadata['AUTHOR'],
    author_email=metadata['AUTHOR_EMAIL'],
    url=metadata['HOMEPAGE'],
    packages=['autosub'],
    entry_points={
        'console_scripts': [
            'autosub = autosub:main',
        ]
    },
    package_data={'autosub': ['data/locale/zh_CN/LC_MESSAGES/*mo']},
    install_requires=[
        'requests>=2.3.0',
        'pysubs2>=0.2.4',
        'progressbar2>=3.34.3',
        'auditok==0.1.5',
        'googletrans>=2.4.0',
        'wcwidth>=0.1.7',
        'fuzzywuzzy>=0.18.0',
        'google-cloud-speech>=1.3.1',
        'websocket-client>=0.56.0',
        'send2trash>=1.5.0'
    ],
    license=open(os.path.join(here, "LICENSE")).read()
)
