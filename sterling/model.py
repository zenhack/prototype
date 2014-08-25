#
# Copyright 2014 Ian Denhardt <ian@zenhack.net>
# Copyright      Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>


class Model(object):
    def __init__(self):
        self.subscriptions = {}
        # Setting changed causes the object to watch for updates; prior
        # to this setattr will work as  normal:
        self.changed = set()

    def __setattr__(self, key, value):
        if hasattr(self, 'changed'):
            self.changed.add(key)
        super(Model, self).__setattr__(key, value)

    def do_updates(self):
        for key in self.subscriptions.keys():
            if key in self.changed and key in self.subscriptions:
                for subscriber in self.subscriptions[key]:
                    subscriber(self)

    def subscribe(self, attr, subscriber):
        if attr not in self.subscriptions:
            self.subscriptions[attr] = [subscriber]
        else:
            self.subscriptions[attr].append(subscriber)
