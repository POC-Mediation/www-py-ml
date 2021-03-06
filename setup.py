"""
PredicteurClauses app
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
    name='www-py-ml',
    version='1.0.0',
    description='PredicteurClauses app on IBM Cloud',
    long_description=long_description,
    url='https://git.eu-de.bluemix.net/xavier.mary/www-py-ml',
    license='MIT'
)
