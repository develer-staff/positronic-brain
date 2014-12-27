# Copyright 2012-2013 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.python import log
from twisted.internet import reactor
from buildbot.status.web.base import HtmlResource, ActionResource

import os, shelve, re


class AddProjectForm(HtmlResource):

    def content(self, req, cxt):
        template = req.site.buildbot_service.templates.get_template("travis.add.html")
        #return (template.render(**cxt))
        return template.render(cxt)


class AddProject(ActionResource):

    def __init__(self, status, path):
        self.status = status
        self.path = path

    def performAction(self, req):
        CAME_FROM = "/add_form"

        name = req.args.get("name", [""])[0].strip().lower()
        if not name:
            return ((CAME_FROM, "You must specify the name of the project"))

        if not re.match('^[a-z0-9\-\.]+$', name):
            return ((CAME_FROM, "Name can currently only contain a-z, 0-9, '-' and '.', and lower case will be forced for consistency"))

        repository = req.args.get("repository", [""])[0].strip()
        if not repository:
            return ((CAME_FROM, "You must specify an SVN repository or GitHub repo"))

        for prefix in self.status.allowed_projects_prefix:
            if repository.startswith(prefix):
                break
        else:
            return ((CAME_FROM, "Only repos at these locations are supported at present: %s" % ",".join(self.status.allowed_projects_prefix)))

        branch = req.args.get("branch", [""])[0].strip()
        #if not branch:
        #    return ((CAME_FROM, "You must specify an SVN repository or GitHub repo"))

        shelf = shelve.open(self.path, writeback=False)

        if name in shelf:
            return ((CAME_FROM, "Project is already defined"))

        for p in shelf.keys():
            details = shelf[p]
            if details["repository"] == repository:
                if not branch:
                    return ((CAME_FROM, "Repository is already defined for project '%s'" % details["name"]))
                if branch == details.get("branch", ""):
                    return ((CAME_FROM, "Repository/branch pair already defined for project '%s'" % details["name"]))

        payload = dict(
            name = name,
            repository = repository,
            )
        if branch:
            payload['branch'] = branch

        shelf[name] = payload

        shelf.sync()
        shelf.close()

        reactor.callLater(0, req.site.buildbot_service.master.reconfig)

        return (("/projects", ""))
