from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='vinlander',
    version='0.1.0',
    description='Occupation explorer using 2018 US BLS ' +
    'Standard Occupational Classification',
    author='Brian Wu',
    packages=find_packages()
)
