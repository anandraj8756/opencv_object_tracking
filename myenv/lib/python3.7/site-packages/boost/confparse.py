# -*- coding: utf-8 -*-
# Copyright © 2017 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Get values of the configuration file
'''Get values of the configuration file'''

# standard library imports
import configparser
import sys
import re

class ConfParse(object):
    '''ConfParse class'''
    def __init__(self, pathtoconf):
        '''Constructor of the ConfParse class'''
        self.userstoboost = ''
        self.usercred = ''
        self.clientcred = ''
        self.boosts = 0
        self.waitminsecs = 1
        self.waitmaxsecs = 1
        self.pathtoconf = pathtoconf
        self.dontboosthashtags = []
        self.onlyifhashtags = []
        self.matchregex = ''
        self.olderthan = 0
        self.stringsep = ','
        self.youngerthan = 0
        self.sqlitepath = 'boost.db'
        self.favorite = False
        self.main()

    def main(self):
        '''Main of the ConfParse class'''
        # read the configuration file
        config = configparser.ConfigParser()
        try:
            with open(self.pathtoconf) as conffile:
                config.read_file(conffile)
                ### mastodon section
                section = 'mastodon'
                if config.has_section(section):
                    # instance_url option
                    confoption = 'instance_url'
                    if config.has_option(section, confoption):
                        self.instanceurl = config.get(section, confoption)
                    else:
                        sys.exit('{confoption} parameter is mandatory in {section} section'.format(confoption=confoption, section=section))
                    # users_to_boost option
                    confoption = 'users_to_boost'
                    if config.has_option(section, confoption):
                        userstoboost =  config.get(section, confoption)
                        self.userstoboost = [i for i in userstoboost.split(self.stringsep) if i]
                    else:
                        sys.exit('{confoption} parameter is mandatory in {section} section'.format(confoption=confoption, section=section))
                    # user_credentials option
                    confoption = 'user_credentials'
                    if config.has_option(section, confoption):
                        self.usercred = config.get(section, confoption)
                    else:
                        sys.exit('{confoption} parameter is mandatory in {section} section'.format(confoption=confoption, section=section))
                    # client_credentials option
                    confoption = 'client_credentials'
                    if config.has_option(section, confoption):
                        self.clientcred = config.get(section, confoption)
                    else:
                        sys.exit('{confoption} parameter is mandatory in {section} section'.format(confoption=confoption, section=section))
                ### boost section
                section = 'boost'
                if config.has_section(section):
                    # boosts option
                    confoption = 'boosts'
                    if config.has_option(section, confoption):
                        self.boosts = config.get(section, confoption)
                    # waitminsec option
                    confoption = 'waitminsecs'
                    if config.has_option(section, confoption):
                        self.waitminsecs = config.get(section, confoption)
                    # waitmaxsec option
                    confoption = 'waitmaxsecs'
                    if config.has_option(section, confoption):
                        self.waitmaxsecs = config.get(section, confoption)
                    # do_not_boost_hashtags option
                    confoption = 'do_not_boost_hashtags'
                    if config.has_option(section, confoption):
                        dontboosthashtags = config.get(section, confoption)
                        if dontboosthashtags:
                            hashtags = [i for i in dontboosthashtags.split(self.stringsep) if i != '']
                            self.dontboosthashtags = hashtags
                    # only_if_hashtags option
                    confoption = 'only_if_hashtags'
                    if config.has_option(section, confoption):
                        onlyifhashtags = config.get(section, confoption)
                        if onlyifhashtags:
                            hashtags = [i for i in onlyifhashtags.split(self.stringsep) if i != '']
                            self.onlyifhashtags = hashtags
                    # match option
                    confoption = 'match'
                    if config.has_option(section, confoption):
                        regex = config.get(section, confoption)
                        if regex:
                            self.matchregex = regex
                            # throws exception if the regex is not valid
                            re.compile(regex)
                    # older_than option
                    confoption = 'older_than'
                    if config.has_option(section, confoption):
                        self.olderthan = config.get(section, confoption)
                    # younger_than option
                    confoption = 'younger_than'
                    if config.has_option(section, confoption):
                        self.youngerthan = config.get(section, confoption)
                    # like option
                    confoption = 'favorite'
                    if config.has_option(section, confoption):
                        self.favorite = config.getboolean(section, confoption)
                ### sqlite section
                section = 'sqlite'
                if config.has_section(section):
                    # sqlitepath option
                    confoption = 'sqlite_path'
                    if config.has_option(section, confoption):
                        self.sqlitepath = config.get(section, confoption)

        except (configparser.Error, IOError, OSError) as err:
            print(err)
            sys.exit(1)
        try:
            self.boosts = int(self.boosts)
        except ValueError as err:
            print(err)
            self.boosts = 0
        try:
            self.waitminsecs = int(self.waitminsecs)
        except ValueError as err:
            print(err)
            self.waitminsecs = 10
        try:
            self.waitmaxsecs = int(self.waitmaxsecs)
        except ValueError as err:
            print(err)
            self.waitmaxsecs = 10
        try:
            self.olderthan = int(self.olderthan)
        except ValueError as err:
            print(err)
            self.olderthan = 0
        try:
            self.youngerthan = int(self.youngerthan)
        except ValueError as err:
            print(err)
            self.youngerthan = 0

        # check if waitminsecs >= waitmaxsecs
        if self.waitminsecs > self.waitmaxsecs:
            sys.exit('In the [{section}] section, waitminsecs should be smaller than waitmaxsecs. Leaving.'.format(section='boost'))

    @property
    def confvalues(self):
        '''get the values of the configuration file'''
        return {'instanceurl': self.instanceurl,
                'userstoboost':  self.userstoboost,
                'usercred': self.usercred,
                'clientcred': self.clientcred,
                'boosts': self.boosts,
                'waitminsecs': self.waitminsecs,
                'waitmaxsecs': self.waitmaxsecs,
                'sqlitepath': self.sqlitepath,
                'dontboosthashtags': self.dontboosthashtags,
                'onlyifhashtags': self.onlyifhashtags,
                'matchregex': self.matchregex,
                'olderthan': self.olderthan,
                'youngerthan': self.youngerthan,
                'favorite': self.favorite}
