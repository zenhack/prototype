# Copyright 2014 Ian Denhardt <ian@zenhack.net>
# Copyright      Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

from sterling import frame
from .csslavie import CssParser
from efl import elementary as elm

# Importing the module has the effect of declaring the appropriate Frame
# classes, which are picked up by the frame module; no additional code is
# needed.
from sterling import widget


def run(model, framespec=None, stylesheet=None):
    def default_filename(obj, ext):
        return type(obj).__name__.lower() + '.' + ext

    elm.init()
    my_frame = frame.from_file(framespec or default_filename(model, 'xml'))
    css = CssParser(stylesheet or default_filename(model, 'css'))
    css.attach(my_frame)
    w = my_frame.widget(model)
    elm.run()
    elm.shutdown()
