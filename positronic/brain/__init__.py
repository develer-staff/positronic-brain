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

from buildbot.buildslave import BuildSlave
from buildbot.status.html import WebStatus
from buildbot.status.web.authz import Authz

from positronic.brain.config import BrainConfig, BuildmasterConfig
from positronic.brain.job.freestyle import FreestyleJob
from positronic.brain.job.matrix import MatrixJob


def master(url, email_from, title='BuildBot'):
    BrainConfig['emailFrom'] = email_from
    BrainConfig['emailLookup'] = email_from.split('@')[-1]

    BuildmasterConfig['buildbotURL'] = url if url.endswith('/') else url + '/'
    BuildmasterConfig['title'] = title
    BuildmasterConfig['titleURL'] = BuildmasterConfig['buildbotURL']

    # Launches the web interface with no authentication by default, allowing all users to start and
    # stop builds.
    BuildmasterConfig['status'] = [
        WebStatus(
            http_port=8010,
            authz=Authz(forceBuild=True, stopBuild=True))
    ]


def slave(name, password):
    # In general, our slaves assume that they have full control of the machine they are running on,
    # thus, we force at most one job running on each node at a time.
    BuildmasterConfig['slaves'].append(BuildSlave(name, password, max_builds=1))
