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

from mock import patch

from buildbot.changes.svnpoller import SVNPoller

from positronic.brain.config import BuildmasterConfig
from positronic.brain.utils import append_dir_sep, get_default_email_address, \
    has_svn_change_source, name, scheduler_name, is_dir_in_change


def test_append_dir_sep():
    assert append_dir_sep('test') == 'test/'
    assert append_dir_sep('test/') == 'test/'
    assert append_dir_sep(['test']) == ['test/']
    assert append_dir_sep(['test/']) == ['test/']
    assert append_dir_sep(['test', 'test']) == ['test/', 'test/']
    assert append_dir_sep(['test/', 'test']) == ['test/', 'test/']
    assert append_dir_sep(['test/', 'test/']) == ['test/', 'test/']


@patch('buildbot.changes.changes.Change')
def test_is_dir_in_change(change):
    change.files = ['test_dir1/file1.py', 'test_dir2/file2.py']

    assert not is_dir_in_change(change, ['test_bogus'])
    assert not is_dir_in_change(change, ['test'])
    assert not is_dir_in_change(change, ['test_dir'])
    assert not is_dir_in_change(change, ['file1'])
    assert not is_dir_in_change(change, ['file1.py'])
    assert is_dir_in_change(change, ['test_dir1'])
    assert is_dir_in_change(change, ['test_dir2'])
    assert is_dir_in_change(change, ['test_dir1', 'test_dir2'])
    assert is_dir_in_change(change, ['test_dir2', 'test_dir1'])


def test_has_svn_change_source():
    BuildmasterConfig['change_source'].append(SVNPoller(svnurl='svn+ssh://test1.example.com'))
    BuildmasterConfig['change_source'].append(SVNPoller(svnurl='svn+ssh://test2.example.com'))

    assert has_svn_change_source('svn+ssh://test2.example.com')
    assert not has_svn_change_source('http://foobar.com')

    BuildmasterConfig['change_source'] = []


def test_get_default_email_address():
    assert get_default_email_address('http://buildbot.example.com') == 'buildbot@example.com'
    assert get_default_email_address('http://example.com') == 'buildbot@example.com'
    assert get_default_email_address('http://intranet') == 'buildbot@intranet'


def test_name():
    assert name('ShouldBeLowercase') == 'shouldbelowercase'
    assert name('  Stripspaces  ') == 'stripspaces'
    assert name('join words') == 'join-words'
    assert name('  join words with trailing spaces   ') == 'join-words-with-trailing-spaces'


def test_scheduler_name():
    class Mock(object):
        name = 'Long Job Name'

    assert scheduler_name(Mock(), 'force') == 'long-job-name-scheduler-force'
