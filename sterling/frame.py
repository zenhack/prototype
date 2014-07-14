
from types import GeneratorType
import xml.etree.ElementTree as ET
from abc import abstractmethod, ABCMeta

from .widget import lookup

OBJ_MODE = 0
LIST_MODE = 1

#class Frame(object):
#    """Generates a UI frame from a definitions file"""
#    def __init__(self, ui_file):
#        self.xml_root = ET.parse(ui_file)
#
#    def generate_list(self, context):
#        for x in context:
#            for i in self.generate(x):
#                yield i
#
#    def generate(self, context, mode=None):
#    	if self.target:
#    		context = getattr(context, self.target)
#
#    	if callable(context):
#    		context = context()
#
#    	if (type(context) in (list, tuple, GeneratorType) and mode is None) or mode == LIST_MODE:
#    		return self.generate_list(context)
#
#    	if self.widget == 'ref':
#    		return self.generate(context, self.find(self.to))
#
#    	widget = EflWidget(self.widget) #{ 'widget', 'id?', 'class?', 'mode?' 'target?', ref_only:'to?' }
#
#    	for child in self:
#    		widget.append( self.generate(context, child, mode=child.mode) )
#
#    	return [widget]
#
#    def __iter__(self):
#        pass
#        # Loop through widgets


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
        for datum in data:
            for widget in self.generate(datum):
                yield widget

    def widget_contents(self, data):
        if self.ctx:
            data = getattr(data, self.ctx)

        if (type(context) in (list, tuple, GeneratorType) and self.mode is None) \
                or mode is LIST_MODE:
            return self.widget_seq(data)

        for i in range(len(self.children)):
            yield self.children[i].widget(data)

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
    widget_cls = lookup(root.tag)
    return widget_cls(attrs=root.attrib, children=children)
