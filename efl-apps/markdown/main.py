#!/usr/bin/env python

from efl import evas
from efl.evas import EVAS_HINT_EXPAND
from efl.elementary import window, entry, panes, web
import efl.elementary as elm

import xml.etree.ElementTree as ET

from markdown import markdown

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND

def compose2(f, g):
    return lambda x: f(g(x))

def compose(*args):
    return reduce(compose2, args)

def _sup(self):
    return super(self.__class__, self)


class Window(window.StandardWindow):
    def __init__(self):
        super(self.__class__, self).__init__('elm_editor', 'Elm Editor',
                autodel=True)

        self.callback_delete_request_add(lambda o: elm.exit())

        self.panes = Panes(self, size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(self.panes)


    def show(self):
        self.panes.show()
        _sup(self).show()


class Entry(entry.Entry): pass

class Panes(panes.Panes):
    def __init__(self, *args, **kwargs):
        _sup(self).__init__(*args, **kwargs)

        top = Entry(self)

#        bottom = elm.web.Web(self)

        bottom = Entry(self)
        bottom.editable = False

        @top.callback_changed_add
        def _(o):
            bottom.text = compose(
                    elm.entry.utf8_to_markup,
                    markdown,
                    elm.entry.markup_to_utf8,
                    )(top.text)

        self.horizontal = True
        self.part_content_set('top', top)
        self.part_content_set('bottom', bottom)

    def show(self):
        _sup(self).show()

def main():
    elm.init()
    win = Window()
    win.show()
    elm.run()
    elm.shutdown()

if __name__ == '__main__':
    main()
