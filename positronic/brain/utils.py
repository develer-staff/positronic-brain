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

from urlparse import urlparse

from buildbot.changes.svnpoller import SVNPoller

from positronic.brain.config import BuildmasterConfig


def get_default_email_address(url):
    """Builds a default email address for all outgoing notifications."""
    return 'noreply@' + '.'.join(urlparse(url).netloc.split('.')[-2:])


def has_svn_change_source(svnurl):
    return has_change_source(SVNPoller, 'svnurl', svnurl)


def has_change_source(kind, attr, value):
    for change_source in [c for c in BuildmasterConfig['change_source'] if isinstance(c, kind)]:
        if getattr(change_source, attr, '') == value:
            return True
    else:
        return False


# See: http://stackoverflow.com/a/8313042
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))

        return method

    return overrider


def scheduler_name(job, *args):
    return name(job.name, 'scheduler', *args)


def name(*args):
    return ('-'.join(args)).strip()
