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

packages = ['choppyzs']
setup(name='choppyzs',
        version='1.0.4',
        author='Joshua N. Grant',
        description=long_description,
        scripts=scripts,
        examples=examples,
        author_email='grantjn@ornl.gov',
        url='https://github.com/gshs-ornl/choppy',
        packages=packages)

