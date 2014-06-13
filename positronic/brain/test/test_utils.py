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


from positronic.brain.utils import get_default_email_address, name, scheduler_name


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
