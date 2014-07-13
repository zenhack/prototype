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
sys.path.insert(0, '.')

import unittest
from sterling.csslavie import PropertyObject
try:
    from test import test_support
except ImportError:
    from test import support as test_support

class PropertyTestCase(unittest.TestCase):
    """Test property object's capabilities."""
    def setUp(self):
        self.p = PropertyObject()
        self.p.add_to({'foo': 2})

    def test_01_get_attr(self):
        """Get attributes"""
        self.assertEqual(self.p.foo, 2)

    def test_02_replace(self):
        """Replace Attributes"""
        self.p.add_to({'foo': 1})
        self.assertEqual(self.p.foo, 1)

    def test_03_set_attr(self):
        """Set user attributes"""
        self.p.foo = 3
        self.assertEqual(self.p.foo, 3)

    def test_04_multi_attr(self):
        """Multiple attributes"""
        self.p.add_to({'foo': 5}, 'hover')
        self.assertEqual(self.p.foo, 5)
        self.p.add_to({'foo': 6}, 'down')
        self.assertEqual(self.p.foo, 6)

    def test_05_multi_remove(self):
        """Remove extra state"""
        self.p.add_to({'foo': 5}, 'hover')
        self.assertEqual(self.p.foo, 5)
        self.p.remove('hover')
        self.assertEqual(self.p.foo, 2)

    def test_06_multi_and_user(self):
        """Attribute Order"""
        self.p.foo = 12
        self.assertEqual(self.p.foo, 12)
        self.p.add_to({'foo': 6}, 'down')
        self.assertEqual(self.p.foo, 12)

    def test_07_refreshed(self):
        """Refresh Attributes"""
        self.p.add_to({'foo': 5}, 'hover')
        self.p.foo = 12
        self.p.refresh()
        self.assertEqual(self.p.foo, 12)


    def test_08_del_attr(self):
        """Delete attributes"""
        self.p.foo = 3
        del self.p.foo
        self.assertEqual(self.p.foo, 2)

         


if __name__ == '__main__':
    test_support.run_unittest(
       PropertyTestCase,
    )
