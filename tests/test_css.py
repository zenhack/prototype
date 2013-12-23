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
Test our stand in css module.
"""

import os
import sys
import readline

sys.path.insert(0, '../')
sys.ps1 = "[myshell] "

import unittest

from sterling.css import StyleSheet

try:
    from test import test_support
except ImportError:
    from test import support as test_support

#class CssTestCase(unittest.TestCase):
#    def setUp(self):

css = StyleSheet("""
#hello {
 propA: 8;
}

.foo {
 propB: "hello";
}

bar {
 propC: 5;
}

""")

#    def test_00_load(self):
#        """Test Load of css"""
#        self.css


os.environ['PYTHONINSPECT'] = 'True'

