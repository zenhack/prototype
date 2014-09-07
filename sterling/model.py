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
    """a model in the traditional MVC sense

    In terms of concrete functionality, instances of `Model` allow client code
    to subscribe to updates to the object's attributes.

    Assignment to the model's attributes will flag those attributes as
    changed if any subscriptions exist. `subscribe` registers a handler
    for updates to a given attribute, and `do_updates` actually invokes
    the subscribers.
    """

    def __init__(self):
        """Initialize the model.

        Subclasses of `Model` *must* invoke `Model`'s `__init__`.
        """
        self.subscriptions = {}
        # Setting changed causes the object to watch for updates; prior
        # to this setattr will work as  normal:
        self.changed = set()

    def __setattr__(self, key, value):
        if hasattr(self, 'changed'):
            self.changed.add(key)
        super(Model, self).__setattr__(key, value)

    def do_updates(self):
        """Notify subscribers of any changed attributes.

        `do_updates` invokes each subscriber whose attribute has changed with
        the model as its argument. The order in which the subscribers are
        called is unspecified. When `do_updates` returns, all attributes will
        be flagged as unchanged.
        """
        for key in self.subscriptions.keys():
            if key in self.changed:
                for subscriber in self.subscriptions[key]:
                    subscriber(self)
        super(Model, self).__setattr__('changed', set())

    def subscribe(self, attr, subscriber):
        """Subscribe to updates to the attribute `attr`.

        Parameters:

            attr - name of the attribute to subscribe to
            subscriber - a callable accepting a single argument, which will be
                         the model itself. `subscriber` will be called by
                         `do_updates` if the attribute has changed.
        """
        if attr not in self.subscriptions:
            self.subscriptions[attr] = [subscriber]
        else:
            self.subscriptions[attr].append(subscriber)
