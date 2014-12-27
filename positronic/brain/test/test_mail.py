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

from mock import patch, MagicMock
import pytest

from buildbot.process.buildstep import SUCCESS, FAILURE

from positronic.brain.mail import html_message_formatter


EXPECTED_EMPTY_MESSAGE = """<!-- ============== -->
<!-- Build overview -->
<!-- ============== -->

<h3>Build status: SUCCESS</h3>

<table cellspacing="10">
    <tbody>
    <tr>
        <td><strong>Logs:</strong></td>
        <td>http://localhost:8080/build/1</td>
    </tr>
    <tr>
        <td><strong>Worker node:</strong></td>
        <td>worker</td>
    </tr>
    <tr>
        <td><strong>Build reason:</strong></td>
        <td>running a test</td>
    </tr>
    </tbody>
</table>

<!-- ============== -->
<!-- Recent Changes -->
<!-- ============== -->





<!-- =============================== -->
<!-- Logs of last failing build step -->
<!-- =============================== -->


    <p>There are no logs for this build.</p>
"""


EXPECTED_FAILURE_LOG = """<!-- ============== -->
<!-- Build overview -->
<!-- ============== -->

<h3>Build status: FAILURE</h3>

<table cellspacing="10">
    <tbody>
    <tr>
        <td><strong>Logs:</strong></td>
        <td>http://localhost:8080/build/1</td>
    </tr>
    <tr>
        <td><strong>Worker node:</strong></td>
        <td>worker</td>
    </tr>
    <tr>
        <td><strong>Build reason:</strong></td>
        <td>running a test</td>
    </tr>
    </tbody>
</table>

<!-- ============== -->
<!-- Recent Changes -->
<!-- ============== -->





<!-- =============================== -->
<!-- Logs of last failing build step -->
<!-- =============================== -->


    <h3>Last 1 Lines From Build Log</h3>
    <p><a href="http://localhost:8080/build/1/steps/step/logs/stdio">http://localhost:8080/build/1/steps/step/logs/stdio</a></p>
    <pre>
        A failed build step
    </pre>
"""


def diffeq_(a, b):
    from difflib import unified_diff

    assert a == b, '\n'.join(unified_diff(a.splitlines(), b.splitlines()))


@patch('buildbot.status.build.BuildStatus')
@patch('buildbot.status.master.Status')
def test_html_message_formatter_empty_message(build_status, status):
    # Mock
    build_status.getLogs.return_value = []
    build_status.getReason.return_value = 'running a test'
    build_status.getSlavename.return_value = 'worker'
    build_status.getSourceStamps.return_value = []

    status.getURLForThing.return_value = 'http://localhost:8080/build/1'

    # Run
    ret = html_message_formatter(None, 'test-build', build_status, SUCCESS, status)

    # Assert
    assert ret == {
        'body': EXPECTED_EMPTY_MESSAGE,
        'subject': '[test-build] SUCCESS on worker',
        'type': 'html',
    }


@patch('buildbot.status.build.BuildStatus')
@patch('buildbot.status.logfile.LogFile')
@patch('buildbot.status.master.Status')
def test_html_message_formatter_log_failure_but_results_success(build_status, log_file, status):
    # Mock
    log_file.getText.return_value = 'A failed build step'
    log_file.step.results = FAILURE

    build_status.getLogs.return_value = [log_file]
    build_status.getReason.return_value = 'running a test'
    build_status.getSlavename.return_value = 'worker'
    build_status.getSourceStamps.return_value = []

    status.getURLForThing.return_value = 'http://localhost:8080/build/1'

    # Run. this should blow up.
    with pytest.raises(AssertionError):
        html_message_formatter(None, 'test-build', build_status, SUCCESS, status)


@patch('buildbot.status.build.BuildStatus')
@patch('buildbot.status.logfile.LogFile')
@patch('buildbot.status.master.Status')
def test_html_message_formatter_failed_log(build_status, log_file, status):
    # Mock
    log_file.getName.return_value = 'stdio'
    log_file.getStep.return_value = MagicMock()
    log_file.getStep().getName = MagicMock(return_value='step')
    log_file.getText.return_value = 'A failed build step'
    log_file.step.results = FAILURE

    build_status.getLogs.return_value = [log_file]
    build_status.getReason.return_value = 'running a test'
    build_status.getSlavename.return_value = 'worker'
    build_status.getSourceStamps.return_value = []

    status.getURLForThing.return_value = 'http://localhost:8080/build/1'

    # Run
    ret = html_message_formatter(None, 'test-build', build_status, FAILURE, status)

    # Assert
    assert ret == {
        'body': EXPECTED_FAILURE_LOG,
        'subject': '[test-build] FAILURE on worker',
        'type': 'html',
    }
