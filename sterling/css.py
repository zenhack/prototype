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

def block(string, f1, f2, s):
    """Return the start and end char positions of a block."""
    i = string.find(f1, s)
    j = string.find(f2, i)
    return (i, j)

def parse(string, sep='=', eol='\n', t=str, start=0):
    """Parse a block and return a dictionary"""
    result = {}
    while True:
        (i, j) = block(string, sep, eol, start)
        if i < 0 or j < 0 or j < i:
            break
        name = string[start:i].strip()
        result[name] = t(string[i+1:j].strip())
        start = j+1
    return result

def remove(string, left='"""', right='"""'):
    """Remove a block of text"""
    start = 0
    while True:
        (i, j) = block(string, left, right, start)
        if i < 0 or j < 0 or j < i:
            break
        string = string[:i] + string[j+2:]
        start = i
    return string


class StyleController(dict):
    """Control the default values, give access to a simple
    dictionary of types with sub dictionaries of properties"""
    def __init__(self):
        dict.__init__(self)
        self['*'] = {}
        self.filters = {}
        self.lames = {}

    def add_filters(self, filters):
        """Add filters to apply to values when loaded."""
        self.filters.update(filters)

    def add_globals(self, namespace):
        """Add names to be available in the css for all names."""
        pass

    def add_locals(self, namespaces):
        """Add a dictionary of namespaces to be used on those names only."""
        self.lames.update(namespaces)

    def add_defaults(self, defaults):
        """Add multiple defaults for different kinds of objects, '*' for all"""
        for (otype, default) in defaults.iteritems():
            self.set_default(otype, default)

    def set_default(self, otype, *args, **kwargs):
        """
        Set multiple defaults for the given type:

        defaults.set(type_id, name, value)
        defaults.set(type_id, { 'name': value })
        defaults.set(type_id, name=value)

        """
        target = self.setdefault(otype, {})
        if args:
            if isinstance(args[0], dict):
                target.update(args[0])
            else:
                target[args[0]] = args[1]
        if kwargs:
            target.update(kwargs)

    def get_default(self, otype, name=None):
        """Return a dictionary of available defaults"""
        if name:
            return self._get_single_default(otype, name)
        result = self['*'].copy()
        if otype != None and self.has_key(otype):
            result.update(self[otype])
        return result

    def _get_single_default(self, otype, name):
        """Get the single default value for this type/name"""
        if otype != None and self.has_key(otype):
            if self[otype].has_key(name):
                return self[otype][name]
        return self['*'].get(name, None)

    def has_default(self, otype, name):
        """Returns true if there is a default value at all"""
        if otype != None and self.has_key(otype):
            if self[otype].has_key(name):
                return True
        return self['*'].has_key(name)

    def get_value(self, name, value):
        """Process the value from css and get the real value"""
        if callable(value):
            return value()
        elif name in self.filters.keys():
            # This value came from the css sheet and is handled.
            return self.filters[name](value)
        elif isinstance(value, basestring):
            # This value came from the css sheet and is code.
            # We could run code here, these are literals and we can handle them as choices in a dictionary or as some other data.
            raise NotImplementedError("Literals not implimented");
        else:
            logging.error("Unknown type: %s" % type(value))


class StyleSheet(object):
    """A single style sheet objct"""
    def __init__(self, content=None):
        self.styles = {}
        if content:
            content = remove(content, '/*', '*/')
            content = remove(content, '//', '\n')
            self.load(content)

    def load(self, content):
        """Parse some basic contents"""
        s = parse(content, '{', '}')
        for key in s.keys():
            value = parse(s.pop(key), ':', ';', str)
            for kins in key.split(','):
                s[kins.strip()] = value
        r = {}
        for key in s.keys():
            (name, state) = ':' in key and key.split(':') or (key, '')
            if not r.has_key(name):
                r[name] = {}
            if r[name].has_key(state):
                r[name][state].update(s[key])
            else:
               r[name][state] = s[key]
        self.styles = [ Style(name, r[name]) for name in r.keys() ]

    def get_style(self, tid, oid, classes):
        """Return a style controll for the given names"""
        result = Styles()
        for style in self.styles:
            if style.style_match(tid, oid, classes):
                result.append(style)
                style.used = True
        return result

    def style_check(self):
        for style in self.styles:
            if not style.used:
                logging.warn("Style '%s' not used." % style.name)


class Style(dict):
    """A single style with multiple states, used internally"""
    def __init__(self, name, states):
        self.used = False
        self.name = name
        self.update(states)
        self.deep = []
        for part in name.split():
            (tid, cls, oid) = (None, None, None)
            if '.' in part:
                (tid, part) = part.split('.')
            if '#' in part:
                (cls, oid) = part.split('#')
            elif part:
                cls = part
            self.deep.append([tid, cls, oid])
        self.shallow = self.deep[-1]

    def style_match(self, tid, oid, classes):
        """Returns True if this style matches the given ids"""
        (xtid, xcls, xoid) = self.shallow
        if xtid not in (None, '') and tid != xtid:
            return False
        if xoid not in (None, '') and oid != xoid:
            return False
        if xcls not in (None, '') and xcls not in classes:
            return False
        return True


class Styles(list):
    """Represent a chain of styles and allow access to getting properties"""
    def get_properties(self, states, changed, otype=None):
        """Get the loaded style properties, return a default value
        if not found, or if no default set, property ignored."""
        props = {}
        if changed and changed in states:
            states = [ changed ]
        for state in states:
            props.update(self.get_state(state))
        return props.iteritems()

    def get_state(self, state):
        """Gets the combined states for this style collection"""
        result = {}
        for style in self:
            result.update(style.get(state, {}))
        return result

    def apply_properties(self, states, changed, target):
        """Apply properties from the css and catch problems"""
        for name, value in self.get_properties(states, changed):
             try:
                 target(name, *self.get_value(name, value))
             except TypeError, error:
                 logging.error("Can't set '%s' to '%s': %s" % \
                     (name, value, "(value not acceptable)"))
             except KeyError, error:
                 logging.error("Can't set '%s' to '%s': %s" % \
                     (name, value, str(error)))

    def get_value(self, name, value=None):
        """Get value for property, or default value"""
        value = GlobalStyles.get_value(name, value)
        if not isinstance(value, tuple):
            value = value,
        return value

GlobalStyles = StyleController()
