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
This module contains all functions needed to deal with artifacts such as adding the build steps
necessary to host them on worker nodes and then transferring them back to the master.
"""

import os
import os.path
import shutil

from buildbot.process.buildstep import BuildStep
from buildbot.process.buildstep import SUCCESS, FAILURE
from buildbot.process.properties import Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.slave import MakeDirectory
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.transfer import DirectoryUpload

from positronic.brain.config import BrainConfig
from positronic.brain.utils import abspath


ARTIFACTS_MASTER_BUILD_DIR = Interpolate('~/artifacts/%(prop:buildername)s/%(prop:buildnumber)s')
ARTIFACTS_MASTER_DIR = Interpolate('~/artifacts/%(prop:buildername)s')
ARTIFACTS_WORKER_DIR = Interpolate('%(prop:builddir)s/artifacts')


class PruneOldArtifacts(BuildStep):
    name = 'Delete Old Artifacts'

    alwaysRun = False
    flunkOnFailure = True
    haltOnFailure = True

    def __init__(self, **kwargs):
        super(PruneOldArtifacts, self).__init__(**kwargs)

    def start(self):
        log = self.addLog("stdio")
        artifacts = abspath(ARTIFACTS_MASTER_DIR.getRenderingFor(self).result)
        max_old_builds = BrainConfig['maxArtifacts']

        log.addStdout('Artifacts: %s\n' % artifacts)
        log.addStdout('Max old builds: %s\n' % max_old_builds)

        try:
            # This works under the assumption that all directory names are build number (integers).
            all_builds = sorted(map(int, os.listdir(artifacts)))
        except ValueError:
            self.finished(FAILURE)

            return

        log.addStdout('All builds: %s\n' % all_builds)

        if len(all_builds) > max_old_builds:
            for old_build in all_builds[:-max_old_builds]:
                scrub_path = os.path.join(artifacts, str(old_build))

                log.addStdout('Deleting: %s\n' % scrub_path)

                shutil.rmtree(scrub_path)

        log.finish()
        self.finished(SUCCESS)


def add_artifact_pre_build_steps(job):
    job.add_step(SetProperty(
        property="artifactsdir",
        value=ARTIFACTS_WORKER_DIR,
        hideStepIf=True))

    job.add_step(RemoveDirectory(
        dir=Interpolate('%(prop:artifactsdir)s'),
        hideStepIf=True))

    job.add_step(MakeDirectory(
        dir=Interpolate('%(prop:artifactsdir)s'),
        hideStepIf=True))


def add_artifact_post_build_steps(job):
    job.add_step(DirectoryUpload(
        name='Archive Artifacts',
        slavesrc=Interpolate('%(prop:artifactsdir)s'),
        masterdest=ARTIFACTS_MASTER_BUILD_DIR))

    job.add_step(PruneOldArtifacts())
