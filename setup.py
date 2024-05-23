from setuptools import setup, find_packages

setup(
  name='qoo10',
  version='0.0.1',
  packages=find_packages(include=['qoo10', 'qoo10.*']),
  install_requires=['selenium'],
)