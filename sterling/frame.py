
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

    @abstractmethod
    def make_widget(self, data, parent=None):
        pass

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
