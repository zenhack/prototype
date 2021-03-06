#
# Copyright 2012-2014 Martin Owens <doctormo@gmail.com>
# Copyright      2014 Ian Denhardt <ian@zenhack.net>
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

import re
import os
import sys
import logging

from collections import defaultdict, OrderedDict


class FilterRejection(ValueError):
    """Raised when a filter fails to recognise the value"""
    pass

class CssValueFilters(list):
    """
    Filters allow values to be pre-packaged into the right format. This
    includes numbers, lengths (units) colours, urls, animations and so forth.
    Objectifying the value before it gets passed to the target object.
    """
    dd_f = "CSS Filter '%s' died with the error '%s', removed from filter list"

    def __init__(self, *filters):
        self.add(filters)

    def add(self, filters):
        for fil in filters:
            self.append(fil)

    def __call__(self, value):
        to_remove = []
        for fil in self:
            try:
                return fil(value)
            except FilterRejection:
                pass
            except Exception, error:
                to_remove.append(fil)
                name = getattr(fil, '__name__', str(fil))
                logging.error(self.dd_f % (name, str(error)))
        for fil in to_remove:
            self.remove(fil)
        return value


def number_filter(value):
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        raise FilterRejection("Not a Number")

def bool_filter(value):
    if value.lower() in {'true', 'false'}:
        return value.lower() == 'true'
    else:
        raise FilterRejection("Not a Boolean")

GLOBAL_FILTERS = {
    number_filter,
    bool_filter,
}


def _block(string, f1, f2, s):
    """Find the start and end of a block in a string"""
    i = string.find(f1, s)
    j = string.find(f2, i)
    return (i, j)


def _parse(string, sep='=', eol='\n', vtype=str, ktype=str, start=0):
    """Parse any content between a start, end and seperator.

    sep   - seperator between a name and value pair
    eol   - An end of line marker to stop the parsing.
    start - Starting character number.
    vtype - Type or filter for each of the values before returning.
    ktype - Type or filter for each of the keys, if the function returns a list
            each immutable item in the list is a key with a duplicate of the value.

    Both sep and eol must be single characters - multi-character delimiters are
    *not* supported.
    """
    result = []
    while True:
        (i, j) = _block(string, sep, eol, start)
        if i < 0 or j < 0 or j < i:
            break
        name = string[start:i].strip()
        keys = ktype(name)
        value = vtype(string[i+1:j].strip())
        if not isinstance(keys, list):
            keys = [ keys ]
        for key in keys:
            result.append((key,value))
        start = j+1
    return result

def _remove(string, left='"""', right='"""'):
    """Removes comments from an input string (should be done first)."""
    start = 0
    while True:
        (i, j) = _block(string, left, right, start)
        if i < 0 or j < 0 or j < i:
            break
        string = string[:i] + string[j+2:]
        start = i
    return string

def _parse_names(content):
    result = []
    # We want to make sure the direct parent/child
    # chevron can be with or without spaces.
    for name in content.replace('>', ' > ').split():
        for char in '.#:':
            name = name.replace(char, ' '+char)
        result.append( name.strip() )
    return result

def _parse_css(content, filters=None):
    """Parse css formated content"""
    filters = filters or CssValueFilters(*GLOBAL_FILTERS)
    content = _remove(content, '/*', '*/')
    content = _remove(content, '//', '\n')
    return _parse(content, '{', '}',
        ktype=lambda c: [ _parse_names(p) for p in c.split(',') ],
        vtype=lambda c: dict( _parse(c,":",";", vtype=filters))
    )


def CssParser(filename=None):
    """Returns a style sheet for the given filename"""
    if filename:
        with open(filename, 'r') as fhl:
            return StyleSheet(fhl.read())
    return StyleSheet()


def get_weight(name):
    """Returns a weight based on the name construction,

     ! this might be standardised somewhere, but I didn't look it up.
    """
    return name.count(".") + name.count("*") * 2 + name.count("#") * 4 + name.count(">") * 8

class StyleSheet(object):
    """This stylesheet object allows one to 'attach' objects to css, this css
    will use the attributes in the object and update their properties."""
    _attr_name = '__name__'
    _attr_oid  = 'name'
    _attr_cls  = 'classes'
    _attr_children = 'children'

    filters    = None

    def __init__(self, content=None):
        self.styles = []
        self.filters = CssValueFilters(*(self.filters or []))
        self.filters.add(GLOBAL_FILTERS)

        if content:
            self.styles = _parse_css(content, filters=self.filters)

        _i = defaultdict(list)

        for names, style in self.styles:
            _i['*'.join(names)].append(style)

        # Weigh up the names and sort them by weight here
        self._index = OrderedDict(sorted(_i.iteritems(), key=lambda x: get_weight(x[0])))

    def attach(self, obj, parent=None):
        names = Names()
        names.add( getattr(type(obj), self._attr_name, None) )
        names.add( getattr(obj, self._attr_oid, None), '#' )
        names.set_parent(parent)
        for c in getattr(obj, self._attr_cls, []) or []:
            names.add(c, '.')
        for (ns, style) in self._index.items():
            if names.match(ns):
                for s in style:
                    obj.add_to(s)
        # XXX Attach signal here for state updates
        return names

    def attach_all(self, obj, parent=None):
        children = getattr(obj, self._attr_children, [])
        new_parent = self.attach(obj, parent=parent)
        for child in children:
            self.attach_all(child, parent=new_parent)
        return new_parent


class Names(set):
    def add(self, name, sep=''):
        if name != None:
            set.add(self, sep + str(name).lower())

    def set_parent(self, parent):
        if not isinstance(parent, (Names, type(None))):
            name = type(parent).__name__
            raise TypeError("Can not add '%s' as a CSS Names Set" % name)
        self.parent = parent

    def match(self, ns):
        if type(ns) is str:
            ns = ns.split('*')
        (sublist, rest) = (ns[-1], ns[:-1])

        if type(sublist) is str:
            sublist = sublist.split(' ')

        for name in sublist:
            if name not in self:
                return False 

        # Do we need a parent tested? (and does one exist?)
        if not rest or not getattr(self, 'parent', None):
            return not bool(rest)

        # Direct parent test (parent must match the next stanza)
        if rest[-1] == '>':
            return self.parent.match(rest[:-1])

        # Indirect parent test (any parent can match the next stanza)
        parent = self.parent
        while parent and parent.match(rest):
            parent = getattr(parent, 'parent', None)
        return bool(parent)



