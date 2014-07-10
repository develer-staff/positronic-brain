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
This module contains miscellaneous utility functions.
"""

import binascii
import os
import os.path
from urlparse import urlparse

from buildbot.changes.svnpoller import SVNPoller

from positronic.brain.config import BuildmasterConfig


def is_dir_in_change(directories, change):
    """
    :param change: A list of path strings
    :param directories: A list of path strings
    :type change: buildbot.changes.changes.Change
    :return: True if a file in `change` starts with a path from `directories`

    """
    for change_dirname in append_dir_sep([os.path.dirname(f) for f in change.files]):
        for directory in append_dir_sep(directories):
            if change_dirname.startswith(directory):
                return True
    else:
        return False


def append_dir_sep(item_or_items):
    sep = os.path.sep

    if type(item_or_items) is list:
        return [i if i.endswith(sep) else i + sep for i in item_or_items]
    else:
        return item_or_items if item_or_items.endswith(sep) else item_or_items + sep


def abspath(p):
    return os.path.abspath(os.path.expanduser(p))


def get_default_email_address(url):
    """Builds a default email address for all outgoing notifications."""

    domain = urlparse(url).netloc.split('.')

    assert len(domain) >= 1

    return 'buildbot@' + '.'.join(domain[-2:])


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
    for change_source in [c for c in BuildmasterConfig['change_source'] if
                          isinstance(c, filter_by)]:
        if getattr(change_source, attr, '') == value:
            return True
    else:
        return False


def hashify(data):
    return binascii.hexlify(str(binascii.crc32(data)))


def scheduler_name(job, scheduler_name):
    """Creates a name for a scheduler."""
    return name('%s-scheduler-%s' % (job.name, scheduler_name))


def name(n):
    """Normalizes a name.

    Normalizes a name so that it becomes all lower case, trims spaces and replaces spaces between
    words with dashes.

    """
    return '-'.join(p.strip().lower() for p in n.split())
