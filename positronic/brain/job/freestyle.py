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

from buildbot.changes.filter import ChangeFilter
from buildbot.changes.svnpoller import SVNPoller
from buildbot.process.properties import Interpolate
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.status.mail import MailNotifier
from buildbot.steps.shell import ShellCommand
from buildbot.steps.source.svn import SVN

from positronic.brain.artifact import add_artifact_pre_build_steps, add_artifact_post_build_steps
from positronic.brain.config import BrainConfig, BuildmasterConfig
from positronic.brain.job import Job
from positronic.brain.mail import html_message_formatter
from positronic.brain.utils import has_svn_change_source, hashify, scheduler_name


class FreestyleJob(Job):
    def __init__(self, name, workers):
        super(FreestyleJob, self).__init__(name, workers)

        add_artifact_pre_build_steps(self)

    def __exit__(self, type, value, traceback):
        add_artifact_post_build_steps(self)
        # As the last step, we grab artifacts from the worker. This MUST always be the last step.

    def checkout(self, workdir, url, branch):
        repourl = '%s/%s' % (url, branch)

        self.add_step(SVN(
            mode='full',
            method='clean',
            repourl=repourl,
            workdir=workdir))

        if not has_svn_change_source(repourl):
            BuildmasterConfig['change_source'].append(SVNPoller(
                svnurl=repourl,
                pollInterval=120,
                histmax=10))

        BuildmasterConfig['schedulers'].append(SingleBranchScheduler(
            name=scheduler_name(self, 'svn-' + hashify(repourl)),
            treeStableTimer=60,
            builderNames=[self.name],
            change_filter=ChangeFilter(repository=repourl)))

        return self

    def command(self, *args, **kwargs):
        env = {
            'BUILD': Interpolate('%(prop:buildnumber)s'),
            'BUILD_ARTIFACTS': Interpolate('%(prop:artifactsdir)s'),
            'CI': '1',
        }

        if 'env' in kwargs:
            kwargs['env'].update(env)
        else:
            kwargs['env'] = env

        self.add_step(ShellCommand(command=list(args), **kwargs))

        return self

    def notify(self, *recipients):
        BuildmasterConfig['status'].append(MailNotifier(
            builders=[self.name],
            extraRecipients=recipients,
            fromaddr=BrainConfig['emailFrom'],
            messageFormatter=html_message_formatter,
            mode=['change', 'failing'],
            sendToInterestedUsers=False))

        return self
