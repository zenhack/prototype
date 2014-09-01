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

from sterling import frame
from sterling.frame import Frame
from efl.elementary import window, box, button

from abc import ABCMeta, abstractmethod


class Widget(object):
    """A GUI widget (in the traditional sense).

    This class acts as a wrapper around the backend toolkit's widget
    objects.
    """
    __metaclass__ = ABCMeta

    def attach_callbacks(self, data):
        """Attach attributes of `data` to the callbacks for this widget.

        `attach_callbacks` looks at self's 'callbacks' attribute, which
        (if it exists) must be an iterable of strings. for each item,
        it attaches the callback by that name to the attribute of `data`
        specified by the frame.

        Subclasses should ensure the following is true before invoking
        this method:

        1. self has a `frame` attribute, corresponding to the widget's frame.
        2. self is in a state such that raw() is ready to be called.
        """
        if not hasattr(self, 'callbacks'):
            return

        for cb in self.callbacks:
            cb_add = getattr(self.raw(), 'callback_%s_add' % cb)

            def wrapped_callback(obj):
                real_cb = getattr(data, self.frame.attrs[cb])
                real_cb(obj)
                data.do_updates()

            cb_add(wrapped_callback)

    @abstractmethod
    def raw(self):
        """Return the backend toolkit's widget.

        This is helpful for code that cares about the underlying toolkit, but
        portable code should never use this.
        """


class Container(Widget):

    @abstractmethod
    def raw_contents(self):
        """Return the underlying container widget.

        The return value should be a container widget in the underlying
        toolkit, capable of containing multiple child widgets. This need not be
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

    def make_children(self, data):
        """Generate a sequence of child widgets based on the container's frame."""
        mode = self.frame.mode or frame.default_mode(data)
        if mode is frame.SEQ_MODE:
            for datum in data:
                yield self.frame.make_widget(datum, parent=self)
        else:
            for child in self.frame.children:
                yield child.make_widget(data, parent=self)


class Window(Frame):
    """A widow widget based ontop of the windows and box EFL widgets"""

    def make_widget(self, data, parent=None):
        if parent is not None:
            # We need to accept the parameter to conform to the interface, but
            # we can't actually use it, and if we're being called as a child,
            # something is wrong:
            raise TypeError('Parent of Window must be None.')
        return self._Widget(data)

    class _Widget(Container):

        def __init__(self, data):
            self._win = window.StandardWindow('test', 'Test')
            self._box = box.Box(self._win)
            self._win.resize_object_add(self._box)
            self._box.show()
            self._win.show()

        def raw(self):
            return self._win

        def raw_contents(self):
            return self._box

        def add(self, child):
            self._box.pack_end(child.raw())

class Button(Frame):

    def make_widget(self, data, parent):
        return self._Widget(data, parent, self)

    class _Widget(Widget):

        callbacks = ['clicked']

        def __init__(self, data, parent, fr):
            self._btn = button.Button(parent.raw_contents())
            self.data = data
            self.frame = fr
            if 'text' in fr.attrs:
                self._btn.text = getattr(data, fr.attrs['text'])
            self.attach_callbacks(data)
            data.subscribe(fr.attrs['text'], self.update)
            self._btn.show()

        def update(self, data):
            self._btn.text = getattr(data, self.frame.attrs['text'])

        def raw(self):
            return self._btn
