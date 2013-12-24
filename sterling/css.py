#
# Copyright 2012 Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""
Take in CSS text and produce a property map to be applied to items.
"""

import os
import sys
import logging

import tinycss

class Stylesheet(object):
    """A single style sheet objct"""
    def __init__(self, content):
        self.rules = []
        parser = tinycss.make_parser()
        ast = parser.parse_stylesheet(content)
        for rule in ast.rules:
            selector = Selector(rule.selector)
            self.rules.append((selector,rule))

    def matches(self, **kwargs):
        results = []

        for selector, rule in self.rules:
            if selector.match(**kwargs):
                results.append((selector, rule))

        return (results,[],[])

class ParseError(Exception): pass

class Selector(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.name = None
        self.id = None
        self.cls = []
        self._parse()

    def _parse(self):
        return self._parse_simple(self.tokens, 0)

    def _parse_simple(self, tokens, idx):
        if tokens[idx].type == 'IDENT':
            self.name = tokens[idx].value
            return self._parse_simple_suffix(tokens, idx + 1)
        else:
            new_idx = self._parse_simple_suffix(tokens, idx)
            if new_idx <= idx:
                raise ParseError("Empty simple selector")
            else:
                return new_idx

    def _parse_simple_suffix(self, tokens, idx):
        if len(tokens) <= idx:
            return idx
        name = tokens[idx].type
        value = tokens[idx].value
        if name == 'HASH':
            if self.id != None:
                raise ParseError("Dupilicate id in simple selector")
            self.id = value[1:]
            return self._parse_simple_suffix(tokens, idx + 1)
        elif name == 'DELIM' and value == '.':
            if not len(tokens) > idx + 1 and tokens[idx + 1].name == 'IDENT':
                raise ParseError("Missing identifier after '.'")
            self.cls.append(tokens[idx + 1].value)
            return self._parse_simple_suffix(tokens, idx + 2)
        else:
            # XXX: implement attributes and psuedo elements
            raise ParseError("Expected identifier or class, found neither.")


    def child_match(self, name=None, id=None, cls=[]):
        return False # TODO

    def descendant_match(self, name=None, id=None, cls=[]):
        return False # TODO

    def match(self, name=None, id=None, cls=[]):
        # Make sure the element type matches.
        if self.name != None and name != self.name:
            return False
        # same for the id
        if self.id != None and id != self.id:
            return False
        # Make sure all of required the cls are there.
        if type(cls) == type(''):
            cls = [cls]
        for cls in self.cls:
            if not cls in cls:
                return False
        # Nothing missing.
        return True

