#
# Copyright 2012-2014 Martin Owens <doctormo@gmail.com>
# Copyright      2014 Ian Denhardt <ian@zenhack.net>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
The idea here is to provide a machanism for getting attributes at the right time.

Should provide stateful attribute access and some signal support for changes.
"""

from .base import DefaultOrderedDict, Event
from collections import defaultdict

class PropertyObject(object):
    """Property objects control system of layered property dictionaries,
       attributes returned are from the top most stack with that item key

    ! Keeping the user attributes ahead of the pack is trouble. Is this useful?

    """
    def __new__(cls, *p, **k):
        inst = object.__new__(cls)
        inst.__attrs__ = DefaultOrderedDict(dict)
        inst.__watch__ = defaultdict(Event)
        return inst

    def __init__(self, name=None, classes=None):
        self.name = name
        self.classes = classes

    def __setattr__(self, name, value):
        if name[0] != '_':
            self.__attrs__['user'][name] = value
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name[0] != '_' and name in self.__attrs__['user']:
            self.__attrs__['user'].pop(name)
        self.refresh([name])

    def add_to(self, d, name='base'):
        reorder = name not in self.__attrs__

        self.__attrs__[name].update(d)
        if reorder:
            self.__attrs__.sort_to_end('user')

        self.__dict__.update(d)

        if 'user' in self.__attrs__:
            self.__dict__.update(self.__attrs__['user'])

    def remove(self, name):
        old = self.__attrs__.pop(name)
        self.refresh(old.keys())

    def refresh(self, keys=None):
        keys = keys or self.__attrs__.super_keys()
        self.__dict__.update(self.__attrs__.super_gets(keys))

    def watch(self, callback, name, value=None, callback_off=None):
        """A single watcher for attribute changes... can also detect on/off switching"""
        self.__watch__[name] += callback



