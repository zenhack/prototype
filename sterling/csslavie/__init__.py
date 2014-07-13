
"""
CssLaVie is the CSS parsing and CSS property control for sterling.

It's used like this::

 from sterling.csslavie import PropertyObject, CssParser

 class MyRenderableObject(PropertyObject):
     pass

 css = CssParser('main.css')

 obj = MyRenderableObject()
 css.attach(obj)

Assuming main.css contained this::

 myrenderableobject {
   foo: bar;
 }

One can accept the value like this::

 obj.foo == 'bar'

Values can be over-ridden from their css settings like this::

 obj.foo = "No bar"

And will alway be the in-code version until::

 del obj.foo

When the value will go back to::

 obj.foo == "bar"

"""

__version__ = "0.4"
__pkgname__ = "csslavie"

from .parse import CssParser
from .objects import PropertyObject

