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
Contains functions to perform basic initialization of a master node.
"""

import os
import os.path

import jinja2
from buildbot.buildslave import BuildSlave
from buildbot.changes.pb import PBChangeSource
from buildbot.status.html import WebStatus
from buildbot.status.mail import MailNotifier
from buildbot.status.web.authz import Authz

from positronic.brain.config import BrainConfig, BuildmasterConfig
from positronic.brain.mail import html_message_formatter
from positronic.brain.utils import get_default_email_address


def master(basedir, url, admins=[], email_from=None, title='BuildBot'):
    """Configures the BuildBot master.

    This should be the first call in your BuildBot configuration file. It spawns the web server on
    port 8010. The web server DOES NOT HAVE AUTHENTICATION ENABLED, so make sure to put a reverse
    proxy in front of it.

    Arguments:

    - basedir: The master's base directory. This should be the `basedir` global variable which would
      be defined inside the `master.cfg` configuration file.
    - url: The URL where users can find this BuildBot instance.
    - admins: A list of strings which contains the email addresses of all administrators. NOTE: They
      will receive an email for any build that happens.
    - email_from: The email address used in the 'From:' field for all outgoin email messages.
    - title: The title shown in the web interface.

    Example:

        master(basedir=basedir, url='http://buildbot.example.com')

    """
    # BrainConfig holds global configuration values which would not be recognized if put in
    # BuildmasterConfig.
    BrainConfig['basedir'] = basedir
    BrainConfig['emailFrom'] = email_from if email_from else get_default_email_address(url)
    BrainConfig['emailLookup'] = BrainConfig['emailFrom'].split('@')[-1]
    BrainConfig['maxArtifacts'] = 5
    BrainConfig['artifactsDir'] = os.path.join(basedir, 'public_html', 'artifacts')

    # Site definition
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#site-definitions
    BuildmasterConfig['buildbotURL'] = url if url.endswith('/') else url + '/'
    BuildmasterConfig['title'] = title
    BuildmasterConfig['titleURL'] = BuildmasterConfig['buildbotURL']

    # Data retention
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#horizons
    BuildmasterConfig['buildHorizon'] = 100  # How many builds to keep.
    BuildmasterConfig['changeHorizon'] = 200  # How many Change(s) to keep.
    BuildmasterConfig['eventHorizon'] = 50  # Connection/Disconnection to slaves to keep.
    BuildmasterConfig['logHorizon'] = 50  # How many build logs to keep. Must be <= buildHorizon.

    # Caches
    # See: http://docs.buildbot.net/current/manual/cfg-global.html#caches
    BuildmasterConfig['caches'] = {
        'BuildRequests': 10,
        'Builds': 500,
        'Changes': 100,
        'chdicts': 100,
        'objectids': 10,
        'SourceStamps': 20,
        'ssdicts': 20,
        'usdicts': 100,
    }

    # Launches the web interface with no authentication by default, allowing all users to start and
    # stop builds.
    BuildmasterConfig['status'] = [
        WebStatus(
            authz=Authz(forceBuild=True, stopBuild=True),
            http_port=8010,
            change_hook_dialects={
                'base': True,
                'bitbucket': True,
                'github': True,
            },
            jinja_loaders=[
                jinja2.PackageLoader('positronic.brain.status.web', 'templates'),
            ])
    ]

    # These people receive emails for EVERYTHING that happens within this BuildBot.
    if admins:
        BuildmasterConfig['status'].append(MailNotifier(
            extraRecipients=admins,
            fromaddr=BrainConfig['emailFrom'],
            messageFormatter=html_message_formatter,
            mode='all',
            sendToInterestedUsers=False))


def worker(name, password):
    """Adds a new worker node.

    All worker nodes are configured to run at most one build at a time.

    Arguments:
    - name: The name of the worker node, shown in the web interface.
    - password: Password used by the agent installed on worker nodes to authenticate with the
      master.

    """
    # In general, our slaves assume that they have full control of the machine they are running on,
    # thus, we force at most one job running on each node at a time.
    BuildmasterConfig['slaves'].append(BuildSlave(name, password, max_builds=1))


def change_source(name, password):
    """
    Adds a new change source. This causes BuildBot to start listening on TCP port 9999. Make sure
    to have it behind a firewall and open only to addresses from which you want to listen for
    change notifications.

    """
    BuildmasterConfig['change_source'].append(
        PBChangeSource(port=9999, user=name, passwd=password))