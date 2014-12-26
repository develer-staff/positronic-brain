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
from os.path import isdir, join
from shutil import rmtree

from buildbot.process.buildstep import BuildStep
from buildbot.process.buildstep import SUCCESS
from buildbot.process.properties import Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.slave import MakeDirectory
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.transfer import DirectoryUpload

from positronic.brain.config import BuildmasterConfig
from positronic.brain.config import BrainConfig


class PruneOldArtifacts(BuildStep):
    name = 'remove old artifacts'

    def __init__(self, **kwargs):
        super(PruneOldArtifacts, self).__init__(**kwargs)

    def start(self):
        root = BrainConfig['artifactsDir']
        max_artifacts = BrainConfig['maxArtifacts']
        artifacts = Interpolate(join(root, '%(prop:buildername)s')).getRenderingFor(self).result

        remove_obsolete_artifact_dirs(artifacts, max_artifacts)

        self.finished(SUCCESS)


def remove_obsolete_artifact_dirs(root, max_artifacts):
    """Remove obsolete artifacts from the given root directory.

    This function asserts that the root directory does not contain files and that all directory
    names can be converted to integers in strictly increasing order. Each directory name should
    correspond to a build number for that particular builder.

    This function also removes empty artifacts directories.
    """
    assert max_artifacts > 0

    # This ensures we only get files or directories with names that can be converted to an integer,
    # we also first sort it in increasing order. Strictly increasing order should be guaranteed by
    # fs semantics: you can't have two directories with the same name!
    dirs = map(str, sorted(map(int, listdir(root))))
    paths = [join(root, d) for d in dirs]

    # We only want directories.
    for p in paths:
        assert isdir(p)

    paths_to_remove = paths[:-max_artifacts]

    for p in paths:
        if not listdir(p):
            rmtree(p)
        elif p in paths_to_remove:
            rmtree(p)


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
        masterdest=Interpolate(
            join(BrainConfig['artifactsDir'], '%(prop:buildername)s', '%(prop:buildnumber)s')),
        url=Interpolate(BuildmasterConfig[
                            'buildbotURL'] + 'artifacts/%(prop:buildername)s/%(prop:buildnumber)s/')))

    job.add_step(PruneOldArtifacts())
