# -*- coding: utf-8 -*-
#
# Positronic Brain - Opinionated Buildbot Workflow
# Copyright 2014 Develer S.r.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
