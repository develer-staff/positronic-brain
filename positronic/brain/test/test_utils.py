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

    assert not is_dir_in_change(['test_bogus'], change)
    assert not is_dir_in_change(['test'], change)
    assert not is_dir_in_change(['test_dir'], change)
    assert not is_dir_in_change(['file1'], change)
    assert not is_dir_in_change(['file1.py'], change)
    assert is_dir_in_change(['test_dir1'], change)
    assert is_dir_in_change(['test_dir2'], change)
    assert is_dir_in_change(['test_dir1', 'test_dir2'], change)
    assert is_dir_in_change(['test_dir2', 'test_dir1'], change)


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
