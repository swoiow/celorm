#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="myorm",
    version="0.0.5",

    license='MIT',

    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks", "app"],
    ),

    entry_points={
        "console_scripts": [
            "myorm=myorm:main",
        ],
    },

    zip_safe=False,
    install_requires=[
        "fire",
        "alembic",
    ],
    python_requires='>=3.3',
)
