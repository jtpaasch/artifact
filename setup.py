# -*- coding: utf-8 -*-

"""The ``setup.py`` script."""

from setuptools import setup, find_packages
from codecs import open
from os import path

# Where are we? Full path.
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(

    # What's the project name?
    # E.g., so you can type ``pip install <name>``.
    name="artifact",

    # Semantic versioning (comlpiant with PEP-440).
    version="0.1.0",

    # What's the project about?
    description="A tool for deploying into AWS.",
    long_description=long_description,
    keywords="cli amazon aws deployment",

    # Which license?
    license="MIT",

    # Where is the source code hosted?
    url="http://github.com/jtpaasch/artifact",

    # Author(s)?
    author="JT Paasch",
    author_email="jt.paasch@gmail.com",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
    ],

    # Include non-Python files? (E.g., LICENSE, etc.)
    include_package_data=True,

    # Which packages are included in the dist?
    packages=find_packages(
        exclude=[
            "venv",
            "tests",
        ]
    ),

    # What are the run-time dependencies?
    install_requires=[
        "jupyter",
        "click",
        "boto3",
    ],

    # Are there any other dependencies, e.g., for testing?
    extras_require={
        "test": [
            "coverage",
            "hypothesis",
            "flake8",
            "pep257",
        ],
    },

    # What are the scripts/executables?
    entry_points={
        "console_scripts": [
            "artifact = artifact.cli.main:cli",
            "stats = artifact.stats.console.main:start",
        ]
    },

)
