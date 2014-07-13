#
# Copyright 2014, Martin Owens
#
# License goes here.
#
"""

Documentation goes here

"""

try:
    from xssd import Validator, ParseXML
except ImportError:
    Validator = None

from .csslavie import CssParser

#
# This schema for our ui files will need to be thought out
# as we expand. More checks and details etc.
#
VALD = {
  'root' : [ { 'name' : 'window',  'type' : 'container' } ],
  'complexTypes': {
    'widget': [
      { 'name': '_class', },
      { 'name': '_click', },
    ],
    'container': [
      { 'name' : 'label',  'type' : 'widget', 'minOccurs': 0, 'maxOccurs': 'unbounded' },
    ],
  },
}
if Validator:
    VALD = Validator(VALD)

class InvalidFile(ValueError):
    pass

class Model(object):
    def __init__(self):
        pass

    def _name(self):
        return type(self).__name__.lower()



class App(Model):
    ui = None
    css = None

    def __init__(self):
        if not Validator:
            raise ImportError("Can't find xssd python module.")
        self._css = CssParser(self.css or self._name() + '.css')
        self._ui  = ParseXML(self.ui or self._name() + '.xml').data

        errors = VALD.validate(self._ui)
        if errors:
            raise InvalidFile(str(errors))

    def run(self):
        print "Do stuff here?"


