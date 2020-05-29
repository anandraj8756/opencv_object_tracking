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

# Validate class
'''Validate class'''

# standard library imports
import datetime
import os.path
import sys
import re

# boost library imports
from boost.tootwasposted import TootWasPosted
from boost.waitamoment import WaitAMoment


class Validate(object):
    '''Validate class'''
    def __init__(self, cfgvalues, args, api, toot):
        '''send the toot'''
        self.api = api
        self.args = args
        self.cfgvalues = cfgvalues
        self.storeit = False
        self.toot = toot
        self.twp = TootWasPosted(self.cfgvalues)
        self.main()

    def main(self):
        '''Main of the Validate class'''
        # test if it was boosted enough to be boosted by me
        if self.toot['reblogs_count'] >= self.cfgvalues['boosts']:
            # send the toot if all checks are ok
            if not self.not_boost_hashtags() and self.boost_only_if_hashtags() and self.boost_only_if_older_than() and self.boost_only_if_younger_than() and self.boost_only_if_matching_regex():
                self.storeit = True
                if self.args.dryrun:
                    if not self.args.populatedb:
                        print("toot {} should have been sent!".format(self.toot['id']))
                    else:
                        print("toot {} should have been populated!".format(self.toot['id']))
                else:
                    # at last boost the toot
                    if not self.args.populatedb:
                        self.api.status_reblog(self.toot['id'])
                    if self.cfgvalues['favorite']:
                        self.api.status_favourite(self.toot['id'])
            else:
                self.storeit = False
        # now store the toot
        if not self.twp.wasposted(self.toot['id']) and self.storeit:
            if not self.args.dryrun:
                self.twp.storetoot(self.toot['id'])
            WaitAMoment(self.cfgvalues['waitminsecs'], self.cfgvalues['waitmaxsecs'])

    def not_boost_hashtags(self):
        '''check if the toot has a hashtag for not boosting'''
        found = False
        # check if the current toot contains a do-not-boost hashtag
        for i in self.cfgvalues['dontboosthashtags']:
            if '#<span>{}</span></a>'.format(i) in self.toot['content']:
                found = True
        return found

    def boost_only_if_hashtags(self):
        '''boost only if the toot has the following hashtag'''
        found = False
        if self.cfgvalues['onlyifhashtags']:
            # check if the current toot contains one of the hashtags to be boosted
            for i in self.cfgvalues['onlyifhashtags']:
                if '#<span>{}</span></a>'.format(i) in self.toot['content']:
                    found = True
        else:
            found = True
        return found

    def boost_only_if_older_than(self):
        '''boost only if the toot is older than a number of minutes'''
        send = False
        if self.cfgvalues['olderthan']:
            # check if the toot is older than a number of minutes
            now = datetime.datetime.utcnow()
            tootbirth = datetime.datetime.strptime(self.toot['created_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            lapse = now - tootbirth
            try:
                if (lapse.seconds / 60) > self.cfgvalues['olderthan']:
                    send = True
                else:
                    send = False
            except ValueError:
                send = False
        else:
            send = True
        return send

    def boost_only_if_younger_than(self):
        '''boost only if the toot is younger than a number of minutes'''
        send = False
        if self.cfgvalues['youngerthan']:
            # check if the toot is younger than a number of minutes
            now = datetime.datetime.utcnow()
            tootbirth = datetime.datetime.strptime(self.toot['created_at'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
            lapse = now - tootbirth
            try:
                if (lapse.seconds / 60) < self.cfgvalues['youngerthan']:
                    send = True
                else:
                    send = False
            except ValueError:
                send = False
        else:
            send = True
        return send
        
    def boost_only_if_matching_regex(self):
        '''boost only if the toot contains given regex'''
        match = True
        if self.cfgvalues['matchregex']:            
            match = re.search(self.cfgvalues['matchregex'], self.toot['content'])            
        return True if match else False
