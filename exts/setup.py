"""Installation script for the 'genesis_go2' python package."""

import os
import toml

from setuptools import setup

# Installation operation
from setuptools import setup, find_packages

setup(
    name="genesis_go2",
    version="0.1.0",
    packages=["genesis_go2"],
    author="Sol Choi",
    author_email="solchoi@yonsei.ac.kr",
    maintainer="Sol Choi",
    maintainer_email="solchoi@yonsei.ac.kr",
    description="Scripts and utilities for genesis_go2",
    url="https://github.com/ARC-KIST/genesis-go2.git",
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
)
