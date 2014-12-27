# -*- coding: utf-8 -*-
#
# Positronic Brain - Opinionated Buildbot Workflow
# Copyright 2014 Develer S.r.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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