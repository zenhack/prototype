#
# Copyright 2014 Ian Denhardt <ian@zenhack.net>
# Copyright      Martin Owens <doctormo@gmail.com>
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
EFL based widgets to display the kinds of things we want... more docs to follow.
"""

from sterling.frame import Frame
from efl.elementary import window, box, button

from abc import ABCMeta, abstractmethod


class Widget(object):
    """A GUI widget (in the traditional sense).

    This class acts as a wrapper around the underlying toolkit's widget
    objects. It may actually comprise multiple widgets; see `raw_contents()`.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def raw(self):
        """Return the underlying toolkit widget.

        This is useful mainly for implementing other widgets, as it allows the
        caller to e.g. add them to container widgets.

        Access to the underlying toolkit object is useful for some backends,
        but is not a substitute for the `add()` method. Toolkit-agnostic code
        should not use this method.
        """

    @abstractmethod
    def raw_contents(self):
        """Return the underlying container widget.

        The return value should be a container widget in the underlying
        toolkit, capable of containing multiple child widgets. This may not be
        the same as `raw()`. For example, if the result of `raw()` is unable
        to contain more than one child, the implementation may add another
        widget (which can contain more than one widget) as its child, and
        return that from `raw_contents()`.

        Access to the underlying toolkit object is useful for some backends,
        but is not a substitute for the `add()` method. Toolkit-agnostic code
        should not use this method.
        """

    @abstractmethod
    def add(self, child):
        """Add the child widget `child`."""


class Window(Frame):
    """A widow widget based ontop of the windows and box EFL widgets"""

    def make_widget(self, data, parent=None):
        return self.widget_cls(data)

    class widget_cls(Widget):

        def __init__(self):
            self._win = window.StandardWindow('test', 'Test')
            self._box = box.Box(self._win)
            self._win.resize_object_add(self._box)
            self._box.show()
            self._win.show()

        def raw_contents(self):
            return self._box

        def add(self, child):
            self._box.pack_end(child.raw())


class Button(Frame):
    callbacks = ['clicked']

    def make_widget(self, data, parent=None):
        if not hasattr(self, '_button'):

            self._button = button.Button(parent.efl_container())
            if 'text' in self.attrs:
                self._button.text = getattr(data, self.attrs['text'])

            self.attach_callbacks(self._button, data)
            data.subscribe(self.attrs['text'], self.update)
            self._button.show()

        return self._button

    def update(self, data):
        self._button.text = getattr(data, self.attrs['text'])

    def efl_container(self):
        return self._button

    def add(self, w):
        pass
