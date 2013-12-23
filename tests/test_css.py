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

    def _match(self, n, **kwargs):
        (this, children, decendants) = self.css.matches(**kwargs)
        self.assertEqual(len(this), n)

    def test_01_match_none(self):
        self._match(0, id='none')
        self._match(0, cls=['none'])
        self._match(0, type='none')

    def test_02_match_id(self):
        self._match(1, id='idtest')

    def test_03_match_class(self):
        self._match(1, cls=['clstest'])
        self._match(2, cls=['clstest', 'othcls'])
        self._match(1, cls=['clstest', 'foo'])

    def test_04_match_type(self):
        self._match(1, type='typetest')

    def test_05_match_two(self):
        self._match(1, type='div', cls='bookmark')
        self._match(0, type='dif', cls='bookmark')
        self._match(0, type='div', cls='balkmark')
        self._match(0, type='div')
        self._match(0, cls='bookmark')

    def test_06_decendant_match(self):
        (this, children, decendants) = self.css.matches(type='div')
        self.assertEqual(len(decendants), 1)
        self.assertEqual(len(decendants[0].match(cls='bookmark')))

    def test_07_child_match(self):
        (this, children, decendants) = self.css.matches(type='div')
        self.assertEqual(len(children), 1)
        self.assertEqual(len(children[0].match(cls='bookmark')))

if __name__ == '__main__':
    test_support.run_unittest(CssTestCase)

