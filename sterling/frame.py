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

_frame_types = None


def default_mode(obj):
    if type(obj) in {list, tuple, GeneratorType}:
        return SEQ_MODE
    else:
        return OBJ_MODE


class Frame(css.PropertyObject):
    """A mapping from models to user interfaces.

    The full documentation of what a frame is, what it defines and how to
    build them is documented (TODO: not yet it isn't) in `doc/frames.md`.

    Frames should not be created directly by the user; see `from_file`.
    """
    __metaclass__ = ABCMeta
    callbacks = ()

    def __init__(self, attrs=None, children=None):
        self.attrs = attrs
        attrs = defaultdict(lambda: None, attrs or {})

        classes = None
        if 'class' in self.attrs:
            classes = self.attrs['class'].split(' ')
        super(Frame, self).__init__(name=self.__class__.__name__.lower(),
                                    classes=classes)

        self.children = children or []
        self.ctx = attrs['ctx']
        self.mode = attrs['mode']

        for child in children:
            child.parent = self

    def widget_seq(self, data):
        """Return a widget for each element of data, based on this frame."""
        for datum in data:
            for widget in self.widget_contents(datum, self):
                yield widget

    def widget_contents(self, data, parent):
        """Return a generator of all direct child widgets of this frame.

        `data` is the model from which to construct the widgets.
        `parent` is the widget for this frame, i.e. the parent of the widgets
        to be created.
        """
        mode = self.mode or default_mode(data)
        if mode is SEQ_MODE:
            self.widget_seq(data)
        else:
            for child in self.children:
                yield child.widget(data, parent=parent)

    def widget(self, data, parent=None):
        """Return a widget for this frame, based on `data`.

        TODO: how is this different from `make_widget`? document."""
        if self.ctx:
            data = getattr(data, self.ctx)
        ret = self.make_widget(data, parent)
        if hasattr(ret, 'raw_contents'):
            for w in self.widget_contents(data, ret):
                ret.add(w)
        return ret

    @abstractmethod
    def make_widget(self, data, parent=None):
        """Generate a widget for the data based on the frame.

        `parent` should be the widget's parent. The default value of None
        is typically only valid for top-level widgets such as windows.
        """


def from_file(filename):
    """Load a frame from the given xml file."""
    root = ET.parse(filename).getroot()
    return _from_xml(root)


def _from_xml(root):
    # The first time we run this, we need to populate the table of frame types:
    global _frame_types
    if _frame_types is None:
        _frame_types = {}
        for cls in Frame.__subclasses__():
            _frame_types[cls.__name__.lower()] = cls

    children = map(_from_xml, root)
    frame_cls = _frame_types[root.tag.lower()]
    return frame_cls(attrs=root.attrib, children=children)
