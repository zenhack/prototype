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
from csslavie import CssParser
try:
    from test import test_support
except ImportError:
    from test import support as test_support

class UseTestCase(unittest.TestCase):
    """Test use documentation in css."""
    def test_01_empty(self):
        """Open empty css"""
        css = CssParser()

    def test_02_usage(self):
        """Open css file"""
        css = CssParser("data/test1.css")


if __name__ == '__main__':
    test_support.run_unittest(
       UseTestCase,
    )
