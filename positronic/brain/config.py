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
This module contains BuildBot's global configuration dictionary, which should eventually appear
as a 'BuildmasterConfig' symbol in the top level configuration file of the master, which means
that you should use 'from config import *' to import this module.
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


BrainConfig = {
    'emailFrom': 'buildbot@example.com',
    'emailLookup': 'example.com',
}
