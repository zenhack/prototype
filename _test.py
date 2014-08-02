import efl.elementary as elm
elm.init()
from sterling import frame, widget, csslavie


class Model(object):

    def __init__(self):
        self.first = 'hello'
        self.last = 'goodbye'

    def do_it(self, o):
        print("Done!")

m = Model()

app = frame.from_file('test.xml')
css = csslavie.CssParser('test.css')
css.attach(app)
w = app.widget(m)

elm.run()
elm.shutdown()
