
from sterling import frame
from efl.elementary import window, box, button


@frame.widget
class Window(frame.Frame):

    def make_widget(self, data, parent=None):
        if hasattr(self, '_win'):
            return self._win

        self._win = window.StandardWindow('test', 'Test')
        self._box = box.Box(self._win)
        self._win.resize_object_add(self._box)
        self._box.show()
        self._win.show()

    def efl_container(self):
        return self._box

    def add(self, w):
        self._box.pack_end(w)


@frame.widget
class Button(frame.Frame):

    def make_widget(self, data, parent=None):
        if not hasattr(self, '_button'):
            self._button = button.Button(parent.efl_container())
            self._button.text = str(data)
            self._button.show()

        return self._button

    def efl_container(self):
        return self._button

    def add(self, w):
        pass
