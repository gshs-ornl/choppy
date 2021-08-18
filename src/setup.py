#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup file for the choppy zonal statistics package."""
import os
import glob
from pathlib import Path
from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))
if os.path.exists('/examples'):
    examples_dir = '/examples'
else:
    repo_dir = str(Path(root_dir).parent)
    examples_dir = os.path.join(repo_dir, 'examples')

scripts = ['choppy-lite.py']
scripts.extend(glob.glob(os.path.join(root_dir, 'scripts/*')))

long_description = open(os.path.join(root_dir, 'README.md')).read()

packages = ['choppyzs']
setup(name='choppyzs',
      version='1.0.4',
      author='Joshua N. Grant',
      description=long_description,
      scripts=scripts,
      examples=examples_dir,
      author_email='grantjn@ornl.gov',
      url='https://github.com/gshs-ornl/choppy',
      packages=packages)
