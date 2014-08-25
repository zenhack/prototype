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
from collections import defaultdict

import sterling.csslavie as css

SEQ_MODE = 1
OBJ_MODE = 2

_widgets = None


def mode(obj):
    if type(obj) in {list, tuple, GeneratorType}:
        return SEQ_MODE
    else:
        return OBJ_MODE


class Frame(css.PropertyObject):
    __metaclass__ = ABCMeta
    callbacks = ()

    def __init__(self, attrs=None, children=None):
        self.attrs = attrs
        attrs = defaultdict(lambda: None, attrs or {})

        classes = None
        if 'class' in self.attrs:
            classes = self.attrs['class'].split(' ')
        # TODO: I (Ian) Think we need to move this to the widgets?
        super(Frame, self).__init__(name=self.__class__.__name__.lower(),
                                    classes=classes)

        self.children = children or []
        self.ctx = attrs['ctx']
        self.mode = attrs['mode']

        for child in children:
            child.parent = self

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
        if hasattr(ret, 'raw_contents'):
            for w in self.widget_contents(data):
                ret.add(w)
        return ret

    @abstractmethod
    def make_widget(self, data, parent=None):
        """Generate a widget for the data based on the frame.

        `parent` should be the widget's parent. The default value of None
        is typically only valid for top-level widgets such as windows.
        """


def from_file(filename):
    root = ET.parse(filename).getroot()
    return _from_xml(root)


def _from_xml(root):

    # XXX: this logic is still "correct," but the names are all wrong; we're
    # talking about frames, not widgets. need to update this.

    # The first time we run this, we need to populate the table of widgets:
    global _widgets
    if _widgets is None:
        _widgets = {}
        for cls in Frame.__subclasses__():
            _widgets[cls.__name__.lower()] = cls

    children = map(_from_xml, root)
    widget_cls = _widgets[root.tag.lower()]
    return widget_cls(attrs=root.attrib, children=children)
