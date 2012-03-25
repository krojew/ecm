# Copyright (c) 2010-2012 Robin Jarry
#
# This file is part of EVE Corporation Management.
#
# EVE Corporation Management is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# EVE Corporation Management is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = '2012 3 23'
__author__ = 'diabeteman'

import shutil
from os import path
from ConfigParser import SafeConfigParser

from ecm.admin import instance_template
from ecm.admin.util import prompt, get_logger

DB_ENGINES = {
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle'
}

#------------------------------------------------------------------------------
def init_instance(command, args):
    """
    Create the instance directory and copy the template scripts in it.
    """
    if not args:
        command.parser.error('Missing instance directory.')
    instance_dir = args[0]
    if path.exists(instance_dir):
        command.parser.error('Directory "%s" already exists.' % instance_dir)
    template_dir = path.abspath(path.dirname(instance_template.__file__))
    shutil.copytree(template_dir, instance_dir)

    return instance_dir

#------------------------------------------------------------------------------
def prompt_missing_options(options):
    """
    Prompt the user if necessary.
    """
    if not options.db_engine:
        options.db_engine = prompt('Database engine?', default_value='sqlite', valid_list=DB_ENGINES.keys())
        options.db_engine = DB_ENGINES.get(options.db_engine, options.db_engine)
    if options.db_engine != DB_ENGINES['sqlite']:
        if not options.db_name:
            options.db_name = prompt('Database name?', default_value='ecm')
        if not options.db_user:
            options.db_user = prompt('Database user?', default_value='ecm')
        if not options.db_pass:
            options.db_pass = prompt('Database password?', default_value='ecm')
    if not options.host_name:
        options.host_name = prompt('External host name?')
    if not options.admin_email:
        options.admin_email = prompt('Email of the server administrator? (for error notifications)')
    if not options.server_email:
        options.server_email = prompt('Email used as "from" address in emails sent by the server?')
    if not options.bind_address:
        options.bind_address = prompt('Server listening address?', default_value='127.0.0.1')
    if not options.bind_port:
        options.bind_port = prompt('Server listening port?', default_value=8888)

#------------------------------------------------------------------------------
def write_settings(command, options, instance_dir):
    """
    Write all options/settings to the settings.ini file.
    """
    config = SafeConfigParser()
    settings_file = path.normpath(path.join(instance_dir, 'settings.ini'))
    if not config.read(settings_file):
        raise IOError('Could not read %s' % settings_file)
    config.set('misc', 'debug', 'False')
    config.set('misc', 'server_bind_ip', str(options.bind_address))
    config.set('misc', 'server_port', str(options.bind_port))
    config.set('misc', 'pid_file', 'ecm.pid')
    config.set('database', 'ecm_engine', str(options.db_engine))
    if options.db_name:
        config.set('database', 'ecm_name', str(options.db_name))
        config.set('database', 'ecm_user', str(options.db_user))
        config.set('database', 'ecm_password', str(options.db_pass))
    config.set('email', 'admin_email', str(options.admin_email))
    config.set('email', 'default_from_email', str(options.server_email))
    config.set('email', 'server_email', str(options.server_email))
    settings_fd = open(settings_file, 'w')
    config.write(settings_fd)
    settings_fd.close()

#------------------------------------------------------------------------------
def run(command, global_options, options, args):
    """
    Create a new ECM instance.
    """
    instance_dir = init_instance(command, args)
    if options.quiet:
        return
    try:
        prompt_missing_options(options)
        write_settings(command, options, instance_dir)
        log = get_logger()
        log.info('')
        log.info('New ECM instance created in "%s".' % instance_dir)
        log.info('Please check the configuration in "%s" before running `ecm-admin init`.'
                 % path.join(instance_dir, 'settings.ini'))
    except:
        # delete the created instance directory if something goes wrong
        shutil.rmtree(instance_dir, ignore_errors=True)
        raise