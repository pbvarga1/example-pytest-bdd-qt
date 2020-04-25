import os
import re

from distutils.core import setup


setup(
    name='example',
    version='0.1.0',
    description='Example pytest-bdd with pytest-qt',
    author='Perry Vargas',
    packages=['example'],
    install_requires=['qtpy==1.9.0']
)
