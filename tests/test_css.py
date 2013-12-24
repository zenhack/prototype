#!/usr/bin/python
#
# Copyright (C) 2013 Martin Owens
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
"""
Test our tinycss based css parser module.
"""

import os
import sys
import unittest

sys.path.insert(0, '../')
sys.path.insert(0, './')

from sterling.css import Stylesheet

try:
    from test import test_support
except ImportError:
    from test import support as test_support

with open('data/test1.css') as fhl:
    DATA = fhl.read()

class CssTestCase(unittest.TestCase):
    def setUp(self):
        self.css = Stylesheet(DATA)

    def test_00_load(self):
        """Test Load of css"""
        self.assertTrue(self.css)

    def _match(self, n, *args, **kwargs):
        """Wrapper for a simple match"""
        matches = self.css.matches(*args, **kwargs)
        self.assertEqual(len(matches), n)

    def test_01_match_none(self):
        """Mismatch Returns None"""
        self._match(0, id='none')
        self._match(0, cls=['none'])
        self._match(0, name='none')

    def test_02_match_id(self):
        """Match Single ID"""
        self._match(1, id='idtest')

    def test_03_match_class(self):
        """Match Classes"""
        self._match(1, cls=['clstest'])
        self._match(2, cls=['clstest', 'othcls'])
        self._match(1, cls=['clstest', 'foo'])

    def test_04_match_name(self):
        """Match Element Type"""
        self._match(1, name='nametest')

    def test_05_match_two(self):
        """Match Type and Class together"""
        self._match(1, name='dove', cls='fried')
        self._match(0, name='dofe', cls='fried')
        self._match(0, name='dove', cls='frozen')
        self._match(0, name='dove')
        self._match(0, cls='fried')

    def test_06_match_two(self):
        """Match Id and Class"""
        self._match(1, id='fox', cls='fried')
        self._match(0, id='fex', cls='fried')
        self._match(0, id='fox', cls='frozen')
        self._match(0, id='fix')
        self._match(0, cls='fried')

    def test_07_match_all(self):
        """Match All"""
        self._match(4, id='idtest', name='nametest', cls=['clstest', 'othcls'])

    def test_07_match_args(self):
        """Allow Args Tuple"""
        self._match(4, 'nametest', 'idtest', ['clstest', 'othcls'])

    def test_08_decendant_match(self):
        """Match Decendants"""
        matches = self.css.matches(name='div')
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(matches.chilren), 0)
        self.assertEqual(len(matches.decendants), 1)
        self.assertEqual(len(matches.match(cls='bookmark')), 1)

    def test_09_child_match(self):
        """Match Direct Children"""
        matches = self.css.matches(name='did')
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(matches.decendants), 0)
        self.assertEqual(len(matches.children), 1)
        self.assertEqual(len(matches.match(cls='storage')), 1)

    def test_10_state(self):
        """Match state change"""
        self._match(2, id='hen', states=['hover'])
        self._match(1, id='hen')

    def test_11_property(self):
        """Single Property"""
        matches = self.css.matches(id='idtest')
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['propertyA'], 'valueA')
        self.assertEqual(matches['propertyA'], 'valueA')

    def test_12_empty(self):
        """No Property is Null"""
        matches = self.css.matches(id='idtest')
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches['propertyB'], None)

    def test_13_cascaded(self):
        """Cascaded Property"""
        matches = self.css.matches(id='hen', states=['hover'])
        self.assertEqual(len(matches), 2)
        # Order is critical!
        self.assertEqual(matches[0]['fly'], 'false')
        self.assertEqual(matches[1]['fly'], 'true')
        self.assertEqual(matches['fly'], 'true')

    def test_14_multiple_selectors(self):
        """Multiple Selectors"""
        for name in ('h1', 'h2', 'h3'):
            matches = self.css.matches(name=name)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches['property'], 'true')


if __name__ == '__main__':
    test_support.run_unittest(CssTestCase)

