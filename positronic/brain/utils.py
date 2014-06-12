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
This module contains miscellaneous utility functions.
"""


from urlparse import urlparse

from buildbot.changes.svnpoller import SVNPoller

from positronic.brain.config import BuildmasterConfig


def get_default_email_address(url):
    """Builds a default email address for all outgoing notifications."""

    return 'noreply@' + '.'.join(urlparse(url).netloc.split('.')[-2:])


def has_svn_change_source(svnurl):
    return has_change_source(SVNPoller, 'svnurl', svnurl)


def has_change_source(filter_by, attr, value):
    """Determines whether a change source has already been added to BuilmasterConfig.

    BuildBot doesn't allow multiple instances of a Change Source pointing to the same repository.
    This function can be used by Jobs to skip adding a new Change Source if an identical one is
    already there.

    Arguments:

    - filter_by: When looking up existing change sources, take only those of this type into account.
    - attr: The attribute to look up.
    - value: The value to compare to determine if a Change Source has already been added.

    """
    for change_source in [c for c in BuildmasterConfig['change_source'] if isinstance(c, filter_by)]:
        if getattr(change_source, attr, '') == value:
            return True
    else:
        return False


def scheduler_name(job, *args):
    """Creates a name for a scheduler."""
    return name(job.name, 'scheduler', *args)


def name(*args):
    """Normalizes a name.

    Normalizes a name so that it becomes all lower case, trims spaces and replaces spaces between
    words with dashes.

    """
    return ('-'.join(args)).strip()
