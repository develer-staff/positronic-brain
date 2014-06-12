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

from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.schedulers.forcesched import ForceScheduler

from positronic.brain.config import BuildmasterConfig
from positronic.brain.utils import scheduler_name


class Job(object):

    """The base class for all job types.
    """

    def __init__(self, name, slaves):
        self.name = name
        self.slaves = slaves

        self.build = BuildFactory()

        BuildmasterConfig['builders'].append(BuilderConfig(
            name=self.name,
            factory=self.build,
            slavenames=self.slaves))

        BuildmasterConfig['schedulers'].append(ForceScheduler(
            name=scheduler_name(self, 'force'),
            builderNames=[self.name]))

    def add_step(self, step):
        # Any fail in the build pipeline MUST cause a build failure
        step.haltOnFailure = True
        step.alwaysRun = False

        self.build.addStep(step)

        return self
