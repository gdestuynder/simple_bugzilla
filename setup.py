#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2015 Mozilla Corporation
#
# Author: gdestuynder@mozilla.com

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bugzilla",
        py_modules = ['bugzilla'],
        version = '1.0.0',
        author = "Guillaume Destuynder",
        author_email = "gdestuynder@mozilla.com",
        description = ("A client library for Bugzilla"),
        license = "MPL",
        keywords = "bugzilla client library",
        url = "https://github.com/gdestuynder/simple_bugzilla",
        long_description = read('README.rst'),
        requires = [],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
)
