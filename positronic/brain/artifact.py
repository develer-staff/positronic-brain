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
This module contains all functions needed to deal with artifacts such as adding the build steps
necessary to host them on worker nodes and then transferring them back to the master.
"""

from os import listdir
from os.path import join
from shutil import rmtree

from buildbot.process.buildstep import BuildStep
from buildbot.process.buildstep import SUCCESS, FAILURE
from buildbot.process.properties import Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.slave import MakeDirectory
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.transfer import DirectoryUpload

from positronic.brain.config import BrainConfig


class PruneOldArtifacts(BuildStep):
    name = 'remove old artifacts'

    alwaysRun = False
    haltOnFailure = True

    def __init__(self, **kwargs):
        super(PruneOldArtifacts, self).__init__(**kwargs)

    def start(self):
        log = self.addLog('stdio')
        artifacts = Interpolate(join(BrainConfig['artifactsDir'], '%(prop:buildername)s'))
        artifacts = artifacts.getRenderingFor(self).result
        max_artifacts = BrainConfig['maxArtifacts']

        log.addStdout('Artifacts directory: %s\n' % artifacts)
        log.addStdout('Max old builds: %s\n' % max_artifacts)

        try:
            # This works under the assumption that all directory names are build number (integers).
            all_build_dirs = map(str, sorted(map(int, listdir(artifacts))))
            old_build_dirs = all_build_dirs[:-max_artifacts]
        except ValueError:
            self.finished(FAILURE)

            return

        log.addStdout('All artifacts: %s\n' % all_build_dirs)
        log.addStdout('Old artifacts: %s\n' % old_build_dirs)

        for build_dir in all_build_dirs:
            abs_build_dir = join(artifacts, build_dir)

            if not listdir(abs_build_dir):
                rmtree(abs_build_dir)

                log.addStdout('Deleted empty artifacts directory: %s\n' % abs_build_dir)
            elif build_dir in old_build_dirs:
                rmtree(abs_build_dir)

                log.addStdout('Deleted old artifacts directory: %s\n' % abs_build_dir)

        log.finish()

        self.finished(SUCCESS)


def add_artifact_pre_build_steps(job):
    artifacts_dir = Interpolate(join('%(prop:builddir)s', 'artifacts'))

    job.add_step(SetProperty(
        property="artifactsdir",
        value=artifacts_dir,
        hideStepIf=True))

    job.add_step(RemoveDirectory(
        dir=Interpolate('%(prop:artifactsdir)s'),
        hideStepIf=True))

    job.add_step(MakeDirectory(
        dir=Interpolate('%(prop:artifactsdir)s'),
        hideStepIf=True))


def add_artifact_post_build_steps(job):
    job.add_step(DirectoryUpload(
        name='collect artifacts',
        slavesrc=Interpolate('%(prop:artifactsdir)s'),
        masterdest=Interpolate(join(BrainConfig['artifactsDir'],
                                    '%(prop:buildername)s', '%(prop:buildnumber)s')),
        url=Interpolate('/artifacts/%(prop:buildername)s/%(prop:buildnumber)s/')))

    job.add_step(PruneOldArtifacts())
