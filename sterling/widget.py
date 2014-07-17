
from sterling import frame
from efl.elementary import window, box


@frame.widget
class Window(frame.Frame):

    def make_widget(self, data):
        if self._win is not None:
            return self._win

        self._win = window.StandardWindow('test', 'Test')
        self._box = box.Box(self._win)
        self._win.resize_object_add(self._box)
        self._box.show()
        self._win.show()

    def add(self, w):
        self._box.pack_end(w)
