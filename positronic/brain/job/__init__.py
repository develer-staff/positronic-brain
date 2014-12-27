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

from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.schedulers.forcesched import ForceScheduler, FixedParameter
from buildbot.steps.trigger import Trigger

from positronic.brain.config import BuildmasterConfig
from positronic.brain import utils
from positronic.brain.utils import scheduler_name


class Job(object):
    """The base class for all job types.

    It doesn't do much by itself, except for creating a new Builder and a new Force Scheduler so
    that users can forcibly trigger a new build.

    This class can be used as a context manager although, by default, it does nothing.

    """

    def __init__(self, name, workers):
        self.name = utils.name(name)
        self.workers = workers

        self.build = BuildFactory()

        BuildmasterConfig['builders'].append(BuilderConfig(
            name=self.name,
            factory=self.build,
            slavenames=self.workers))

        BuildmasterConfig['schedulers'].append(ForceScheduler(
            name=scheduler_name(self, 'force'),
            builderNames=[self.name],
            branch=FixedParameter(name="reason", default=""),
            reason=FixedParameter(name="reason", default="Forced build"),
            revision=FixedParameter(name="revision", default=""),
            repository=FixedParameter(name="repository", default=""),
            project=FixedParameter(name="project", default=""),
            properties=[],
            username=FixedParameter(name="username", default="WebUI")))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def add_step(self, step):
        """Adds a build step on this Job."""
        self.build.addStep(step)

    def trigger(self, job_or_jobs):
        """Adds a build step which triggers execution of another job."""
        if type(job_or_jobs) is list:
            self.add_step(Trigger(
                schedulerNames=[scheduler_name(j, 'trigger') for j in job_or_jobs],
                waitForFinish=True))
        else:
            self.add_step(Trigger(
                schedulerNames=[scheduler_name(job_or_jobs, 'trigger')],
                waitForFinish=True))