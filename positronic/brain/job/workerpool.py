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

from positronic.brain.job import Job
from positronic.brain.job.freestyle import FreestyleJob


class WorkerPoolJob(Job):
    """
    A virtual job that triggers platform-specific builds.

    A WorkerPoolJob makes it easy to re-use build steps to perform builds on multiple platforms
    without having to create different Job(s) for each platform.

    Suppose you have to build a project 'foo' on Windows and Linux. With the standard "FreestyleJob"
    the configuration file would look like this:

    .. code:: python

        with FreestyleJob('foo-linux', ['linux-worker-1', 'linux-worker-2']) as job:
            job.checkout('svn+ssh://svn.example.com/svn/foo', 'trunk')
            job.command('make')
            job.command('make', 'check')

        with FreestyleJob('foo-windows', ['windows-worker-1', 'windows-worker-2']) as job:
            job.checkout('svn+ssh://svn.example.com/svn/foo', 'trunk')
            job.command('make')
            job.command('make', 'check')

    With a WorkerPoolJob, however, one could write:

    .. code:: python

        WORKER_POOLS = {
            'linux': ['linux-worker-1', 'linux-worker-2'],
            'windows': ['windows-worker-1', 'windows-worker-2'],
        }

        with WorkerPoolJob('foo', WORKER_POOLS) as job:
            job.checkout('svn+ssh://svn.example.com/svn/foo', 'trunk')
            job.command('make')
            job.command('make', 'check')

    And three jobs will be created:

    - foo-linux: A FreestyleJob associated with all workers in the 'linux' pool.
    - foo-windows: A FreestyleJob associated to all workers in the 'windows' pool.
    - foo: The "meta" job. Forcing a build of this job will trigger the other two.

    Platform specific jobs can still be addressed via the 'pool' dictionary. As an example, to run
    a different build command on Windows and Linux your can add a fragment like this to your
    configuration file:

    .. code:: python

        WORKER_POOLS = {
            'linux': ['linux-worker-1', 'linux-worker-2'],
            'windows': ['windows-worker-1', 'windows-worker-2'],
        }

        with WorkerPoolJob('foo', WORKER_POOLS) as job:
            job.checkout('svn+ssh://svn.example.com/svn/foo', 'trunk')

            job.pool['linux'].command('make', 'I_AM_ON_LINUX=1')
            job.pool['windows'].command('make', 'I_AM_ON_WINDOWS=1')

            job.command('make', 'check')
    """

    def __init__(self, name, pools):
        super(WorkerPoolJob, self).__init__(name, ['master'])

        # Worker pool name -> Job bound to workers in said pool
        self.pool = dict()

        for pool_name, workers in pools.items():
            self.pool[pool_name] = FreestyleJob(name + '-' + pool_name, workers)

        self.trigger(self.pool.values())

    def __enter__(self):
        # Forward context manager events to all jobs in the pool.
        for job in self.pool.values():
            job.__enter__()

        return self

    def __exit__(self, type, value, traceback):
        # Forward context manager events to all jobs in the pool.
        for job in self.pool.values():
            job.__exit__(type, value, traceback)

    def __getattribute__(self, name):
        if hasattr(self, name):
            # If we have the attribute, do nothing
            return super(WorkerPoolJob, self).__getattribute__(name)
        else:
            # Otherwise forward the method call to all Job(s) in the pool.
            # NOTE: Assumes a method call.
            def wrapper(*args, **kwargs):
                for j in self.pool.values():
                    getattr(j, name)(*args, **kwargs)

            return wrapper