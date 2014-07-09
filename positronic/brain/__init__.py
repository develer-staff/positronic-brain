# -*- coding: utf-8 -*-
#
# Positronic Brain - Opinionated Buildbot Workflow
# Copyright (C) 2014  Develer S.r.L.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Importing this module with the statement

    from positronic.brain import *

imports all classes and symbols needed to configure the master, all workers and build jobs. It
should usually be the only import you need, since we take care to import and expose all you need
from this namespace.
"""

# Monkey patch stuff.
from positronic.brain.monkeypatch import patch_all

patch_all()

# Continue with standard bootstrap.
from positronic.brain.base import change_source, master, worker
from positronic.brain.config import BrainConfig, BuildmasterConfig
from positronic.brain.job.freestyle import FreestyleJob
from positronic.brain.job.workerpool import WorkerPoolJob


__all__ = [
    'BrainConfig',
    'BuildmasterConfig',
    'FreestyleJob',
    'WorkerPoolJob',
    'change_source',
    'master',
    'worker',
]
