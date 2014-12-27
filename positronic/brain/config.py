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
This module contains the `BuildmasterConfig` dictionary used by BuildBot to configure the master.

It additionally contains the `BrainConfig` dictionary for all global settings which we can't put
into the `BuildmasterConfig` dictionary since BuildBot complains if it finds unknown stuff in there.

Please note that the `BuildmasterConfig` MUST appear in the top-level context of the configuration
file read by the master when it starts up, which means that you MUST use the `from
positronic.brain.config import *` and make sure the symbol 'flows up' until it is exposed from the
topmost configuration file.
"""

BuildmasterConfig = {
    'db': {'db_url': 'sqlite:///state.sqlite'},
    'slavePortnum': 9989,

    'builders': [],
    'change_source': [],
    'schedulers': [],
    'slaves': [],
    'status': [],
}

BrainConfig = {}
