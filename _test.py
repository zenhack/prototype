import efl.elementary as elm
elm.init()
from sterling import frame, widget, csslavie


class Model(object):

    def __init(self):
        self.first = 'hello'
        self.last = 'goodbye'

    def do_it(self, o):
        print("Done!")

m = Model()
print(dir(m))

m.__dict__ = {'first': 'hello', 'last': 'goodbye'}
print(dir(m))

print(m.first)

app = frame.from_file('test.xml')
css = csslavie.CssParser('test.css')
css.attach(app)
w = app.widget(m)

elm.run()
elm.shutdown()
