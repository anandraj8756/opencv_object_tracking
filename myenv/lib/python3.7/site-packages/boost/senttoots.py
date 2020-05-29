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

# SentToots mapping for SQLAlchemy
'''SentToots mapping for SQLAlchemy'''

# external library imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

MYBASE = declarative_base()

class SentToots(MYBASE):
    '''SentToots mapping for SQLAlchemy'''
    __tablename__ = 'senttoots'

    id = Column(Integer, primary_key=True)
