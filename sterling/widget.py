#
# Copyright 2014 Ian Denhardt <ian@zenhack.net>
# Copyright      Martin Owens <doctormo@gmail.com>
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
EFL based widgets to display the kinds of things we want... more docs to follow.
"""

from sterling.frame import Frame
from efl.elementary import window, box, button

class Window(Frame):
    """A widow widget based ontop of the windows and box EFL widgets"""

    def make_widget(self, data, parent=None):
        if not hasattr(self, '_win'):
            if not hasattr(self, 'horizontal'):
                # XXX: The 'horizontal' boolean is a pretty lousy way to talk
                # about this; what we'd really like is something like
                # 'orientation', with an enum as a value. I don't see a reason
                # to propogate the efl design wart up to our users. For now
                # though, it's easy to just wrap the existing semantics.
                self.horizontal = False
            self._win = window.StandardWindow('test', 'Test')
            self._box = box.Box(self._win)
            self._box.horizontal_set(self.horizontal)
            self._win.resize_object_add(self._box)
            self._box.show()
            self._win.show()

        return self._win

    def efl_container(self):
        return self._box

    def add(self, w):
        self._box.pack_end(w)


class Button(Frame):
    callbacks = ['clicked']

    def make_widget(self, data, parent=None):
        if not hasattr(self, '_button'):

            self._button = button.Button(parent.efl_container())
            if 'text' in self.attrs:
                self._button.text = getattr(data, self.attrs['text'])

            self.attach_callbacks(self._button, data)
            self._button.show()

        return self._button

    def efl_container(self):
        return self._button

    def add(self, w):
        pass
