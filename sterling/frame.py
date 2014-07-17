
from types import GeneratorType
import xml.etree.ElementTree as ET
from abc import abstractmethod, ABCMeta

SEQ_MODE = 1
OBJ_MODE = 2

_widgets = {}


def widget(cls):
    """A decorator for declaring widget classes.

    The decorated class will be discoverable when generating frames from an
    xml description.

    TODO: There's probably a way to wrap this into the Frame class, so that
    simply subclassing is enough.
    """
    _widgets[cls.__name__.lower()] = cls
    return cls


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


class Frame(object):
    __metaclass__ = ABCMeta

    def __init__(self, attrs=None, children=None):
        self.attrs = attrs or []
        self.children = children or {}
        self.ctx = _default_get(self.attrs, 'ctx', None)
        self.mode = _default_get(self.attrs, 'mode', None)

    def widget_seq(self, data):
        """Returns a widget for each element of data, based on this frame."""
        for datum in data:
            for widget in self.widget_contents(datum):
                yield widget

    def widget_contents(self, data):
        """Returns a generator of all directy child widgets of this frame."""
        if self.ctx:
            data = getattr(data, self.ctx)

        mode = self.mode or _mode(data)
        if mode is SEQ_MODE:
            self.widget_seq(data)
        else:
            for child in self.children:
                yield child.widget(data)

    def widget(self, data):
        ret = self.make_widget(data)
        for w in self.widget_contents():
            ret.add(w)
        return ret

    @abstractmethod
    def make_widget(self, data):
        pass


def from_file(filename):
    root = ET.parse(filename)
    return _from_xml(root)


def _from_xml(root):
    children = map(_from_xml, root)
    widget_cls = _widgets[root.tag.lower()]
    return widget_cls(attrs=root.attrib, children=children)
