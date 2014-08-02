
from sterling import frame
from efl.elementary import window, box, button


class Window(frame.Frame):

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


class Button(frame.Frame):

    callbacks = ['clicked']

    def make_widget(self, data, parent=None):
        if not hasattr(self, '_button'):

            self._button = button.Button(parent.efl_container())
            if 'text' in self.attrs:
                self._button.text = getattr(data, self.attrs['text'])

            for cb in self.__class__.callbacks:
                if cb in self.attrs:
                    cb_add = getattr(self._button, 'callback_%s_add' % cb)
                    cb_add(lambda o: getattr(data, self.attrs[cb])(o))

            self._button.show()

        return self._button

    def efl_container(self):
        return self._button

    def add(self, w):
        pass
