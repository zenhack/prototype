#!/usr/bin/python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
import sys

sys.path.insert(0, '../')

import unittest
from sterling.csslavie import CssParser, PropertyObject
try:
    from test import test_support
except ImportError:
    from test import support as test_support


class Name(PropertyObject):
    value = 0

    def __init__(self, *args, **kwargs):
        self.sticky = 2
        PropertyObject.__init__(self, *args, **kwargs)


class SimpleTestCase(unittest.TestCase):
    """Test use documentation in css."""
    def setUp(self):
        self.css = CssParser("data/test1.css")

    def test_01_name(self):
        """Attach by Type Name"""
        named = Name()
        self.assertEqual(named.value, 0)
        self.css.attach(named)
        self.assertEqual(named.value, 1)

    def test_02_sticky(self):
        """Sticky Values"""
        named = Name()
        self.assertEqual(named.sticky, 2)
        self.css.attach(named)
        self.assertEqual(named.sticky, 2)
        del named.sticky
        self.assertEqual(named.sticky, -1)

    def test_03_id(self):
        """Attach by Id / Object Name"""
        named = Name(name="name")
        self.assertEqual(named.value, 0)
        self.css.attach(named)
        self.assertEqual(named.value, 2)

    def test_04_class(self):
        """Attach by Single Class"""
        named = Name(classes=['name'])
        self.assertEqual(named.value, 0)
        self.css.attach(named)
        self.assertEqual(named.value, 3)

    def test_05_three(self):
        """Attach All Three"""
        named = Name(name="name", classes=['name'])
        self.assertEqual(named.value, 0)
        self.css.attach(named)
        self.assertEqual(named.value, 4)

    def test_06_parent(self):
        """Parent Child Rule"""
        named = Name(name="parent")
        self.css.attach(named)
        self.assertEqual(named.value, 1)

        named = Name(name="child")
        self.css.attach(named)
        self.assertEqual(named.value, 1)

        named = Name(name="parent")
        child = Name(name="child")
        named.children = [child]
        
        self.css.attach_all(named)
        self.assertEqual(named.value, 1)
        self.assertEqual(child.value, 5)

if __name__ == '__main__':
    test_support.run_unittest(
       SimpleTestCase,
    )
