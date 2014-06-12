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


from positronic.brain.utils import get_default_email_address, name


def test_get_default_email_address():
    assert get_default_email_address('http://buildbot.example.com') == 'noreply@example.com'


def test_name():
    assert name('example', 'name') == 'example-name'
    assert name('example', 'name', 'with', 'spaces  ') == 'example-name-with-spaces'
