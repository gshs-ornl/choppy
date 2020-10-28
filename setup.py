#!/usr/bin/env python3

import os
import sys
import glob
from setuptools import setup, find_packages

root_dir = os.path.abspath(os.path.dirname(__file__))

scripts = ['choppy-lite.py']
scripts.extend(glob.glob(os.path.join(root_dir,'scripts/*')))

long_description = open(os.path.join(root_dir, 'README.md')).read()
examples = os.path.join(root_dir,'examples')

setup(name='choppy',
        version='1.0.1',
        author='Joshua N. Grant',
        description=long_description,
        scripts=scripts,
        examples=examples,
        author_email='grantjn@ornl.gov',
        url='https://code.ornl.gov/6ng/choppy-lite',
        packages=find_packages())
