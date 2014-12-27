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
