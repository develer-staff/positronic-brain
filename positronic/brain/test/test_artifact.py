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

import os

import pytest

from positronic.brain.artifact import remove_obsolete_artifact_dirs


def test_remove_obsolete_artifact_dirs_invalid_max_artifacts(tmpdir):
    with pytest.raises(AssertionError):
        remove_obsolete_artifact_dirs(str(tmpdir), 0)


def test_remove_obsolete_artifact_dirs_not_integer(tmpdir):
    root = str(tmpdir)

    os.makedirs(os.path.join(root, 'dir1'))
    os.makedirs(os.path.join(root, 'dir2'))

    with pytest.raises(ValueError):
        remove_obsolete_artifact_dirs(root, 5)


def test_remove_obsolete_artifact_dirs_not_dir(tmpdir):
    root = str(tmpdir)

    create_skel(root, 4)

    with open(os.path.join(root, '5'), 'w') as f:
        f.write('I am a file and should not be here')

    with pytest.raises(AssertionError):
        remove_obsolete_artifact_dirs(root, 5)


def test_remove_obsolete_artifact_dirs_less_than_max(tmpdir):
    root = str(tmpdir)

    create_skel(root, 4)
    remove_obsolete_artifact_dirs(root, 5)
    assert_dirs_exist(root, 4)


def test_remove_obsolete_artifact_dirs_equal_max(tmpdir):
    root = str(tmpdir)

    create_skel(root, 5)
    remove_obsolete_artifact_dirs(root, 5)
    assert_dirs_exist(root, 5)


def test_remove_obsolete_artifact(tmpdir):
    root = str(tmpdir)

    create_skel(root, 5)
    remove_obsolete_artifact_dirs(root, 2)

    assert not os.path.isdir(os.path.join(root, '0'))
    assert not os.path.isdir(os.path.join(root, '1'))
    assert not os.path.isdir(os.path.join(root, '2'))
    assert os.path.isdir(os.path.join(root, '3'))
    assert os.path.isdir(os.path.join(root, '4'))


def test_remove_obsolete_artifact_empty_dirs(tmpdir):
    root = str(tmpdir)

    create_skel(root, 5)
    os.remove(os.path.join(root, '2', 'keep'))
    remove_obsolete_artifact_dirs(root, 5)

    assert os.path.isdir(os.path.join(root, '0'))
    assert os.path.isdir(os.path.join(root, '1'))
    assert not os.path.isdir(os.path.join(root, '2'))
    assert os.path.isdir(os.path.join(root, '3'))
    assert os.path.isdir(os.path.join(root, '4'))


#
# Support Functions
#

def create_skel(root, n):
    for i in range(0, n):
        p = os.path.join(root, str(i))

        os.makedirs(p)

        with open(os.path.join(p, 'keep'), 'w') as f:
            f.write("I'm here so that the parent directory is not removed")


def assert_dirs_exist(root, n):
    for i in range(0, n):
        assert os.path.isdir(os.path.join(root, str(i)))