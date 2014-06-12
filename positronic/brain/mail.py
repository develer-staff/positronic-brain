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

"""
This module contains the message formatter used with the MailNotifier.
"""

import cgi

from buildbot.status.builder import Results



# This function was copied (with some minor edits) from:
# http://docs.buildbot.net/current/manual/cfg-statustargets.html#mailnotifier
def html_message_formatter(mode, name, build, results, master_status):
    """Provide a customized message to Buildbot's MailNotifier.

    The last 80 lines of the log are provided as well as the changes relevant to the build. Message
    content is formatted as html.

    """
    result = Results[results]

    subject = '[%s] Build status: %s' % (name, result.upper())

    limit_lines = 80

    text = list()
    text.append('<h4>Build status: %s</h4>' % result.upper())
    text.append('<table cellspacing="10"><tr>')
    text.append("<td>Worker:</td><td><b>%s</b></td></tr>" % build.getSlavename())

    if master_status.getURLForThing(build):
        text.append('<tr><td>Complete logs for all build steps:</td><td><a href="%s">%s</a></td></tr>'
                    % (master_status.getURLForThing(build),
                       master_status.getURLForThing(build))
                    )
        text.append('<tr><td>Build Reason:</td><td>%s</td></tr>' % build.getReason())

        source = ""

        for ss in build.getSourceStamps():
            if ss.codebase:
                source += '%s: ' % ss.codebase
            if ss.branch:
                source += "[branch %s] " % ss.branch

            if ss.revision:
                source +=  ss.revision
            else:
                source += "HEAD"

            if ss.patch:
                source += " (plus patch)"
            if ss.patch_info: # add patch comment
                source += " (%s)" % ss.patch_info[1]

        text.append("<tr><td>Build Source Stamp:</td><td><b>%s</b></td></tr>" % source)

        if build.getResponsibleUsers():
            text.append("<tr><td>Blame:</td><td>%s</td></tr>" % ",".join(build.getResponsibleUsers()))

        text.append('</table>')

        if ss.changes:
            text.append('<h4>Recent Changes:</h4>')

            for c in ss.changes:
                cd = c.asDict()

                when = datetime.datetime.fromtimestamp(cd['when'] ).ctime()

                text.append('<table cellspacing="10">')
                text.append('<tr><td>Repository:</td><td>%s</td></tr>' % cd['repository'] )
                text.append('<tr><td>Project:</td><td>%s</td></tr>' % cd['project'] )
                text.append('<tr><td>Time:</td><td>%s</td></tr>' % when)
                text.append('<tr><td>Changed by:</td><td>%s</td></tr>' % cd['who'] )
                text.append('<tr><td>Comments:</td><td>%s</td></tr>' % cd['comments'] )
                text.append('</table>')

                files = cd['files']

                if files:
                    text.append('<table cellspacing="10"><tr><th align="left">Files</th></tr>')

                    for file in files:
                        text.append('<tr><td>%s:</td></tr>' % file['name'] )

                    text.append('</table>')

        text.append('<br>')

        if result != 'success':
            # get log for last step
            logs = build.getLogs()

            # logs within a step are in reverse order. Search back until we find stdio
            for log in reversed(logs):
                if log.getName() == 'stdio':
                    break

            name = "%s.%s" % (log.getStep().getName(), log.getName())
            status, dummy = log.getStep().getResults()
            content = log.getText().splitlines() # Note: can be VERY LARGE
            url = '%s/steps/%s/logs/%s' % (master_status.getURLForThing(build),
                                           log.getStep().getName(),
                                           log.getName())

            text.append('<i>Detailed log of last build step:</i> <a href="%s">%s</a>'
                        % (url, url))
            text.append('<br>')
            text.append('<h4>Last %d lines of "%s"</h4>' % (limit_lines, name))

            unilist = list()

            for line in content[len(content)-limit_lines:]:
                unilist.append(cgi.escape(unicode(line,'utf-8')))

            text.append('<pre>'.join([uniline for uniline in unilist]))
            text.append('</pre>')

        # Closing line
        text.append('<br><br>')
        text.append('<b>-The Buildbot</b>')

        return {
            'body': "\n".join(text),
            'type': 'html',
            'subject': subject,
        }
