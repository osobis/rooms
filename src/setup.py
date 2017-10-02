import os
from setuptools import setup, find_packages


setup(
    version='0.0.1',
    name='room_number_calculator',
    packages=find_packages(),
    author='Leszek Skoczylas',
    author_email='leszek.skoczylas@mac.com',
    description='Room Number Calculator',
    entry_points={'console_scripts': [
        "room_calculator_demo = rooms.main:main",
    ]}
)