"""
IBM Coursera Advanced Data Science Capstone Project - Demo App
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dash-capstone',
    version='1.0.0',
    description='IBM Coursera Advanced Data Science Capstone Project - Demo App',
    long_description=long_description,
    url='https://github.com/kcostya/ibm-coursera-capstone/tree/master/dash_app',
    license='Apache-2.0'
)
