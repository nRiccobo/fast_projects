"""Setup script"""
import os

from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name="fast_projects",
    author="Nick Riccobono",
    version=0.1,
    install_requires=open("requirements.txt").readlines(),
)