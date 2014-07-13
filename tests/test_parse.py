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
from csslavie.parse import _parse_css
try:
    from test import test_support
except ImportError:
    from test import support as test_support

class ParseTestCase(unittest.TestCase):
    """Test parsing of css data"""
    def setUp(self):
        with open("data/test1.css", 'r') as fhl:
            self.css = _parse_css(fhl.read())


    def test_01_vars(self):
        """Variables"""
        css = self.css

        self.assertEqual(len(css), 5)
        self.assertEqual( css[0][0][0], 'name' )
        self.assertEqual( css[1][0][0], '.name' )
        self.assertEqual( css[2][0][0], '#name' )
        self.assertEqual( css[3][0][0], 'name .name #name' )

        self.assertEqual( css[0][1]['value'], 1 )
        self.assertEqual( css[1][1]['value'], 3 )
        self.assertEqual( css[2][1]['value'], 2 )
        self.assertEqual( css[3][1]['value'], 4 )

    def test_02_multi(self):
        """Parts"""
        css = self.css

        self.assertEqual( css[4][0][0], 'name #parent' )
        self.assertEqual( css[4][0][1], 'name #child' )


if __name__ == '__main__':
    test_support.run_unittest(
       ParseTestCase,
    )
