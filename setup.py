#!/usr/bin/env python
"""
Setup script for Domain-SC.
"""

import os
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read long description from README.md
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="domain-sc",
    version="0.1.0",
    description="AI-powered system architecture design tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Domain-SC Team",
    author_email="example@example.com",
    url="https://github.com/halitipek/Domain-SC",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "domain-sc=src.cli.cli:run",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)