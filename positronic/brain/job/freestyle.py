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
from buildbot.interfaces import IBuildStepFactory
from buildbot.process.properties import Interpolate
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.status.mail import MailNotifier
from buildbot.steps.master import SetProperty
from buildbot.steps.shell import ShellCommand
from buildbot.steps.slave import MakeDirectory
from buildbot.steps.slave import RemoveDirectory
from buildbot.steps.source.svn import SVN
from buildbot.steps.transfer import DirectoryUpload


from positronic.brain.config import BrainConfig, BuildmasterConfig
from positronic.brain.job import Job
from positronic.brain.utils import has_svn_change_source, overrides, scheduler_name


class FreestyleJob(Job):

    def __init__(self, name, slaves):
        super(FreestyleJob, self).__init__(name, slaves)

        # Creates the artifacts directory, making sure it is gets cleared when the build starts.
        #
        # NOTE: We use Job's add_step() method here because our version messes up with the step
        # execution order, something we don't want to here.
        super(FreestyleJob, self).add_step(SetProperty(
            property="artifactsdir",
            value=Interpolate('%(prop:builddir)s/artifacts'),
            hideStepIf=True))

        super(FreestyleJob, self).add_step(RemoveDirectory(
            dir=Interpolate('%(prop:artifactsdir)s'),
            hideStepIf=True))

        super(FreestyleJob, self).add_step(MakeDirectory(
            dir=Interpolate('%(prop:artifactsdir)s'),
            hideStepIf=True))

        # As the last step, we grab artifacts from the slave. This MUST always be the last step. Use
        # the add_step() helper to insert other steps before this one.
        #
        # NOTE: As above, we use Job's add_step() method here because our version messes up with the
        # step execution order, something we don't want to here.
        super(FreestyleJob, self).add_step(DirectoryUpload(
            slavesrc=Interpolate('%(prop:artifactsdir)s'),
            masterdest=Interpolate('~/artifacts/%(prop:buildername)s/%(prop:buildnumber)s'),
            hideStepIf=True))

    @overrides(Job)
    def add_step(self, step):
        # Any fail in the build pipeline MUST cause a build failure
        step.alwaysRun = False
        step.haltOnFailure = True

        if len(self.build.steps) == 0:
            self.build.addStep(step)
        else:
            self.build.steps.insert(len(self.build.steps) - 1, IBuildStepFactory(step))

        return self

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
            name=scheduler_name(self, 'svn', url, branch),
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
            mode=['change', 'failing'],
            sendToInterestedUsers=False))

        return self
