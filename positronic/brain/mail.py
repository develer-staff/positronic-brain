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
This module contains the message formatter used with the MailNotifier.
"""

import datetime

from buildbot.status.builder import Results
from buildbot.process.buildstep import SUCCESS
from jinja2 import Environment, PackageLoader


LOG_MAX_LINES = 250
TEMPLATES_ENV = Environment(loader=PackageLoader('positronic.brain', 'templates'))


# This function was copied (with some minor edits) from:
# http://docs.buildbot.net/current/manual/cfg-statustargets.html#mailnotifier
def html_message_formatter(_, name, build, results, master_status):
    """Provide a customized message to Buildbot's MailNotifier.

    The last 250 lines of the log are provided as well as the changes relevant to the build. Message
    content is formatted as html.

    """
    result = Results[results]

    subject = '[%s] %s on %s' % (name, result.upper(), build.getSlavename())

    # Obtains the last LOG_MAX_LINES from the last failing build step.
    log = None
    failed_logs = [l for l in reversed(build.getLogs()) if l.step.results != SUCCESS]

    if failed_logs:
        failed_log = failed_logs[0]
        failed_log_lines = failed_log.getText().splitlines()[-LOG_MAX_LINES:]

        if failed_log_lines:
            log = {
                'content': '\n'.join(failed_log_lines),
                'length': len(failed_log_lines),
                'url': '%s/steps/%s/logs/%s' % (master_status.getURLForThing(build),
                                                failed_log.getStep().getName(),
                                                failed_log.getName()),
            }

    # If we have logs but the result is SUCCESS, something is broken.
    if results == SUCCESS:
        assert log is None

    # Changes
    changes = []

    for source_stamp in build.getSourceStamps():
        if source_stamp.changes:
            changes.extend([c.asDict() for c in source_stamp.changes])

    # FIXME: Ugly, this should be a responsibility of the template.
    # TODO: Use a Jinja2 filter to do this.
    for change in changes:
        if 'when' in change:
            change['when'] = datetime.datetime.fromtimestamp(change['when']).ctime()

    # Template context
    body = TEMPLATES_ENV.get_template('email.jinja2').render(
        changes=changes,
        log=log,
        reason=build.getReason(),
        result=result,
        url=master_status.getURLForThing(build),
        worker=build.getSlavename())

    return {
        'body': body,
        'subject': subject,
        'type': 'html',
    }
