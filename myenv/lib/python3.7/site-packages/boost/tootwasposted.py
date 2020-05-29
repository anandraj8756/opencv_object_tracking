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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

'''Was this toot posted before'''

# external library imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# boost library imports
from boost.senttoots import SentToots


class TootWasPosted:
    '''Was this toot posted before'''
    def __init__(self, cfgvalues):
        '''Constructor of the TootWasPosted'''
        self.cfgvalues = cfgvalues
        # activate the sqlite db
        engine = create_engine('sqlite:///{}'.format(self.cfgvalues['sqlitepath']))
        tmpsession = sessionmaker(bind=engine)
        session = tmpsession()
        self.session = session
        SentToots.metadata.create_all(engine)
        self.allsenttootids=[]
        for twid in self.session.query(SentToots.id).all():
            self.allsenttootids.append(twid.id)

    def wasposted(self, toot):
        '''Was this toot posted already'''
        if toot in self.allsenttootids:
            return True
        else:
            return False

    def storetoot(self, toottostore):
        '''Store the last sent toot'''
        lastsenttoot = SentToots(id=toottostore)
        try:
            self.session.add(lastsenttoot)
            self.session.commit()
        except (sqlalchemy.exc.IntegrityError) as err:
            print(err)
            print('toot already posted')
