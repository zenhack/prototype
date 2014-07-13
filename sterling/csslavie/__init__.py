
"""
CssLaVie is the CSS parsing and CSS property control for sterling.

It's used like this::

 from sterling.csslavie import PropertyObject, CssParser

 class MyRenderableObject(PropertyObject):
     pass

 css = CssParser('main.css')

 obj = MyRenderableObject(name='stephen', classes=['red'])
 css.attach(obj)

Assuming main.css contained this::

 myrenderableobject {
   foo: bar;
 }
 #stephen {
   width: heavy;
 }
 .red {
   background: red;
 }

The first matches the object's class name, the second matches the object's
name attribute and the third matches one of items in the object's classes
list.

Once attached, values are accessed like this::

 obj.foo == 'bar'
 obj.width == 'heavy'
 obj.background == 'red'

Values can be over-ridden from their css settings like this::

 obj.foo = "No bar"

Value will persist until::

 del obj.foo

When the value will go back to::

 obj.foo == "bar"

"""

__version__ = "0.4"
__pkgname__ = "csslavie"

from .parse import CssParser
from .objects import PropertyObject

