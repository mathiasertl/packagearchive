# -*- coding: utf-8 -*-
#
# This file is part of packagearchive (https://github.com/mathiasertl/packagearchive).
#
# packagearchive is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# packagearchive is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with packagearchive.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os

from six.moves import configparser

from fabric.api import local
from fabric.context_managers import quiet
from fabric.tasks import Task

config = configparser.ConfigParser({
    'remote': 'origin',
    'branch': 'master',
    'user': 'root',
    'group': '',
})
config.read('fab.conf')

class DeployTask(Task):
    def __init__(self, section='DEFAULT', **kwargs):
        self.section = section
        super(DeployTask, self).__init__(**kwargs)

    def sudo(self, cmd, chdir=True):
        if chdir is True:
            return local('ssh %s sudo sh -c \'"cd %s && %s"\'' % (self.host, self.path, cmd))
        else:
            return local('ssh %s sudo %s' % (self.host, cmd))

    def sg(self, cmd, chdir=True):
        if not self.group:
            return self.sudo(cmd, chdir=chdir)

        sg_cmd = 'ssh %s sudo sg %s -c' % (self.host, self.group)
        if chdir is True:
            return local('%s \'"cd %s && %s"\'' % (sg_cmd, self.path, cmd))
        else:
            return local('%s \'"%s"\'' % (sg_cmd, cmd))

    def exists(self, path):
        """Returns True/False depending on if the given path exists."""
        with quiet():
            return self.sudo('test -e %s' % path, chdir=False).succeeded

    def run(self, section=None):
        if section is None:
            section = self.section

        remote = config.get(section, 'remote')
        branch = config.get(section, 'branch')

        local('bin/python manage.py check')

        # upload source code
        local('git push %s %s --tags' % (remote, branch))

        # deploy on wsgi host
        self.host = config.get(section, 'wsgi-host')
        self.path = config.get(section, 'wsgi-path')
        venv = config.get(section, 'wsgi-venv')
        pip = os.path.join(venv, 'bin', 'pip')
        python = os.path.join(venv, 'bin', 'python')
        manage = '%s manage.py' % python
        self.sudo('git pull %s %s' % (remote, branch))
        self.sudo('%s install -U -r requirements.txt' % pip)
        self.sudo('%s migrate' % manage)
        self.sudo('%s collectstatic --noinput' % manage)
        self.sudo('touch /etc/uwsgi-emperor/vassals/packagearchive.ini')

deploy = DeployTask()
