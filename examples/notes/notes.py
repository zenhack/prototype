import os

from sterling import model, view, style, ui

class Note(model.Model):
    def __init__(self, filename):
        self.title = filename
        with open(filename) as f:
            self.body = f.read()

class App(model.Model):
    def __init__(self):
        filenames = filter(os.path.isfile, os.listdir('.'))

        self.notes = map(Note, filenames)
        self.selected = self.notes[0]

    def event_select(self, context):
        self.selected = context

if __name__ == '__main__':
    ui.UI(App(),
          view.from_filename('view.xml'),
          style.from_filename('style.css'),
          ).run()
