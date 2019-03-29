#!/usr/bin/env python
# -*- coding: utf-8 -*

import setuptools


NAME = "celorm"
VERSION = "0.0.8"
URL = "https://github.com/swoiow/celorm"

EXTRAS_CLI = [
    "fire",
]

EXTRAS_FULL = EXTRAS_CLI + [
    "alembic",
]

DEPENDENCIES = [
    "colorama",
    "sqlalchemy",
]

setuptools.setup(
    name=NAME,
    version=VERSION,

    url=URL,
    license="MPL-2.0",

    packages=[NAME],
    package_dir={
        NAME: "src/orm",
    },
    include_package_data=True,
    entry_points={
        "console_scripts": ["celorm=celorm.cli:main"],
    },

    zip_safe=False,
    extras_require={
        "cli": EXTRAS_CLI,
        "full": EXTRAS_FULL,
    },
    install_requires=DEPENDENCIES,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
)
