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
from positronic.brain.utils import get_default_email_address


def master(url, email_from=None, title='BuildBot'):
    # BrainConfig holds global configuration values which would not be recognized if put in
    # BuildmasterConfig.
    BrainConfig['emailFrom'] = email_from if email_from else get_default_email_address(url)
    BrainConfig['emailLookup'] = BrainConfig['emailFrom'].split('@')[-1]

    # Site definition
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#site-definitions
    BuildmasterConfig['buildbotURL'] = url if url.endswith('/') else url + '/'
    BuildmasterConfig['title'] = title
    BuildmasterConfig['titleURL'] = BuildmasterConfig['buildbotURL']

    # Data retention
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#horizons
    BuildmasterConfig['buildHorizon'] = 100   # How many builds to keep.
    BuildmasterConfig['changeHorizon'] = 200  # How many Change(s) to keep.
    BuildmasterConfig['eventHorizon'] = 50    # Connection/Disconnection to slaves to keep.
    BuildmasterConfig['logHorizon'] = 50      # How many build logs to keep. Must be <= buildHorizon.

    # Caches
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#caches
    BuildmasterConfig['caches'] = {
        'BuildRequests' : 10,
        'Builds' : 500,
        'Changes' : 100,
        'chdicts' : 100,
        'objectids' : 10,
        'SourceStamps' : 20,
        'ssdicts' : 20,
        'usdicts' : 100,
    }

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
