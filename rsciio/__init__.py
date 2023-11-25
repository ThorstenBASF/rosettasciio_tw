# -*- coding: utf-8 -*-
# Copyright 2007-2023 The HyperSpy developers
#
# This file is part of RosettaSciIO.
#
# RosettaSciIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RosettaSciIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RosettaSciIO. If not, see <https://www.gnu.org/licenses/#GPL>.

from importlib.metadata import version
import logging
import os
from pathlib import Path
import yaml


_logger = logging.getLogger(__name__)
IO_PLUGINS = []

__version__ = version("rosettasciio")

# For development version, `setuptools_scm` will be used at
# build time to get the dev version:
# - in case of missing vcs information, it will fallback to the
#   version defined in pyproject.toml will be used
# - in case of shallow checkout (pip install git+https://...)

# if we have a editable install from a git repository try to use
# `setuptools_scm` to find a more accurate version:
# `importlib.metadata` will provide the version at installation
# time and for editable version this may be different

# we only do that if we have enough git history, e.g. not shallow checkout
_root = Path(__file__).resolve().parents[1]
if (_root / ".git").exists() and not (_root / ".git/shallow").exists():
    try:
        # setuptools_scm may not be installed
        from setuptools_scm import get_version

        __version__ = get_version(_root)
    except ImportError:  # pragma: no cover
        # setuptools_scm not install, we keep the existing __version__
        pass


for sub, _, _ in os.walk(os.path.abspath(os.path.dirname(__file__))):
    _specsf = os.path.join(sub, "specifications.yaml")
    if os.path.isfile(_specsf):
        with open(_specsf, "r") as stream:
            _specs = yaml.safe_load(stream)
            # for testing purposes
            _specs["api"] = "rsciio.%s" % os.path.split(sub)[1]
            IO_PLUGINS.append(_specs)


__all__ = [
    "__version__",
    "IO_PLUGINS",
]


def __dir__():
    return sorted(__all__)
