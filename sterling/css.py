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

class CascadingResults(object):
    """The CascadingResults object is returned by the global Stylesheet.matches
       method as well as the CascadingResults.matches method. Each selects from
       their pool of rules a smaller set of rules which apply next.

       This result object then contains that smaller pool of rules for direct
       use and for further matching if applicable.

      Contains three interfaces:
        1. An ordered list of style sheet rules
        2. A dictionary of merged properties from those rules
        3. A method to match further child and descendant selectors
    """
    def __init__(self):
        self.my_rules = []
        self.descendant_rules = []
        self.child_rules = []
        self._properties = None

    def __len__(self):
        return len(self.my_rules)

    def __iter__(self):
        # this must be sorted according to CSS rules TODO.
        for item in self.my_rules:
            yield item

    def __getitem__(self, name):
        return self.properties.__getitem__(name)

    def keys(self):
        """Return a list of property names that this css result affects"""
        return self.properties.keys()

    def get_properties(self, *states):
        """The dictionary of properties merged from the ordered rules.

        If states are given then the dictionary ONLY contains rules with those
        states. If no states are given, only rules without psudoclasses are merged.
        """
        result = {}
        for item in self:
            # XXX Check states here and exclude them or include them
            result.update(item)
        return result

    @property
    def properties(self):
        """Returns a dictionary of non-state rules"""
        if self._properties == None:
            self._properties = self.get_properties()
        return self._properties

    def append(self, item):
        """Add a new rule to the results list (resets property cache)"""
        self.my_rules.append(item)
        # Reset generated properties list
        self._properties = None

    def add_descendant_rule(self, item, level=0):
        """Add a new rule to the prospective descendants to check.

        Item is the rule object, level is how many levels deep of the selector
        this rule has been matches so far.
        """
        self.descendant_rules.append((item, level))

    def add_child_rule(self, item, level):
        """Add a new rule to the direct child rules match"""
        self.child_rules.append((item, level))

    def matches(self, name=None, id=None, cls=[]):
        """Returns result for the next matching part of a selector (descendant)"""
        results = CascadingResults()

        for item, level in self.descendant_rules:
            if item.match(name=name, id=id, cls=cls):
                results.append(item.rule)
            # Must check if selector will match in the future and add
            # To the future rules. Use level to indicate which part of
            # the selector needs checking TODO This needs to be thought out
            if item.child_match(name=name, id=id, cls=cls, level=level):
                results.add_child_rule(item, level=level+1)
            if item.descendant_match(name=name, id=id, cls=cls, level=level):
                results.add_descendant_rule(item, level=level+1)

        return results


class Stylesheet(object):
    """A stylesheet loaded from data. Following CSS2 and some CSS3 rules as
    described by tinycss's css parsing support."""
    def __init__(self, content):
        self.rules = CascadingResults()
        parser = tinycss.make_parser()
        ast = parser.parse_stylesheet(content)
        for rule in ast.rules:
            self.rules.add_descendant_rule(Selector(rule))

    def matches(self, *args, **kwargs):
        """Global stylesheet match.

        Returns a CascadingResults object containing the properties that
        should be applied to the object with the given name, id and classes and
        the functions to apply further selectors for child and descendant matches.

        name: Name of the object that rules should be selected for
        id: unique id of the object that rules should be selected for
        cls: list of classes that rules should be selected for
        """
        return self.rules.matches(*args, **kwargs)


class ParseError(Exception):
    pass


class Selector(object):
    def __init__(self, rule):
        self.rule = rule
        self.tokens = rule.selector
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


    def child_match(self, name=None, id=None, cls=[], level=0):
        return False # TODO

    def descendant_match(self, name=None, id=None, cls=[], level=0):
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
        for required_class in self.cls:
            if not required_class in cls:
                return False
        # Nothing missing.
        return True

