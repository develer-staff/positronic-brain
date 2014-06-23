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
