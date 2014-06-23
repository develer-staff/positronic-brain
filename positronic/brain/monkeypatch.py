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