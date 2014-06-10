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

from buildbot.changes.svnpoller import SVNPoller

from positronic.brain.config import BuildmasterConfig


def has_svn_change_source(svnurl):
    return has_change_source(SVNPoller, 'svnurl', svnurl)


def has_change_source(kind, attr, value):
    for change_source in [c for c in BuildmasterConfig['change_source'] if isinstance(c, kind)]:
        if getattr(change_source, attr, '') == value:
            return True
    else:
        return False


def scheduler_name(job, *args):
    return name(job.name, 'scheduler', *args)


def name(*args):
    return ('-'.join(args)).strip()
