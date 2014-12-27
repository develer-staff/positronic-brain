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


def patch_build_step():
    """
    Changes the default attributes on BuildStep so that:

    - alwaysRun = False
    - flunkOnFailure = True
    - flunkOnWarnings = False
    - haltOnFailure = True
    - warnOnFailure = False
    - warnOnWarnings = True

    I.e.: A build step must always cause the build to fail if it fails and, in that case, BuildBot
    must not execute other build steps in a builder.
    """
    from buildbot.process.buildstep import BuildStep

    BuildStep.alwaysRun = False
    BuildStep.flunkOnFailure = True
    BuildStep.flunkOnWarnings = False
    BuildStep.haltOnFailure = True
    BuildStep.warnOnFailure = False
    BuildStep.warnOnWarnings = True


def patch_all():
    """Applies all patches."""
    patch_build_step()