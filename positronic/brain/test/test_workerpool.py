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

from mock import MagicMock

from positronic.brain.job.workerpool import WorkerPoolJob


def test_forward_context_manager_events():
    pools = {
        'linux': ['linux-worker'],
    }

    job = WorkerPoolJob('test', pools)
    job.pool['linux'] = MagicMock()

    with job:
        pass

    assert job.pool['linux'].__enter__.called
    assert job.pool['linux'].__exit__.called