
from sterling import Model, App

class Main(App):
    name = "In-Press Me"

    def do_it(self):
        self.name = "OK, Done"

Main().run()
