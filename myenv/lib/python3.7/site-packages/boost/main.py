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

# Main class
'''Main class'''

# standard library imports
import configparser
import os.path
import sys

# external library imports
from mastodon import Mastodon

# boost imports
from boost.cliparse import CliParse
from boost.confparse import ConfParse
from boost.tootwasposted import TootWasPosted
from boost.validate import Validate
from boost.waitamoment import WaitAMoment


class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        # parse the command line
        rtargs = CliParse()
        self.args = rtargs.arguments
        # read the configuration file
        cfgparse = ConfParse(self.args.pathtoconf)
        self.cfgvalues = cfgparse.confvalues
        self.twp = TootWasPosted(self.cfgvalues)

        # activate the mastodon api
        self.api = Mastodon(
            client_id = self.cfgvalues['clientcred'],
            access_token = self.cfgvalues['usercred'],
            api_base_url = self.cfgvalues['instanceurl']
        )
        self.main()

    def main(self):
        '''Main of the Main class'''
        for user in self.cfgvalues['userstoboost']:
            lasttoots = self.api.account_statuses(self.api.account_search(user, limit=1)[0]['id'])
            lasttoots.reverse()
            if self.args.limit:
                lasttoots = lasttoots[(len(lasttoots) - self.args.limit) :]
            tootstosend = []
            # test if the last 20 toots were posted
            for lasttoot in lasttoots:
                if not self.twp.wasposted(lasttoot['id']):
                    Validate(self.cfgvalues, self.args, self.api, lasttoot)
        sys.exit(0)
