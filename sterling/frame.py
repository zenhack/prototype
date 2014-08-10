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
A frame is an xml reprentation widget.
"""

from types import GeneratorType
import xml.etree.ElementTree as ET
from abc import abstractmethod, ABCMeta

import sterling.csslavie as css

SEQ_MODE = 1
OBJ_MODE = 2

_widgets = None


def _mode(obj):
    if type(obj) in {list, tuple, GeneratorType}:
        return SEQ_MODE
    else:
        return OBJ_MODE


def _default_get(haystack, needle, default):
    try:
        return haystack[needle]
    except KeyError:
        return default


class Frame(css.PropertyObject):
    __metaclass__ = ABCMeta
    callbacks = ()

    def __init__(self, attrs=None, children=None):
        self.attrs = attrs or {}

        classes = None
        if 'class' in self.attrs:
            classes = self.attrs['class'].split(' ')
        super(Frame, self).__init__(name=self.__class__.__name__.lower(),
                                    classes=classes)

        self.children = children or {}
        self.ctx = _default_get(self.attrs, 'ctx', None)
        self.mode = _default_get(self.attrs, 'mode', None)

        for child in children:
            child.parent = self

    def attach_callbacks(self, widget):
        for cb in self.callbacks:
            if cb in self.attrs:
                cb_add = getattr(widget, 'callback_%s_add' % cb)
                cb_add(lambda o: getattr(data, self.attrs[cb])(o))


    def widget_seq(self, data):
        """Returns a widget for each element of data, based on this frame."""
        for datum in data:
            for widget in self.widget_contents(datum, self):
                yield widget

    def widget_contents(self, data):
        """Returns a generator of all directy child widgets of this frame."""
        mode = self.mode or _mode(data)
        if mode is SEQ_MODE:
            self.widget_seq(data)
        else:
            for child in self.children:
                yield child.widget(data, parent=self)

    def widget(self, data, parent=None):
        if self.ctx:
            data = getattr(data, self.ctx)
        ret = self.make_widget(data, parent)
        for w in self.widget_contents(data):
            self.add(w)
        return ret

    def make_widget(self, data, parent=None):
        # Incomplete!!
        for attr in self.attrs:
            # Map here if needed XXX
            if hasattr(widget, attr):
                setattr(widget, attr, getattr(data, self.attrs[attr]))
            widget.show()

    @abstractmethod
    def efl_container(self):
        pass

    @abstractmethod
    def add(self, widget):
        pass


def from_file(filename):
    root = ET.parse(filename).getroot()
    return _from_xml(root)


def _from_xml(root):

    # The first time we run this, we need to populate the table of widgets:
    global _widgets
    if _widgets is None:
        _widgets = {}
        for cls in Frame.__subclasses__():
            _widgets[cls.__name__.lower()] = cls

    children = map(_from_xml, root)
    widget_cls = _widgets[root.tag.lower()]
    return widget_cls(attrs=root.attrib, children=children)
